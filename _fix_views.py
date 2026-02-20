"""Rewrite page_business with properly quoted strings."""

with open('ads/views.py', encoding='utf-8') as f:
    src = f.read()

# Find and replace the entire page_business function
START = 'def page_business(request):\n'
END   = '\n\ndef index(request):\n'

start_idx = src.find(START)
end_idx   = src.find(END, start_idx)

if start_idx < 0 or end_idx < 0:
    print('ERROR: markers not found')
    exit(1)

NEW_FUNC = (
    'def page_business(request):\n'
    '    ouvertures = [\n'
    "        {'emoji': '\U0001f697', 'nom': 'Auto-\u00e9cole Route 89', 'description': 'Nouvelle auto-\u00e9cole avec moniteurs bilingues fran\u00e7ais/tahitien.', 'secteur': 'Formation', 'lieu': 'Arue'},\n"
    "        {'emoji': '\U0001f35c', 'nom': 'Poke Tahiti Mahina', 'description': 'Restaurant poke bowl avec produits locaux\u00a0: thon, crevettes, l\u00e9gumes du fenua.', 'secteur': 'Restauration', 'lieu': 'Mahina'},\n"
    "        {'emoji': '\U0001f4fa', 'nom': 'Hi-Fi Store Punaauia', 'description': \"Magasin d'\u00e9lectronique grand public avec SAV et livraison sur Tahiti.\", 'secteur': '\u00c9lectronique', 'lieu': 'Punaauia'},\n"
    "        {'emoji': '\U0001f488', 'nom': 'Barbershop Papara', 'description': 'Salon de coiffure homme moderne avec r\u00e9servation en ligne.', 'secteur': 'Beaut\u00e9', 'lieu': 'Papara'},\n"
    "        {'emoji': '\U0001f33f', 'nom': 'Jardinage Vert Fenua', 'description': \"Service d'entretien jardins, taille, arrosage automatique.\", 'secteur': 'Services', 'lieu': 'Papeete'},\n"
    "        {'emoji': '\U0001f3cb\ufe0f', 'nom': 'FitZone Pirae', 'description': 'Nouvelle salle de sport avec \u00e9quipements cardio et musculation derni\u00e8re g\u00e9n\u00e9ration.', 'secteur': 'Sport', 'lieu': 'Pirae'},\n"
    '    ]\n'
    '    recrutements = [\n'
    "        {'emoji': '\U0001f695', 'poste': 'Chauffeurs VTC', 'entreprise': 'Tahiti Taxi Connect', 'lieu': 'Papeete', 'nb': 15, 'detail': 'Permis B requis, horaires flexibles, v\u00e9hicule fourni.'},\n"
    "        {'emoji': '\U0001f4bb', 'poste': 'D\u00e9veloppeurs web', 'entreprise': 'Tahiti Informatique', 'lieu': \"Faa'a\", 'nb': 5, 'detail': 'Django/React, CDI, salaire selon exp\u00e9rience.'},\n"
    "        {'emoji': '\U0001f3e8', 'poste': 'R\u00e9ceptionnistes', 'entreprise': 'Hotel Tara Nui', 'lieu': 'Bora Bora', 'nb': 3, 'detail': 'Anglais indispensable, logement possible sur place.'},\n"
    "        {'emoji': '\U0001f3d7\ufe0f', 'poste': 'Ma\u00e7ons confirm\u00e9s', 'entreprise': 'BTP Polyn\u00e9sie', 'lieu': 'Tahiti', 'nb': 8, 'detail': 'Exp\u00e9rience 3 ans minimum, chantiers r\u00e9sidentiels et commerciaux.'},\n"
    "        {'emoji': '\U0001f4e6', 'poste': 'Livreurs', 'entreprise': 'Fenua Express', 'lieu': 'Tahiti + Moorea', 'nb': 10, 'detail': 'Scooter ou voiture, temps plein ou partiel disponible.'},\n"
    '    ]\n'
    '    tendances = [\n'
    "        {'emoji': '\U0001f3e0', 'titre': 'Immobilier Arue en hausse', 'desc': 'Les prix des terrains \u00e0 Arue ont augment\u00e9 de 12\u00a0% en 2025. Forte demande r\u00e9sidentielle.'},\n"
    "        {'emoji': '\U0001f697', 'titre': \"V\u00e9hicules d'occasion\u00a0: march\u00e9 actif\", 'desc': 'Les annonces v\u00e9hicules repr\u00e9sentent 35\u00a0% du trafic TBG. Les 4x4 et SUV sont les plus recherch\u00e9s.'},\n"
    "        {'emoji': '\U0001f4f1', 'titre': '\u00c9lectronique reconditionn\u00e9 populaire', 'desc': 'Forte hausse des annonces smartphones reconditionnés. iPhone 13/14 dominent le march\u00e9.'},\n"
    "        {'emoji': '\U0001f4bc', 'titre': 'Secteur BTP en pleine expansion', 'desc': \"Nombreux chantiers publics et priv\u00e9s en cours. Forte demande en main-d'\u0153uvre qualifi\u00e9e.\"},\n"
    '    ]\n'
    '    partenaires = [\n'
    "        {'emoji': '\U0001f6d2', 'nom': 'Carrefour Tahiti', 'secteur': 'Grande distribution'},\n"
    "        {'emoji': '\U0001f4e1', 'nom': 'Vini', 'secteur': 'T\u00e9l\u00e9coms'},\n"
    "        {'emoji': '\U0001f3e6', 'nom': 'Banque de Polyn\u00e9sie', 'secteur': 'Finance'},\n"
    "        {'emoji': '\u2708\ufe0f', 'nom': 'Air Tahiti Nui', 'secteur': 'Transport a\u00e9rien'},\n"
    "        {'emoji': '\U0001f3e5', 'nom': 'Clinique Paofai', 'secteur': 'Sant\u00e9'},\n"
    "        {'emoji': '\U0001f393', 'nom': 'UPF', 'secteur': 'Universit\u00e9'},\n"
    "        {'emoji': '\U0001f527', 'nom': 'Total Polyn\u00e9sie', 'secteur': '\u00c9nergie'},\n"
    "        {'emoji': '\U0001f33a', 'nom': 'Office du Tourisme', 'secteur': 'Tourisme'},\n"
    '    ]\n'
    '    return render(request, \'ads/business.html\', {\n'
    "        'ouvertures': ouvertures,\n"
    "        'recrutements': recrutements,\n"
    "        'tendances': tendances,\n"
    "        'partenaires': partenaires,\n"
    '    })'
)

result = src[:start_idx] + NEW_FUNC + src[end_idx:]

with open('ads/views.py', 'w', encoding='utf-8') as f:
    f.write(result)
print('page_business rewritten OK')