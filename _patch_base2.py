"""Patch base.html — canonical, admin stats in slide menu, favoris in bottom nav."""

with open('templates/base.html', encoding='utf-8') as f:
    base = f.read()

# ── 1. Add canonical link after og:image ────────────────────────────────────
CANONICAL_ANCHOR = '  <meta property="og:image"'
CANONICAL_TAG    = '  <link rel="canonical" href="{{ request.build_absolute_uri }}">\n'
if 'canonical' not in base:
    base = base.replace(CANONICAL_ANCHOR, CANONICAL_TAG + CANONICAL_ANCHOR, 1)
    print('base.html: canonical added')
else:
    print('base.html: canonical already present')

# ── 2. Add Admin Stats to slide menu (for staff) ────────────────────────────
OLD_STAFF_LINKS = (
    '    {% if user.is_staff %}\n'
    '    <a href="{% url \'moderation_dashboard\' %}" class="slide-cat-link slide-cat-link--admin">'
    '<span class="slide-cat-icon">\U0001f6e1\ufe0f</span>\u00a0Mod\u00e9ration</a>\n'
    '    {% endif %}'
)
NEW_STAFF_LINKS = (
    '    {% if user.is_staff %}\n'
    '    <a href="{% url \'moderation_dashboard\' %}" class="slide-cat-link slide-cat-link--admin">'
    '<span class="slide-cat-icon">\U0001f6e1\ufe0f</span>\u00a0Mod\u00e9ration</a>\n'
    '    <a href="{% url \'admin_stats\' %}" class="slide-cat-link slide-cat-link--admin">'
    '<span class="slide-cat-icon">\U0001f4ca</span>\u00a0Dashboard stats</a>\n'
    '    {% endif %}'
)
if 'admin_stats' not in base:
    if OLD_STAFF_LINKS in base:
        base = base.replace(OLD_STAFF_LINKS, NEW_STAFF_LINKS, 1)
        print('base.html: admin stats link added to slide menu')
    else:
        print('WARNING: staff links anchor not found in slide menu')
else:
    print('base.html: admin stats already in slide menu')

# ── 3. Add Favoris to bottom nav between Annonces and Déposer ───────────────
# The bottom nav has: Accueil | Annonces | [+ Déposer] | Messages | Compte
# We add ❤️ Favoris before the Messages button
FAV_LINK = (
    '  <a href="{% url \'mes_favoris\' %}" class="bottom-nav__item{% if request.resolver_match.url_name == \'mes_favoris\' %} bottom-nav__item--active{% endif %}">\n'
    '    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">\n'
    '      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" '
    'd="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>\n'
    '    </svg>\n'
    '    <span>Favoris</span>\n'
    '  </a>\n'
)
MSG_ANCHOR = '  {% if user.is_authenticated %}\n  <a href="{% url \'mes_messages\' %}"'
if 'mes_favoris' not in base and MSG_ANCHOR in base:
    base = base.replace(MSG_ANCHOR, FAV_LINK + MSG_ANCHOR, 1)
    print('base.html: favoris added to bottom nav')
else:
    print('base.html: favoris already in bottom nav or anchor not found')

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(base)
print('base.html: OK')