/* ============================================
   TAHITI BUSINESS GROUPE — Main JS V2
   API Integration + Auth + Mock Fallback
   ============================================ */

const API_BASE = 'http://localhost:8000';

// ============================================================
//  AUTH STATE
// ============================================================

let currentUser = JSON.parse(localStorage.getItem('tbg_user') || 'null');
let authToken   = localStorage.getItem('tbg_token') || null;

function setAuth(token, user) {
  authToken   = token;
  currentUser = user;
  localStorage.setItem('tbg_token', token);
  localStorage.setItem('tbg_user', JSON.stringify(user));
  updateHeaderAuth();
}

function clearAuth() {
  authToken   = null;
  currentUser = null;
  localStorage.removeItem('tbg_token');
  localStorage.removeItem('tbg_user');
  updateHeaderAuth();
}

function updateHeaderAuth() {
  const loginBtn    = document.getElementById('btnLogin');
  const registerBtn = document.getElementById('btnRegister');
  const userMenu    = document.getElementById('userMenu');
  const userLabel   = document.getElementById('userLabel');

  if (currentUser) {
    if (loginBtn)    loginBtn.classList.add('hidden');
    if (registerBtn) registerBtn.classList.add('hidden');
    if (userMenu)    userMenu.classList.remove('hidden');
    if (userLabel)   userLabel.textContent = currentUser.nom;
  } else {
    if (loginBtn)    loginBtn.classList.remove('hidden');
    if (registerBtn) registerBtn.classList.remove('hidden');
    if (userMenu)    userMenu.classList.add('hidden');
  }
}

// ============================================================
//  API HELPERS
// ============================================================

async function apiFetch(endpoint, options = {}) {
  const url = API_BASE + endpoint;
  const headers = { ...(options.headers || {}) };

  if (authToken) headers['Authorization'] = `Bearer ${authToken}`;
  if (!(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json';
  }

  const res = await fetch(url, { ...options, headers });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Erreur réseau' }));
    throw new Error(err.detail || `Erreur ${res.status}`);
  }
  return res.json();
}

async function apiGet(endpoint, params = {}) {
  const url = new URL(API_BASE + endpoint);
  Object.entries(params).forEach(([k, v]) => {
    if (v !== null && v !== undefined && v !== '') url.searchParams.append(k, v);
  });
  const headers = {};
  if (authToken) headers['Authorization'] = `Bearer ${authToken}`;
  const res = await fetch(url.toString(), { headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Erreur réseau' }));
    throw new Error(err.detail || `Erreur ${res.status}`);
  }
  return res.json();
}

// ============================================================
//  MOCK DATA (fallback si API indisponible)
// ============================================================

const EMOJIS = {
  promo:    ['📱','❄️','🛵'],
  immo:     ['🏠','🏢','🏡','🏘️','🌴','🏗️','🛏️','🏠'],
  vehicule: ['🚗','🏍️','🚙','🛵','🚐','🚜','🚤','🏎️'],
  nouveau:  ['💻','🏄','🎮','🚲','🚁','📷','📱','🎸'],
  emploi:   ['💼','👩‍💻','🏗️','🍳','📊','🎨','🔧','📦'],
  vente:    ['🛋️','📺','🖥️','🎧','🏋️','🧊','💡','🔌']
};

const COLORS = [
  ['#1e3a5f','#2a5f8f'], ['#1a4d3a','#2d7a5c'], ['#4a1a5e','#7a2d8f'],
  ['#5e3a1a','#8f6a2d'], ['#1a3a5e','#2d6a8f'], ['#3a1a5e','#5a2d8f'],
  ['#1a5e3a','#2d8f5a'], ['#5e1a3a','#8f2d5a']
];

const LOCATIONS = ['Papeete','Punaauia','Faaa','Pirae','Moorea','Taravao','Mahina','Arue'];
const DATES_AGO = ['il y a 2h','il y a 5h','Aujourd\'hui','Hier','il y a 2j','il y a 3j','il y a 5j','il y a 1 sem'];

const MOCK_DATA = {
  promo: [
    { id:'m1', titre:'iPhone 15 Pro Max 256Go — PROMO LIMITÉE', prix:165000, prix_label:'165 000 XPF', localisation:'Papeete', categorie:'promo', specs:{Modèle:'iPhone 15 Pro Max',Stockage:'256 Go',État:'Très bon'}, discount:'-15%', oldPrice:195000, emoji:'📱' },
    { id:'m2', titre:'Climatiseur Samsung Inverter — DÉSTOCKAGE', prix:45000, prix_label:'45 000 XPF', localisation:'Punaauia', categorie:'promo', specs:{Puissance:'12 000 BTU',Type:'Inverter',Marque:'Samsung'}, discount:'-27%', oldPrice:62000, emoji:'❄️' },
    { id:'m3', titre:'Scooter Yamaha NMAX 125cc — URGENT', prix:280000, prix_label:'280 000 XPF', localisation:'Faaa', categorie:'promo', specs:{Année:'2022',Km:'18 000 km',Cylindrée:'125 cc'}, discount:'-20%', oldPrice:350000, emoji:'🛵' },
  ],
  immobilier: [
    { id:'m4', titre:'Appartement F3 vue mer — Papeete centre', prix_label:'180 000 XPF/mois', localisation:'Papeete', categorie:'immobilier', specs:{Type:'Appartement F3',Surface:'75 m²',Étage:'3ème',Parking:'Oui'} },
    { id:'m5', titre:'Maison 4 chambres avec piscine', prix_label:'420 000 XPF/mois', localisation:'Punaauia', categorie:'immobilier', specs:{Type:'Maison',Surface:'150 m²',Chambres:'4',Piscine:'Oui'} },
    { id:'m6', titre:'Studio meublé proche centre', prix_label:'85 000 XPF/mois', localisation:'Pirae', categorie:'immobilier', specs:{Type:'Studio',Surface:'28 m²',Meublé:'Oui'} },
    { id:'m7', titre:'Terrain 1200m² viabilisé', prix_label:'12 500 000 XPF', localisation:'Taravao', categorie:'immobilier', specs:{Type:'Terrain',Surface:'1 200 m²',Viabilisé:'Oui',Vue:'Montagne'} },
    { id:'m8', titre:'Villa luxe bord de lagon', prix_label:'850 000 XPF/mois', localisation:'Moorea', categorie:'immobilier', specs:{Type:'Villa',Surface:'220 m²',Chambres:'5',Vue:'Lagon'} },
    { id:'m9', titre:'Local commercial 60m²', prix_label:'150 000 XPF/mois', localisation:'Papeete', categorie:'immobilier', specs:{Type:'Commercial',Surface:'60 m²',Vitrine:'Oui'} },
    { id:'m10', titre:'Colocation F4 — 1 chambre dispo', prix_label:'55 000 XPF/mois', localisation:'Faaa', categorie:'immobilier', specs:{Type:'Colocation',Surface:'15 m²',Meublé:'Oui'} },
    { id:'m11', titre:'Duplex neuf standing Paofai', prix_label:'350 000 XPF/mois', localisation:'Papeete', categorie:'immobilier', specs:{Type:'Duplex F4',Surface:'120 m²',Neuf:'Oui'} },
  ],
  vehicules: [
    { id:'m12', titre:'Toyota Hilux 2022 — Excellent état', prix_label:'3 200 000 XPF', localisation:'Papeete', categorie:'vehicules', specs:{Année:'2022',Km:'45 000 km',Énergie:'Diesel','Boîte':'Automatique'} },
    { id:'m13', titre:'Peugeot 208 2021 — Peu de km', prix_label:'1 800 000 XPF', localisation:'Punaauia', categorie:'vehicules', specs:{Année:'2021',Km:'28 000 km',Énergie:'Essence'} },
    { id:'m14', titre:'Yamaha MT-07 2023', prix_label:'1 450 000 XPF', localisation:'Pirae', categorie:'vehicules', specs:{Année:'2023',Km:'8 000 km',Cylindrée:'689 cc',Type:'Roadster'} },
    { id:'m15', titre:'Nissan Navara Double Cab 4x4', prix_label:'2 900 000 XPF', localisation:'Taravao', categorie:'vehicules', specs:{Année:'2020',Km:'62 000 km',Énergie:'Diesel'} },
    { id:'m16', titre:'Suzuki Jimny 2023 — Comme neuf', prix_label:'3 500 000 XPF', localisation:'Moorea', categorie:'vehicules', specs:{Année:'2023',Km:'12 000 km',Énergie:'Essence'} },
    { id:'m17', titre:'Honda PCX 125', prix_label:'320 000 XPF', localisation:'Faaa', categorie:'vehicules', specs:{Année:'2022',Km:'15 000 km',Cylindrée:'125 cc',Type:'Scooter'} },
    { id:'m18', titre:'Bateau alu 5m moteur Yamaha 60cv', prix_label:'1 200 000 XPF', localisation:'Papeete', categorie:'vehicules', specs:{Longueur:'5m',Moteur:'Yamaha 60cv',Année:'2021'} },
    { id:'m19', titre:'Renault Duster 4x4 2022', prix_label:'2 100 000 XPF', localisation:'Mahina', categorie:'vehicules', specs:{Année:'2022',Km:'35 000 km',Énergie:'Diesel'} },
  ],
  nouveautes: [
    { id:'m20', titre:'MacBook Air M3 15" — Neuf sous blister', prix_label:'285 000 XPF', localisation:'Papeete', categorie:'nouveautes', specs:{Modèle:'MacBook Air M3',Écran:'15.3"',RAM:'16 Go',SSD:'512 Go'} },
    { id:'m21', titre:"Planche de surf 6'2 Al Merrick", prix_label:'65 000 XPF', localisation:'Punaauia', categorie:'nouveautes', specs:{Taille:'6\'2"',Volume:'32L',État:'Très bon'} },
    { id:'m22', titre:'PS5 Slim + 2 manettes + 3 jeux', prix_label:'75 000 XPF', localisation:'Pirae', categorie:'nouveautes', specs:{Modèle:'PS5 Slim Digital',Manettes:'2',Jeux:'3 inclus'} },
    { id:'m23', titre:'Vélo électrique Decathlon 2024', prix_label:'120 000 XPF', localisation:'Faaa', categorie:'nouveautes', specs:{Autonomie:'80 km',Vitesse:'25 km/h',Taille:'M/L'} },
    { id:'m24', titre:'Drone DJI Mini 4 Pro + accessoires', prix_label:'145 000 XPF', localisation:'Moorea', categorie:'nouveautes', specs:{Modèle:'DJI Mini 4 Pro',Poids:'249g',Vidéo:'4K HDR'} },
    { id:'m25', titre:'Appareil photo Canon R50 + objectif', prix_label:'180 000 XPF', localisation:'Papeete', categorie:'nouveautes', specs:{Modèle:'Canon EOS R50',Capteur:'24.2 MP',Vidéo:'4K'} },
    { id:'m26', titre:'Samsung Galaxy S24 Ultra 256Go', prix_label:'195 000 XPF', localisation:'Arue', categorie:'nouveautes', specs:{Modèle:'S24 Ultra',Stockage:'256 Go',RAM:'12 Go',État:'Neuf'} },
    { id:'m27', titre:'Ukulele Kamaka HF-2 Concert', prix_label:'95 000 XPF', localisation:'Papeete', categorie:'nouveautes', specs:{Modèle:'HF-2 Concert',Bois:'Koa hawaïen',État:'Excellent'} },
  ],
  emploi: [
    { id:'m28', titre:'Développeur Web Full-Stack — CDI', prix_label:'450 000 XPF/mois', localisation:'Papeete', categorie:'emploi', specs:{Contrat:'CDI',Niveau:'3-5 ans exp.',Secteur:'Tech',Début:'Immédiat'} },
    { id:'m29', titre:'Serveur/Serveuse restaurant — Temps plein', prix_label:'200 000 XPF/mois', localisation:'Punaauia', categorie:'emploi', specs:{Contrat:'CDI',Niveau:'Débutant accepté',Horaires:'Soir + WE'} },
    { id:'m30', titre:'Comptable expérimenté(e)', prix_label:'380 000 XPF/mois', localisation:'Papeete', categorie:'emploi', specs:{Contrat:'CDI',Niveau:'5 ans min.',Logiciel:'Sage'} },
    { id:'m31', titre:'Agent immobilier indépendant', prix_label:'Commission 3-5%', localisation:'Tahiti', categorie:'emploi', specs:{Contrat:'Indépendant',Secteur:'Immobilier',Permis:'Obligatoire'} },
    { id:'m32', titre:'Graphiste / Webdesigner freelance', prix_label:'Sur devis', localisation:'Remote', categorie:'emploi', specs:{Contrat:'Freelance',Logiciels:'Figma, Adobe',Secteur:'Créatif'} },
    { id:'m33', titre:'Mécanicien auto — Garage Faaa', prix_label:'250 000 XPF/mois', localisation:'Faaa', categorie:'emploi', specs:{Contrat:'CDI',Niveau:'CAP/BEP',Permis:'B obligatoire'} },
    { id:'m34', titre:'Réceptionniste hôtel 4 étoiles', prix_label:'220 000 XPF/mois', localisation:'Moorea', categorie:'emploi', specs:{Contrat:'CDD 6 mois',Langues:'FR + EN',Horaires:'Décalés'} },
    { id:'m35', titre:'Livreur colis — Temps partiel', prix_label:'120 000 XPF/mois', localisation:'Papeete', categorie:'emploi', specs:{Contrat:'Temps partiel',Permis:'B obligatoire',Véhicule:'Fourni'} },
  ],
  'vente-privee': [
    { id:'m36', titre:"Canapé d'angle cuir véritable", prix_label:'180 000 XPF', localisation:'Punaauia', categorie:'vente-privee', specs:{Matière:'Cuir véritable',Couleur:'Noir',Places:'5-6',État:'Excellent'} },
    { id:'m37', titre:'TV Samsung 65" QLED 4K 2024', prix_label:'120 000 XPF', localisation:'Papeete', categorie:'vente-privee', specs:{Taille:'65 pouces',Techno:'QLED 4K',Smart:'Tizen OS'} },
    { id:'m38', titre:'Machine à laver LG 9kg A+++', prix_label:'55 000 XPF', localisation:'Faaa', categorie:'vente-privee', specs:{Capacité:'9 kg',Classe:'A+++',Marque:'LG'} },
    { id:'m39', titre:'Bureau gaming + chaise ergonomique', prix_label:'85 000 XPF', localisation:'Pirae', categorie:'vente-privee', specs:{Bureau:'140x60cm',Chaise:'Ergonomique',LED:'RGB inclus'} },
    { id:'m40', titre:'Réfrigérateur double porte Inox', prix_label:'95 000 XPF', localisation:'Papeete', categorie:'vente-privee', specs:{Volume:'450L',Classe:'A++',Marque:'Samsung'} },
    { id:'m41', titre:'Matelas King Size mémoire de forme', prix_label:'65 000 XPF', localisation:'Arue', categorie:'vente-privee', specs:{Taille:'180x200',Type:'Mémoire de forme',Épaisseur:'25 cm',État:'Neuf'} },
    { id:'m42', titre:'Enceinte JBL PartyBox 310', prix_label:'48 000 XPF', localisation:'Papeete', categorie:'vente-privee', specs:{Puissance:'240W',Batterie:'18h',Bluetooth:'5.1'} },
    { id:'m43', titre:'Trottinette électrique Xiaomi Pro 2', prix_label:'42 000 XPF', localisation:'Mahina', categorie:'vente-privee', specs:{Autonomie:'45 km',Vitesse:'25 km/h',Poids:'14.2 kg',Pliable:'Oui'} },
  ]
};

// Indicateur de source de données
let isLiveData = false;

function showDataBadge(live) {
  const badge = document.getElementById('dataBadge');
  if (!badge) return;
  isLiveData = live;
  badge.textContent  = live ? '🟢 Live API' : '🟡 Données démo';
  badge.className    = `data-badge ${live ? 'live' : 'demo'}`;
}

// ============================================================
//  PLACEHOLDER IMAGES
// ============================================================

function placeholderImg(emoji, colorIdx) {
  const c = COLORS[colorIdx % COLORS.length];
  return `<div class="placeholder-img" style="background:linear-gradient(135deg,${c[0]},${c[1]})">${emoji}</div>`;
}

function getEmojiForCat(cat, idx) {
  const map = { promo: EMOJIS.promo, immobilier: EMOJIS.immo, vehicules: EMOJIS.vehicule, nouveautes: EMOJIS.nouveau, emploi: EMOJIS.emploi, 'vente-privee': EMOJIS.vente };
  const set = map[cat] || EMOJIS.nouveau;
  return set[idx % set.length];
}

function renderPhotoOrPlaceholder(item, idx) {
  if (item.photos && item.photos.length > 0) {
    return `<img src="${API_BASE}${item.photos[0]}" alt="${item.titre}" onerror="this.parentElement.innerHTML='${placeholderImg(getEmojiForCat(item.categorie, idx), idx)}'">`;
  }
  const emoji = item.emoji || getEmojiForCat(item.categorie, idx);
  return placeholderImg(emoji, idx);
}

// ============================================================
//  PRICE HELPERS
// ============================================================

function formatPrice(n) {
  if (typeof n !== 'number') return n;
  return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + ' XPF';
}

function displayPrice(item) {
  if (item.prix_label) return item.prix_label;
  if (item.prix)       return formatPrice(item.prix);
  if (item.price)      return (typeof item.price === 'number' ? formatPrice(item.price) : item.price);
  return 'Prix sur demande';
}

function displayDate(item) {
  if (item.created_at) {
    const d = new Date(item.created_at);
    const diff = Math.floor((Date.now() - d) / 1000 / 60);
    if (diff < 60)       return `il y a ${diff} min`;
    if (diff < 1440)     return `il y a ${Math.floor(diff/60)}h`;
    if (diff < 10080)    return `il y a ${Math.floor(diff/1440)} j`;
    return d.toLocaleDateString('fr-FR');
  }
  return DATES_AGO[Math.floor(Math.random() * DATES_AGO.length)];
}

// ============================================================
//  RENDER — PROMOS
// ============================================================

function renderPromoItems(items) {
  const grid = document.getElementById('grid-promo');
  grid.innerHTML = items.map((item, i) => {
    const oldPrice = item.oldPrice ? formatPrice(item.oldPrice) : '';
    const discount = item.discount || '';
    const newPrice = displayPrice(item);
    return `
      <div class="promo-card" style="animation-delay:${i*0.1}s" onclick="openProduct('${item.id || i}')">
        <div class="promo-card-img">
          ${renderPhotoOrPlaceholder(item, i)}
          <div class="promo-card-overlay"></div>
        </div>
        <button class="ad-card-fav" onclick="event.stopPropagation();toggleFavorite(this)">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
        </button>
        <div class="promo-card-body">
          ${discount ? `<span class="promo-card-discount">${discount}</span>` : ''}
          <div class="promo-card-title">${item.titre || item.title}</div>
          <div class="promo-card-price">
            ${oldPrice ? `<span class="old">${oldPrice}</span>` : ''}
            <span class="new">${newPrice}</span>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

// ============================================================
//  RENDER — STANDARD CARDS
// ============================================================

function renderAdItems(items, gridId, cat) {
  const grid = document.getElementById(gridId);
  if (!grid) return;
  grid.innerHTML = items.map((item, i) => {
    const isNew   = i === 0 || (item.boost);
    const badgeHTML = cat === 'emploi'
      ? `<span class="ad-card-badge bg-emerald-500 text-white">EMPLOI</span>`
      : (isNew ? `<span class="ad-card-badge bg-accent-500 text-dark-950">NEW</span>` : '');

    return `
      <div class="ad-card" style="animation-delay:${i*0.08}s" onclick="openProduct('${item.id || ('m' + i)}')">
        <div class="ad-card-img">
          ${renderPhotoOrPlaceholder(item, i)}
          ${badgeHTML}
          <button class="ad-card-fav" onclick="event.stopPropagation();toggleFavorite(this)">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
          </button>
        </div>
        <div class="ad-card-body">
          <div class="ad-card-title">${item.titre || item.title}</div>
          <div class="ad-card-price">${displayPrice(item)}</div>
          <div class="ad-card-meta">
            <span>${item.localisation || item.loc}</span>
            <span>•</span>
            <span>${displayDate(item)}</span>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

// ============================================================
//  LOAD SECTIONS FROM API (avec fallback mock)
// ============================================================

// Cache des annonces chargées (id → objet) pour le modal
const annonceCache = {};

async function loadSection(cat, gridId, isMockKey) {
  const grid = document.getElementById(gridId);
  if (!grid) return;

  grid.innerHTML = `<div class="col-span-full py-10 flex justify-center">
    <div class="w-8 h-8 border-2 border-accent-500 border-t-transparent rounded-full animate-spin"></div>
  </div>`;

  try {
    const params = { categorie: cat, limit: 8 };
    const items = await apiGet('/annonces', params);
    if (items.length === 0) throw new Error('empty');

    items.forEach(a => { annonceCache[a.id] = a; });
    showDataBadge(true);

    if (cat === 'promo') {
      renderPromoItems(items);
    } else {
      renderAdItems(items, gridId, cat);
    }
  } catch {
    // API indisponible → fallback données mock
    const mockItems = MOCK_DATA[isMockKey || cat] || [];
    mockItems.forEach(a => { annonceCache[a.id] = a; });
    showDataBadge(false);

    if (cat === 'promo') {
      renderPromoItems(mockItems);
    } else {
      renderAdItems(mockItems, gridId, cat);
    }
  }
}

// ============================================================
//  PRODUCT MODAL
// ============================================================

let currentProductId = null;

async function openProduct(id) {
  currentProductId = id;
  const modal = document.getElementById('productModal');

  // Chercher dans le cache en premier
  let item = annonceCache[id] || annonceCache[String(id)];

  // Si pas en cache et ID numérique → appeler l'API
  if (!item && !String(id).startsWith('m')) {
    try {
      item = await apiGet(`/annonces/${id}`);
      annonceCache[id] = item;
    } catch {
      item = null;
    }
  }

  if (!item) return;

  const cat    = item.categorie;
  const idx    = 0;
  const emojis = { promo: EMOJIS.promo, immobilier: EMOJIS.immo, vehicules: EMOJIS.vehicule, nouveautes: EMOJIS.nouveau, emploi: EMOJIS.emploi, 'vente-privee': EMOJIS.vente };
  const emojiSet = emojis[cat] || EMOJIS.nouveau;
  const mainEmoji = item.emoji || emojiSet[0];

  // Image principale
  const mainImgEl = document.getElementById('modalMainImage');
  if (item.photos && item.photos.length > 0) {
    mainImgEl.innerHTML = `<img src="${API_BASE}${item.photos[0]}" alt="${item.titre}" class="w-full h-full object-cover" onerror="this.parentElement.innerHTML='${placeholderImg(mainEmoji, 0)}'">`;
  } else {
    mainImgEl.innerHTML = placeholderImg(mainEmoji, 0);
  }

  // Thumbnails
  const thumbsEl = document.getElementById('modalThumbnails');
  const photos = (item.photos && item.photos.length > 0) ? item.photos : null;
  if (photos) {
    thumbsEl.innerHTML = photos.slice(0, 4).map((p, i) => `
      <div class="thumb-item ${i===0?'active':''}" onclick="switchThumb(this,'${API_BASE}${p}')">
        <img src="${API_BASE}${p}" alt="photo ${i+1}" onerror="this.parentElement.innerHTML='${placeholderImg(emojiSet[i % emojiSet.length], i)}'">
      </div>
    `).join('');
  } else {
    thumbsEl.innerHTML = [0,1,2,3].map((n, i) => `
      <div class="thumb-item ${i===0?'active':''}" onclick="this.parentElement.querySelectorAll('.thumb-item').forEach(t=>t.classList.remove('active'));this.classList.add('active')">
        ${placeholderImg(emojiSet[(idx+n) % emojiSet.length], idx+n)}
      </div>
    `).join('');
  }

  // Badge catégorie
  const badgeMap   = { promo:'bg-red-500 text-white', immobilier:'bg-primary-500 text-white', vehicules:'bg-orange-500 text-white', nouveautes:'bg-purple-500 text-white', emploi:'bg-emerald-500 text-white', 'vente-privee':'bg-pink-500 text-white' };
  const badgeLabel = { promo:'PROMO', immobilier:'IMMOBILIER', vehicules:'VÉHICULE', nouveautes:'NOUVEAU', emploi:'EMPLOI', 'vente-privee':'VENTE PRIVÉE' };
  document.getElementById('modalBadge').innerHTML = `<span class="inline-block px-3 py-1 rounded-lg text-xs font-bold ${badgeMap[cat]||'bg-white/10 text-white'}">${badgeLabel[cat]||cat.toUpperCase()}</span>`;

  // Texte
  document.getElementById('modalTitle').textContent       = item.titre || item.title;
  document.getElementById('modalPrice').textContent       = displayPrice(item);
  document.getElementById('modalLocation').innerHTML      = `<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg> ${item.localisation||item.loc}`;
  document.getElementById('modalDate').innerHTML          = `<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg> ${displayDate(item)}`;

  // Description
  const descriptions = {
    promo: 'Offre exceptionnelle à saisir rapidement ! Produit en excellent état, vendu en dessous du prix du marché.',
    immobilier: 'Bien immobilier disponible immédiatement. Situé dans un quartier calme, proche de toutes commodités.',
    vehicules: 'Véhicule bien entretenu, carnet d\'entretien complet. Contrôle technique à jour.',
    nouveautes: 'Article récent en parfait état. Vendu avec tous les accessoires d\'origine.',
    emploi: 'Nous recherchons un(e) candidat(e) motivé(e) pour rejoindre notre équipe dynamique.',
    'vente-privee': 'Article en très bon état, quasi neuf. Vendu car déménagement / renouvellement.',
  };
  document.getElementById('modalDescription').textContent = item.description || descriptions[cat] || '';

  // Specs
  const specs = item.specs || {};
  const specsEl = document.getElementById('modalSpecs');
  if (Object.keys(specs).length > 0) {
    specsEl.innerHTML = `<table class="specs-table">${Object.entries(specs).map(([k,v])=>`<tr><td>${k}</td><td>${v}</td></tr>`).join('')}</table>`;
  } else {
    specsEl.innerHTML = '';
  }

  // Vendeur (si API)
  const sellerEl = document.getElementById('modalSeller');
  if (sellerEl) {
    const owner = item.owner;
    if (owner) {
      sellerEl.innerHTML = `
        <div class="flex items-center gap-3 p-3 rounded-xl bg-white/5 border border-white/10">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-600 to-accent-600 flex items-center justify-center font-bold text-lg">${owner.nom.charAt(0).toUpperCase()}</div>
          <div>
            <p class="text-sm font-semibold">${owner.nom}</p>
            <p class="text-xs text-white/40">${owner.role === 'pro' ? '✓ Professionnel vérifié' : 'Particulier'}</p>
          </div>
          ${owner.whatsapp ? `<a href="https://wa.me/${owner.whatsapp}" target="_blank" class="ml-auto py-1.5 px-3 rounded-lg bg-green-500/20 text-green-400 text-xs font-bold hover:bg-green-500/30 transition-all">WhatsApp</a>` : ''}
        </div>`;
      sellerEl.classList.remove('hidden');
    } else {
      sellerEl.classList.add('hidden');
    }
  }

  modal.classList.add('active');
  document.body.style.overflow = 'hidden';
}

function switchThumb(el, src) {
  el.closest('#modalThumbnails').querySelectorAll('.thumb-item').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  const mainImg = document.querySelector('#modalMainImage img');
  if (mainImg) mainImg.src = src;
}

function closeProductModal() {
  document.getElementById('productModal').classList.remove('active');
  document.body.style.overflow = '';
  currentProductId = null;
}

// ============================================================
//  AUTH MODAL
// ============================================================

let authMode = 'login';

function openAuthModal(mode) {
  authMode = mode || 'login';
  updateAuthUI();
  document.getElementById('authModal').classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeAuthModal() {
  document.getElementById('authModal').classList.remove('active');
  document.body.style.overflow = '';
  clearAuthError();
}

function switchAuthMode() {
  authMode = authMode === 'login' ? 'register' : 'login';
  updateAuthUI();
  clearAuthError();
}

function updateAuthUI() {
  const isLogin = authMode === 'login';
  document.getElementById('authTitle').textContent      = isLogin ? 'Connexion' : 'Inscription';
  document.getElementById('authNameField').classList.toggle('hidden', isLogin);
  document.getElementById('authTelField').classList.toggle('hidden', isLogin);
  document.getElementById('authRoleField').classList.toggle('hidden', isLogin);
  document.getElementById('authSubmitBtn').textContent  = isLogin ? 'Se connecter' : 'Créer mon compte';
  document.getElementById('authSwitchBtn').textContent  = isLogin ? 'Créer un compte' : 'Se connecter';
  document.querySelector('#authSwitch').firstChild.textContent = isLogin ? 'Pas encore inscrit ? ' : 'Déjà un compte ? ';
}

function clearAuthError() {
  const err = document.getElementById('authError');
  if (err) err.textContent = '';
}

function showAuthError(msg) {
  const err = document.getElementById('authError');
  if (err) {
    err.textContent = msg;
    err.classList.remove('hidden');
  }
}

async function submitAuth(event) {
  event.preventDefault();
  clearAuthError();

  const btn = document.getElementById('authSubmitBtn');
  btn.disabled    = true;
  btn.textContent = 'Chargement…';

  const email    = document.getElementById('authEmail').value.trim();
  const password = document.getElementById('authPassword').value;

  try {
    let result;
    if (authMode === 'login') {
      result = await apiFetch('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      });
    } else {
      const nom      = document.getElementById('authNom').value.trim();
      const tel      = document.getElementById('authTel')?.value.trim() || '';
      const role     = document.getElementById('authRole')?.value || 'personnel';
      result = await apiFetch('/auth/register', {
        method: 'POST',
        body: JSON.stringify({ email, password, nom, tel, role }),
      });
    }

    setAuth(result.access_token, result.user);
    closeAuthModal();
    showToast(`Bienvenue ${result.user.nom} ! 🌺`);
  } catch (err) {
    showAuthError(err.message);
  } finally {
    btn.disabled    = false;
    btn.textContent = authMode === 'login' ? 'Se connecter' : 'Créer mon compte';
  }
}

function logout() {
  clearAuth();
  showToast('Déconnexion réussie.');
}

// ============================================================
//  POST AD MODAL
// ============================================================

function openPostAdModal() {
  if (!currentUser) {
    openAuthModal('register');
    return;
  }
  document.getElementById('postAdModal').classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closePostAdModal() {
  document.getElementById('postAdModal').classList.remove('active');
  document.body.style.overflow = '';
}

async function submitPostAd(event) {
  event.preventDefault();
  if (!currentUser) { openAuthModal('register'); return; }

  const btn = document.getElementById('postAdSubmitBtn');
  btn.disabled    = true;
  btn.textContent = 'Publication…';

  const form = event.target;
  const fd   = new FormData();
  fd.append('titre',       form.querySelector('[name="titre"]').value);
  fd.append('categorie',   form.querySelector('[name="categorie"]').value);
  fd.append('localisation',form.querySelector('[name="localisation"]').value);
  fd.append('prix_label',  form.querySelector('[name="prix_label"]').value);
  fd.append('description', form.querySelector('[name="description"]').value);

  const photoInput = form.querySelector('[name="photos"]');
  if (photoInput && photoInput.files.length > 0) {
    [...photoInput.files].slice(0, 5).forEach(f => fd.append('photos', f));
  }

  try {
    const ann = await apiFetch('/annonces', { method: 'POST', body: fd });
    annonceCache[ann.id] = ann;
    closePostAdModal();
    showToast('Annonce publiée avec succès ! ✅');
    // Reload la section concernée
    const sectionMap = {
      immobilier: 'grid-immobilier', vehicules: 'grid-vehicules', emploi: 'grid-emploi',
      'vente-privee': 'grid-vente-privee', nouveautes: 'grid-nouveautes', promo: 'grid-promo',
    };
    const gridId = sectionMap[ann.categorie];
    if (gridId) await loadSection(ann.categorie, gridId);
  } catch (err) {
    showToast(`Erreur : ${err.message}`, 'error');
  } finally {
    btn.disabled    = false;
    btn.textContent = 'Publier mon annonce';
  }
}

// ============================================================
//  CONTACT MODAL
// ============================================================

function openContactModal() {
  const modal = document.getElementById('contactModal');
  if (modal) {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}

function closeContactModal() {
  const modal = document.getElementById('contactModal');
  if (modal) {
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }
}

async function submitContact(event) {
  event.preventDefault();
  const btn  = event.target.querySelector('button[type="submit"]');
  btn.disabled    = true;
  btn.textContent = 'Envoi…';

  const content       = event.target.querySelector('[name="content"]').value.trim();
  const contact_email = event.target.querySelector('[name="contact_email"]')?.value || (currentUser?.email || '');
  const contact_tel   = event.target.querySelector('[name="contact_tel"]')?.value || '';

  if (!content) { btn.disabled = false; btn.textContent = 'Envoyer'; return; }

  if (!currentProductId || String(currentProductId).startsWith('m')) {
    // Mode mock (pas d'ID réel)
    closeContactModal();
    showToast('Message envoyé ! (démo) 📩');
    btn.disabled    = false;
    btn.textContent = 'Envoyer';
    return;
  }

  try {
    await apiFetch(`/annonces/${currentProductId}/contact`, {
      method: 'POST',
      body: JSON.stringify({ content, contact_email, contact_tel }),
    });
    closeContactModal();
    closeProductModal();
    showToast('Message envoyé au vendeur ! 📩');
  } catch (err) {
    showToast(`Erreur : ${err.message}`, 'error');
  } finally {
    btn.disabled    = false;
    btn.textContent = 'Envoyer';
  }
}

// ============================================================
//  TOAST NOTIFICATIONS
// ============================================================

function showToast(msg, type = 'success') {
  let toast = document.getElementById('tbgToast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'tbgToast';
    toast.style.cssText = 'position:fixed;bottom:1.5rem;right:1.5rem;z-index:9999;padding:.8rem 1.4rem;border-radius:.9rem;font-size:.9rem;font-weight:600;max-width:320px;transition:all .3s;transform:translateY(20px);opacity:0;pointer-events:none;';
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.style.background = type === 'error' ? 'rgba(239,68,68,0.95)' : 'rgba(0,230,135,0.95)';
  toast.style.color = type === 'error' ? 'white' : '#0b0e17';
  toast.style.transform  = 'translateY(0)';
  toast.style.opacity    = '1';
  setTimeout(() => {
    toast.style.transform = 'translateY(20px)';
    toast.style.opacity   = '0';
  }, 3000);
}

// ============================================================
//  FAVORITES
// ============================================================

function toggleFavorite(btn) {
  btn.classList.toggle('active');
  const svg = btn.querySelector('svg');
  if (btn.classList.contains('active')) {
    svg.setAttribute('fill', 'currentColor');
    showToast('Ajouté aux favoris ❤️');
  } else {
    svg.setAttribute('fill', 'none');
  }
}

// ============================================================
//  HEADER SCROLL
// ============================================================

window.addEventListener('scroll', () => {
  const header = document.getElementById('header');
  header.classList.toggle('scrolled', window.scrollY > 50);
});

// ============================================================
//  SEARCH (temps réel — filtre affichage + appel API)
// ============================================================

let searchTimeout = null;

document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase().trim();

      // Filtre immédiat sur les cartes affichées
      document.querySelectorAll('.ad-card, .promo-card').forEach(card => {
        const text = card.textContent.toLowerCase();
        card.style.display = !q || text.includes(q) ? '' : 'none';
      });

      // Appel API après 500ms (si backend disponible)
      clearTimeout(searchTimeout);
      if (q.length >= 3) {
        searchTimeout = setTimeout(async () => {
          try {
            const results = await apiGet('/annonces', { search: q, limit: 20 });
            results.forEach(a => { annonceCache[a.id] = a; });
          } catch { /* mode démo */ }
        }, 500);
      }
    });
  }
});

// ============================================================
//  CATEGORY FILTER
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
  const bar = document.getElementById('categoryBar');
  if (!bar) return;
  bar.addEventListener('click', (e) => {
    const btn = e.target.closest('.cat-btn');
    if (!btn) return;

    document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    const cat = btn.dataset.cat;
    const map = {
      all: 'sections',
      promo: 'sec-promo',
      immobilier: 'sec-immobilier',
      vehicules: 'sec-vehicules',
      nouveautes: 'sec-nouveautes',
      emploi: 'sec-emploi',
      'vente-privee': 'sec-vente-privee',
    };
    const el = document.getElementById(map[cat] || 'sections');
    if (el) window.scrollTo({ top: el.offsetTop - 120, behavior: 'smooth' });
  });
});

// ============================================================
//  SCROLL REVEAL
// ============================================================

function initReveal() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) entry.target.classList.add('visible');
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
}

// ============================================================
//  COUNTERS
// ============================================================

function animateCounters() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el     = entry.target;
        const target = parseInt(el.dataset.target);
        let current  = 0;
        const step   = target / 60;
        const timer  = setInterval(() => {
          current += step;
          if (current >= target) {
            el.textContent = target.toLocaleString('fr-FR');
            clearInterval(timer);
          } else {
            el.textContent = Math.floor(current).toLocaleString('fr-FR');
          }
        }, 16);
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('.counter').forEach(c => observer.observe(c));
}

// ============================================================
//  KEYBOARD
// ============================================================

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeProductModal();
    closeAuthModal();
    closePostAdModal();
    closeContactModal();
  }
});

// ============================================================
//  INIT
// ============================================================

document.addEventListener('DOMContentLoaded', async () => {
  updateHeaderAuth();
  initReveal();
  animateCounters();

  // Chargement parallèle de toutes les sections
  await Promise.all([
    loadSection('promo',        'grid-promo',        'promo'),
    loadSection('immobilier',   'grid-immobilier',   'immobilier'),
    loadSection('vehicules',    'grid-vehicules',    'vehicules'),
    loadSection('nouveautes',   'grid-nouveautes',   'nouveautes'),
    loadSection('emploi',       'grid-emploi',       'emploi'),
    loadSection('vente-privee', 'grid-vente-privee', 'vente-privee'),
  ]);

  initReveal(); // Re-déclencher après rendu
});
