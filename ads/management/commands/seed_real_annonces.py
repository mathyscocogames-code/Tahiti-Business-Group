"""python manage.py seed_real_annonces — importe les vraies annonces TBG en production."""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ads.models import Annonce

ANNONCES = [
    {
        "titre": "Voiture hybride \u2014 Capture Hybride",
        "description": "Renault Capture hybride en excellent \u00e9tat. Faible kilom\u00e9trage, entretien suivi, premi\u00e8re main. Id\u00e9ale pour la ville et les longues distances.",
        "prix": 2900000, "prix_label": "",
        "categorie": "vehicules", "sous_categorie": "vehicules-4x4",
        "localisation": "Papeete",
        "photos": ["/media/annonces/49f8b399e7.webp", "/media/annonces/8de5612a5f.webp"],
    },
    {
        "titre": "Citro\u00ebn C3 \u2014 Tr\u00e8s bon \u00e9tat",
        "description": "Citro\u00ebn C3 en tr\u00e8s bon \u00e9tat g\u00e9n\u00e9ral. Climatisation, faible consommation. Parfaite pour la ville de Papeete.",
        "prix": 1200000, "prix_label": "",
        "categorie": "vehicules", "sous_categorie": "vehicules-4x4",
        "localisation": "Faa'a",
        "photos": ["/media/annonces/c00022ab87.webp", "/media/annonces/a9af7b19a8.webp", "/media/annonces/51fce098ad.webp"],
    },
    {
        "titre": "DFM Joyear \u2014 Utilitaire",
        "description": "DFM Joyear utilitaire, id\u00e9al pour les professionnels. Cabine double, benne, robuste et \u00e9conomique.",
        "prix": 1800000, "prix_label": "",
        "categorie": "vehicules", "sous_categorie": "vehicules-utilitaires",
        "localisation": "Papeete",
        "photos": ["/media/annonces/2d40c4311f.webp"],
    },
    {
        "titre": "Renault Kadjar \u2014 SUV familial",
        "description": "Renault Kadjar SUV familial, finition Intens. GPS, cam\u00e9ra de recul, toit panoramique. Parfait \u00e9tat.",
        "prix": 2200000, "prix_label": "",
        "categorie": "vehicules", "sous_categorie": "vehicules-4x4",
        "localisation": "Pirae",
        "photos": ["/media/annonces/62f9e4f39e.webp"],
    },
    {
        "titre": "PC Lenovo \u2014 Workstation Pro",
        "description": "PC Lenovo Workstation haute performance. Id\u00e9al pour le travail, le graphisme et le montage vid\u00e9o. \u00c9tat impeccable avec facture.",
        "prix": 450000, "prix_label": "",
        "categorie": "electronique", "sous_categorie": "elec-pc",
        "localisation": "Papeete",
        "photos": ["/media/annonces/c30d78992e.webp", "/media/annonces/4e8a19c8a8.webp", "/media/annonces/74cf757da5.webp", "/media/annonces/403b6280d9.webp"],
    },
    {
        "titre": "Peugeot \u2014 Citadine \u00e9conomique",
        "description": "Peugeot en tr\u00e8s bon \u00e9tat, faible kilom\u00e9trage. Parfaite pour les d\u00e9placements quotidiens en ville. Entretien \u00e0 jour.",
        "prix": 950000, "prix_label": "",
        "categorie": "vehicules", "sous_categorie": "vehicules-4x4",
        "localisation": "Mahina",
        "photos": ["/media/annonces/3c9a04d120.webp", "/media/annonces/fce9ee6054.webp"],
    },
    {
        "titre": "Air Fryer \u2014 Friteuse sans huile",
        "description": "Friteuse a air chaud, capacite 4L. Parfaite pour cuisiner sainement sans huile. Excellent etat, peu utilisee.",
        "prix": 15000, "prix_label": "",
        "categorie": "electronique", "sous_categorie": "elec-electromenager",
        "localisation": "Papeete",
        "photos": ["/media/annonces/d76fe1d7e6.webp"],
    },
    {
        "titre": "F2 a louer \u2014 Punaauia",
        "description": "Bel appartement F2 lumineux a Punaauia. Cuisine equipee, salle de bain, parking. Proche commerces et transports.",
        "prix": 75000, "prix_label": "",
        "categorie": "immobilier", "sous_categorie": "immo-appartements",
        "localisation": "Punaauia",
        "photos": ["/media/annonces/1ab9251ee8.webp", "/media/annonces/d2661df933.webp"],
    },
    {
        "titre": "Recherche Agent Commercial Immobilier",
        "description": "Agence immobiliere recrute agent commercial independant. Portefeuille clients existant, formation assuree. Remuneration a la commission attractive.",
        "prix": 0, "prix_label": "Commission",
        "categorie": "emploi", "sous_categorie": "emploi-commerciaux",
        "localisation": "Papeete",
        "photos": ["/media/annonces/4166d8a0b5.webp"],
    },
    {
        "titre": "Agent Immobilier \u2014 Offre emploi",
        "description": "Cabinet immobilier recherche agent immobilier experimente. CDI, salaire fixe + commissions. Gestion de biens residentiels et commerciaux en Polynesie.",
        "prix": 200000, "prix_label": "",
        "categorie": "emploi", "sous_categorie": "emploi-commerciaux",
        "localisation": "Papeete",
        "photos": ["/media/annonces/8ef484d857.webp", "/media/annonces/eba907ad5a.webp", "/media/annonces/c0bd038388.webp", "/media/annonces/00d2b1b15e.webp", "/media/annonces/f84b2228b5.webp"],
    },
    {
        "titre": "Animateur Commercial \u2014 CDD",
        "description": "Entreprise recherche animateur commercial pour promotions en grande surface. CDD 3 mois renouvelable, dynamique et souriant(e) bienvenu(e).",
        "prix": 170000, "prix_label": "",
        "categorie": "emploi", "sous_categorie": "emploi-commerciaux",
        "localisation": "Papeete",
        "photos": ["/media/annonces/dbc5dd1d47.webp"],
    },
    {
        "titre": "Appartement T3 \u2014 A louer Papeete",
        "description": "Grand appartement T3 en centre-ville de Papeete. Vue mer partielle, climatisation, securise. Proche de toutes commodites.",
        "prix": 95000, "prix_label": "",
        "categorie": "immobilier", "sous_categorie": "immo-appartements",
        "localisation": "Papeete",
        "photos": ["/media/annonces/070d32e87c.webp", "/media/annonces/a3d1904b3e.webp", "/media/annonces/fcaf2fe430.webp", "/media/annonces/3a6089dcc1.webp", "/media/annonces/02c57cbc04.webp"],
    },
    {
        "titre": "Appartement F2 \u2014 Location meublee",
        "description": "F2 entierement meuble et equipe, ideal pour une personne ou un couple. Calme, lumineux, acces rapide au centre.",
        "prix": 80000, "prix_label": "",
        "categorie": "immobilier", "sous_categorie": "immo-appartements",
        "localisation": "Papeete",
        "photos": ["/media/annonces/732f4d2e22.webp", "/media/annonces/ed5905fade.webp", "/media/annonces/4470f6d1a9.webp", "/media/annonces/fa67295447.webp", "/media/annonces/466c203371.webp"],
    },
    {
        "titre": "Canap\u00e9 convertible \u2014 Tr\u00e8s bon \u00e9tat",
        "description": "Canap\u00e9 3 places convertible en lit, tissu gris chin\u00e9. M\u00e9canisme fluide, couchage confortable. Peu utilis\u00e9.",
        "prix": 35000, "prix_label": "",
        "categorie": "autres", "sous_categorie": "autres-meubles",
        "localisation": "Papeete",
        "photos": ["/media/annonces/47a8e878ec.webp"],
    },
    {
        "titre": "Canap\u00e9 d'angle \u2014 Simili cuir",
        "description": "Grand canap\u00e9 d'angle en simili cuir noir, 5 places. Confortable et en bon \u00e9tat. Id\u00e9al pour grand salon.",
        "prix": 55000, "prix_label": "",
        "categorie": "autres", "sous_categorie": "autres-meubles",
        "localisation": "Faa'a",
        "photos": ["/media/annonces/493ba47cb3.webp"],
    },
    {
        "titre": "Lot de 4 chaises salle \u00e0 manger",
        "description": "Lot de 4 chaises design pour salle \u00e0 manger. Structure m\u00e9tal, assise rembourr\u00e9e. Prix pour le lot complet.",
        "prix": 12000, "prix_label": "",
        "categorie": "autres", "sous_categorie": "autres-meubles",
        "localisation": "Papeete",
        "photos": ["/media/annonces/f36d909268.webp"],
    },
    {
        "titre": "Conseiller Immobilier \u2014 CDI",
        "description": "Agence immobili\u00e8re de renom recrute conseiller immobilier confirm\u00e9. Gestion portefeuille clients, prospection, visites. V\u00e9hicule de service fourni.",
        "prix": 220000, "prix_label": "",
        "categorie": "emploi", "sous_categorie": "emploi-commerciaux",
        "localisation": "Papeete",
        "photos": ["/media/annonces/571a2a538a.webp"],
    },
    {
        "titre": "iPad Air \u2014 Comme neuf 256 Go",
        "description": "iPad Air 5e g\u00e9n\u00e9ration, 256 Go, WiFi + Cellular. Tr\u00e8s peu utilis\u00e9, vendu avec chargeur et \u00e9tui de protection.",
        "prix": 85000, "prix_label": "",
        "categorie": "electronique", "sous_categorie": "elec-ordinateurs",
        "localisation": "Papeete",
        "photos": ["/media/annonces/a239043af6.webp", "/media/annonces/755e40b497.webp"],
    },
    {
        "titre": "Lot 2 vasques \u00e0 poser \u2014 Neuves",
        "description": "Lot de 2 vasques rondes \u00e0 poser, c\u00e9ramique blanche. Diam\u00e8tre 40cm. Jamais install\u00e9es, encore dans leur emballage.",
        "prix": 18000, "prix_label": "",
        "categorie": "autres", "sous_categorie": "autres-divers",
        "localisation": "Papeete",
        "photos": ["/media/annonces/6a838b348f.webp"],
    },
    {
        "titre": "PC Gamer \u2014 RTX 4090 / 64 Go DDR5",
        "description": "PC gaming haut de gamme : RTX 4090, 64 Go DDR5, SSD NVMe 2 To. Watercooling AIO 360mm. Performances exceptionnelles pour gaming 4K et montage vid\u00e9o.",
        "prix": 650000, "prix_label": "",
        "categorie": "electronique", "sous_categorie": "elec-pc",
        "localisation": "Papeete",
        "photos": ["/media/annonces/65bef33a88.webp"],
    },
    {
        "titre": "Studio meubl\u00e9 \u2014 Location Papeete",
        "description": "Studio enti\u00e8rement meubl\u00e9 et \u00e9quip\u00e9 au centre de Papeete. Cuisine am\u00e9ricaine, salle d'eau, climatis\u00e9. Id\u00e9al \u00e9tudiant ou jeune actif.",
        "prix": 60000, "prix_label": "",
        "categorie": "immobilier", "sous_categorie": "immo-appartements",
        "localisation": "Papeete",
        "photos": ["/media/annonces/d2ed60d837.webp", "/media/annonces/4fc7e1ec01.webp", "/media/annonces/65ceaa3572.webp", "/media/annonces/5c8ccd9fb3.webp", "/media/annonces/cbfc5ef20d.webp"],
    },
]


class Command(BaseCommand):
    help = 'Importe les 21 vraies annonces TBG en production'

    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.filter(email='admin@tahitibusinessgroup.com').first()
        if not user:
            self.stdout.write(self.style.ERROR('Admin introuvable — lancez create_admin d\'abord.'))
            return

        created = 0
        for data in ANNONCES:
            if Annonce.objects.filter(titre=data['titre']).exists():
                self.stdout.write(f'  ~ Existante : {data["titre"][:55]}')
                continue
            Annonce.objects.create(
                user=user,
                titre=data['titre'],
                description=data['description'],
                prix=data['prix'],
                prix_label=data['prix_label'],
                categorie=data['categorie'],
                sous_categorie=data['sous_categorie'],
                localisation=data['localisation'],
                photos=data['photos'],
                statut='actif',
                boost=False,
            )
            created += 1
            self.stdout.write(f'  + {data["titre"][:60]}')

        self.stdout.write(self.style.SUCCESS(f'\n[OK] {created} annonces importées.'))
