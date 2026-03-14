import json
import uuid
from datetime import date, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import (
    Publicite, DemandePublicite,
    PRIX_PAR_EMPLACEMENT, DISCOUNT_PAR_DUREE, calculer_prix,
)
from .forms import PubliciteForm, DemandePubliciteForm, DepotPubliciteForm
from .payzen import build_payzen_form, verify_signature


def _staff_required(request):
    """Retourne True si l'accès est autorisé, sinon redirige."""
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, "Accès réservé aux administrateurs.")
        return False
    return True


# ═══════════════════════════════════════════════════════════════════════════════
# Admin CRUD (inchangé)
# ═══════════════════════════════════════════════════════════════════════════════

@login_required
def pub_creer(request):
    if not _staff_required(request):
        return redirect('index')
    emplacement = request.GET.get('emplacement', '')
    initial = {'emplacement': emplacement} if emplacement else {}
    form = PubliciteForm(request.POST or None, request.FILES or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Publicité créée avec succès.")
        return redirect('admin_dashboard')
    return render(request, 'pubs/pub_form.html', {'form': form, 'action': 'Créer'})


@login_required
def pub_modifier(request, pk):
    if not _staff_required(request):
        return redirect('index')
    pub = get_object_or_404(Publicite, pk=pk)
    form = PubliciteForm(request.POST or None, request.FILES or None, instance=pub)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Publicité modifiée avec succès.")
        return redirect('admin_dashboard')
    return render(request, 'pubs/pub_form.html', {'form': form, 'pub': pub, 'action': 'Modifier'})


@login_required
def pub_supprimer(request, pk):
    if not _staff_required(request):
        return redirect('index')
    pub = get_object_or_404(Publicite, pk=pk)
    if request.method == 'POST':
        if pub.image:
            pub.image.delete(save=False)
        pub.titre        = 'Emplacement disponible'
        pub.description  = ''
        pub.image_url    = ''
        pub.lien         = ''
        pub.actif        = False
        pub.client_nom   = ''
        pub.client_email = ''
        pub.client_tel   = ''
        pub.date_debut   = None
        pub.date_fin     = None
        pub.payment_status = 'none'
        pub.save()
        messages.success(request, "Slot libéré — l'emplacement est à nouveau disponible à la réservation.")
    return redirect('admin_dashboard')


@login_required
def pub_toggle(request, pk):
    if not _staff_required(request):
        return redirect('index')
    pub = get_object_or_404(Publicite, pk=pk)
    if request.method == 'POST':
        pub.actif = not pub.actif
        pub.save()
    return redirect('admin_dashboard')


# ═══════════════════════════════════════════════════════════════════════════════
# Pages publiques (tarifs, demande manuelle)
# ═══════════════════════════════════════════════════════════════════════════════

def tarifs_pubs(request):
    pubs_haut   = Publicite.objects.filter(emplacement='haut', actif=True).first()
    pubs_milieu = Publicite.objects.filter(emplacement='milieu', actif=True).first()
    pubs_bas    = Publicite.objects.filter(emplacement='bas', actif=True).first()

    return render(request, 'pubs/tarifs.html', {
        'pubs_haut':   pubs_haut,
        'pubs_milieu': pubs_milieu,
        'pubs_bas':    pubs_bas,
        'tarifs': [
            {'emplacement': 'Haut de sidebar', 'prix': 60000, 'desc': 'Meilleure visibilité, premier regard', 'slug': 'haut'},
            {'emplacement': 'Milieu de sidebar', 'prix': 40000, 'desc': 'Position centrale, très efficace', 'slug': 'milieu'},
            {'emplacement': 'Bas de sidebar', 'prix': 20000, 'desc': 'Présence permanente, tarif abordable', 'slug': 'bas'},
        ],
    })


def demande_pub(request):
    form = DemandePubliciteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Votre demande a été envoyée ! Nous vous contacterons sous 24h.")
        return redirect('tarifs_pubs')
    return render(request, 'pubs/demande.html', {'form': form})


# ═══════════════════════════════════════════════════════════════════════════════
# Self-service : Déposer une pub + payer via PayZen
# ═══════════════════════════════════════════════════════════════════════════════

def deposer_pub(request):
    """Formulaire public pour déposer et payer une publicité."""
    emplacement_pre = request.GET.get('emplacement', '')
    initial = {}
    if emplacement_pre:
        initial['emplacement'] = emplacement_pre

    form = DepotPubliciteForm(request.POST or None, request.FILES or None, initial=initial)

    if request.method == 'POST' and form.is_valid():
        cd = form.cleaned_data
        duree = int(cd['duree'])
        prix_total = calculer_prix(cd['emplacement'], duree)

        # Créer la pub en attente de paiement
        pub = Publicite(
            titre=cd['titre'],
            image=cd['image'],
            lien=cd['lien'],
            emplacement=cd['emplacement'],
            prix=prix_total,
            actif=False,
            client_nom=cd['client_nom'],
            client_email=cd['client_email'],
            client_tel=cd.get('client_tel', ''),
            duree_semaines=duree,
            payment_status='pending',
            payment_ref=f"TBG{uuid.uuid4().hex[:8].upper()}",
        )
        pub.save()

        # Stocker l'ID en session pour vérification
        request.session['pub_pending_pk'] = pub.pk
        return redirect('initier_paiement', pk=pub.pk)

    # Données de prix pour le JS
    prix_json = json.dumps(PRIX_PAR_EMPLACEMENT)
    discount_json = json.dumps(DISCOUNT_PAR_DUREE)

    return render(request, 'pubs/deposer.html', {
        'form': form,
        'prix_json': prix_json,
        'discount_json': discount_json,
    })


def initier_paiement(request, pk):
    """Construit et affiche le formulaire de redirection PayZen."""
    pub = get_object_or_404(Publicite, pk=pk, payment_status='pending')

    # Vérifier que c'est bien l'utilisateur qui a créé cette pub
    if request.session.get('pub_pending_pk') != pub.pk:
        messages.error(request, "Accès non autorisé.")
        return redirect('deposer_pub')

    form_data, payment_url = build_payzen_form(pub, request)

    return render(request, 'pubs/payzen_redirect.html', {
        'form_data':   form_data,
        'payment_url': payment_url,
        'pub':         pub,
    })


@csrf_exempt
def retour_paiement(request):
    """Page de retour après paiement (navigateur de l'acheteur)."""
    data = request.POST if request.method == 'POST' else request.GET

    order_id = data.get('vads_order_id', '')
    result   = data.get('vads_result', '')
    status   = data.get('vads_trans_status', '')

    success = (result == '00' and status in ('AUTHORISED', 'CAPTURED'))

    pub = None
    if order_id:
        pub = Publicite.objects.filter(payment_ref=order_id).first()

    return render(request, 'pubs/paiement_resultat.html', {
        'success': success,
        'pub':     pub,
    })


@csrf_exempt
def ipn_paiement(request):
    """IPN (Instant Payment Notification) — appel serveur-à-serveur de PayZen.

    C'est ici que la pub est réellement activée après vérification cryptographique.
    """
    if request.method != 'POST':
        return HttpResponse('Method not allowed', status=405)

    # Vérifier la signature
    if not verify_signature(request.POST):
        return HttpResponse('Invalid signature', status=400)

    order_id = request.POST.get('vads_order_id', '')
    result   = request.POST.get('vads_result', '')
    status   = request.POST.get('vads_trans_status', '')
    trans_id = request.POST.get('vads_trans_id', '')

    try:
        pub = Publicite.objects.get(payment_ref=order_id)
    except Publicite.DoesNotExist:
        return HttpResponse('Order not found', status=404)

    if result == '00' and status in ('AUTHORISED', 'CAPTURED'):
        # Paiement réussi → activer la pub
        pub.payment_status  = 'paid'
        pub.payment_trans_id = trans_id
        pub.actif           = True
        pub.date_debut      = date.today()
        pub.date_fin        = date.today() + timedelta(weeks=pub.duree_semaines)
        pub.save()
    else:
        # Paiement échoué
        pub.payment_status   = 'failed'
        pub.payment_trans_id = trans_id
        pub.save()

    return HttpResponse('OK', status=200)
