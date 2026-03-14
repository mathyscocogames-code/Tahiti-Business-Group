"""
Module utilitaire pour PayZen by OSB — API Formulaire V2.

Génère les paramètres vads_* signés pour rediriger l'acheteur vers la page
de paiement PayZen, et vérifie la signature des retours (IPN / retour navigateur).

Devise : XPF (ISO 4217 n°953, exposant 0 → 1 XPF = 1 unité).
"""
import hashlib
import hmac
import uuid
from datetime import datetime, timezone

from django.conf import settings


def _get_key():
    """Retourne la clé active (test ou production)."""
    if settings.PAYZEN_MODE == 'PRODUCTION':
        return settings.PAYZEN_KEY_PROD
    return settings.PAYZEN_KEY_TEST


def compute_signature(form_data, key=None):
    """Calcule la signature HMAC-SHA-256 des champs vads_*.

    1. Trier les champs vads_* par ordre alphabétique
    2. Concaténer leurs valeurs avec '+'
    3. Ajouter la clé après un dernier '+'
    4. HMAC-SHA-256, encoder en base64
    """
    import base64
    if key is None:
        key = _get_key()
    # Ne garder que les champs vads_*
    vads = {k: v for k, v in form_data.items() if k.startswith('vads_')}
    # Trier par nom de champ
    sorted_values = [str(vads[k]) for k in sorted(vads.keys())]
    payload = '+'.join(sorted_values)
    signature = hmac.new(
        key.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).digest()
    return base64.b64encode(signature).decode('utf-8')


def build_payzen_form(publicite, request):
    """Construit le dict complet des champs pour le formulaire PayZen.

    Retourne (form_data, payment_url).
    """
    now = datetime.now(timezone.utc)

    # vads_trans_id : 6 caractères alphanumériques, unique par jour par boutique
    trans_id = uuid.uuid4().hex[:6]

    form_data = {
        'vads_site_id':        settings.PAYZEN_SHOP_ID,
        'vads_ctx_mode':       settings.PAYZEN_MODE,
        'vads_trans_date':     now.strftime('%Y%m%d%H%M%S'),
        'vads_trans_id':       trans_id,
        'vads_amount':         str(publicite.prix),  # XPF exponent=0
        'vads_currency':       '953',                # XPF
        'vads_action_mode':    'INTERACTIVE',
        'vads_page_action':    'PAYMENT',
        'vads_payment_config': 'SINGLE',
        'vads_version':        'V2',
        'vads_order_id':       publicite.payment_ref,
        'vads_cust_email':     publicite.client_email,
        'vads_cust_name':      publicite.client_nom,
        'vads_cust_cell_phone': publicite.client_tel,
        'vads_order_info':     f"Pub {publicite.get_emplacement_display()} — {publicite.duree_semaines} sem.",
        'vads_return_mode':    'POST',
        'vads_hash_type':      'HMAC_SHA_256',
    }

    # URLs absolues
    base = request.build_absolute_uri('/')[:-1]  # sans le trailing /
    form_data['vads_url_return'] = f"{base}/pubs/paiement/retour/"
    form_data['vads_url_check']  = f"{base}/pubs/paiement/ipn/"

    # Calculer la signature
    form_data['signature'] = compute_signature(form_data)

    return form_data, settings.PAYZEN_PAYMENT_URL


def verify_signature(post_data):
    """Vérifie la signature d'un retour PayZen (IPN ou navigateur).

    Retourne True si la signature est valide.
    """
    received_sig = post_data.get('signature', '')
    if not received_sig:
        return False
    expected_sig = compute_signature(dict(post_data))
    return hmac.compare_digest(received_sig, expected_sig)
