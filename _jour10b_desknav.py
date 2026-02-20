"""Jour 10b — Add Info + Business dropdowns to desktop cat-nav"""

with open('templates/base.html', encoding='utf-8') as f:
    base = f.read()

# ── Check state ────────────────────────────────────────────────────────────────
z2_start = base.find('id="cat-zone-2"')
z2_end   = base.find('</header>', z2_start)
z2       = base[z2_start:z2_end]

if 'page_info' in z2:
    print('desktop nav: Info already in cat-zone-2, nothing to do')
    exit()

# ── Find the unique anchor: <div class="flex-1"> + pub link ──────────────────
# The flex-1 spacer + pub link sit just before </nav>
ANCHOR = '      <div class="flex-1"></div>'
if ANCHOR not in z2:
    print('WARNING: flex-1 spacer not found in cat-zone-2')
    exit()

NEW_ITEMS = (
    # Info dropdown
    '      <div class="cat-nav-item">\n'
    "        <a href=\"{% url 'page_info' %}\" class=\"cat-nav-link\">\n"
    '          \U0001f4e2 Info\n'
    '          <svg class="cat-nav-chevron" fill="none" stroke="currentColor" viewBox="0 0 24 24">\n'
    '            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7"/>\n'
    '          </svg>\n'
    '        </a>\n'
    '        <div class="cat-dropdown cat-dropdown--right">\n'
    '          <div class="cat-dropdown__header">Informations</div>\n'
    "          <a href=\"{% url 'page_info' %}\">Comment utiliser</a>\n"
    "          <a href=\"{% url 'page_info' %}#tarifs\">Tarifs publicit\u00e9s</a>\n"
    "          <a href=\"{% url 'page_info' %}#contact\">Nous contacter</a>\n"
    "          <a href=\"{% url 'page_info' %}#faq\">FAQ</a>\n"
    '        </div>\n'
    '      </div>\n\n'
    # Business dropdown
    '      <div class="cat-nav-item">\n'
    "        <a href=\"{% url 'page_business' %}\" class=\"cat-nav-link\">\n"
    '          \U0001f4bc Business\n'
    '          <svg class="cat-nav-chevron" fill="none" stroke="currentColor" viewBox="0 0 24 24">\n'
    '            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7"/>\n'
    '          </svg>\n'
    '        </a>\n'
    '        <div class="cat-dropdown cat-dropdown--right">\n'
    '          <div class="cat-dropdown__header">Business Tahiti</div>\n'
    "          <a href=\"{% url 'page_business' %}\">Nouveaut\u00e9s Tahiti</a>\n"
    "          <a href=\"{% url 'page_business' %}#recrutements\">Recrutements</a>\n"
    "          <a href=\"{% url 'page_business' %}#tendances\">Tendances march\u00e9</a>\n"
    "          <a href=\"{% url 'page_business' %}#partenaires\">Partenaires</a>\n"
    '        </div>\n'
    '      </div>\n\n'
)

# Insert NEW_ITEMS right before the flex-1 spacer (inside cat-zone-2 only)
# We replace the first occurrence of ANCHOR that is INSIDE z2
insert_pos = base.find(ANCHOR, z2_start)
if insert_pos < 0 or insert_pos > z2_end:
    print('WARNING: anchor outside cat-zone-2')
else:
    base = base[:insert_pos] + NEW_ITEMS + base[insert_pos:]
    print('desktop nav: Info + Business dropdowns inserted')

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(base)
print('base.html OK')