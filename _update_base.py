"""Update base.html dropdown sous-cat links to use real ?sous_cat= params"""
import re

with open('templates/base.html', encoding='utf-8') as f:
    html = f.read()

# ── Véhicules ──────────────────────────────────────────────────
html = html.replace(
    "          <a href=\"{% url 'liste_annonces' %}?categorie=vehicules&q=voiture\">Voitures</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=vehicules&q=moto\">Motos &amp; Scooters</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=vehicules&q=bateau\">Bateaux</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=vehicules&q=camion\">Camions &amp; Utilitaires</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=vehicules&q=pieces\">Pi\u00e8ces d\u00e9tach\u00e9es</a>",

    "          <a href=\"{% url 'liste_annonces' %}?categorie=vehicules&sous_cat=vehicules-4x4\">4x4 &amp; SUV (Tahiti)</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=vehicules&sous_cat=vehicules-2roues\">2 roues (scooters/motos)</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=vehicules&sous_cat=vehicules-bateaux\">Bateaux &amp; jet-skis</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=vehicules&sous_cat=vehicules-utilitaires\">Utilitaires &amp; camions</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=vehicules&sous_cat=vehicules-pieces\">Pi\u00e8ces auto &amp; accessoires</a>"
)

# ── Immobilier ──────────────────────────────────────────────────
html = html.replace(
    "          <a href=\"{% url 'liste_annonces' %}?categorie=immobilier&q=appartement\">Appartements</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=immobilier&q=maison\">Maisons</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=immobilier&q=terrain\">Terrains</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=immobilier&q=location\">Locations</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=immobilier&q=commerce\">Locaux commerciaux</a>",

    "          <a href=\"{% url 'liste_annonces' %}?categorie=immobilier&sous_cat=immo-appartements\">Appartements &amp; studios</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=immobilier&sous_cat=immo-maisons\">Maisons &amp; villas</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=immobilier&sous_cat=immo-terrains\">Terrains &amp; lots</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=immobilier&sous_cat=immo-bureaux\">Bureaux &amp; commerces</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=immobilier&sous_cat=immo-saisonnieres\">Saisonni\u00e8res (Arue/Papeete)</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=immobilier&sous_cat=immo-parkings\">Parkings &amp; garages</a>"
)

# ── Électronique ────────────────────────────────────────────────
html = html.replace(
    "          <a href=\"{% url 'liste_annonces' %}?categorie=electronique&q=telephone\">T\u00e9l\u00e9phones</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=electronique&q=ordinateur\">Ordinateurs</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=electronique&q=tv\">TV &amp; Audio</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=electronique&q=jeux\">Jeux vid\u00e9o</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=electronique&q=electromenager\">\u00c9lectrom\u00e9nager</a>",

    "          <a href=\"{% url 'liste_annonces' %}?categorie=electronique&sous_cat=elec-telephones\">T\u00e9l\u00e9phones &amp; accessoires</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=electronique&sous_cat=elec-ordinateurs\">Ordinateurs &amp; tablettes</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=electronique&sous_cat=elec-tv\">TV &amp; Audio</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=electronique&sous_cat=elec-jeux\">Jeux vid\u00e9o</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=electronique&sous_cat=elec-electromenager\">\u00c9lectrom\u00e9nager</a>"
)

# ── Emploi ──────────────────────────────────────────────────────
html = html.replace(
    "          <a href=\"{% url 'liste_annonces' %}?categorie=emploi&q=cdi\">CDI / CDD</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=emploi&q=interim\">Int\u00e9rim</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=emploi&q=alternance\">Alternance</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=emploi&q=freelance\">Freelance</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=emploi&q=stage\">Stages</a>",

    "          <a href=\"{% url 'liste_annonces' %}?categorie=emploi&sous_cat=emploi-commerciaux\">Commerciaux</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=emploi&sous_cat=emploi-informatique\">Informatique &amp; D\u00e9v</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=emploi&sous_cat=emploi-hotellerie\">H\u00f4tellerie &amp; Resto</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=emploi&sous_cat=emploi-btp\">BTP &amp; Construction</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=emploi&sous_cat=emploi-services\">Services \u00e0 la personne</a>"
)

# ── Services ────────────────────────────────────────────────────
html = html.replace(
    "          <a href=\"{% url 'liste_annonces' %}?categorie=services&q=travaux\">Travaux &amp; BTP</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=services&q=cours\">Cours &amp; Formation</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=services&q=transport\">Transport</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=services&q=sante\">Sant\u00e9 &amp; Beaut\u00e9</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=services&q=jardinage\">Jardinage</a>",

    "          <a href=\"{% url 'liste_annonces' %}?categorie=services&sous_cat=services-travaux\">Travaux &amp; BTP</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=services&sous_cat=services-cours\">Cours &amp; Formation</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=services&sous_cat=services-transport\">Transport</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=services&sous_cat=services-sante\">Sant\u00e9 &amp; Beaut\u00e9</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=services&sous_cat=services-jardinage\">Jardinage</a>"
)

# ── Autres → Vente privée ───────────────────────────────────────
html = html.replace(
    "          <div class=\"cat-dropdown__header\">Autres</div>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=autres\">Toutes</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=autres&q=loisirs\">Loisirs &amp; Sports</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=autres&q=vetements\">V\u00eatements &amp; Mode</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=autres&q=meubles\">Meubles &amp; D\u00e9co</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=autres&q=animaux\">Animaux</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=autres&q=divers\">Divers</a>",

    "          <div class=\"cat-dropdown__header\">Vente priv\u00e9e &amp; Autres</div>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=autres\">Toutes</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=autres&sous_cat=autres-electronique\">\u00c9lectronique &amp; PC</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=autres&sous_cat=autres-meubles\">Meubles &amp; D\u00e9co</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=autres&sous_cat=autres-vetements\">V\u00eatements &amp; Mode</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=autres&sous_cat=autres-sport\">Sport &amp; Loisirs</a>\n"
    "          <a href=\"{% url 'liste_annonces' %}?categorie=autres&sous_cat=autres-puericulture\">Pu\u00e9riculture</a>"
)

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('base.html dropdown links updated OK')