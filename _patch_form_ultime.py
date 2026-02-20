# -*- coding: utf-8 -*-
"""
Patch formulaire ultime :
- Animation slide-in/out sur la section specs
- Exemples inline sur chaque label
- Bulle flottante "Annonce parfaite" contextuelle
"""
import re

path = 'templates/ads/deposer.html'
with open(path, encoding='utf-8') as f:
    src = f.read()

# ─── 1. BLOC CSS ──────────────────────────────────────────────────────────────
CSS_BLOCK = """\
{% block extra_css %}
<style>
/* ── Animation specs container ── */
#specs-container {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
#specs-container.specs-hidden {
  opacity: 0;
  transform: translateY(-6px);
  pointer-events: none;
}

/* ── Hint exemple inline ── */
.champ-exemple {
  font-size: 11px;
  color: #9ca3af;
  font-style: italic;
  margin-left: 4px;
}

/* ── Bulle annonce parfaite ── */
#bulle-parfaite {
  position: fixed;
  bottom: 80px;
  right: 16px;
  z-index: 999;
  background: #111827;
  color: #fff;
  padding: 12px 16px;
  border-radius: 16px;
  max-width: 280px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.35);
  font-size: 12px;
  line-height: 1.5;
  opacity: 0;
  transform: translateY(12px);
  transition: opacity 0.3s ease, transform 0.3s ease;
  pointer-events: none;
}
#bulle-parfaite.visible {
  opacity: 1;
  transform: translateY(0);
}
#bulle-parfaite .bulle-titre {
  font-weight: 700;
  font-size: 11px;
  letter-spacing: .05em;
  text-transform: uppercase;
  color: #60a5fa;
  margin-bottom: 4px;
}
#bulle-parfaite .bulle-close {
  position: absolute;
  top: 8px; right: 10px;
  cursor: pointer;
  font-size: 14px;
  color: #6b7280;
  pointer-events: all;
}
</style>
{% endblock %}

"""

# Insérer avant {% block extra_js %}
src = src.replace('{% block extra_js %}', CSS_BLOCK + '{% block extra_js %}', 1)

# ─── 2. BULLE FLOTTANTE HTML (avant {% endblock %} du content) ───────────────
BULLE_HTML = """
  <!-- Bulle annonce parfaite -->
  <div id="bulle-parfaite">
    <span class="bulle-close" onclick="this.parentElement.classList.remove('visible')">✕</span>
    <div class="bulle-titre">💡 Annonce parfaite</div>
    <div id="bulle-texte"></div>
  </div>
"""

# Insérer juste avant le premier {% endblock %} du content
src = src.replace('</div>\n{% endblock %}', '</div>\n' + BULLE_HTML + '\n{% endblock %}', 1)

# ─── 3. EXEMPLES PARFAITS + updateBubble dans le bloc JS ─────────────────────
EXEMPLES_JS = """
// ─── Exemples "Annonce parfaite" par sous-catégorie ──────────────────────────
const EXEMPLES_PARFAITS = {
  'vehicules-4x4':         '"Toyota Yaris 2020 — 45 000 km — Essence — Boite auto — 1 800 000 XPF, Papeete"',
  'vehicules-2roues':      '"Scooter Honda 125cc 2022 — 8 000 km — Très bon état — 380 000 XPF"',
  'vehicules-bateaux':     '"Hors-bord Yamaha 60CV 2018 — 6m — Excellent état — 2 200 000 XPF"',
  'vehicules-utilitaires': '"Fourgon Renault Trafic 2019 — 120 000 km — Diesel — 1 600 000 XPF"',
  'vehicules-pieces':      '"Pare-chocs avant Toyota Hilux 2015-2019 — Neuf — Ref: ABC123 — 45 000 XPF"',
  'immo-appartements':     '"T3 meublé 65m² étage 2 — Parking inclus — Loyer 80 000 XPF/mois, Papeete"',
  'immo-maisons':          '"Villa 120m² + terrain 500m² — Piscine — Climatisée — 180 000 XPF/mois"',
  'immo-terrains':         '"Terrain 1 000m² viabilisé — Accès route — Zone résidentielle — 8 000 000 XPF"',
  'immo-bureaux':          '"Plateau 80m² — 4 bureaux — Parking — Centre Papeete — 120 000 XPF/mois"',
  'immo-saisonnieres':     '"Bungalow 2ch — Piscine — Plage 200m — 150 000 XPF/semaine, Moorea"',
  'immo-parkings':         '"Box fermé sécurisé — Accès 24h/24 — Centre Papeete — 15 000 XPF/mois"',
  'elec-telephones':       '"iPhone 15 Pro 256Go — Impeccable — Facture incluse — 180 000 XPF"',
  'elec-ordinateurs':      '"MacBook Air M2 — 16Go RAM — 512Go SSD — Très bon état — 280 000 XPF"',
  'elec-pc':               '"PC Gaming RTX 4060 — Ryzen 5 5600X — 32Go — 1To SSD — Watercooling — 350 000 XPF"',
  'elec-tv':               '"Samsung 65\\" 4K Smart TV — Neuf déballé — 130 000 XPF"',
  'elec-jeux':             '"PS5 + FIFA 25 + GTA VI — Très bon état — Manette extra — 135 000 XPF"',
  'elec-electromenager':   '"Lave-linge Samsung 8kg — Très bon état — Notice incluse — 70 000 XPF"',
  'emploi-commerciaux':    '"Commercial CDI Papeete — Fixe 200 000 + variable — Voiture de fonction"',
  'emploi-informatique':   '"Dev Django/React CDI — Télétravail partiel — 350 000 XPF/mois"',
  'emploi-hotellerie':     '"Serveur bilingue FR/EN — CDD saisonnier Bora Bora — Logé et nourri"',
  'emploi-btp':            '"Maçon confirmé — Chantier résidentiel Papeete — Début immédiat — 12 000 XPF/jour"',
  'emploi-services':       '"Aide à domicile CDI — CAP requis — Références exigées — Papeete"',
  'services-travaux':      '"Peinture intérieure — Devis gratuit — Matériel fourni — Papeete + 20 km"',
  'services-cours':        '"Cours maths Lycée à domicile — Tous niveaux — 3 500 XPF/heure, Papeete"',
  'services-transport':    '"Aéroport Faa\\'a → centre ville — 7j/7 — 5 places — 3 000 XPF"',
  'services-sante':        '"Massage polynésien à domicile — Diplômée — 8 000 XPF/séance"',
  'services-jardinage':    '"Entretien jardin hebdomadaire — Matériel fourni — Surface max 300m²"',
  'autres-meubles':        '"Canapé angle gris tissu — 240×160 cm — Très bon état — Livraison possible — 35 000 XPF"',
  'autres-vetements':      '"Robe de soirée Zara taille M — Neuve avec étiquette — 4 500 XPF"',
  'autres-sport':          '"Planche de surf 6\\'2 — Bon état — Housses incluses — 35 000 XPF"',
  'autres-puericulture':   '"Poussette Babymoov 0-3 ans — Très bon état — Accessoires inclus — 25 000 XPF"',
  'autres-divers':         'Titre clair + photos nettes + prix + localisation = annonce vue 5× plus !',
};

let _bulleTimer = null;
function updateBubble(souscat) {
  const bulle = document.getElementById('bulle-parfaite');
  const texte = document.getElementById('bulle-texte');
  if (!bulle || !texte) return;
  const ex = EXEMPLES_PARFAITS[souscat];
  if (!ex) { bulle.classList.remove('visible'); return; }
  texte.textContent = ex;
  bulle.classList.remove('visible');
  clearTimeout(_bulleTimer);
  _bulleTimer = setTimeout(() => bulle.classList.add('visible'), 120);
}

"""

# Insérer après la ligne "// Écouter sous-catégorie"
src = src.replace(
    '// Écouter sous-catégorie\n',
    '// Écouter sous-catégorie\n' + EXEMPLES_JS
)

# ─── 4. MISE À JOUR DES LISTENERS pour appeler updateBubble ──────────────────
# Dans updateSousCatsDep, après renderSpecs(firstSousCat)
src = src.replace(
    '  renderSpecs(firstSousCat);\n  adaptPrix(cat, firstSousCat);\n}',
    '  renderSpecs(firstSousCat);\n  adaptPrix(cat, firstSousCat);\n  updateBubble(firstSousCat);\n}'
)

# Le listener sous-catégorie
src = src.replace(
    "  sousCatSel.addEventListener('change', () => renderSpecs(sousCatSel.value));\n",
    "  sousCatSel.addEventListener('change', () => { renderSpecs(sousCatSel.value); updateBubble(sousCatSel.value); });\n"
)

# ─── 5. ANIMATION dans renderSpecs ───────────────────────────────────────────
OLD_RENDER_START = """function renderSpecs(souscat) {
  const container = document.getElementById('specs-container');
  if (!container) return;

  // Adapter le label Prix
  const cat = document.getElementById('id_categorie') ? document.getElementById('id_categorie').value : '';
  adaptPrix(cat, souscat);

  const fields = SPECS_DEF[souscat];
  if (!fields || fields.length === 0) { container.innerHTML = ''; return; }"""

NEW_RENDER_START = """function renderSpecs(souscat) {
  const container = document.getElementById('specs-container');
  if (!container) return;

  // Adapter le label Prix
  const cat = document.getElementById('id_categorie') ? document.getElementById('id_categorie').value : '';
  adaptPrix(cat, souscat);

  const fields = SPECS_DEF[souscat];
  if (!fields || fields.length === 0) {
    container.classList.add('specs-hidden');
    setTimeout(() => { container.innerHTML = ''; container.classList.remove('specs-hidden'); }, 250);
    return;
  }
  container.classList.add('specs-hidden');
  setTimeout(() => {
    container.classList.remove('specs-hidden');
  }, 30);"""

src = src.replace(OLD_RENDER_START, NEW_RENDER_START)

# ─── 6. EXEMPLES INLINE sur les labels dans renderSpecs ─────────────────────
# Remplace la ligne du label dans renderSpecs pour afficher l'exemple du placeholder
OLD_LABEL_LINE = "      html += `<label class=\"block text-xs font-bold text-gray-600 uppercase tracking-wide mb-1.5\">${f.label}</label>`;"
NEW_LABEL_LINE = "      const ex = f.placeholder ? `<span class='champ-exemple'>Ex: ${f.placeholder}</span>` : '';\n      html += `<label class=\"block text-xs font-bold text-gray-600 uppercase tracking-wide mb-1.5\">${f.label}${ex}</label>`;"
src = src.replace(OLD_LABEL_LINE, NEW_LABEL_LINE)

with open(path, 'w', encoding='utf-8') as f:
    f.write(src)

print("✅ Patch formulaire ultime appliqué !")
print("   • CSS animation + styles bulle")
print("   • Bulle 'Annonce parfaite' flottante")
print("   • 31 exemples par sous-catégorie")
print("   • Exemples inline sur chaque label")
print("   • Listeners mis à jour")