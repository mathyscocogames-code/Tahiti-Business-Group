"""Jour 13 — 20 pré-launch fixes : rate-limiting, signalement, stats, CSV, sitemap."""

# ═══════════════════════════════════════════════════════════════
# 1. ads/models.py — add Signalement
# ═══════════════════════════════════════════════════════════════
with open('ads/models.py', encoding='utf-8') as f:
    models_src = f.read()

SIGNALEMENT = '''

class Signalement(models.Model):
    RAISONS = [
        ('spam',    'Spam / Annonce en double'),
        ('arnaque', 'Arnaque / Fraude'),
        ('illegal', 'Contenu illégal ou choquant'),
        ('autre',   'Autre'),
    ]
    annonce    = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='signalements')
    auteur     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   null=True, blank=True)
    raison     = models.CharField(max_length=20, choices=RAISONS)
    details    = models.TextField(blank=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Signalement'
        verbose_name_plural = 'Signalements'

    def __str__(self):
        return f"Signal #{self.pk} — {self.annonce.titre}"
'''

if 'Signalement' not in models_src:
    models_src += SIGNALEMENT
    with open('ads/models.py', 'w', encoding='utf-8') as f:
        f.write(models_src)
    print('models.py: Signalement added')
else:
    print('models.py: Signalement already exists')

# ═══════════════════════════════════════════════════════════════
# 2. ads/admin.py — register Signalement
# ═══════════════════════════════════════════════════════════════
with open('ads/admin.py', encoding='utf-8') as f:
    admin_src = f.read()

if 'Signalement' not in admin_src:
    admin_src = admin_src.replace(
        'from .models import Annonce, Message',
        'from .models import Annonce, Message, Signalement'
    )
    admin_src += '''

@admin.register(Signalement)
class SignalementAdmin(admin.ModelAdmin):
    list_display  = ['annonce', 'raison', 'auteur', 'created_at']
    list_filter   = ['raison', 'created_at']
    search_fields = ['annonce__titre', 'details']
    readonly_fields = ['created_at']
    actions = ['supprimer_annonce_signalee']

    def supprimer_annonce_signalee(self, request, queryset):
        for s in queryset:
            s.annonce.statut = 'modere'
            s.annonce.save()
        self.message_user(request, f"{queryset.count()} annonce(s) modérée(s).")
    supprimer_annonce_signalee.short_description = "Modérer l'annonce signalée"
'''
    with open('ads/admin.py', 'w', encoding='utf-8') as f:
        f.write(admin_src)
    print('admin.py: Signalement registered')
else:
    print('admin.py: Signalement already registered')

# ═══════════════════════════════════════════════════════════════
# 3. ads/views.py — add new views + rate limiting + imports
# ═══════════════════════════════════════════════════════════════
with open('ads/views.py', encoding='utf-8') as f:
    views_src = f.read()

# Add imports if missing
NEW_IMPORTS = [
    ('import csv', 'import csv\n'),
    ('import datetime', 'import datetime\n'),
    ('from django.db.models import Count', 'from django.db.models import Count\n'),
    ('from django.db.models.functions import TruncDay', 'from django.db.models.functions import TruncDay\n'),
    ('from django.contrib.auth import get_user_model', 'from django.contrib.auth import get_user_model\n'),
    ('from django.http import HttpResponse', 'from django.http import HttpResponse, JsonResponse\n'),
]

for check, line in NEW_IMPORTS:
    if check not in views_src:
        # Insert after the last import block
        views_src = views_src.replace('from PIL import Image as PILImage\n', 'from PIL import Image as PILImage\n' + line)

# Fix HttpResponse duplicate
views_src = views_src.replace(
    'from django.http import HttpResponse, JsonResponse\nfrom django.http import JsonResponse',
    'from django.http import HttpResponse, JsonResponse'
)

# Replace .models import to include Signalement
if 'Signalement' not in views_src:
    views_src = views_src.replace(
        'from .models import Annonce, Message, CATEGORIES, SOUS_CATEGORIES',
        'from .models import Annonce, Message, CATEGORIES, SOUS_CATEGORIES, Signalement'
    )

# Add User model reference if missing
if 'get_user_model' in views_src and 'User = get_user_model()' not in views_src:
    views_src = views_src.replace(
        'from rubriques.models import ArticlePromo, ArticleInfo, ArticleNouveaute',
        'from rubriques.models import ArticlePromo, ArticleInfo, ArticleNouveaute\nUser = get_user_model()'
    )

# Add rate-limit helper + new views (before the last blank line)
NEW_VIEWS = '''

# ── Rate limiting (session-based) ─────────────────────────────────────────
def _rate_limited(request, action, max_count=3, period_minutes=60):
    key = f'rl_{action}'
    now = datetime.datetime.now().timestamp()
    cutoff = now - period_minutes * 60
    history = [t for t in request.session.get(key, []) if t > cutoff]
    if len(history) >= max_count:
        return True
    history.append(now)
    request.session[key] = history
    request.session.modified = True
    return False


# ── Mes Favoris ──────────────────────────────────────────────────────────
def mes_favoris(request):
    ids_raw = request.GET.get('ids', '')
    annonces = []
    if ids_raw:
        try:
            pk_list = [int(x.strip()) for x in ids_raw.split(',') if x.strip().isdigit()][:50]
            annonces = list(Annonce.objects.filter(pk__in=pk_list, statut='actif').select_related('user'))
        except (ValueError, TypeError):
            pass
    return render(request, 'ads/mes_favoris.html', {'annonces': annonces})


# ── Signaler une annonce ─────────────────────────────────────────────────
def signaler_annonce(request, pk):
    annonce = get_object_or_404(Annonce, pk=pk, statut='actif')
    if request.method == 'POST':
        raison  = request.POST.get('raison', 'autre')
        details = request.POST.get('details', '').strip()[:500]
        Signalement.objects.create(
            annonce=annonce,
            auteur=request.user if request.user.is_authenticated else None,
            raison=raison,
            details=details,
        )
        messages.success(request, "Merci, votre signalement a été envoyé à l'équipe TBG.")
        return redirect('annonce_detail', pk=pk)
    return render(request, 'ads/signaler.html', {'annonce': annonce})


# ── Admin stats dashboard ────────────────────────────────────────────────
@login_required
def admin_stats(request):
    if not request.user.is_staff:
        from django.http import Http404
        raise Http404
    from django.utils import timezone as tz
    import datetime as dt
    today  = tz.now()
    last30 = today - dt.timedelta(days=30)

    annonces_par_jour = list(
        Annonce.objects
        .filter(created_at__gte=last30)
        .annotate(jour=TruncDay('created_at'))
        .values('jour')
        .annotate(count=Count('id'))
        .order_by('jour')
    )
    par_categorie = list(
        Annonce.objects.filter(statut='actif')
        .values('categorie')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    stats = {
        'total_actives':  Annonce.objects.filter(statut='actif').count(),
        'total_annonces': Annonce.objects.count(),
        'total_users':    User.objects.count(),
        'signalements':   Signalement.objects.count(),
        'aujourd_hui':    Annonce.objects.filter(created_at__date=today.date()).count(),
        'cette_semaine':  Annonce.objects.filter(created_at__gte=today - dt.timedelta(days=7)).count(),
    }
    cat_labels = dict(CATEGORIES)
    for c in par_categorie:
        c['label'] = cat_labels.get(c['categorie'], c['categorie'])
    max_day = max((d['count'] for d in annonces_par_jour), default=1)
    dernieres         = Annonce.objects.select_related('user').order_by('-created_at')[:15]
    signalements_list = Signalement.objects.select_related('annonce', 'auteur').order_by('-created_at')[:10]
    return render(request, 'ads/admin_stats.html', {
        'stats':              stats,
        'annonces_par_jour':  annonces_par_jour,
        'par_categorie':      par_categorie,
        'max_day':            max_day,
        'dernieres':          dernieres,
        'signalements_list':  signalements_list,
    })


# ── Export CSV ───────────────────────────────────────────────────────────
@login_required
def export_csv(request):
    if not request.user.is_staff:
        from django.http import Http404
        raise Http404
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="tbg_annonces.csv"'
    response.write('\\ufeff')  # BOM Excel UTF-8
    writer = csv.writer(response)
    writer.writerow(['ID', 'Titre', 'Catégorie', 'Prix (XPF)', 'Localisation',
                     'Vendeur', 'Email', 'Téléphone', 'Statut', 'Vues', 'Date'])
    for a in Annonce.objects.select_related('user').order_by('-created_at'):
        writer.writerow([
            a.pk, a.titre, a.get_categorie_display(),
            a.prix, a.localisation,
            a.user.nom or '', a.user.email, a.user.tel or '',
            a.statut, a.views, a.created_at.strftime('%d/%m/%Y %H:%M'),
        ])
    return response


# ── Custom 404 ───────────────────────────────────────────────────────────
def custom_404(request, exception=None):
    return render(request, '404.html', status=404)
'''

if 'mes_favoris' not in views_src:
    views_src += NEW_VIEWS
    print('views.py: new views added')
else:
    print('views.py: new views already present')

# Patch deposer_annonce to add rate limiting
if '_rate_limited' in views_src and 'rate_limited' not in views_src.split('@login_required\ndef deposer_annonce')[1][:50]:
    OLD_DEPOSER = (
        '@login_required\n'
        'def deposer_annonce(request):\n'
        '    from .forms import AnnonceForm\n'
        '    if request.method == \'POST\':\n'
    )
    NEW_DEPOSER = (
        '@login_required\n'
        'def deposer_annonce(request):\n'
        '    from .forms import AnnonceForm\n'
        '    if request.method == \'POST\':\n'
        '        if _rate_limited(request, \'deposer\', max_count=5, period_minutes=60):\n'
        '            messages.error(request, "Limite atteinte : 5 annonces par heure maximum. Réessayez plus tard.")\n'
        '            return redirect(\'deposer_annonce\')\n'
    )
    if OLD_DEPOSER in views_src:
        views_src = views_src.replace(OLD_DEPOSER, NEW_DEPOSER, 1)
        print('views.py: rate limiting added to deposer_annonce')
    else:
        print('WARNING: deposer_annonce anchor not found for rate limiting patch')

with open('ads/views.py', 'w', encoding='utf-8') as f:
    f.write(views_src)
print('views.py: OK')

# ═══════════════════════════════════════════════════════════════
# 4. ads/urls.py
# ═══════════════════════════════════════════════════════════════
URLS_NEW = """from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('annonces/', views.liste_annonces, name='liste_annonces'),
    path('annonces/<int:pk>/', views.annonce_detail, name='annonce_detail'),
    path('deposer/', views.deposer_annonce, name='deposer_annonce'),
    path('mes-annonces/', views.mes_annonces, name='mes_annonces'),
    path('annonces/<int:pk>/edit/', views.edit_annonce, name='edit_annonce'),
    path('annonces/<int:pk>/supprimer/', views.supprimer_annonce, name='supprimer_annonce'),
    path('annonces/<int:pk>/vendu/', views.marquer_vendu, name='marquer_vendu'),
    path('annonces/<int:pk>/contact/', views.contact_annonce, name='contact_annonce'),
    path('annonces/<int:pk>/signaler/', views.signaler_annonce, name='signaler_annonce'),
    path('mes-messages/', views.mes_messages, name='mes_messages'),
    path('mes-favoris/', views.mes_favoris, name='mes_favoris'),
    path('info/', views.page_info, name='page_info'),
    path('business/', views.page_business, name='page_business'),
    path('admin-stats/', views.admin_stats, name='admin_stats'),
    path('admin-stats/export-csv/', views.export_csv, name='export_csv'),
]
"""
with open('ads/urls.py', 'w', encoding='utf-8') as f:
    f.write(URLS_NEW)
print('urls.py: OK')

# ═══════════════════════════════════════════════════════════════
# 5. tahiti_business/urls.py — add handler404 + sitemap + robots
# ═══════════════════════════════════════════════════════════════
MAIN_URLS = """from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.views.generic import TemplateView

handler404 = 'ads.views.custom_404'


def robots_txt(request):
    base = request.build_absolute_uri('/')
    content = (
        "User-agent: *\\n"
        "Allow: /\\n"
        "Disallow: /admin/\\n"
        "Disallow: /admin-stats/\\n"
        "Disallow: /rubriques/moderation/\\n"
        f"Sitemap: {base}sitemap.xml\\n"
    )
    return HttpResponse(content, content_type='text/plain')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ads.urls')),
    path('users/', include('users.urls')),
    path('pubs/', include('pubs.urls')),
    path('rubriques/', include('rubriques.urls')),
    path('robots.txt', robots_txt),
    path('sitemap.xml', TemplateView.as_view(
        template_name='sitemap.xml',
        content_type='application/xml',
    )),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
with open('tahiti_business/urls.py', 'w', encoding='utf-8') as f:
    f.write(MAIN_URLS)
print('tahiti_business/urls.py: OK')

print('\\n=== _jour13_all.py done ===')