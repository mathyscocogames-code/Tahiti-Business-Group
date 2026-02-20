"""
Script de seed Django — crée superuser + 3 pubs mockées + 5 annonces de test
Lancer avec : python seed_django.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tahiti_business.settings')
django.setup()

from users.models import User
from pubs.models import Publicite
from ads.models import Annonce

# ─── SUPERUSER ───────────────────────────────────────────────────────────────
email = 'mathyscocogames@gmail.com'
password = 'CocoGames25@'

if not User.objects.filter(email=email).exists():
    admin = User.objects.create_superuser(email=email, password=password)
    admin.nom = 'Mathys Admin'
    admin.tel = '89 61 06 13'
    admin.role = 'admin'
    admin.save()
    print(f'✅ Superuser créé : {email}')
else:
    admin = User.objects.get(email=email)
    admin.is_staff = True
    admin.is_superuser = True
    admin.role = 'admin'
    admin.set_password(password)
    admin.save()
    print(f'ℹ️  Superuser déjà existant, mot de passe mis à jour : {email}')

# ─── PUBS MOCKÉES ────────────────────────────────────────────────────────────
pubs_data = [
    {
        'titre': 'Air Tahiti Nui',
        'description': 'Vols directs Paris ↔ Papeete',
        'emplacement': 'haut',
        'lien': 'https://www.airtahitinui.com',
        'image_url': '',
        'client_nom': 'Air Tahiti Nui',
        'client_email': 'pub@airtahitinui.com',
        'actif': True,
    },
    {
        'titre': 'Carrefour Polynésie',
        'description': 'Courses en ligne — livraison Tahiti',
        'emplacement': 'milieu',
        'lien': 'https://www.carrefour.pf',
        'image_url': '',
        'client_nom': 'Carrefour PF',
        'client_email': 'pub@carrefour.pf',
        'actif': True,
    },
    {
        'titre': 'Toyota Tahiti',
        'description': 'Concessionnaire officiel Toyota',
        'emplacement': 'bas',
        'lien': '',
        'image_url': '',
        'client_nom': 'Toyota Tahiti',
        'client_email': 'contact@toyotatahiti.pf',
        'actif': True,
    },
]

for pub_data in pubs_data:
    if not Publicite.objects.filter(titre=pub_data['titre']).exists():
        Publicite.objects.create(**pub_data)
        print(f"📢 Pub créée : {pub_data['titre']} [{pub_data['emplacement']}]")
    else:
        print(f"ℹ️  Pub déjà existante : {pub_data['titre']}")

# ─── ANNONCES TEST ───────────────────────────────────────────────────────────
annonces_data = [
    {
        'titre': 'Toyota Hilux 2020 — excellent état',
        'description': 'Double cabine, diesel, 80 000 km. Première main, carnet entretien complet. Idéal pour l\'île.',
        'prix': 3500000,
        'prix_label': '3 500 000 XPF',
        'categorie': 'vehicules',
        'localisation': 'Papeete',
        'statut': 'actif',
        'boost': True,
    },
    {
        'titre': 'iPhone 14 Pro 256Go — Neuf sous blister',
        'description': 'Jamais ouvert, acheté en France il y a 2 mois. Garantie Apple. Toutes couleurs.',
        'prix': 150000,
        'prix_label': '150 000 XPF',
        'categorie': 'electronique',
        'localisation': 'Faa\'a',
        'statut': 'actif',
    },
    {
        'titre': 'Appartement F3 à louer — Papeete centre',
        'description': '3 pièces, 65m², vue mer partielle. Cuisinée, balcon, parking. Proche commerces.',
        'prix': 120000,
        'prix_label': '120 000 XPF/mois',
        'categorie': 'immobilier',
        'localisation': 'Papeete',
        'statut': 'actif',
    },
    {
        'titre': 'Cherche cuisinier expérimenté',
        'description': 'Restaurant gastronomique cherche chef de partie avec 3 ans expérience minimum. Salaire selon profil.',
        'prix': 0,
        'prix_label': 'À négocier',
        'categorie': 'emploi',
        'localisation': 'Moorea',
        'statut': 'actif',
    },
    {
        'titre': 'Planche de surf longboard 9\'2 — occasion',
        'description': 'Longboard Noserider 9\'2, finbox simple, très bon état. Quelques dings réparés. Idéale débutants.',
        'prix': 45000,
        'prix_label': '45 000 XPF',
        'categorie': 'autres',
        'localisation': 'Paea',
        'statut': 'actif',
    },
]

for ad_data in annonces_data:
    if not Annonce.objects.filter(titre=ad_data['titre']).exists():
        Annonce.objects.create(user=admin, **ad_data)
        print(f"📋 Annonce créée : {ad_data['titre'][:40]}...")
    else:
        print(f"ℹ️  Annonce déjà existante : {ad_data['titre'][:40]}")

print('\n🎉 Seed terminé !')
print(f'   → Admin : {email} / {password}')
print(f'   → Site : http://127.0.0.1:8000')
print(f'   → Admin Django : http://127.0.0.1:8000/admin')
print(f'   → Dashboard : http://127.0.0.1:8000/users/admin-dashboard/')