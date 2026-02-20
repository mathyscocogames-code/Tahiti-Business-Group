"""Jour 11 — Add Rubriques (Promo/Info/Nouveauté) to hamburger + desktop nav."""

with open('templates/base.html', encoding='utf-8') as f:
    base = f.read()

# ── 1. Hamburger slide panel — insert Rubriques section before Déposer CTA ──────
# Anchor: the separator just before "Déposer une annonce" CTA
# We look for the slide-menu__sep right before the CTA link

RUB_SECTION = (
    '    <div class="slide-menu__sep"></div>\n'
    '    <div class="slide-menu__section-title">Rubriques</div>\n'
    "    <a href=\"{% url 'rubriques_index' %}\" class=\"slide-cat-link\">"
    "<span class=\"slide-cat-icon\">\U0001f4f0</span>\u00a0Promo, Info &amp; Nouveaut\u00e9s</a>\n"
    "    {% if user.is_pro %}\n"
    "    <a href=\"{% url 'deposer_promo' %}\" class=\"slide-cat-link\">"
    "<span class=\"slide-cat-icon\">\U0001f4b0</span>\u00a0D\u00e9poser une promo</a>\n"
    "    <a href=\"{% url 'deposer_nouveaute' %}\" class=\"slide-cat-link\">"
    "<span class=\"slide-cat-icon\">\U0001f680</span>\u00a0Publier une nouveaut\u00e9</a>\n"
    "    {% endif %}\n"
    "    {% if user.is_staff %}\n"
    "    <a href=\"{% url 'moderation_dashboard' %}\" class=\"slide-cat-link slide-cat-link--admin\">"
    "<span class=\"slide-cat-icon\">\U0001f6e1\ufe0f</span>\u00a0Mod\u00e9ration</a>\n"
    "    {% endif %}\n"
)

# Find the separator before the deposer CTA that we want to insert before
# We search for the pattern of the deposer CTA link
CTA_ANCHOR = '    <div class="slide-menu__sep"></div>\n    <a href="{% url \'deposer_annonce\' %}" class="slide-cat-link slide-cat-link--cta">'

if 'rubriques_index' not in base:
    if CTA_ANCHOR in base:
        base = base.replace(CTA_ANCHOR, RUB_SECTION + CTA_ANCHOR, 1)
        print('hamburger: Rubriques section added')
    else:
        print('WARNING: hamburger CTA anchor not found')
else:
    print('hamburger: Rubriques already present')

# ── 2. Desktop cat-nav Zone 2 — add Rubriques dropdown ──────────────────────────
# We look for the Info dropdown we added earlier and insert before it
RUBRIQUES_DROPDOWN = (
    '      <div class="cat-nav-item">\n'
    "        <a href=\"{% url 'rubriques_index' %}\" class=\"cat-nav-link\">\n"
    '          \U0001f4f0 Rubriques\n'
    '          <svg class="cat-nav-chevron" fill="none" stroke="currentColor" viewBox="0 0 24 24">\n'
    '            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7"/>\n'
    '          </svg>\n'
    '        </a>\n'
    '        <div class="cat-dropdown cat-dropdown--right">\n'
    '          <div class="cat-dropdown__header">Rubriques TBG</div>\n'
    "          <a href=\"{% url 'rubriques_index' %}\">\U0001f4b0 Promos professionnelles</a>\n"
    "          <a href=\"{% url 'rubriques_index' %}#info\">\U0001f4f0 Actualit\u00e9s</a>\n"
    "          <a href=\"{% url 'rubriques_index' %}#nouveautes\">\U0001f680 Nouveaut\u00e9s business</a>\n"
    "          {% if user.is_pro %}<a href=\"{% url 'deposer_promo' %}\">\u2795 D\u00e9poser une promo</a>{% endif %}\n"
    "          {% if user.is_staff %}<a href=\"{% url 'moderation_dashboard' %}\">\U0001f6e1\ufe0f Mod\u00e9ration</a>{% endif %}\n"
    '        </div>\n'
    '      </div>\n\n'
)

# Find anchor: the Info dropdown in Zone 2
INFO_ANCHOR = '      <div class="cat-nav-item">\n        <a href="{% url \'page_info\' %}" class="cat-nav-link">'

if 'rubriques_index' not in base:
    # Try to find the Info anchor in Zone 2
    z2_start = base.find('id="cat-zone-2"')
    info_pos = base.find(INFO_ANCHOR, z2_start)
    if info_pos > 0:
        base = base[:info_pos] + RUBRIQUES_DROPDOWN + base[info_pos:]
        print('desktop nav: Rubriques dropdown added before Info')
    else:
        print('WARNING: Info dropdown anchor not found in cat-zone-2')
else:
    print('desktop nav: Rubriques already present')

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(base)
print('base.html OK')