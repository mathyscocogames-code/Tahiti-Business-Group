"""Script temporaire pour écrire les templates"""
import os

# ── mes_annonces.html ──────────────────────────────────────────
mes_annonces = """\
{% extends 'base.html' %}
{% block title %}Mes annonces{% endblock %}

{% block content %}
<div class="max-w-4xl mx-auto px-4 py-8">

  <div class="flex items-center justify-between mb-6">
    <h1 class="text-2xl font-bold text-gray-900">Mes annonces</h1>
    <a href="{% url 'deposer_annonce' %}" class="btn btn-accent">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4"/>
      </svg>
      Nouvelle annonce
    </a>
  </div>

  {% if annonces %}
  <div class="space-y-3">
    {% for annonce in annonces %}
    <div class="bg-white border border-gray-200 rounded-2xl p-4 flex items-center gap-4 shadow-sm hover:shadow-md hover:border-gray-300 transition">

      <!-- Miniature -->
      <a href="{% url 'annonce_detail' annonce.pk %}" class="w-20 h-16 rounded-xl overflow-hidden flex-shrink-0 bg-gray-100 block">
        {% if annonce.get_main_photo %}
        <img src="{{ annonce.get_main_photo }}" class="w-full h-full object-cover" alt="{{ annonce.titre }}">
        {% else %}
        <div class="w-full h-full flex items-center justify-center text-2xl">
          {% if annonce.categorie == 'vehicules' %}&#x1F697;
          {% elif annonce.categorie == 'immobilier' %}&#x1F3E0;
          {% elif annonce.categorie == 'electronique' %}&#x1F4F1;
          {% elif annonce.categorie == 'emploi' %}&#x1F4BC;
          {% elif annonce.categorie == 'services' %}&#x1F527;
          {% else %}&#x1F4E6;{% endif %}
        </div>
        {% endif %}
      </a>

      <!-- Infos -->
      <div class="flex-1 min-w-0">
        <a href="{% url 'annonce_detail' annonce.pk %}"
          class="font-semibold text-gray-900 hover:text-blue-600 transition truncate block text-sm">
          {{ annonce.titre }}
        </a>
        <div class="flex flex-wrap items-center gap-x-3 gap-y-1 mt-1 text-xs text-gray-500">
          <span class="font-bold text-blue-600">{{ annonce.get_prix_display_label }}</span>
          <span>{{ annonce.get_categorie_display }}</span>
          <span>{{ annonce.localisation }}</span>
          <span>{{ annonce.views }} vue{{ annonce.views|pluralize }}</span>
          <span>{{ annonce.photos|length }} photo{{ annonce.photos|length|pluralize }}</span>
        </div>
        <div class="mt-1.5 flex items-center gap-2">
          <span class="badge
            {% if annonce.statut == 'actif' %}badge-actif
            {% elif annonce.statut == 'modere' %}badge-modere
            {% elif annonce.statut == 'vendu' %}badge-vendu
            {% else %}badge-expire{% endif %}">
            {{ annonce.get_statut_display }}
          </span>
          <span class="text-xs text-gray-400">{{ annonce.created_at|date:"d/m/Y" }}</span>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex items-center gap-1.5 flex-shrink-0 flex-wrap justify-end">
        <a href="{% url 'annonce_detail' annonce.pk %}"
          class="text-xs px-3 py-1.5 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium rounded-lg transition">
          Voir
        </a>
        <a href="{% url 'edit_annonce' annonce.pk %}"
          class="text-xs px-3 py-1.5 bg-blue-50 hover:bg-blue-100 text-blue-700 font-semibold rounded-lg transition">
          &#x270F; Modifier
        </a>
        {% if annonce.statut == 'actif' %}
        <form method="post" action="{% url 'marquer_vendu' annonce.pk %}">
          {% csrf_token %}
          <button type="submit" class="text-xs px-3 py-1.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 font-semibold rounded-lg transition">
            Vendu
          </button>
        </form>
        {% endif %}
        <form method="post" action="{% url 'supprimer_annonce' annonce.pk %}"
          onsubmit="return confirm('Supprimer d\u00e9finitivement cette annonce ?')">
          {% csrf_token %}
          <button type="submit" class="text-xs px-3 py-1.5 bg-red-50 hover:bg-red-100 text-red-600 font-semibold rounded-lg transition">
            Supprimer
          </button>
        </form>
      </div>

    </div>
    {% endfor %}
  </div>
  <div class="mt-6 text-center text-sm text-gray-400">
    {{ annonces|length }} annonce{{ annonces|length|pluralize }} au total
  </div>

  {% else %}
  <div class="bg-white border border-gray-200 rounded-2xl p-16 text-center shadow-sm">
    <div class="text-6xl mb-4">&#x1F4ED;</div>
    <h2 class="text-xl font-bold text-gray-800 mb-2">Aucune annonce</h2>
    <p class="text-gray-500 mb-6">Vous n'avez pas encore publi\u00e9 d'annonce.</p>
    <a href="{% url 'deposer_annonce' %}" class="btn btn-accent">
      D\u00e9poser ma premi\u00e8re annonce
    </a>
  </div>
  {% endif %}

</div>
{% endblock %}
"""

with open('templates/ads/mes_annonces.html', 'w', encoding='utf-8') as f:
    f.write(mes_annonces)
print('mes_annonces.html OK')

# ── deposer.html — ajouter sous_categorie ────────────────────
with open('templates/ads/deposer.html', encoding='utf-8') as f:
    deposer = f.read()

# Insert sous_categorie select after categorie block
old_block = """              <div>
                <label class="block text-xs font-bold text-gray-600 uppercase tracking-wide mb-1.5">Localisation</label>
                {{ form.localisation }}
              </div>
            </div>"""

new_block = """              <div>
                <label class="block text-xs font-bold text-gray-600 uppercase tracking-wide mb-1.5">Sous-cat\u00e9gorie</label>
                <select name="sous_categorie" id="id_sous_categorie" class="form-input">
                  <option value="">— Toutes / G\u00e9n\u00e9ral</option>
                </select>
              </div>
            </div>

            <div>
              <label class="block text-xs font-bold text-gray-600 uppercase tracking-wide mb-1.5">Localisation</label>
              {{ form.localisation }}
            </div>"""

deposer = deposer.replace(old_block, new_block)

# Add sous_categories_json to the JS block
sous_cats_js = """
// Sous-cat\u00e9gories dynamiques
const SOUS_CATS_DEP = {{ sous_categories_json|safe }};
function updateSousCatsDep(cat) {
  const sel = document.getElementById('id_sous_categorie');
  if (!sel) return;
  sel.innerHTML = '<option value="">\u2014 Toutes / G\u00e9n\u00e9ral</option>';
  (SOUS_CATS_DEP[cat] || []).forEach(({value, label}) => {
    const opt = document.createElement('option');
    opt.value = value; opt.textContent = label;
    sel.appendChild(opt);
  });
}
const catSelDep = document.getElementById('id_categorie');
if (catSelDep) {
  catSelDep.addEventListener('change', () => updateSousCatsDep(catSelDep.value));
  updateSousCatsDep(catSelDep.value);
}
"""

deposer = deposer.replace(
    'function previewPhotos(input) {',
    sous_cats_js + '\nfunction previewPhotos(input) {'
)

with open('templates/ads/deposer.html', 'w', encoding='utf-8') as f:
    f.write(deposer)
print('deposer.html OK')