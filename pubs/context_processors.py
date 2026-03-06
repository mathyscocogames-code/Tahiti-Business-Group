from .models import Publicite
from ads.models import SOUS_CATEGORIES


def sidebar_pubs(request):
    ctx = {
        "pub_billboard": Publicite.objects.filter(emplacement="billboard", actif=True).first(),
        "pub_strip_1":   Publicite.objects.filter(emplacement="strip_1",   actif=True).first(),
        "pub_strip_2":   Publicite.objects.filter(emplacement="strip_2",   actif=True).first(),
        "pub_strip_3":   Publicite.objects.filter(emplacement="strip_3",   actif=True).first(),
        "pub_haut":      Publicite.objects.filter(emplacement="haut",      actif=True).first(),
        "pub_milieu":    Publicite.objects.filter(emplacement="milieu",    actif=True).first(),
        "pub_bas":       Publicite.objects.filter(emplacement="bas",       actif=True).first(),
        "sous_categories": SOUS_CATEGORIES,
        "unread_count":    0,
    }
    if request.user.is_authenticated:
        from ads.models import Message
        ctx["unread_count"] = Message.objects.filter(
            to_user=request.user, read=False
        ).count()
    return ctx


def admin_stats(request):
    """Stats injectées dans le dashboard /admin/ uniquement."""
    if not request.path.startswith('/admin/') or not getattr(request.user, 'is_staff', False):
        return {}
    try:
        from django.utils import timezone
        from django.contrib.auth import get_user_model
        from ads.models import Annonce, Message, Signalement
        from rubriques.models import ArticlePromo, ArticleInfo, ArticleNouveaute
        User = get_user_model()
        sept_jours = timezone.now() - timezone.timedelta(days=7)
        rubriques_attente = (
            ArticlePromo.objects.filter(statut='en_attente').count()
            + ArticleInfo.objects.filter(statut='en_attente').count()
            + ArticleNouveaute.objects.filter(statut='en_attente').count()
        )
        return {"tbg_stats": {
            "annonces_actives":   Annonce.objects.filter(statut='actif').count(),
            "annonces_moderees":  Annonce.objects.filter(statut='modere').count(),
            "users_total":        User.objects.count(),
            "users_new_7j":       User.objects.filter(date_joined__gte=sept_jours).count(),
            "messages_total":     Message.objects.count(),
            "rubriques_attente":  rubriques_attente,
            "pubs_actives":       Publicite.objects.filter(actif=True).count(),
            "vues_totales":       sum(Annonce.objects.values_list('views', flat=True)),
            "dernières_annonces": Annonce.objects.order_by('-created_at').select_related('user')[:5],
            "signalements":       Signalement.objects.order_by('-created_at').select_related('annonce')[:5],
        }}
    except Exception:
        return {}
