"""
Seed initial — Tahiti Business Groupe
Lance ce script UNE SEULE FOIS pour peupler la base avec les données mockées du Jour 1.

Usage (depuis le dossier backend/) :
    python seed_data.py
"""

import json
import sys
from datetime import datetime, timedelta
import random

from database import SessionLocal, engine
import models
from auth import get_password_hash

models.Base.metadata.create_all(bind=engine)
db = SessionLocal()


def seed():
    # ------------------------------------------------------------------ #
    #  Vérification : déjà seedé ?                                        #
    # ------------------------------------------------------------------ #
    if db.query(models.User).count() > 0:
        print("⚠️  La base de données contient déjà des données. Seed ignoré.")
        print("    Supprimez tahiti_business.db et relancez pour repartir de zéro.")
        sys.exit(0)

    print("🌴  Seeding Tahiti Business Groupe…")

    # ------------------------------------------------------------------ #
    #  USERS                                                               #
    # ------------------------------------------------------------------ #
    users_data = [
        {
            "email": "admin@tbg.pf",
            "password": "Admin2026!",
            "nom": "Admin TBG",
            "role": "admin",
            "tel": "89 00 00 00",
            "whatsapp": "68900000",
        },
        {
            "email": "pro@tbg.pf",
            "password": "Pro2026!",
            "nom": "Agence Immo Tahiti",
            "role": "pro",
            "tel": "89 11 11 11",
            "whatsapp": "68911111",
        },
        {
            "email": "user@tbg.pf",
            "password": "User2026!",
            "nom": "Marie Teriitaumihau",
            "role": "personnel",
            "tel": "89 22 22 22",
            "whatsapp": "68922222",
        },
        {
            "email": "garage@tbg.pf",
            "password": "Garage2026!",
            "nom": "Garage Central Papeete",
            "role": "pro",
            "tel": "89 33 33 33",
            "whatsapp": "68933333",
        },
    ]

    users = {}
    for u in users_data:
        db_user = models.User(
            email=u["email"],
            password_hash=get_password_hash(u["password"]),
            nom=u["nom"],
            role=u["role"],
            tel=u.get("tel"),
            whatsapp=u.get("whatsapp"),
        )
        db.add(db_user)
        db.flush()
        users[u["email"]] = db_user
        print(f"   ✅ User créé : {u['email']} ({u['role']})")

    db.commit()

    # ------------------------------------------------------------------ #
    #  ANNONCES — données du Jour 1 converties                            #
    # ------------------------------------------------------------------ #
    now = datetime.utcnow()

    annonces_data = [
        # === PROMO ===
        {
            "titre": "iPhone 15 Pro Max 256Go — PROMO LIMITÉE",
            "categorie": "promo",
            "localisation": "Papeete",
            "prix": 165000,
            "prix_label": "165 000 XPF",
            "description": "iPhone 15 Pro Max 256Go en excellent état, vendu avec boîte et accessoires d'origine. Motif : upgrade vers 16. Prix ferme.",
            "specs": {"Modèle": "iPhone 15 Pro Max", "Stockage": "256 Go", "État": "Très bon", "Couleur": "Titane Naturel"},
            "user": "user@tbg.pf",
            "boost": False,
            "offset_days": 0,
        },
        {
            "titre": "Climatiseur Samsung Inverter — DÉSTOCKAGE",
            "categorie": "promo",
            "localisation": "Punaauia",
            "prix": 45000,
            "prix_label": "45 000 XPF",
            "description": "Climatiseur Samsung Inverter 12 000 BTU, déstockage boutique. Neuf dans son carton. Installation non incluse.",
            "specs": {"Puissance": "12 000 BTU", "Type": "Inverter", "Marque": "Samsung", "État": "Neuf"},
            "user": "pro@tbg.pf",
            "boost": True,
            "offset_days": 1,
        },
        {
            "titre": "Scooter Yamaha NMAX 125cc — URGENT",
            "categorie": "promo",
            "localisation": "Faaa",
            "prix": 280000,
            "prix_label": "280 000 XPF",
            "description": "NMAX 125cc 2022 en très bon état, révision faite. Vendu URGENT, départ en métropole. Carte grise propre.",
            "specs": {"Année": "2022", "Km": "18 000 km", "Cylindrée": "125 cc", "Type": "Scooter"},
            "user": "garage@tbg.pf",
            "boost": False,
            "offset_days": 0,
        },

        # === IMMOBILIER ===
        {
            "titre": "Appartement F3 vue mer — Papeete centre",
            "categorie": "immobilier",
            "localisation": "Papeete",
            "prix": 180000,
            "prix_label": "180 000 XPF/mois",
            "description": "Bel appartement F3 avec vue mer, lumineux, au 3ème étage sans ascenseur. Charges comprises. Disponible immédiatement. Visite sur RDV.",
            "specs": {"Type": "Appartement F3", "Surface": "75 m²", "Étage": "3ème", "Parking": "Oui"},
            "user": "pro@tbg.pf",
            "boost": True,
            "offset_days": 2,
        },
        {
            "titre": "Maison 4 chambres avec piscine",
            "categorie": "immobilier",
            "localisation": "Punaauia",
            "prix": 420000,
            "prix_label": "420 000 XPF/mois",
            "description": "Magnifique maison 4 chambres avec piscine privée, jardin tropical et vue montagne. Quartier résidentiel calme. Garage 2 voitures.",
            "specs": {"Type": "Maison", "Surface": "150 m²", "Chambres": "4", "Piscine": "Oui"},
            "user": "pro@tbg.pf",
            "boost": True,
            "offset_days": 3,
        },
        {
            "titre": "Studio meublé proche centre",
            "categorie": "immobilier",
            "localisation": "Pirae",
            "prix": 85000,
            "prix_label": "85 000 XPF/mois",
            "description": "Studio entièrement meublé équipé à 5 min à pied du marché de Papeete. Idéal pour travailleur seul ou étudiant.",
            "specs": {"Type": "Studio", "Surface": "28 m²", "Meublé": "Oui", "Parking": "Non"},
            "user": "user@tbg.pf",
            "boost": False,
            "offset_days": 4,
        },
        {
            "titre": "Terrain 1200m² viabilisé — Taravao",
            "categorie": "immobilier",
            "localisation": "Taravao",
            "prix": 12500000,
            "prix_label": "12 500 000 XPF",
            "description": "Beau terrain plat de 1200 m² entièrement viabilisé (eau, électricité, téléphone) avec belle vue montagne. Permis de construire possible.",
            "specs": {"Type": "Terrain", "Surface": "1 200 m²", "Viabilisé": "Oui", "Vue": "Montagne"},
            "user": "pro@tbg.pf",
            "boost": False,
            "offset_days": 5,
        },
        {
            "titre": "Villa luxe bord de lagon — Moorea",
            "categorie": "immobilier",
            "localisation": "Moorea",
            "prix": 850000,
            "prix_label": "850 000 XPF/mois",
            "description": "Villa prestige directement sur le lagon, 5 chambres, piscine à débordement, plage privée. Idéal pour famille ou investissement touristique.",
            "specs": {"Type": "Villa", "Surface": "220 m²", "Chambres": "5", "Vue": "Lagon"},
            "user": "pro@tbg.pf",
            "boost": True,
            "offset_days": 6,
        },
        {
            "titre": "Local commercial 60m² — Papeete",
            "categorie": "immobilier",
            "localisation": "Papeete",
            "prix": 150000,
            "prix_label": "150 000 XPF/mois",
            "description": "Local commercial en rez-de-chaussée, grande vitrine sur rue passante. Climatisation, WC. 3 places de parking incluses.",
            "specs": {"Type": "Commercial", "Surface": "60 m²", "Vitrine": "Oui", "Parking": "3 places"},
            "user": "pro@tbg.pf",
            "boost": False,
            "offset_days": 7,
        },
        {
            "titre": "Colocation F4 — 1 chambre disponible",
            "categorie": "immobilier",
            "localisation": "Faaa",
            "prix": 55000,
            "prix_label": "55 000 XPF/mois",
            "description": "Chambre meublée disponible dans colocation sympathique de 3 personnes. Cuisine et salon communs. Proche marché Faaa.",
            "specs": {"Type": "Colocation", "Surface": "15 m² (chambre)", "Meublé": "Oui", "Colocataires": "2"},
            "user": "user@tbg.pf",
            "boost": False,
            "offset_days": 8,
        },
        {
            "titre": "Duplex neuf standing — Paofai",
            "categorie": "immobilier",
            "localisation": "Papeete",
            "prix": 350000,
            "prix_label": "350 000 XPF/mois",
            "description": "Duplex F4 neuf haut standing, finitions luxe, terrasse vue mer, 2 parkings. Résidence sécurisée avec gardien.",
            "specs": {"Type": "Duplex F4", "Surface": "120 m²", "Neuf": "Oui", "Parking": "2 places"},
            "user": "pro@tbg.pf",
            "boost": True,
            "offset_days": 9,
        },

        # === VEHICULES ===
        {
            "titre": "Toyota Hilux 2022 — Excellent état",
            "categorie": "vehicules",
            "localisation": "Papeete",
            "prix": 3200000,
            "prix_label": "3 200 000 XPF",
            "description": "Hilux double cabine 4x4 en excellent état. Toutes révisions concessionnaire. Carnet d'entretien complet. Pas de négociation.",
            "specs": {"Année": "2022", "Km": "45 000 km", "Énergie": "Diesel", "Boîte": "Automatique"},
            "user": "garage@tbg.pf",
            "boost": True,
            "offset_days": 1,
        },
        {
            "titre": "Peugeot 208 2021 — Peu de km",
            "categorie": "vehicules",
            "localisation": "Punaauia",
            "prix": 1800000,
            "prix_label": "1 800 000 XPF",
            "description": "208 automatique très propre, climatisée, GPS, Bluetooth. Contrôle technique récent. Idéale pour ville.",
            "specs": {"Année": "2021", "Km": "28 000 km", "Énergie": "Essence", "Boîte": "Automatique"},
            "user": "user@tbg.pf",
            "boost": False,
            "offset_days": 2,
        },
        {
            "titre": "Yamaha MT-07 2023 — Roadster",
            "categorie": "vehicules",
            "localisation": "Pirae",
            "prix": 1450000,
            "prix_label": "1 450 000 XPF",
            "description": "MT-07 2023 en parfait état, peu de km. Accessoires : sacoches, protection carrosserie. Vendu avec casque.",
            "specs": {"Année": "2023", "Km": "8 000 km", "Cylindrée": "689 cc", "Type": "Roadster"},
            "user": "user@tbg.pf",
            "boost": False,
            "offset_days": 3,
        },
        {
            "titre": "Nissan Navara Double Cab 4x4",
            "categorie": "vehicules",
            "localisation": "Taravao",
            "prix": 2900000,
            "prix_label": "2 900 000 XPF",
            "description": "Navara robuste, idéal pour la campagne et le travail. Benne en aluminium. Quelques rayures sans importance.",
            "specs": {"Année": "2020", "Km": "62 000 km", "Énergie": "Diesel", "Boîte": "Manuelle"},
            "user": "garage@tbg.pf",
            "boost": False,
            "offset_days": 4,
        },
        {
            "titre": "Suzuki Jimny 2023 — Comme neuf",
            "categorie": "vehicules",
            "localisation": "Moorea",
            "prix": 3500000,
            "prix_label": "3 500 000 XPF",
            "description": "Jimny 2023 en parfait état, 12 000 km seulement. Icône du 4x4 compact, parfait pour les pistes de Moorea.",
            "specs": {"Année": "2023", "Km": "12 000 km", "Énergie": "Essence", "Boîte": "Automatique"},
            "user": "user@tbg.pf",
            "boost": False,
            "offset_days": 5,
        },
        {
            "titre": "Honda PCX 125 — 2022",
            "categorie": "vehicules",
            "localisation": "Faaa",
            "prix": 320000,
            "prix_label": "320 000 XPF",
            "description": "PCX 125cc très propre, entretenu avec soin. Idéal pour les déplacements quotidiens en ville. Casque offert.",
            "specs": {"Année": "2022", "Km": "15 000 km", "Cylindrée": "125 cc", "Type": "Scooter"},
            "user": "user@tbg.pf",
            "boost": False,
            "offset_days": 6,
        },
        {
            "titre": "Bateau alu 5m + moteur Yamaha 60cv",
            "categorie": "vehicules",
            "localisation": "Papeete",
            "prix": 1200000,
            "prix_label": "1 200 000 XPF",
            "description": "Bateau aluminium 5m avec moteur Yamaha 60cv injection, remorque incluse. Révisé, gilets de sauvetage fournis.",
            "specs": {"Longueur": "5 m", "Moteur": "Yamaha 60cv", "Année": "2021", "Remorque": "Incluse"},
            "user": "user@tbg.pf",
            "boost": False,
            "offset_days": 7,
        },
        {
            "titre": "Renault Duster 4x4 2022",
            "categorie": "vehicules",
            "localisation": "Mahina",
            "prix": 2100000,
            "prix_label": "2 100 000 XPF",
            "description": "Duster 4x4 en bon état, idéal pour famille. Climatisation, GPS, régulateur. Vendu avec 4 pneus neige offerts.",
            "specs": {"Année": "2022", "Km": "35 000 km", "Énergie": "Diesel", "Boîte": "Manuelle"},
            "user": "garage@tbg.pf",
            "boost": True,
            "offset_days": 8,
        },

        # === NOUVEAUTÉS ===
        {
            "titre": "MacBook Air M3 15\" — Neuf sous blister",
            "categorie": "nouveautes",
            "localisation": "Papeete",
            "prix": 285000,
            "prix_label": "285 000 XPF",
            "description": "MacBook Air M3 15 pouces neuf sous blister, jamais ouvert. Facture Fnac avec garantie 1 an. Couleur Minuit.",
            "specs": {"Modèle": "MacBook Air M3", "Écran": "15.3\"", "RAM": "16 Go", "SSD": "512 Go"},
            "user": "user@tbg.pf",
            "boost": False,
            "offset_days": 0,
        },
        {
            "titre": "Planche de surf 6'2 Al Merrick",
            "categorie": "nouveautes",
            "localisation": "Punaauia",
            "prix": 65000,
            "prix_label": "65 000 XPF",
            "description": "Al Merrick 6'2 en très bon état, 2 sessions seulement. Dérives FCS2 incluses. Idéale pour reef de Teahupo'o.",
            "specs": {"Taille": "6'2\"", "Volume": "32L", "État": "Très bon", "Dérives": "Incluses"},
            "user": "user@tbg.pf",
            "boost": False,
            "offset_days": 1,
        },
        {
            "titre": "PS5 Slim + 2 manettes + 3 jeux",
            "categorie": "nouveautes",
            "localisation": "Pirae",
            "prix": 75000,
            "prix_label": "75 000 XPF",
            "description": "Pack PS5 Slim Digital Edition avec 2 manettes DualSense et 3 jeux : FIFA 25, Spider-Man 2, God of War Ragnarok.",
            "specs": {"Modèle": "PS5 Slim Digital", "Manettes": "2", "Jeux": "3 inclus", "Garantie": "6 mois"},
            "user": "user@tbg.pf",
            "boost": False,
            "offset_days": 2,
        },
        {
            "titre": "Vélo électrique Decathlon 2024",
            "categorie": "nouveautes",
            "localisation": "Faaa",
            "prix": 120000,
            "prix_label": "120 000 XPF",
            "description": "VTC électrique Decathlon Riverside 500E, autonomie 80 km, taille M/L. Chargeur, antivol et garde-boues inclus.",
            "specs": {"Autonomie": "80 km", "Vitesse": "25 km/h", "Taille": "M/L", "Batterie": "500 Wh"},
            "user": "user@tbg.pf",
            "boost": False,
            "offset_days": 3,
        },
        {
            "titre": "Drone DJI Mini 4 Pro + accessoires",
            "categorie": "nouveautes",
            "localisation": "Moorea",
            "prix": 145000,
            "prix_label": "145 000 XPF",
            "description": "DJI Mini 4 Pro avec Fly More Combo : 3 batteries, station de charge, filtres ND, sac de transport. Très peu utilisé.",
            "specs": {"Modèle": "DJI Mini 4 Pro", "Poids": "249 g", "Vidéo": "4K HDR", "Autonomie": "34 min"},
            "user": "user@tbg.pf",
            "boost": False,
            "offset_days": 4,
        },
        {
            "titre": "Appareil photo Canon R50 + objectif",
            "categorie": "nouveautes",
            "localisation": "Papeete",
            "prix": 180000,
            "prix_label": "180 000 XPF",
            "description": "Canon EOS R50 avec objectif 18-45mm, moins de 200 déclenchements. Idéal pour débutant ou semi-pro. Chargeur + carte 64Go inclus.",
            "specs": {"Modèle": "Canon EOS R50", "Capteur": "24.2 MP", "Objectif": "18-45 mm", "Vidéo": "4K"},
            "user": "user@tbg.pf",
            "boost": False,
            "offset_days": 5,
        },
        {
            "titre": "Samsung Galaxy S24 Ultra 256Go",
            "categorie": "nouveautes",
            "localisation": "Arue",
            "prix": 195000,
            "prix_label": "195 000 XPF",
            "description": "S24 Ultra 256Go neuf sous blister. Couleur Titanium Black. S-Pen inclus. Facture avec garantie Samsung 2 ans.",
            "specs": {"Modèle": "Galaxy S24 Ultra", "Stockage": "256 Go", "RAM": "12 Go", "État": "Neuf"},
            "user": "user@tbg.pf",
            "boost": False,
            "offset_days": 6,
        },
        {
            "titre": "Ukulele Kamaka HF-2 Concert",
            "categorie": "nouveautes",
            "localisation": "Papeete",
            "prix": 95000,
            "prix_label": "95 000 XPF",
            "description": "Kamaka HF-2 Concert en bois de koa hawaïen, son exceptionnel. Housse Kamaka incluse. En parfait état, acheté neuf à Hawaï.",
            "specs": {"Modèle": "HF-2 Concert", "Bois": "Koa hawaïen", "État": "Excellent", "Housse": "Incluse"},
            "user": "user@tbg.pf",
            "boost": False,
            "offset_days": 7,
        },

        # === EMPLOI ===
        {
            "titre": "Développeur Web Full-Stack — CDI",
            "categorie": "emploi",
            "localisation": "Papeete",
            "prix": 450000,
            "prix_label": "450 000 XPF/mois",
            "description": "Nous recrutons un développeur Full-Stack (React/Node.js ou Python/FastAPI). Télétravail partiel possible. Equipe jeune et dynamique.",
            "specs": {"Contrat": "CDI", "Niveau": "3-5 ans exp.", "Secteur": "Tech", "Début": "Immédiat"},
            "user": "pro@tbg.pf",
            "boost": True,
            "offset_days": 0,
        },
        {
            "titre": "Serveur/Serveuse restaurant — Temps plein",
            "categorie": "emploi",
            "localisation": "Punaauia",
            "prix": 200000,
            "prix_label": "200 000 XPF/mois",
            "description": "Restaurant gastronomique recherche serveur(se) motivé(e). Débutants acceptés si sérieux. Pourboires importants. Fermeture lundi.",
            "specs": {"Contrat": "CDI", "Niveau": "Débutant accepté", "Horaires": "Soir + WE", "Début": "Mars 2026"},
            "user": "pro@tbg.pf",
            "boost": False,
            "offset_days": 2,
        },
        {
            "titre": "Comptable expérimenté(e) — CDI",
            "categorie": "emploi",
            "localisation": "Papeete",
            "prix": 380000,
            "prix_label": "380 000 XPF/mois",
            "description": "Cabinet d'expertise comptable recherche comptable confirmé(e) maîtrisant Sage et la fiscalité polynésienne. Poste évolutif.",
            "specs": {"Contrat": "CDI", "Niveau": "5 ans min.", "Logiciel": "Sage", "Début": "Avril 2026"},
            "user": "pro@tbg.pf",
            "boost": False,
            "offset_days": 3,
        },
        {
            "titre": "Agent immobilier indépendant",
            "categorie": "emploi",
            "localisation": "Tahiti",
            "prix": None,
            "prix_label": "Commission 3-5%",
            "description": "Agence immobilière cherche agent indépendant pour développer le portefeuille clients. Formation initiale assurée. Permis B obligatoire.",
            "specs": {"Contrat": "Indépendant", "Secteur": "Immobilier", "Permis": "Obligatoire", "Formation": "Assurée"},
            "user": "pro@tbg.pf",
            "boost": False,
            "offset_days": 4,
        },
        {
            "titre": "Graphiste / Webdesigner freelance",
            "categorie": "emploi",
            "localisation": "Remote",
            "prix": None,
            "prix_label": "Sur devis",
            "description": "Agence créative recherche graphiste freelance pour missions ponctuelles (identité visuelle, sites web, réseaux sociaux). Portfolio requis.",
            "specs": {"Contrat": "Freelance", "Logiciels": "Figma, Adobe", "Secteur": "Créatif", "Niveau": "Confirmé"},
            "user": "pro@tbg.pf",
            "boost": False,
            "offset_days": 5,
        },
        {
            "titre": "Mécanicien auto — Garage Faaa",
            "categorie": "emploi",
            "localisation": "Faaa",
            "prix": 250000,
            "prix_label": "250 000 XPF/mois",
            "description": "Garage multimarques recherche mécanicien sérieux et motivé. Poste CDI avec évolution. Outillage fourni. Équipe de 5 mécaniciens.",
            "specs": {"Contrat": "CDI", "Niveau": "CAP/BEP", "Permis": "B obligatoire", "Début": "Immédiat"},
            "user": "garage@tbg.pf",
            "boost": False,
            "offset_days": 6,
        },
        {
            "titre": "Réceptionniste hôtel 4 étoiles — Moorea",
            "categorie": "emploi",
            "localisation": "Moorea",
            "prix": 220000,
            "prix_label": "220 000 XPF/mois",
            "description": "Hôtel de charme à Moorea cherche réceptionniste bilingue FR/EN. CDD renouvelable avec possible logement sur place.",
            "specs": {"Contrat": "CDD 6 mois", "Langues": "FR + EN", "Horaires": "Décalés", "Logement": "Possible"},
            "user": "pro@tbg.pf",
            "boost": False,
            "offset_days": 7,
        },
        {
            "titre": "Livreur colis — Temps partiel matinal",
            "categorie": "emploi",
            "localisation": "Papeete",
            "prix": 120000,
            "prix_label": "120 000 XPF/mois",
            "description": "Société de livraison cherche livreur sérieux pour tournée matinale 8h-13h. Véhicule fourni. Permis B obligatoire. CDI possible après 3 mois.",
            "specs": {"Contrat": "Temps partiel", "Permis": "B obligatoire", "Véhicule": "Fourni", "Horaires": "8h-13h"},
            "user": "pro@tbg.pf",
            "boost": False,
            "offset_days": 8,
        },

        # === VENTE PRIVÉE ===
        {
            "titre": "Canapé d'angle cuir véritable — Noir",
            "categorie": "vente-privee",
            "localisation": "Punaauia",
            "prix": 180000,
            "prix_label": "180 000 XPF",
            "description": "Grand canapé d'angle cuir véritable, 5-6 places, coloris noir. Vendu cause déménagement. Excellent état, sans rayures.",
            "specs": {"Matière": "Cuir véritable", "Couleur": "Noir", "Places": "5-6", "État": "Excellent"},
            "user": "user@tbg.pf",
            "boost": False,
            "offset_days": 1,
        },
        {
            "titre": "TV Samsung 65\" QLED 4K — 2024",
            "categorie": "vente-privee",
            "localisation": "Papeete",
            "prix": 120000,
            "prix_label": "120 000 XPF",
            "description": "Samsung 65 pouces QLED 4K acheté en 2024, comme neuf. Smart TV Tizen, Wifi, Bluetooth, pied et télécommande. Garantie 1 an.",
            "specs": {"Taille": "65 pouces", "Techno": "QLED 4K", "Smart": "Tizen OS", "Garantie": "1 an"},
            "user": "user@tbg.pf",
            "boost": False,
            "offset_days": 2,
        },
        {
            "titre": "Lave-linge LG 9kg A+++ — Presque neuf",
            "categorie": "vente-privee",
            "localisation": "Faaa",
            "prix": 55000,
            "prix_label": "55 000 XPF",
            "description": "Machine à laver LG 9kg classe A+++, 18 mois d'utilisation, très bon état. Départ car achat ensemble combiné.",
            "specs": {"Capacité": "9 kg", "Classe": "A+++", "Marque": "LG", "Garantie": "6 mois"},
            "user": "user@tbg.pf",
            "boost": False,
            "offset_days": 3,
        },
        {
            "titre": "Bureau gaming + chaise ergonomique",
            "categorie": "vente-privee",
            "localisation": "Pirae",
            "prix": 85000,
            "prix_label": "85 000 XPF",
            "description": "Ensemble bureau gaming 140x60cm avec éclairage RGB et chaise ergonomique haut de gamme. Vendu ensemble uniquement. Comme neuf.",
            "specs": {"Bureau": "140x60 cm", "Chaise": "Ergonomique", "LED": "RGB inclus", "État": "Comme neuf"},
            "user": "user@tbg.pf",
            "boost": False,
            "offset_days": 4,
        },
        {
            "titre": "Réfrigérateur double porte Inox Samsung",
            "categorie": "vente-privee",
            "localisation": "Papeete",
            "prix": 95000,
            "prix_label": "95 000 XPF",
            "description": "Samsung 450L double porte Inox avec distributeur d'eau et glaçons. Classe A++. Vendu car rénovation cuisine.",
            "specs": {"Volume": "450 L", "Classe": "A++", "Marque": "Samsung", "Distributeur": "Eau + Glaçons"},
            "user": "user@tbg.pf",
            "boost": False,
            "offset_days": 5,
        },
        {
            "titre": "Matelas King Size mémoire de forme",
            "categorie": "vente-privee",
            "localisation": "Arue",
            "prix": 65000,
            "prix_label": "65 000 XPF",
            "description": "Matelas King Size 180x200cm mémoire de forme haute densité, 25cm d'épaisseur. Neuf dans son emballage, jamais ouvert.",
            "specs": {"Taille": "180x200", "Type": "Mémoire de forme", "Épaisseur": "25 cm", "État": "Neuf"},
            "user": "user@tbg.pf",
            "boost": False,
            "offset_days": 6,
        },
        {
            "titre": "Enceinte JBL PartyBox 310 — 240W",
            "categorie": "vente-privee",
            "localisation": "Papeete",
            "prix": 48000,
            "prix_label": "48 000 XPF",
            "description": "JBL PartyBox 310 en excellent état, son puissant 240W avec effets lumières LED. Batterie 18h autonomie. Micro sans fil inclus.",
            "specs": {"Puissance": "240 W", "Batterie": "18h", "Bluetooth": "5.1", "Lumières": "LED intégrées"},
            "user": "user@tbg.pf",
            "boost": False,
            "offset_days": 7,
        },
        {
            "titre": "Trottinette électrique Xiaomi Pro 2",
            "categorie": "vente-privee",
            "localisation": "Mahina",
            "prix": 42000,
            "prix_label": "42 000 XPF",
            "description": "Xiaomi Mi Electric Scooter Pro 2 en très bon état, autonomie 45km. Chargeur, manuel et housse inclus. Homologuée route.",
            "specs": {"Autonomie": "45 km", "Vitesse": "25 km/h", "Poids": "14.2 kg", "Pliable": "Oui"},
            "user": "user@tbg.pf",
            "boost": False,
            "offset_days": 8,
        },
    ]

    for i, a in enumerate(annonces_data):
        user_obj = users[a["user"]]
        created = now - timedelta(days=a["offset_days"], hours=random.randint(0, 12))
        db_ann = models.Annonce(
            titre=a["titre"],
            description=a["description"],
            prix=a["prix"],
            prix_label=a["prix_label"],
            categorie=a["categorie"],
            localisation=a["localisation"],
            user_id=user_obj.id,
            statut="active",
            photos="[]",
            specs=json.dumps(a["specs"]),
            boost=a["boost"],
            views=random.randint(5, 250),
            created_at=created,
            updated_at=created,
        )
        db.add(db_ann)

    db.commit()
    total = len(annonces_data)
    print(f"   ✅ {total} annonces créées.")

    # ------------------------------------------------------------------ #
    #  MESSAGES d'exemple                                                  #
    # ------------------------------------------------------------------ #
    db.flush()
    sample_annonce = db.query(models.Annonce).filter(
        models.Annonce.categorie == "immobilier"
    ).first()

    if sample_annonce:
        msg = models.Message(
            annonce_id=sample_annonce.id,
            from_user_id=users["user@tbg.pf"].id,
            to_user_id=sample_annonce.user_id,
            content="Bonjour, est-ce que le bien est toujours disponible ? Je souhaite visiter ce week-end.",
            contact_email="user@tbg.pf",
            contact_tel="89 22 22 22",
        )
        db.add(msg)
        db.commit()
        print("   ✅ Message d'exemple créé.")

    # ------------------------------------------------------------------ #
    #  Résumé                                                              #
    # ------------------------------------------------------------------ #
    print("\n🎉  Seed terminé avec succès !")
    print("=" * 50)
    print("  Comptes de test :")
    print("  👑 admin@tbg.pf       / Admin2026!")
    print("  🏢 pro@tbg.pf         / Pro2026!")
    print("  👤 user@tbg.pf        / User2026!")
    print("  🔧 garage@tbg.pf      / Garage2026!")
    print("=" * 50)
    print("  Lancez le serveur : uvicorn main:app --reload")
    print("  Swagger UI        : http://localhost:8000/docs")


if __name__ == "__main__":
    seed()
    db.close()
