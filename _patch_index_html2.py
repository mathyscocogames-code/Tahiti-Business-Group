"""Replace the rubriques section in ads/index.html with article-card style."""

with open('templates/ads/index.html', encoding='utf-8') as f:
    html = f.read()

# Find and replace the rubriques section
START_MARKER = '      <!-- \u2500\u2500 RUBRIQUES (Promo / Info / Nouveaut\u00e9) \u2500\u2500 -->'
END_MARKER   = '      <!-- \u2500\u2500 /RUBRIQUES \u2500\u2500 -->'

start_idx = html.find(START_MARKER)
end_idx   = html.find(END_MARKER)
if start_idx < 0 or end_idx < 0:
    print('WARNING: rubriques section not found in index.html')
    exit(1)

# end_idx points to start of end marker, we include the end marker line
end_idx_full = html.find('\n', end_idx) + 1

NEW_SECTION = '''\
      <!-- \u2500\u2500 RUBRIQUES (Promo / Info / Nouveaut\u00e9) \u2500\u2500 -->
      {% if promos_home or infos_home or nouveautes_home %}
      <div class="mb-10">
        <div class="flex items-center justify-between mb-5 pb-3 border-b-2 border-gray-900">
          <h2 class="text-xl font-bold text-gray-900" style="font-family:\'Libre Baskerville\',Georgia,serif">Rubriques TBG</h2>
          <a href="{% url \'rubriques_index\' %}" class="text-xs font-bold text-gray-900 underline underline-offset-2">Voir tout \u2192</a>
        </div>

        {% if promos_home %}
        <div class="mb-6">
          <div class="flex items-center gap-3 mb-3">
            <span class="text-xs font-bold text-gray-900 border border-gray-900 px-2 py-0.5" style="letter-spacing:.06em;text-transform:uppercase">Promo</span>
            <span class="text-xs text-gray-400 font-medium">\U0001f4b0 R\u00e9ductions pros</span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {% for p in promos_home %}
            <a href="{{ p.lien_promo|default:\'#\' }}"
               {% if p.lien_promo %}target="_blank" rel="noopener"{% endif %}
               class="article-card">
              <div class="article-card__body">
                <div class="article-card__title">{{ p.titre }}</div>
                <div class="article-card__desc">{{ p.contenu }}</div>
                <div class="article-card__meta">
                  <span>{{ p.pro_user.nom|default:p.pro_user.email }}</span>
                  {% if p.lien_promo %}<span class="article-card__cta">Voir \u2192</span>{% endif %}
                </div>
              </div>
            </a>
            {% endfor %}
          </div>
        </div>
        {% endif %}

        {% if infos_home %}
        <div class="mb-6">
          <div class="flex items-center gap-3 mb-3">
            <span class="text-xs font-bold text-gray-900 border border-gray-900 px-2 py-0.5" style="letter-spacing:.06em;text-transform:uppercase">Info</span>
            <span class="text-xs text-gray-400 font-medium">\U0001f4f0 Actualit\u00e9s locales</span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {% for a in infos_home %}
            <a href="{{ a.source_media|default:\'#\' }}"
               {% if a.source_media %}target="_blank" rel="noopener"{% endif %}
               class="article-card">
              <div class="article-card__body">
                <div class="article-card__title">{{ a.titre }}</div>
                <div class="article-card__desc">{{ a.contenu }}</div>
                <div class="article-card__meta">
                  <span>{% if a.auteur %}{{ a.auteur.nom|default:a.auteur.email }}{% else %}TBG{% endif %}</span>
                  {% if a.source_media %}<span class="article-card__cta">Source \u2192</span>{% endif %}
                </div>
              </div>
            </a>
            {% endfor %}
          </div>
        </div>
        {% endif %}

        {% if nouveautes_home %}
        <div class="mb-2">
          <div class="flex items-center gap-3 mb-3">
            <span class="text-xs font-bold text-gray-900 border border-gray-900 px-2 py-0.5" style="letter-spacing:.06em;text-transform:uppercase">Nouveaut\u00e9</span>
            <span class="text-xs text-gray-400 font-medium">\U0001f680 Nouveaux business</span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {% for n in nouveautes_home %}
            <a href="{{ n.lien_redirection|default:\'#\' }}"
               {% if n.lien_redirection %}target="_blank" rel="noopener"{% endif %}
               class="article-card">
              <div class="article-card__body">
                <div class="article-card__title">{{ n.titre }}</div>
                <div class="article-card__desc">{{ n.contenu }}</div>
                <div class="article-card__meta">
                  <span>{{ n.pro_user.nom|default:n.pro_user.email }}</span>
                  {% if n.lien_redirection %}<span class="article-card__cta">En savoir + \u2192</span>{% endif %}
                </div>
              </div>
            </a>
            {% endfor %}
          </div>
        </div>
        {% endif %}

      </div>
      {% endif %}
      <!-- \u2500\u2500 /RUBRIQUES \u2500\u2500 -->
'''

html = html[:start_idx] + NEW_SECTION + html[end_idx_full:]
with open('templates/ads/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('index.html rubriques section updated')