"""Add Favoris link to slide menu (hamburger) and fix bottom-nav anchor."""

with open('templates/base.html', encoding='utf-8') as f:
    base = f.read()

# ── 1. Add Favoris to slide menu (after Annonces link) ─────────────────────
# Anchor: the Annonces slide-cat-link
OLD_ANNONCES = (
    '    <a href="{% url \'liste_annonces\' %}" class="slide-cat-link">'
    '<span class="slide-cat-icon">🔍</span>\u00a0Toutes les annonces</a>\n'
)
NEW_ANNONCES = (
    '    <a href="{% url \'liste_annonces\' %}" class="slide-cat-link">'
    '<span class="slide-cat-icon">🔍</span>\u00a0Toutes les annonces</a>\n'
    '    <a href="{% url \'mes_favoris\' %}" class="slide-cat-link">'
    '<span class="slide-cat-icon">❤️</span>\u00a0Mes Favoris</a>\n'
)

if 'mes_favoris' not in base:
    if OLD_ANNONCES in base:
        base = base.replace(OLD_ANNONCES, NEW_ANNONCES, 1)
        print('slide menu: Favoris added')
    else:
        # Try simpler anchor
        ALT_ANCHOR = "{% url 'liste_annonces' %}"
        print(f'WARNING: slide annonces anchor not found. "liste_annonces" in base: {ALT_ANCHOR in base}')
else:
    print('Favoris already in base.html')

# ── 2. Add Favoris to bottom nav (before Messages link) ──────────────────────
MSG_ANCHOR = '  <a href="{% url \'mes_messages\' %}" class="bottom-nav__item">'
FAV_NAV = (
    '  <a href="{% url \'mes_favoris\' %}" class="bottom-nav__item'
    '{% if request.resolver_match.url_name == \'mes_favoris\' %} bottom-nav__item--active{% endif %}">\n'
    '    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">\n'
    '      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" '
    'd="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>\n'
    '    </svg>\n'
    '    <span>Favoris</span>\n'
    '  </a>\n\n'
)

if 'mes_favoris' not in base:
    if MSG_ANCHOR in base:
        base = base.replace(MSG_ANCHOR, FAV_NAV + MSG_ANCHOR, 1)
        print('bottom-nav: Favoris added before Messages')
    else:
        print(f'WARNING: bottom-nav Messages anchor not found')
else:
    print('bottom-nav: mes_favoris already present')

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(base)
print('base.html: OK')