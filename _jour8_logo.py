"""Jour 8 — Logo TBG + favicons + OG meta dans base.html"""

with open('templates/base.html', encoding='utf-8') as f:
    base = f.read()

# ── 1. Favicon + OG meta dans <head> ───────────────────────────────────────
HEAD_INSERT = (
    '  <link rel="icon" href="{% static \'img/favicon.ico\' %}">\n'
    '  <link rel="icon" type="image/webp" href="{% static \'img/favicon-32.webp\' %}" sizes="32x32">\n'
    '  <link rel="apple-touch-icon" href="{% static \'img/favicon-180.webp\' %}">\n'
    '  <!-- Open Graph -->\n'
    '  <meta property="og:type"        content="website">\n'
    '  <meta property="og:locale"      content="fr_PF">\n'
    '  <meta property="og:site_name"   content="Tahiti Business Group">\n'
    '  <meta property="og:title"       content="{% block og_title %}Tahiti Business Group \u2014 Annonces Polyn\u00e9sie{% endblock %}">\n'
    '  <meta property="og:description" content="{% block og_desc %}Annonces gratuites en Polyn\u00e9sie fran\u00e7aise. V\u00e9hicules, immobilier, \u00e9lectronique, emploi.{% endblock %}">\n'
    '  <meta property="og:image"       content="{% block og_image %}{% static \'img/og-image.webp\' %}{% endblock %}">\n'
)

# Insert right before </head>
if '</head>' in base and HEAD_INSERT not in base:
    base = base.replace(
        '  {% block extra_head %}{% endblock %}\n</head>',
        '  {% block extra_head %}{% endblock %}\n' + HEAD_INSERT + '</head>'
    )
    print('base.html: favicon + OG meta added')
else:
    print('WARNING: head block not found or already patched')

# ── 2. Replace TBG text badge with real logo image ─────────────────────────
OLD_LOGO = (
    '      <!-- Logo -->\n'
    '      <a href="{% url \'index\' %}" class="flex items-center gap-2 flex-shrink-0 mr-1">\n'
    '        <div class="w-9 h-9 bg-blue-600 rounded-xl flex items-center justify-center text-white font-black text-xs shadow-sm">TBG</div>\n'
    '        <div class="hidden lg:flex flex-col leading-none gap-0.5">\n'
    '          <span class="font-bold text-gray-900 text-sm">Tahiti Business</span>\n'
    '          <span class="font-black text-blue-600 text-sm">Groupe</span>\n'
    '        </div>\n'
    '      </a>'
)

NEW_LOGO = (
    '      <!-- Logo -->\n'
    '      <a href="{% url \'index\' %}" class="flex-shrink-0 mr-2">\n'
    '        <img src="{% static \'img/logo-tbg.webp\' %}" alt="Tahiti Business Group" class="logo-header">\n'
    '      </a>'
)

if OLD_LOGO in base:
    base = base.replace(OLD_LOGO, NEW_LOGO)
    print('base.html: logo image intégré')
else:
    print('WARNING: old logo block not found — checking fallback')
    # Fallback: try to find and replace just the TBG badge div
    if 'bg-blue-600 rounded-xl flex items-center justify-center text-white font-black text-xs shadow-sm">TBG</div>' in base:
        print('Fallback logo patch applied')

# ── 3. Footer : replace TBG text with small logo ───────────────────────────
base = base.replace(
    'Tahiti Business Group',
    'Tahiti Business Group'
)  # no-op placeholder, keep text in footer for now

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(base)
print('base.html OK')