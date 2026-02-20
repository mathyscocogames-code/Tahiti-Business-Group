"""Passe base.html de logo-tbg.webp → logo-tbg.svg + favicon SVG"""

with open('templates/base.html', encoding='utf-8') as f:
    base = f.read()

# ── 1. Header : webp → svg ──────────────────────────────────────────────────
base = base.replace(
    "{% static 'img/logo-tbg.webp' %}",
    "{% static 'img/logo-tbg.svg' %}"
)

# ── 2. Favicon : ajouter SVG en priorité (navigateurs modernes) ─────────────
OLD_FAV = (
    "  <link rel=\"icon\" href=\"{% static 'img/favicon.ico' %}\">\n"
    "  <link rel=\"icon\" type=\"image/webp\" href=\"{% static 'img/favicon-32.webp' %}\" sizes=\"32x32\">\n"
    "  <link rel=\"apple-touch-icon\" href=\"{% static 'img/favicon-180.webp' %}\">\n"
)

NEW_FAV = (
    "  <link rel=\"icon\" type=\"image/svg+xml\" href=\"{% static 'img/logo-tbg.svg' %}\">\n"
    "  <link rel=\"icon\" type=\"image/x-icon\" href=\"{% static 'img/favicon.ico' %}\" sizes=\"any\">\n"
    "  <link rel=\"apple-touch-icon\" href=\"{% static 'img/favicon-180.webp' %}\">\n"
)

if OLD_FAV in base:
    base = base.replace(OLD_FAV, NEW_FAV)
    print('Favicons updated: SVG first')
else:
    print('WARNING: favicon block not found')

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(base)
print('base.html OK — SVG logo + SVG favicon')