"""Insert 3 rubriques sections into ads/index.html before Annonces recentes."""

with open('templates/ads/index.html', encoding='utf-8') as f:
    html = f.read()

ANCHOR = '      <!-- Annonces r\u00e9centes -->'
if ANCHOR not in html:
    # Try simpler anchor
    ANCHOR = '      <!-- Annonces r'
    if ANCHOR not in html:
        print('WARNING: anchor not found')
        exit(1)

RUBRIQUES_SECTION = '''\
      <!-- ── RUBRIQUES (Promo / Info / Nouveaut\u00e9) ── -->
      {% if promos_home or infos_home or nouveautes_home %}
      <div class="mb-10">
        <div class="flex items-center justify-between mb-5">
          <h2 class="text-xl font-bold text-gray-900">Rubriques TBG</h2>
          <a href="{% url 'rubriques_index' %}" class="text-sm text-blue-600 hover:underline font-medium">Voir tout \u2192</a>
        </div>

        {% if promos_home %}
        <div class="mb-6">
          <div class="flex items-center gap-2 mb-3">
            <span class="text-base font-bold text-amber-700 flex items-center gap-1.5">
              \U0001f4b0 Promos
              <span class="text-xs font-normal bg-amber-100 text-amber-700 px-2 py-0.5 rounded-full">PRO</span>
            </span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {% for p in promos_home %}
            <div class="bg-amber-50 border border-amber-200 rounded-xl p-4 hover:border-amber-400 transition">
              <div class="font-semibold text-gray-900 text-sm mb-1 truncate">{{ p.titre }}</div>
              <p class="text-xs text-gray-500 line-clamp-2 mb-2">{{ p.contenu }}</p>
              <div class="flex items-center justify-between">
                <span class="text-xs text-gray-400">{{ p.pro_user.nom|default:p.pro_user.email }}</span>
                {% if p.lien_promo %}<a href="{{ p.lien_promo }}" target="_blank" class="text-xs font-bold text-amber-700 hover:underline">Voir \u2192</a>{% endif %}
              </div>
            </div>
            {% endfor %}
          </div>
        </div>
        {% endif %}

        {% if infos_home %}
        <div class="mb-6">
          <div class="flex items-center gap-2 mb-3">
            <span class="text-base font-bold text-blue-700">\U0001f4f0 Actualit\u00e9s</span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {% for a in infos_home %}
            <div class="bg-blue-50 border border-blue-200 rounded-xl p-4 hover:border-blue-400 transition">
              <div class="font-semibold text-gray-900 text-sm mb-1 truncate">{{ a.titre }}</div>
              <p class="text-xs text-gray-500 line-clamp-2 mb-2">{{ a.contenu }}</p>
              <div class="flex items-center justify-between">
                <span class="text-xs text-gray-400">
                  {% if a.auteur %}{{ a.auteur.nom|default:a.auteur.email }}{% else %}TBG{% endif %}
                </span>
                {% if a.source_media %}<a href="{{ a.source_media }}" target="_blank" class="text-xs font-bold text-blue-700 hover:underline">Source \u2192</a>{% endif %}
              </div>
            </div>
            {% endfor %}
          </div>
        </div>
        {% endif %}

        {% if nouveautes_home %}
        <div class="mb-2">
          <div class="flex items-center gap-2 mb-3">
            <span class="text-base font-bold text-emerald-700 flex items-center gap-1.5">
              \U0001f680 Nouveaut\u00e9s
              <span class="text-xs font-normal bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded-full">PRO</span>
            </span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {% for n in nouveautes_home %}
            <div class="bg-emerald-50 border border-emerald-200 rounded-xl p-4 hover:border-emerald-400 transition">
              <div class="font-semibold text-gray-900 text-sm mb-1 truncate">{{ n.titre }}</div>
              <p class="text-xs text-gray-500 line-clamp-2 mb-2">{{ n.contenu }}</p>
              <div class="flex items-center justify-between">
                <span class="text-xs text-gray-400">{{ n.pro_user.nom|default:n.pro_user.email }}</span>
                {% if n.lien_redirection %}<a href="{{ n.lien_redirection }}" target="_blank" class="text-xs font-bold text-emerald-700 hover:underline">En savoir + \u2192</a>{% endif %}
              </div>
            </div>
            {% endfor %}
          </div>
        </div>
        {% endif %}

      </div>
      {% endif %}
      <!-- ── /RUBRIQUES ── -->

'''

html = html.replace(ANCHOR, RUBRIQUES_SECTION + ANCHOR, 1)
with open('templates/ads/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('index.html patched OK')