"""Add Rubriques dropdown to desktop cat-nav Zone 2 only."""

with open('templates/base.html', encoding='utf-8') as f:
    base = f.read()

# Locate Zone 2
z2_start = base.find('id="cat-zone-2"')
if z2_start < 0:
    print('ERROR: cat-zone-2 not found')
    exit(1)
z2_end = base.find('</header>', z2_start)
z2_slice = base[z2_start:z2_end]

if 'rubriques_index' in z2_slice:
    print('desktop nav: Rubriques already present in cat-zone-2')
    exit(0)

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
    "          <a href=\"{% url 'rubriques_index' %}\">\U0001f4b0 Promos pro</a>\n"
    "          <a href=\"{% url 'rubriques_index' %}\">\U0001f4f0 Actualit\u00e9s</a>\n"
    "          <a href=\"{% url 'rubriques_index' %}\">\U0001f680 Nouveaut\u00e9s business</a>\n"
    "          {% if user.is_pro %}<a href=\"{% url 'deposer_promo' %}\">\u2795 D\u00e9poser une promo</a>{% endif %}\n"
    "          {% if user.is_staff %}<a href=\"{% url 'moderation_dashboard' %}\">\U0001f6e1\ufe0f Mod\u00e9ration</a>{% endif %}\n"
    '        </div>\n'
    '      </div>\n\n'
)

# Insert before the Info dropdown (which is the first cat-nav-item in zone 2)
INFO_ANCHOR = "        <a href=\"{% url 'page_info' %}\" class=\"cat-nav-link\">"
info_pos_in_z2 = z2_slice.find(INFO_ANCHOR)
if info_pos_in_z2 < 0:
    # Fallback: insert before flex-1 spacer
    FLEX_ANCHOR = '      <div class="flex-1"></div>'
    flex_pos_in_z2 = z2_slice.find(FLEX_ANCHOR)
    if flex_pos_in_z2 < 0:
        print('WARNING: no anchor found in cat-zone-2')
        exit(1)
    insert_abs = z2_start + flex_pos_in_z2
else:
    # Step back to the opening div of the item
    item_open = z2_slice.rfind('      <div class="cat-nav-item">', 0, info_pos_in_z2)
    insert_abs = z2_start + item_open

base = base[:insert_abs] + RUBRIQUES_DROPDOWN + base[insert_abs:]
print('desktop nav: Rubriques dropdown inserted')

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(base)
print('base.html OK')