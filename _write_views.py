"""Script temporaire pour écrire ads/views.py"""
content = """\
import os
import json
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings as django_settings
from PIL import Image as PILImage
from .models import Annonce, Message, CATEGORIES, SOUS_CATEGORIES


def _save_webp(file_obj, user_pk):
    img = PILImage.open(file_obj)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    img.thumbnail((900, 700), PILImage.LANCZOS)
    upload_dir = os.path.join(django_settings.MEDIA_ROOT, 'annonces')
    os.makedirs(upload_dir, exist_ok=True)
    filename = f"{user_pk}_{uuid.uuid4().hex[:8]}.webp"
    filepath = os.path.join(upload_dir, filename)
    img.save(filepath, format='WEBP', quality=85, method=6)
    return f"{django_settings.MEDIA_URL}annonces/{filename}"


def _sous_cats_json():
    return json.dumps(
        {cat: [{'value': v, 'label': l} for v, l in items]
         for cat, items in SOUS_CATEGORIES.items()},
        ensure_ascii=False
    )


def index(request):
    annonces_recentes = Annonce.objects.filter(statut='actif').select_related('user')[:12]
    annonces_par_cat = {}
    for code, label in CATEGORIES:
        annonces_par_cat[code] = {
            'label': label,
            'annonces': Annonce.objects.filter(
                statut='actif', categorie=code
            ).select_related('user')[:4],
        }
    return render(request, 'ads/index.html', {
        'annonces_recentes': annonces_recentes,
        'annonces_par_cat':  annonces_par_cat,
        'categories':        CATEGORIES,
    })


def liste_annonces(request):
    qs = Annonce.objects.filter(statut='actif').select_related('user')
    q        = request.GET.get('q', '')
    cat      = request.GET.get('categorie', '')
    sous_cat = request.GET.get('sous_cat', '')
    ville    = request.GET.get('localisation', '')
    prix_max = request.GET.get('prix_max', '')

    if q:
        qs = qs.filter(Q(titre__icontains=q) | Q(description__icontains=q))
    if cat:
        qs = qs.filter(categorie=cat)
    if sous_cat:
        qs = qs.filter(sous_categorie=sous_cat)
    if ville:
        qs = qs.filter(localisation__icontains=ville)
    if prix_max:
        try:
            qs = qs.filter(prix__lte=int(prix_max))
        except ValueError:
            pass

    paginator = Paginator(qs, 24)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'ads/liste.html', {
        'annonces':   page,
        'categories': CATEGORIES,
        'q':          q,
        'cat_active': cat,
        'sous_cat':   sous_cat,
        'ville':      ville,
        'prix_max':   prix_max,
    })


def annonce_detail(request, pk):
    annonce = get_object_or_404(Annonce, pk=pk, statut='actif')
    annonce.increment_views()
    from .forms import MessageForm
    form_message = MessageForm()

    if request.method == 'POST':
        form_message = MessageForm(request.POST)
        if form_message.is_valid():
            msg = form_message.save(commit=False)
            msg.annonce = annonce
            if request.user.is_authenticated:
                msg.expediteur = request.user
            msg.save()
            messages.success(request, "Votre message a bien \u00e9t\u00e9 envoy\u00e9 !")
            return redirect('annonce_detail', pk=pk)

    annonces_similaires = Annonce.objects.filter(
        statut='actif', categorie=annonce.categorie
    ).exclude(pk=pk).select_related('user')[:4]

    return render(request, 'ads/detail.html', {
        'annonce':             annonce,
        'form_message':        form_message,
        'annonces_similaires': annonces_similaires,
    })


@login_required
def deposer_annonce(request):
    from .forms import AnnonceForm
    if request.method == 'POST':
        form = AnnonceForm(request.POST, request.FILES)
        if form.is_valid():
            annonce = form.save(commit=False)
            annonce.user = request.user
            annonce.sous_categorie = request.POST.get('sous_categorie', '')
            photos = []
            for f in request.FILES.getlist('photos')[:5]:
                try:
                    photos.append(_save_webp(f, request.user.pk))
                except Exception:
                    pass
            annonce.photos = photos
            annonce.save()
            messages.success(request, f"Annonce publi\u00e9e ! {len(photos)} photo(s) converties en WebP.")
            return redirect('annonce_detail', pk=annonce.pk)
    else:
        form = AnnonceForm()

    return render(request, 'ads/deposer.html', {
        'form':                form,
        'sous_categories_json': _sous_cats_json(),
    })


@login_required
def mes_annonces(request):
    annonces = Annonce.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'ads/mes_annonces.html', {'annonces': annonces})


@login_required
def edit_annonce(request, pk):
    # Admins peuvent \u00e9diter toutes les annonces
    if request.user.is_staff:
        annonce = get_object_or_404(Annonce, pk=pk)
    else:
        annonce = get_object_or_404(Annonce, pk=pk, user=request.user)

    if request.method == 'POST':
        annonce.titre          = request.POST.get('titre', '').strip() or annonce.titre
        annonce.description    = request.POST.get('description', '').strip() or annonce.description
        annonce.categorie      = request.POST.get('categorie', annonce.categorie)
        annonce.sous_categorie = request.POST.get('sous_categorie', '')
        annonce.localisation   = request.POST.get('localisation', '').strip() or annonce.localisation
        annonce.prix_label     = request.POST.get('prix_label', '').strip()
        try:
            annonce.prix = int(request.POST.get('prix', 0) or 0)
        except (ValueError, TypeError):
            annonce.prix = 0

        # Supprimer les photos coch\u00e9es
        to_delete = request.POST.getlist('delete_photos')
        current   = [p for p in annonce.photos if p not in to_delete]
        for url in to_delete:
            try:
                rel  = url.replace(django_settings.MEDIA_URL, '')
                path = os.path.join(django_settings.MEDIA_ROOT, rel)
                if os.path.exists(path):
                    os.remove(path)
            except Exception:
                pass

        # Ajouter nouvelles photos (max 5 total)
        for photo_file in request.FILES.getlist('photos'):
            if len(current) >= 5:
                break
            try:
                current.append(_save_webp(photo_file, request.user.pk))
            except Exception:
                pass

        annonce.photos = current
        annonce.save()
        messages.success(request, "Annonce modifi\u00e9e avec succ\u00e8s.")
        return redirect('mes_annonces')

    return render(request, 'ads/edit_annonce.html', {
        'annonce':              annonce,
        'categories':           CATEGORIES,
        'sous_categories_json': _sous_cats_json(),
        'remaining_slots':      max(0, 5 - len(annonce.photos)),
    })


@login_required
def supprimer_annonce(request, pk):
    annonce = get_object_or_404(Annonce, pk=pk, user=request.user)
    if request.method == 'POST':
        for photo_url in annonce.photos:
            try:
                rel  = photo_url.replace(django_settings.MEDIA_URL, '')
                path = os.path.join(django_settings.MEDIA_ROOT, rel)
                if os.path.exists(path):
                    os.remove(path)
            except Exception:
                pass
        annonce.delete()
        messages.success(request, "Annonce supprim\u00e9e.")
    return redirect('mes_annonces')


@login_required
def marquer_vendu(request, pk):
    annonce = get_object_or_404(Annonce, pk=pk, user=request.user)
    annonce.statut = 'vendu'
    annonce.save()
    messages.success(request, "Annonce marqu\u00e9e comme vendue.")
    return redirect('mes_annonces')
"""

with open('ads/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('OK')