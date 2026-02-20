"""Remplace le bloc extra_js de deposer.html par la version complète 16 catégories."""

with open('templates/ads/deposer.html', encoding='utf-8') as f:
    html = f.read()

OLD = """{% block extra_js %}
<script>

// Sous-catégories dynamiques
const SOUS_CATS_DEP = {{ sous_categories_json|safe }};
function updateSousCatsDep(cat) {
  const sel = document.getElementById('id_sous_categorie');
  if (!sel) return;
  sel.innerHTML = '<option value="">— Toutes / Général</option>';
  (SOUS_CATS_DEP[cat] || []).forEach(({value, label}) => {
    const opt = document.createElement('option');
    opt.value = value; opt.textContent = label;
    sel.appendChild(opt);
  });
  renderSpecs(''); // reset specs when category changes
}
function togglePrix(cat) {
  const row = document.getElementById('prix-row');
  if (row) row.style.display = cat === 'emploi' ? 'none' : '';
}
const catSelDep = document.getElementById('id_categorie');
if (catSelDep) {
  catSelDep.addEventListener('change', () => {
    updateSousCatsDep(catSelDep.value);
    togglePrix(catSelDep.value);
  });
  updateSousCatsDep(catSelDep.value);
  togglePrix(catSelDep.value);
}"""

if OLD not in html:
    print("ERROR: OLD anchor not found")
    exit(1)

NEW = """{% block extra_js %}
<script>

// ─── Sous-catégories dynamiques ────────────────────────────────────────────────
const SOUS_CATS_DEP = {{ sous_categories_json|safe }};

function updateSousCatsDep(cat) {
  const sel = document.getElementById('id_sous_categorie');
  if (!sel) return;
  sel.innerHTML = '<option value="">— Toutes / Général</option>';
  (SOUS_CATS_DEP[cat] || []).forEach(({value, label}) => {
    const opt = document.createElement('option');
    opt.value = value; opt.textContent = label;
    sel.appendChild(opt);
  });
  renderSpecs('');
  adaptPrix(cat, '');
}

function togglePrix(cat) {
  const row = document.getElementById('prix-row');
  if (row) row.style.display = cat === 'emploi' ? 'none' : '';
}

// Adapte le label Prix selon la catégorie/sous-catégorie
function adaptPrix(cat, sousCat) {
  const row = document.getElementById('prix-row');
  if (!row) return;
  const lbl = row.querySelector('label');
  const inp = row.querySelector('input');
  if (cat === 'emploi') {
    row.style.display = 'none';
    return;
  }
  row.style.display = '';
  if (cat === 'immobilier') {
    const isLoc = ['immo-appartements','immo-maisons','immo-bureaux'].includes(sousCat);
    const isSaison = sousCat === 'immo-saisonnieres';
    if (lbl) lbl.textContent = isSaison ? 'Tarif de base (XPF)' : (isLoc ? 'Loyer / mois (XPF)' : 'Prix de vente (XPF)');
    if (inp) inp.placeholder = isSaison ? '150 000' : (isLoc ? '80 000' : '25 000 000');
  } else {
    if (lbl) lbl.textContent = 'Prix (XPF)';
    if (inp) inp.placeholder = '';
  }
}

const catSelDep = document.getElementById('id_categorie');
if (catSelDep) {
  catSelDep.addEventListener('change', () => {
    updateSousCatsDep(catSelDep.value);
    adaptPrix(catSelDep.value, '');
  });
  updateSousCatsDep(catSelDep.value);
  adaptPrix(catSelDep.value, '');
}"""

html = html.replace(OLD, NEW, 1)

# ── Remplacer l'ancien bloc SPECS_DEF + renderSpecs ──────────────────────────
OLD2 = """// ─── Formulaire adaptatif par sous-catégorie ─────────────────────────────────
const SPECS_DEF = {
  'vehicules-4x4': [
    { name: 'kilometrage', label: 'Kilométrage (km)', type: 'number', placeholder: 'Ex: 45 000' },
    { name: 'annee',       label: 'Année',            type: 'number', placeholder: 'Ex: 2019' },
    { name: 'carburant',   label: 'Carburant',         type: 'select', options: ['Essence','Diesel','Électrique','Hybride'] },
    { name: 'boite',       label: 'Boîte de vitesse',  type: 'select', options: ['Manuelle','Automatique'] },
  ],
  'vehicules-2roues': [
    { name: 'cylindree', label: 'Cylindrée (cc)',  type: 'number', placeholder: 'Ex: 125' },
    { name: 'annee',     label: 'Année',           type: 'number', placeholder: 'Ex: 2021' },
    { name: 'permis',    label: 'Permis requis',   type: 'select', options: ['Non (50cc)','A1 (125cc)','A2','A'] },
  ],
  'vehicules-bateaux': [
    { name: 'longueur_m', label: 'Longueur (m)',        type: 'number', placeholder: 'Ex: 6' },
    { name: 'moteur_hp',  label: 'Puissance moteur (CV)', type: 'number', placeholder: 'Ex: 40' },
    { name: 'annee',      label: 'Année',               type: 'number', placeholder: 'Ex: 2018' },
  ],
  'vehicules-utilitaires': [
    { name: 'kilometrage', label: 'Kilométrage (km)', type: 'number', placeholder: 'Ex: 120 000' },
    { name: 'annee',       label: 'Année',            type: 'number', placeholder: 'Ex: 2017' },
    { name: 'carburant',   label: 'Carburant',         type: 'select', options: ['Diesel','Essence','Électrique'] },
  ],
  'immo-appartements': [
    { name: 'surface_m2',  label: 'Surface (m²)',         type: 'number', placeholder: 'Ex: 65' },
    { name: 'nb_pieces',   label: 'Nombre de pièces',     type: 'number', placeholder: 'Ex: 3' },
    { name: 'loyer_mois',  label: 'Loyer / mois (XPF)',   type: 'number', placeholder: 'Ex: 80 000' },
    { name: 'caution_xpf', label: 'Caution (XPF)',        type: 'number', placeholder: 'Ex: 160 000' },
  ],
  'immo-maisons': [
    { name: 'surface_m2',  label: 'Surface habitable (m²)', type: 'number', placeholder: 'Ex: 120' },
    { name: 'terrain_m2',  label: 'Surface terrain (m²)',   type: 'number', placeholder: 'Ex: 500' },
    { name: 'nb_pieces',   label: 'Nombre de pièces',       type: 'number', placeholder: 'Ex: 4' },
  ],
  'immo-terrains': [
    { name: 'surface_m2', label: 'Surface (m²)', type: 'number', placeholder: 'Ex: 1 000' },
  ],
  'immo-bureaux': [
    { name: 'surface_m2', label: 'Surface (m²)',       type: 'number', placeholder: 'Ex: 80' },
    { name: 'loyer_mois', label: 'Loyer / mois (XPF)', type: 'number', placeholder: 'Ex: 120 000' },
  ],
  'immo-saisonnieres': [
    { name: 'surface_m2',     label: 'Surface (m²)',         type: 'number', placeholder: 'Ex: 50' },
    { name: 'nb_couchages',   label: 'Nombre de couchages',  type: 'number', placeholder: 'Ex: 4' },
    { name: 'tarif_semaine',  label: 'Tarif / semaine (XPF)', type: 'number', placeholder: 'Ex: 50 000' },
  ],
  'emploi-commerciaux':  _emploiFields(),
  'emploi-informatique': _emploiFields(),
  'emploi-hotellerie':   _emploiFields(),
  'emploi-btp':          _emploiFields(),
  'emploi-services':     _emploiFields(),
  'elec-telephones': [
    { name: 'marque', label: 'Marque',  type: 'text',   placeholder: 'Ex: Samsung, Apple\u2026' },
    { name: 'modele', label: 'Mod\u00e8le',  type: 'text',   placeholder: 'Ex: iPhone 14' },
    { name: 'etat',   label: '\u00c9tat',    type: 'select', options: ['Neuf','Tr\u00e8s bon','Bon','Passable'] },
  ],
  'elec-ordinateurs': [
    { name: 'ram_gb',      label: 'RAM (Go)',     type: 'number', placeholder: 'Ex: 16' },
    { name: 'stockage_gb', label: 'Stockage (Go)', type: 'number', placeholder: 'Ex: 512' },
    { name: 'processeur',  label: 'Processeur',   type: 'text',   placeholder: 'Ex: Intel i5 12e gen' },
    { name: 'etat',        label: '\u00c9tat',         type: 'select', options: ['Neuf','Tr\u00e8s bon','Bon','Passable'] },
  ],
  'elec-pc': [
    { name: 'ram_gb',      label: 'RAM (Go)',     type: 'number', placeholder: 'Ex: 8' },
    { name: 'stockage_gb', label: 'Stockage (Go)', type: 'number', placeholder: 'Ex: 256' },
    { name: 'processeur',  label: 'Processeur',   type: 'text',   placeholder: 'Ex: Ryzen 5 5600X' },
    { name: 'etat',        label: '\u00c9tat',         type: 'select', options: ['Neuf','Tr\u00e8s bon','Bon','Passable'] },
  ],
  'elec-tv': [
    { name: 'taille_pouces', label: 'Taille (pouces)', type: 'number', placeholder: 'Ex: 55' },
    { name: 'etat',          label: '\u00c9tat',            type: 'select', options: ['Neuf','Tr\u00e8s bon','Bon','Passable'] },
  ],
  'elec-electromenager': [
    { name: 'marque', label: 'Marque', type: 'text',   placeholder: 'Ex: Samsung, LG\u2026' },
    { name: 'etat',   label: '\u00c9tat',   type: 'select', options: ['Neuf','Tr\u00e8s bon','Bon','Passable'] },
  ],
};

function _emploiFields() {
  return [
    { name: 'type_contrat',    label: 'Type de contrat',      type: 'select', options: ['CDI','CDD','Int\u00e9rim','Stage','Freelance'] },
    { name: 'salaire_xpf',     label: 'Salaire brut (XPF/mois)', type: 'number', placeholder: 'Ex: 200 000' },
    { name: 'heures_semaine',  label: 'Heures / semaine',     type: 'number', placeholder: 'Ex: 39' },
    { name: 'experience_ans',  label: 'Exp\u00e9rience requise (ans)', type: 'number', placeholder: 'Ex: 2' },
  ];
}
// Patch : assign emploi functions now that _emploiFields is defined
['emploi-commerciaux','emploi-informatique','emploi-hotellerie','emploi-btp','emploi-services'].forEach(k => {
  SPECS_DEF[k] = _emploiFields();
});

function renderSpecs(souscat) {
  const container = document.getElementById('specs-container');
  if (!container) return;
  const fields = SPECS_DEF[souscat];
  if (!fields || fields.length === 0) { container.innerHTML = ''; return; }

  let html = '<div class="border-t border-gray-200 pt-5 mt-1">';
  html += '<p class="text-xs font-bold text-gray-500 uppercase tracking-wide mb-3">Caract\u00e9ristiques optionnelles</p>';
  html += '<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">';
  fields.forEach(f => {
    html += '<div>';
    html += `<label class="block text-xs font-bold text-gray-600 uppercase tracking-wide mb-1.5">${f.label}</label>`;
    if (f.type === 'select') {
      html += `<select name="spec_${f.name}" class="form-input"><option value="">— Choisir</option>`;
      f.options.forEach(o => { html += `<option value="${o}">${o}</option>`; });
      html += '</select>';
    } else {
      html += `<input type="${f.type}" name="spec_${f.name}" class="form-input" placeholder="${f.placeholder || ''}">`;
    }
    html += '</div>';
  });
  html += '</div></div>';
  container.innerHTML = html;
}

// Écouter sous-catégorie
const sousCatSel = document.getElementById('id_sous_categorie');
if (sousCatSel) {
  sousCatSel.addEventListener('change', () => renderSpecs(sousCatSel.value));
}"""

if OLD2 not in html:
    print("ERROR: OLD2 SPECS_DEF block not found")
    # Try to detect where we are
    idx = html.find('const SPECS_DEF')
    print(f"SPECS_DEF found at index: {idx}")
    exit(1)

NEW2 = """// ─── Formulaire adaptatif — définitions par sous-catégorie ───────────────────
const SPECS_DEF = {

  // VÉHICULES
  'vehicules-4x4': [
    { name: 'annee',       label: 'Année',              type: 'number', placeholder: 'Ex: 2019' },
    { name: 'kilometrage', label: 'Kilométrage (km)',    type: 'number', placeholder: 'Ex: 45 000' },
    { name: 'carburant',   label: 'Carburant',           type: 'select', options: ['Essence','Diesel','Hybride','Électrique','GPL'] },
    { name: 'boite',       label: 'Boîte de vitesse',    type: 'select', options: ['Manuelle','Automatique'] },
    { name: 'nb_places',   label: 'Places',              type: 'number', placeholder: 'Ex: 5' },
    { name: 'etat',        label: 'État général',        type: 'select', options: ['Excellent','Bon','Correct','À réparer'] },
  ],
  'vehicules-2roues': [
    { name: 'annee',      label: 'Année',           type: 'number', placeholder: 'Ex: 2021' },
    { name: 'cylindree',  label: 'Cylindrée (cc)',   type: 'number', placeholder: 'Ex: 125' },
    { name: 'kilometrage',label: 'Kilométrage (km)', type: 'number', placeholder: 'Ex: 8 000' },
    { name: 'permis',     label: 'Permis requis',    type: 'select', options: ['Non requis (50cc)','A1 (125cc)','A2','A (moto)'] },
    { name: 'etat',       label: 'État',             type: 'select', options: ['Neuf','Très bon','Bon','Passable'] },
  ],
  'vehicules-bateaux': [
    { name: 'annee',      label: 'Année',             type: 'number', placeholder: 'Ex: 2018' },
    { name: 'longueur_m', label: 'Longueur (m)',       type: 'number', placeholder: 'Ex: 6' },
    { name: 'moteur_hp',  label: 'Puissance (CV)',      type: 'number', placeholder: 'Ex: 40' },
    { name: 'type_bateau',label: 'Type',               type: 'select', options: ['Hors-bord','Voilier','Catamaran','Jet-ski','Pneumatique','Autre'] },
    { name: 'etat',       label: 'État',               type: 'select', options: ['Excellent','Bon','Correct','À réviser'] },
  ],
  'vehicules-utilitaires': [
    { name: 'annee',        label: 'Année',            type: 'number', placeholder: 'Ex: 2017' },
    { name: 'kilometrage',  label: 'Kilométrage (km)',  type: 'number', placeholder: 'Ex: 120 000' },
    { name: 'carburant',    label: 'Carburant',         type: 'select', options: ['Diesel','Essence','Électrique'] },
    { name: 'charge_kg',    label: 'Charge utile (kg)', type: 'number', placeholder: 'Ex: 1 500' },
    { name: 'ptac_kg',      label: 'PTAC (kg)',          type: 'number', placeholder: 'Ex: 3 500' },
  ],
  'vehicules-pieces': [
    { name: 'marque',         label: 'Marque véhicule',     type: 'text',   placeholder: 'Ex: Toyota, Peugeot…' },
    { name: 'modele',         label: 'Modèle / référence',  type: 'text',   placeholder: 'Ex: Corolla, 308…' },
    { name: 'annee_compat',   label: 'Année de compatibilité', type: 'number', placeholder: 'Ex: 2015' },
    { name: 'etat',           label: 'État de la pièce',    type: 'select', options: ['Neuve','Occasion TBE','Occasion bon état','Pour pièces'] },
  ],

  // IMMOBILIER
  'immo-appartements': [
    { name: 'surface_m2',  label: 'Surface (m²)',          type: 'number', placeholder: 'Ex: 65' },
    { name: 'nb_pieces',   label: 'Nombre de pièces',      type: 'number', placeholder: 'Ex: 3' },
    { name: 'etage',       label: 'Étage',                 type: 'number', placeholder: 'Ex: 2' },
    { name: 'meuble',      label: 'Meublé',                type: 'checkbox' },
    { name: 'parking',     label: 'Parking inclus',        type: 'checkbox' },
    { name: 'caution_xpf', label: 'Caution (XPF)',         type: 'number', placeholder: 'Ex: 160 000' },
  ],
  'immo-maisons': [
    { name: 'surface_m2',  label: 'Surface habitable (m²)', type: 'number', placeholder: 'Ex: 120' },
    { name: 'terrain_m2',  label: 'Surface terrain (m²)',   type: 'number', placeholder: 'Ex: 500' },
    { name: 'nb_pieces',   label: 'Nombre de pièces',       type: 'number', placeholder: 'Ex: 4' },
    { name: 'piscine',     label: 'Piscine',                type: 'checkbox' },
    { name: 'climatise',   label: 'Climatisé',              type: 'checkbox' },
    { name: 'parking',     label: 'Parking / garage',       type: 'checkbox' },
  ],
  'immo-terrains': [
    { name: 'surface_m2',  label: 'Surface (m²)',     type: 'number', placeholder: 'Ex: 1 000' },
    { name: 'viabilise',   label: 'Viabilisé',        type: 'checkbox' },
    { name: 'acces_route', label: 'Accès route',      type: 'checkbox' },
    { name: 'zone',        label: 'Zone',             type: 'select', options: ['Résidentielle','Agricole','Commerciale','Mixte'] },
  ],
  'immo-bureaux': [
    { name: 'surface_m2',  label: 'Surface (m²)',        type: 'number', placeholder: 'Ex: 80' },
    { name: 'nb_bureaux',  label: 'Nombre de bureaux',   type: 'number', placeholder: 'Ex: 4' },
    { name: 'parking',     label: 'Parking inclus',      type: 'checkbox' },
    { name: 'ascenseur',   label: 'Ascenseur',           type: 'checkbox' },
    { name: 'caution_xpf', label: 'Caution (XPF)',       type: 'number', placeholder: 'Ex: 240 000' },
  ],
  'immo-saisonnieres': [
    { name: 'surface_m2',    label: 'Surface (m²)',          type: 'number', placeholder: 'Ex: 50' },
    { name: 'nb_couchages',  label: 'Nombre de couchages',   type: 'number', placeholder: 'Ex: 4' },
    { name: 'tarif_semaine', label: 'Tarif / semaine (XPF)', type: 'number', placeholder: 'Ex: 50 000' },
    { name: 'piscine',       label: 'Piscine',               type: 'checkbox' },
    { name: 'climatise',     label: 'Climatisé',             type: 'checkbox' },
  ],
  'immo-parkings': [
    { name: 'type_parking', label: 'Type',      type: 'select', options: ['Extérieur','Intérieur / box','Sous-sol'] },
    { name: 'securise',     label: 'Sécurisé',  type: 'checkbox' },
    { name: 'acces_24h',    label: 'Accès 24h/24', type: 'checkbox' },
  ],

  // EMPLOI (commun à toutes les sous-catégories — voir patch ci-dessous)
  // ÉLECTRONIQUE
  'elec-telephones': [
    { name: 'marque',    label: 'Marque',       type: 'text',   placeholder: 'Ex: Samsung, Apple…' },
    { name: 'modele',    label: 'Modèle',       type: 'text',   placeholder: 'Ex: iPhone 15' },
    { name: 'stockage',  label: 'Stockage (Go)', type: 'select', options: ['32','64','128','256','512','1 024'] },
    { name: 'etat',      label: 'État',         type: 'select', options: ['Neuf (sous blister)','Neuf déballé','Très bon','Bon','Passable'] },
    { name: 'facture',   label: 'Facture incluse', type: 'checkbox' },
  ],
  'elec-ordinateurs': [
    { name: 'ram_gb',      label: 'RAM (Go)',      type: 'select', options: ['4','8','16','32','64'] },
    { name: 'stockage_gb', label: 'Stockage (Go)', type: 'select', options: ['128','256','512','1 000','2 000'] },
    { name: 'processeur',  label: 'Processeur',    type: 'text',   placeholder: 'Ex: Intel i5 12e gen' },
    { name: 'os',          label: 'Système',       type: 'select', options: ['Windows 11','Windows 10','macOS','Linux'] },
    { name: 'etat',        label: 'État',          type: 'select', options: ['Neuf','Très bon','Bon','Passable'] },
  ],
  'elec-pc': [
    { name: 'ram_gb',      label: 'RAM (Go)',      type: 'select', options: ['8','16','32','64'] },
    { name: 'stockage_gb', label: 'Stockage (Go)', type: 'select', options: ['256','512','1 000','2 000','4 000'] },
    { name: 'processeur',  label: 'Processeur',    type: 'text',   placeholder: 'Ex: Ryzen 5 5600X' },
    { name: 'gpu',         label: 'Carte graphique', type: 'text', placeholder: 'Ex: RTX 4060, RX 7600' },
    { name: 'os',          label: 'Système',       type: 'select', options: ['Windows 11','Windows 10','Linux','Sans OS'] },
    { name: 'etat',        label: 'État',          type: 'select', options: ['Neuf','Très bon','Bon','Passable'] },
  ],
  'elec-tv': [
    { name: 'marque',        label: 'Marque',         type: 'text',   placeholder: 'Ex: Samsung, LG, Sony…' },
    { name: 'taille_pouces', label: 'Taille (pouces)', type: 'number', placeholder: 'Ex: 55' },
    { name: 'smart_tv',      label: 'Smart TV',       type: 'checkbox' },
    { name: 'resolution',    label: 'Résolution',     type: 'select', options: ['HD','Full HD','4K','8K'] },
    { name: 'etat',          label: 'État',           type: 'select', options: ['Neuf','Très bon','Bon','Passable'] },
  ],
  'elec-jeux': [
    { name: 'console',      label: 'Console',         type: 'select', options: ['PS5','PS4','Xbox Series','Xbox One','Nintendo Switch','PC','Autre'] },
    { name: 'jeux_inclus',  label: 'Jeux inclus',     type: 'text',   placeholder: 'Ex: FIFA 24, GTA V…' },
    { name: 'etat',         label: 'État',            type: 'select', options: ['Neuf','Très bon','Bon','Passable'] },
  ],
  'elec-electromenager': [
    { name: 'marque',  label: 'Marque',     type: 'text',   placeholder: 'Ex: Samsung, LG, Bosch…' },
    { name: 'type_app',label: 'Type',       type: 'select', options: ['Réfrigérateur','Lave-linge','Lave-vaisselle','Micro-ondes','Climatiseur','Autre'] },
    { name: 'etat',    label: 'État',       type: 'select', options: ['Neuf','Très bon','Bon','Passable'] },
    { name: 'notice',  label: 'Notice incluse', type: 'checkbox' },
  ],

  // SERVICES
  'services-travaux': [
    { name: 'type_travaux',  label: 'Type de travaux',  type: 'select', options: ['Maçonnerie','Peinture','Électricité','Plomberie','Carrelage','Toiture','Autre'] },
    { name: 'devis_gratuit', label: 'Devis gratuit',     type: 'checkbox' },
    { name: 'materiel',      label: 'Matériel fourni',   type: 'checkbox' },
    { name: 'deplacement',   label: 'Zone de déplacement', type: 'text', placeholder: 'Ex: Papeete + 20 km' },
  ],
  'services-cours': [
    { name: 'matiere',     label: 'Matière / discipline', type: 'text',   placeholder: 'Ex: Maths, Anglais, Guitare…' },
    { name: 'niveau',      label: 'Niveau',               type: 'select', options: ['Primaire','Collège','Lycée','Supérieur','Adultes','Tous niveaux'] },
    { name: 'format',      label: 'Format',               type: 'select', options: ['À domicile','En ligne','Sur place','Les deux'] },
    { name: 'tarif_h',     label: 'Tarif / heure (XPF)',  type: 'number', placeholder: 'Ex: 3 000' },
  ],
  'services-transport': [
    { name: 'type_trajet',  label: 'Type de trajet',     type: 'select', options: ['Aéroport','Interurbain','Colis','Déménagement','Autre'] },
    { name: 'capacite_kg',  label: 'Capacité (kg/m³)',   type: 'text',   placeholder: 'Ex: 500 kg' },
    { name: 'tarif_km',     label: 'Tarif / km (XPF)',   type: 'number', placeholder: 'Ex: 150' },
  ],
  'services-sante': [
    { name: 'service',    label: 'Type de service',     type: 'text',   placeholder: 'Ex: Massage, Coiffure, Soin…' },
    { name: 'diplome',    label: 'Diplômé(e)',           type: 'checkbox' },
    { name: 'domicile',   label: 'À domicile',           type: 'checkbox' },
  ],
  'services-jardinage': [
    { name: 'frequence',   label: 'Fréquence',           type: 'select', options: ['Une fois','Hebdomadaire','Mensuel','À la demande'] },
    { name: 'materiel',    label: 'Matériel fourni',     type: 'checkbox' },
    { name: 'surface_m2',  label: 'Surface max (m²)',    type: 'number', placeholder: 'Ex: 300' },
  ],

  // AUTRES
  'autres-meubles': [
    { name: 'materiau',    label: 'Matériau',      type: 'select', options: ['Bois','Métal','Tissu','Plastique','Verre','Autre'] },
    { name: 'dimensions',  label: 'Dimensions',    type: 'text',   placeholder: 'Ex: 180×90×80 cm' },
    { name: 'livraison',   label: 'Livraison possible', type: 'checkbox' },
    { name: 'etat',        label: 'État',          type: 'select', options: ['Neuf','Très bon','Bon','Passable'] },
  ],
  'autres-vetements': [
    { name: 'taille',  label: 'Taille',   type: 'select', options: ['XS','S','M','L','XL','XXL','Autre'] },
    { name: 'marque',  label: 'Marque',   type: 'text',   placeholder: 'Ex: Zara, Nike…' },
    { name: 'etat',    label: 'État',     type: 'select', options: ['Neuf avec étiquette','Neuf sans étiquette','Très bon','Bon','Acceptable'] },
  ],
  'autres-sport': [
    { name: 'type_sport',  label: 'Sport / activité',  type: 'text',   placeholder: 'Ex: Surf, Tennis, Running…' },
    { name: 'niveau',      label: 'Niveau visé',        type: 'select', options: ['Débutant','Intermédiaire','Avancé','Tous niveaux'] },
    { name: 'etat',        label: 'État',               type: 'select', options: ['Neuf','Très bon','Bon','Passable'] },
  ],
  'autres-puericulture': [
    { name: 'age_enfant', label: 'Âge enfant',   type: 'select', options: ['0-3 mois','3-6 mois','6-12 mois','1-2 ans','2-4 ans','4-6 ans','6+ ans'] },
    { name: 'marque',     label: 'Marque',        type: 'text',   placeholder: 'Ex: Chicco, Babymoov…' },
    { name: 'etat',       label: 'État',          type: 'select', options: ['Neuf','Très bon','Bon','Passable'] },
  ],
};

// ─── Emploi : champs communs à toutes les sous-catégories ────────────────────
function _emploiFields(extra) {
  const base = [
    { name: 'type_contrat',   label: 'Type de contrat',       type: 'select', options: ['CDI','CDD','Intérim','Stage','Alternance','Freelance'] },
    { name: 'salaire_xpf',    label: 'Salaire brut (XPF/mois)', type: 'number', placeholder: 'Ex: 200 000' },
    { name: 'heures_semaine', label: 'Heures / semaine',       type: 'number', placeholder: 'Ex: 39' },
    { name: 'experience_ans', label: 'Expérience requise (ans)', type: 'number', placeholder: 'Ex: 2' },
    { name: 'permis_b',       label: 'Permis B requis',        type: 'checkbox' },
  ];
  return extra ? base.concat(extra) : base;
}
SPECS_DEF['emploi-commerciaux']  = _emploiFields([{ name: 'deplacements', label: 'Déplacements fréquents', type: 'checkbox' }]);
SPECS_DEF['emploi-informatique'] = _emploiFields([{ name: 'langages', label: 'Langages / stack', type: 'text', placeholder: 'Ex: Python, React, Django' }]);
SPECS_DEF['emploi-hotellerie']   = _emploiFields([{ name: 'langues', label: 'Langues requises', type: 'text', placeholder: 'Ex: Français, Anglais' }]);
SPECS_DEF['emploi-btp']          = _emploiFields([{ name: 'type_chantier', label: 'Type chantier', type: 'text', placeholder: 'Ex: Résidentiel, Génie civil' }]);
SPECS_DEF['emploi-services']     = _emploiFields([{ name: 'diplome_requis', label: 'Diplôme requis', type: 'text', placeholder: 'Ex: BTS, CAP…' }]);

// ─── Rendu des champs adaptatifs ──────────────────────────────────────────────
function renderSpecs(souscat) {
  const container = document.getElementById('specs-container');
  if (!container) return;

  // Adapter le label Prix
  const cat = document.getElementById('id_categorie') ? document.getElementById('id_categorie').value : '';
  adaptPrix(cat, souscat);

  const fields = SPECS_DEF[souscat];
  if (!fields || fields.length === 0) { container.innerHTML = ''; return; }

  let html = '<div class="border-t border-gray-200 pt-5 mt-1">';
  html += '<p class="text-xs font-bold text-gray-500 uppercase tracking-wide mb-3">Caractéristiques optionnelles</p>';
  html += '<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">';

  fields.forEach(f => {
    if (f.type === 'checkbox') {
      // Checkbox : rendu inline sur une colonne entière
      html += '<div class="flex items-center gap-2 pt-4 sm:pt-6">';
      html += `<input type="checkbox" name="spec_${f.name}" value="Oui" id="spec_${f.name}" class="w-4 h-4 accent-gray-900">`;
      html += `<label for="spec_${f.name}" class="text-sm font-medium text-gray-700">${f.label}</label>`;
      html += '</div>';
    } else {
      html += '<div>';
      html += `<label class="block text-xs font-bold text-gray-600 uppercase tracking-wide mb-1.5">${f.label}</label>`;
      if (f.type === 'select') {
        html += `<select name="spec_${f.name}" class="form-input"><option value="">— Choisir</option>`;
        f.options.forEach(o => { html += `<option value="${o}">${o}</option>`; });
        html += '</select>';
      } else {
        html += `<input type="${f.type}" name="spec_${f.name}" class="form-input" placeholder="${f.placeholder || ''}">`;
      }
      html += '</div>';
    }
  });

  html += '</div></div>';
  container.innerHTML = html;
}

// Écouter sous-catégorie
const sousCatSel = document.getElementById('id_sous_categorie');
if (sousCatSel) {
  sousCatSel.addEventListener('change', () => renderSpecs(sousCatSel.value));
}"""

html = html.replace(OLD2, NEW2, 1)

with open('templates/ads/deposer.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('deposer.html: JS adaptatif complet 16 catégories OK')
