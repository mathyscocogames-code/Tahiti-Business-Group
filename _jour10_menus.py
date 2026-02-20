"""Jour 10 — Ajouter Info + Business dans le menu hamburger et la nav desktop"""

with open('templates/base.html', encoding='utf-8') as f:
    base = f.read()

# ── 1. Slide panel : add Info & Business sections before the deposer CTA ──────
OLD_SEP = (
    '    <div class="slide-menu__sep"></div>\n'
    "    <a href=\"{% url 'deposer_annonce' %}\" class=\"slide-cat-link slide-cat-link--cta\">"
    "<span class=\"slide-cat-icon\">\u271a</span>\u00a0D\u00e9poser une annonce</a>\n"
)

NEW_SEP = (
    '    <div class="slide-menu__sep"></div>\n'
    # Info section
    '    <div class="slide-menu__section-title">Infos &amp; Aide</div>\n'
    "    <a href=\"{% url 'page_info' %}\" class=\"slide-cat-link\">"
    "<span class=\"slide-cat-icon\">\U0001f4e2</span>\u00a0Guide &amp; FAQ</a>\n"
    "    <a href=\"{% url 'tarifs_pubs' %}\" class=\"slide-cat-link\">"
    "<span class=\"slide-cat-icon\">\U0001f4b0</span>\u00a0Tarifs publicit\u00e9s</a>\n"
    # Business section
    '    <div class="slide-menu__sep"></div>\n'
    '    <div class="slide-menu__section-title">Business Tahiti</div>\n'
    "    <a href=\"{% url 'page_business' %}\" class=\"slide-cat-link\">"
    "<span class=\"slide-cat-icon\">\U0001f4bc</span>\u00a0Nouveaut\u00e9s &amp; Recrutements</a>\n"
    '    <div class="slide-menu__sep"></div>\n'
    # Deposer CTA (kept)
    "    <a href=\"{% url 'deposer_annonce' %}\" class=\"slide-cat-link slide-cat-link--cta\">"
    "<span class=\"slide-cat-icon\">\u271a</span>\u00a0D\u00e9poser une annonce</a>\n"
)

if OLD_SEP in base:
    base = base.replace(OLD_SEP, NEW_SEP)
    print('slide menu: Info + Business sections added')
elif 'page_info' in base:
    print('slide menu: Info already present')
else:
    print('WARNING: slide menu sep not found')

# ── 2. Desktop cat-nav Zone 2 : add Info + Business before "Faire de la pub" ──
OLD_PUB_LINK = (
    '      <div class="flex-1"></div>\n\n'
    '      <a href="{% url \'tarifs_pubs\' %}" class="cat-nav-link cat-nav-link--pub flex-shrink-0">'
    '\u2736 Faire de la pub</a>\n'
)

NEW_PUB_LINK = (
    '      <div class="flex-1"></div>\n\n'
    # Info link with dropdown
    '      <div class="cat-nav-item">\n'
    '        <a href="{% url \'page_info\' %}" class="cat-nav-link">\n'
    '          \U0001f4e2 Info\n'
    '          <svg class="cat-nav-chevron" fill="none" stroke="currentColor" viewBox="0 0 24 24">\n'
    '            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7"/>\n'
    '          </svg>\n'
    '        </a>\n'
    '        <div class="cat-dropdown cat-dropdown--right">\n'
    '          <div class="cat-dropdown__header">Informations</div>\n'
    '          <a href="{% url \'page_info\' %}">Comment utiliser</a>\n'
    '          <a href="{% url \'page_info\' %}#tarifs">Tarifs publicit\u00e9s</a>\n'
    '          <a href="{% url \'page_info\' %}#contact">Nous contacter</a>\n'
    '          <a href="{% url \'page_info\' %}#faq">FAQ</a>\n'
    '        </div>\n'
    '      </div>\n\n'
    # Business link with dropdown
    '      <div class="cat-nav-item">\n'
    '        <a href="{% url \'page_business\' %}" class="cat-nav-link">\n'
    '          \U0001f4bc Business\n'
    '          <svg class="cat-nav-chevron" fill="none" stroke="currentColor" viewBox="0 0 24 24">\n'
    '            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7"/>\n'
    '          </svg>\n'
    '        </a>\n'
    '        <div class="cat-dropdown cat-dropdown--right">\n'
    '          <div class="cat-dropdown__header">Business Tahiti</div>\n'
    '          <a href="{% url \'page_business\' %}">Nouveaut\u00e9s Tahiti</a>\n'
    '          <a href="{% url \'page_business\' %}#recrutements">Recrutements</a>\n'
    '          <a href="{% url \'page_business\' %}#tendances">Tendances march\u00e9</a>\n'
    '          <a href="{% url \'page_business\' %}#partenaires">Partenaires</a>\n'
    '        </div>\n'
    '      </div>\n\n'
    '      <a href="{% url \'tarifs_pubs\' %}" class="cat-nav-link cat-nav-link--pub flex-shrink-0">'
    '\u2736 Faire de la pub</a>\n'
)

if OLD_PUB_LINK in base and 'page_info' not in base.split('cat-zone-2')[1][:500]:
    base = base.replace(OLD_PUB_LINK, NEW_PUB_LINK)
    print('desktop nav: Info + Business dropdowns added')
elif 'page_business' in base:
    print('desktop nav: Business already present')
else:
    print('WARNING: desktop nav pub link not found')

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(base)
print('\nbase.html OK — menus updated')