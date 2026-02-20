"""Jour 5 — Fix CSS dropdown hover + billboard milieu dans index.html"""

# ── 1. style.css — fix dropdown hover ──────────────────────────────────────────
with open('static/css/style.css', encoding='utf-8') as f:
    css = f.read()

# Remplacer le bloc .cat-dropdown (display:none) par opacity/visibility
OLD_DROPDOWN = """\
.cat-dropdown {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 210px;
  background: white;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-lg);
  z-index: 200;
  padding: 6px 0;
  animation: dropIn .15s ease;
}
.cat-dropdown--right { left: auto; right: 0; }

@keyframes dropIn {
  from { opacity: 0; transform: translateY(-6px); }
  to   { opacity: 1; transform: translateY(0); }
}

.cat-nav-item:hover .cat-dropdown { display: block; }"""

NEW_DROPDOWN = """\
.cat-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 210px;
  background: white;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  box-shadow: 0 20px 60px rgba(0,0,0,.15);
  z-index: 1000;
  padding: 6px 0;
  /* Fix hover gap : opacity+visibility > display:none */
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  transform: translateY(-8px);
  transition: opacity .18s cubic-bezier(.4,0,.2,1),
              transform .18s cubic-bezier(.4,0,.2,1),
              visibility .18s;
}
.cat-dropdown--right { left: auto; right: 0; }

/* Hover ET focus-within (accessibilit\u00e9 clavier) */
.cat-nav-item:hover .cat-dropdown,
.cat-nav-item:focus-within .cat-dropdown {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
  transform: translateY(0);
}"""

if OLD_DROPDOWN in css:
    css = css.replace(OLD_DROPDOWN, NEW_DROPDOWN)
    print('CSS dropdown fix: OLD bloc found & replaced')
else:
    # Fallback: chercher et remplacer par morceaux
    css = css.replace(
        '.cat-nav-item:hover .cat-dropdown { display: block; }',
        ''  # supprime la ligne, le nouveau bloc inclut d\u00e9j\u00e0 la r\u00e8gle hover
    )
    # Injecter le nouveau bloc avant .cat-dropdown a {
    css = css.replace(
        '.cat-dropdown a {',
        NEW_DROPDOWN + '\n\n.cat-dropdown a {'
    )
    print('CSS dropdown fix: fallback injection')

with open('static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
print('style.css OK')


# ── 2. index.html — billboard milieu entre 2e et 3e cat\u00e9gorie ──────────────────
with open('templates/ads/index.html', encoding='utf-8') as f:
    idx = f.read()

# Ins\u00e9rer le billboard milieu dans la boucle, apr\u00e8s forloop.counter == 2
LOOP_END = "      {% endif %}\n      {% endfor %}"

BILLBOARD_MILIEU_BLOCK = """\
      {% endif %}

      {% if forloop.counter == 2 %}
      <!-- BILLBOARD MILIEU (15 000 XPF/mois) -->
      <div class="mb-10">
        {% if pub_billboard_milieu %}
        <a href="{{ pub_billboard_milieu.lien }}" target="_blank" rel="noopener sponsored"
          class="billboard-wrap block">
          <img src="{{ pub_billboard_milieu.get_image }}"
            alt="{{ pub_billboard_milieu.titre }}"
            class="billboard-img">
        </a>
        {% else %}
        <a href="{% url 'tarifs_pubs' %}" class="billboard-milieu-empty">
          <div class="billboard-milieu-empty__inner">
            <div class="billboard-milieu-empty__badge">PUBLICITE</div>
            <div class="billboard-milieu-empty__title">VOTRE MARQUE ICI</div>
            <div class="billboard-milieu-empty__price">15\u202f000 XPF / mois</div>
            <div class="billboard-milieu-empty__cta">
              R\u00e9server \u2192 89 61 06 13
            </div>
          </div>
        </a>
        {% endif %}
      </div>
      {% endif %}

      {% endfor %}"""

if LOOP_END in idx:
    idx = idx.replace(LOOP_END, BILLBOARD_MILIEU_BLOCK)
    print('index.html billboard milieu injected')
else:
    print('WARNING: loop end marker not found in index.html')

with open('templates/ads/index.html', 'w', encoding='utf-8') as f:
    f.write(idx)
print('index.html OK')