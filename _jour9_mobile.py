"""Jour 9 — Responsive mobile: viewport-fit, PWA meta, manifest, bottom-nav"""

with open('templates/base.html', encoding='utf-8') as f:
    base = f.read()

# ── 1. viewport-fit=cover ─────────────────────────────────────────────────────
base = base.replace(
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
    '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">'
)
print('viewport-fit=cover OK')

# ── 2. Manifest + PWA meta (after apple-touch-icon line) ──────────────────────
OLD_APPLE = "  <link rel=\"apple-touch-icon\" href=\"{% static 'img/favicon-180.webp' %}\">"
NEW_APPLE = (
    "  <link rel=\"apple-touch-icon\" href=\"{% static 'img/favicon-180.webp' %}\">\n"
    "  <link rel=\"manifest\" href=\"{% static 'manifest.json' %}\">\n"
    "  <meta name=\"theme-color\" content=\"#1a6cf1\">\n"
    "  <meta name=\"apple-mobile-web-app-capable\" content=\"yes\">\n"
    "  <meta name=\"apple-mobile-web-app-title\" content=\"TBG\">"
)
if OLD_APPLE in base and 'manifest.json' not in base:
    base = base.replace(OLD_APPLE, NEW_APPLE)
    print('manifest + PWA meta added')
elif 'manifest.json' in base:
    print('manifest link already present — skipping')
else:
    print('WARNING: apple-touch-icon line not found')

# ── 3. Replace sticky-cta with proper 5-tab bottom navigation ─────────────────
OLD_STICKY = (
    "<!-- Mobile CTA -->\n"
    "<div class=\"sticky-cta\">\n"
    "  <a href=\"{% url 'deposer_annonce' %}\" class=\"flex-1 btn btn-accent justify-center text-sm\">+ D\u00e9poser</a>\n"
    "  <a href=\"{% url 'liste_annonces' %}\" class=\"flex-1 btn btn-outline justify-center text-sm\">Parcourir</a>\n"
    "</div>"
)

NEW_NAV = (
    "<!-- Bottom navigation (mobile) -->\n"
    "<nav class=\"bottom-nav\" aria-label=\"Navigation mobile\">\n"
    "\n"
    "  <a href=\"{% url 'index' %}\" class=\"bottom-nav__item\">\n"
    "    <svg class=\"w-5 h-5\" fill=\"none\" stroke=\"currentColor\" viewBox=\"0 0 24 24\">\n"
    "      <path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6\"/>\n"
    "    </svg>\n"
    "    <span>Accueil</span>\n"
    "  </a>\n"
    "\n"
    "  <a href=\"{% url 'liste_annonces' %}\" class=\"bottom-nav__item\">\n"
    "    <svg class=\"w-5 h-5\" fill=\"none\" stroke=\"currentColor\" viewBox=\"0 0 24 24\">\n"
    "      <path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z\"/>\n"
    "    </svg>\n"
    "    <span>Annonces</span>\n"
    "  </a>\n"
    "\n"
    "  <a href=\"{% url 'deposer_annonce' %}\" class=\"bottom-nav__item bottom-nav__item--deposer\">\n"
    "    <svg class=\"w-6 h-6\" fill=\"none\" stroke=\"currentColor\" viewBox=\"0 0 24 24\">\n"
    "      <path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2.5\" d=\"M12 4v16m8-8H4\"/>\n"
    "    </svg>\n"
    "  </a>\n"
    "\n"
    "  <a href=\"{% url 'mes_messages' %}\" class=\"bottom-nav__item\">\n"
    "    <svg class=\"w-5 h-5\" fill=\"none\" stroke=\"currentColor\" viewBox=\"0 0 24 24\">\n"
    "      <path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z\"/>\n"
    "    </svg>\n"
    "    {% if unread_count %}<span class=\"bottom-nav__badge\">{{ unread_count }}</span>{% endif %}\n"
    "    <span>Messages</span>\n"
    "  </a>\n"
    "\n"
    "  {% if user.is_authenticated %}\n"
    "  <a href=\"{% url 'mon_compte' %}\" class=\"bottom-nav__item\">\n"
    "    <svg class=\"w-5 h-5\" fill=\"none\" stroke=\"currentColor\" viewBox=\"0 0 24 24\">\n"
    "      <path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z\"/>\n"
    "    </svg>\n"
    "    <span>Compte</span>\n"
    "  </a>\n"
    "  {% else %}\n"
    "  <a href=\"{% url 'login' %}\" class=\"bottom-nav__item\">\n"
    "    <svg class=\"w-5 h-5\" fill=\"none\" stroke=\"currentColor\" viewBox=\"0 0 24 24\">\n"
    "      <path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z\"/>\n"
    "    </svg>\n"
    "    <span>Connexion</span>\n"
    "  </a>\n"
    "  {% endif %}\n"
    "\n"
    "</nav>"
)

if OLD_STICKY in base:
    base = base.replace(OLD_STICKY, NEW_NAV)
    print('bottom-nav replaced sticky-cta OK')
else:
    print('WARNING: sticky-cta block not found — checking for partial match...')
    if 'sticky-cta' in base:
        print('Note: .sticky-cta class exists in HTML but string did not match exactly')
    else:
        print('Note: sticky-cta not found at all in base.html')

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(base)
print('base.html OK — Jour 9 mobile done')