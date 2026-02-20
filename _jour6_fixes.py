"""Jour 6 fixes: dropdown, accueil 8 annonces, emploi prix, pagination"""
import re

# ── 1. base.html — remove overflow-x-auto from Zone 2 wrapper ──────────────
with open('templates/base.html', encoding='utf-8') as f:
    base = f.read()

base = base.replace(
    '  <div class="overflow-x-auto border-b border-gray-200">',
    '  <div class="border-b border-gray-200">'
)
with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(base)
print('base.html: overflow-x-auto removed from Zone 2 wrapper')

# ── 2. ads/views.py — 8 annonces + total_count + pagination 20 ──────────────
with open('ads/views.py', encoding='utf-8') as f:
    views = f.read()

# 2a. index(): [:12] -> [:8] + add total_count
views = views.replace(
    "    annonces_recentes = Annonce.objects.filter(statut='actif').select_related('user')[:12]",
    "    annonces_recentes = Annonce.objects.filter(statut='actif').select_related('user')[:8]\n"
    "    total_count = Annonce.objects.filter(statut='actif').count()"
)

# 2b. pass total_count in context
views = views.replace(
    "        'annonces_par_cat':  annonces_par_cat,\n"
    "        'categories':        CATEGORIES,\n"
    "    })",
    "        'annonces_par_cat':  annonces_par_cat,\n"
    "        'categories':        CATEGORIES,\n"
    "        'total_count':       total_count,\n"
    "    })"
)

# 2c. Paginator 24 -> 20
views = views.replace('Paginator(qs, 24)', 'Paginator(qs, 20)')

with open('ads/views.py', 'w', encoding='utf-8') as f:
    f.write(views)
print('ads/views.py: 8 annonces, total_count, paginator 20')

# ── 3. index.html — add VOIR TOUT big button after annonces grid ─────────────
with open('templates/ads/index.html', encoding='utf-8') as f:
    idx = f.read()

# Replace the end of the annonces-recentes grid block
OLD_GRID_END = """\
      </div>
      {% else %}
      <div class="bg-white border border-gray-200 rounded-2xl p-12 text-center shadow-sm mb-10">"""

NEW_GRID_END = """\
      </div>
      <!-- VOIR TOUT button -->
      <div class="text-center mb-10">
        <a href="{% url 'liste_annonces' %}"
          class="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-bold px-8 py-3.5 rounded-xl transition shadow-sm text-sm">
          Voir toutes les annonces{% if total_count %}&nbsp;({{ total_count }}){% endif %} &rarr;
        </a>
      </div>
      {% else %}
      <div class="bg-white border border-gray-200 rounded-2xl p-12 text-center shadow-sm mb-10">"""

if OLD_GRID_END in idx:
    idx = idx.replace(OLD_GRID_END, NEW_GRID_END)
    print('index.html: VOIR TOUT button added')
else:
    print('WARNING: grid end marker not found in index.html')

# Also update grid mb-10 -> mb-6 since we have a button below
idx = idx.replace(
    '<div id="annonces-grid" class="ads-grid mb-10">',
    '<div id="annonces-grid" class="ads-grid mb-6">'
)

with open('templates/ads/index.html', 'w', encoding='utf-8') as f:
    f.write(idx)
print('index.html OK')

# ── 4. deposer.html — add id=prix-row + JS togglePrix ───────────────────────
with open('templates/ads/deposer.html', encoding='utf-8') as f:
    dep = f.read()

# Add id to prix row
dep = dep.replace(
    '            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">\n'
    '              <div>\n'
    '                <label class="block text-xs font-bold text-gray-600 uppercase tracking-wide mb-1.5">Prix (XPF)</label>',
    '            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4" id="prix-row">\n'
    '              <div>\n'
    '                <label class="block text-xs font-bold text-gray-600 uppercase tracking-wide mb-1.5">Prix (XPF)</label>'
)

# Patch JS event listener to also toggle prix
dep = dep.replace(
    'const catSelDep = document.getElementById(\'id_categorie\');\n'
    'if (catSelDep) {\n'
    '  catSelDep.addEventListener(\'change\', () => updateSousCatsDep(catSelDep.value));\n'
    '  updateSousCatsDep(catSelDep.value);\n'
    '}',
    'function togglePrix(cat) {\n'
    '  const row = document.getElementById(\'prix-row\');\n'
    '  if (row) row.style.display = cat === \'emploi\' ? \'none\' : \'\';\n'
    '}\n'
    'const catSelDep = document.getElementById(\'id_categorie\');\n'
    'if (catSelDep) {\n'
    '  catSelDep.addEventListener(\'change\', () => {\n'
    '    updateSousCatsDep(catSelDep.value);\n'
    '    togglePrix(catSelDep.value);\n'
    '  });\n'
    '  updateSousCatsDep(catSelDep.value);\n'
    '  togglePrix(catSelDep.value);\n'
    '}'
)

with open('templates/ads/deposer.html', 'w', encoding='utf-8') as f:
    f.write(dep)
print('deposer.html: id=prix-row + togglePrix JS')

# ── 5. edit_annonce.html — add id=prix-row + JS togglePrix ──────────────────
with open('templates/ads/edit_annonce.html', encoding='utf-8') as f:
    edit = f.read()

# Add id to prix row in edit form
edit = edit.replace(
    '            <!-- Prix -->\n'
    '            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">',
    '            <!-- Prix -->\n'
    '            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4" id="prix-row">'
)

# Add togglePrix after the existing sous_cats listener
edit = edit.replace(
    'document.getElementById(\'id_categorie\').addEventListener(\'change\', function () {\n'
    '  updateSousCats(this.value, \'\');\n'
    '});',
    'document.getElementById(\'id_categorie\').addEventListener(\'change\', function () {\n'
    '  updateSousCats(this.value, \'\');\n'
    '});\n'
    '\n'
    '// ── Toggle prix (cach\u00e9 pour emploi) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n'
    'function togglePrix(cat) {\n'
    '  const row = document.getElementById(\'prix-row\');\n'
    '  if (row) row.style.display = cat === \'emploi\' ? \'none\' : \'\';\n'
    '}\n'
    'const catElEdit = document.getElementById(\'id_categorie\');\n'
    'togglePrix(catElEdit.value);\n'
    'catElEdit.addEventListener(\'change\', function() { togglePrix(this.value); });'
)

with open('templates/ads/edit_annonce.html', 'w', encoding='utf-8') as f:
    f.write(edit)
print('edit_annonce.html: id=prix-row + togglePrix JS')

print('\nAll Jour 6 fixes applied!')