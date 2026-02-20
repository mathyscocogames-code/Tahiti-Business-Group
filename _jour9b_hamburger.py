"""Jour 9b — Hamburger menu + slide panel catégories (mobile)"""

with open('templates/base.html', encoding='utf-8') as f:
    base = f.read()

# ── 1. Add id="cat-zone-2" to Zone 2 wrapper ─────────────────────────────────
old_z2 = '  <div class="border-b border-gray-200">\n    <nav class="max-w-7xl mx-auto px-4 cat-nav"'
new_z2 = '  <div id="cat-zone-2" class="border-b border-gray-200">\n    <nav class="max-w-7xl mx-auto px-4 cat-nav"'
if old_z2 in base and 'id="cat-zone-2"' not in base:
    base = base.replace(old_z2, new_z2)
    print('cat-zone-2 id OK')
elif 'id="cat-zone-2"' in base:
    print('cat-zone-2 id already present')
else:
    print('WARNING: Zone 2 div not found')

# ── 2. Add msg-icon-header class to messages badge link ───────────────────────
old_msg = 'class="relative flex items-center justify-center w-9 h-9 rounded-xl hover:bg-gray-100 transition flex-shrink-0" title="Mes messages"'
new_msg = 'class="msg-icon-header relative flex items-center justify-center w-9 h-9 rounded-xl hover:bg-gray-100 transition flex-shrink-0" title="Mes messages"'
if old_msg in base:
    base = base.replace(old_msg, new_msg)
    print('msg-icon-header class OK')
elif 'msg-icon-header' in base:
    print('msg-icon-header already present')
else:
    print('WARNING: messages badge link not found')

# ── 3. Add hamburger button before auth block ──────────────────────────────────
old_auth = (
    '        {% if user.is_authenticated %}\n'
    '        <!-- Messages badge -->'
)
new_auth = (
    '        <!-- Hamburger cat\u00e9gories (mobile) -->\n'
    '        <button class="hamburger-btn" onclick="openCatMenu()" '
    'aria-label="Cat\u00e9gories" id="hamburgerBtn">\n'
    '          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">\n'
    '            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" '
    'd="M4 6h16M4 12h16M4 18h16"/>\n'
    '          </svg>\n'
    '        </button>\n'
    '        {% if user.is_authenticated %}\n'
    '        <!-- Messages badge -->'
)
if old_auth in base and 'hamburger-btn' not in base:
    base = base.replace(old_auth, new_auth)
    print('hamburger button OK')
elif 'hamburger-btn' in base:
    print('hamburger button already present')
else:
    print('WARNING: auth block anchor not found for hamburger')

# ── 4. Slide panel HTML (right after </header>) ────────────────────────────────
SLIDE_HTML = (
    '\n<!-- \u2550\u2550\u2550 SLIDE MENU \u2014 Cat\u00e9gories (mobile) \u2550\u2550\u2550 -->\n'
    '<div class="slide-overlay" id="slideOverlay" onclick="closeCatMenu()"></div>\n'
    '<div class="slide-menu" id="slideMenu">\n'
    '  <div class="slide-menu__header">\n'
    '    <span class="font-bold text-gray-900 text-base">Cat\u00e9gories</span>\n'
    '    <button onclick="closeCatMenu()" class="slide-menu__close" aria-label="Fermer">\n'
    '      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">\n'
    '        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>\n'
    '      </svg>\n'
    '    </button>\n'
    '  </div>\n'
    '  <div class="slide-menu__body">\n'
    "    <a href=\"{% url 'liste_annonces' %}\" class=\"slide-cat-link slide-cat-link--all\"><span class=\"slide-cat-icon\">\U0001f50d</span>\u00a0Toutes les annonces</a>\n"
    "    <a href=\"{% url 'liste_annonces' %}?categorie=vehicules\" class=\"slide-cat-link\"><span class=\"slide-cat-icon\">\U0001f697</span>\u00a0V\u00e9hicules</a>\n"
    "    <a href=\"{% url 'liste_annonces' %}?categorie=immobilier\" class=\"slide-cat-link\"><span class=\"slide-cat-icon\">\U0001f3e0</span>\u00a0Immobilier</a>\n"
    "    <a href=\"{% url 'liste_annonces' %}?categorie=electronique\" class=\"slide-cat-link\"><span class=\"slide-cat-icon\">\U0001f4f1</span>\u00a0\u00c9lectronique</a>\n"
    "    <a href=\"{% url 'liste_annonces' %}?categorie=emploi\" class=\"slide-cat-link\"><span class=\"slide-cat-icon\">\U0001f4bc</span>\u00a0Emploi</a>\n"
    "    <a href=\"{% url 'liste_annonces' %}?categorie=services\" class=\"slide-cat-link\"><span class=\"slide-cat-icon\">\U0001f527</span>\u00a0Services</a>\n"
    "    <a href=\"{% url 'liste_annonces' %}?categorie=autres\" class=\"slide-cat-link\"><span class=\"slide-cat-icon\">\U0001f4e6</span>\u00a0Autres</a>\n"
    '    <div class="slide-menu__sep"></div>\n'
    "    <a href=\"{% url 'deposer_annonce' %}\" class=\"slide-cat-link slide-cat-link--cta\"><span class=\"slide-cat-icon\">\u271a</span>\u00a0D\u00e9poser une annonce</a>\n"
    '  </div>\n'
    '</div>\n'
)

if 'slideMenu' not in base:
    # Try to insert after </header> followed by blank line + <!-- MESSAGES -->
    if '</header>\n\n<!-- MESSAGES -->' in base:
        base = base.replace('</header>\n\n<!-- MESSAGES -->', '</header>\n' + SLIDE_HTML + '\n<!-- MESSAGES -->')
        print('slide panel added after </header>')
    elif '</header>\n<!-- MESSAGES -->' in base:
        base = base.replace('</header>\n<!-- MESSAGES -->', '</header>\n' + SLIDE_HTML + '\n<!-- MESSAGES -->')
        print('slide panel added after </header> (no blank line variant)')
    else:
        # Fallback: insert right after </header> using index
        idx = base.find('</header>')
        if idx >= 0:
            base = base[:idx + 9] + '\n' + SLIDE_HTML + base[idx + 9:]
            print('slide panel added (index fallback)')
        else:
            print('WARNING: </header> not found, slide panel not added')
else:
    print('slide panel already present')

# ── 5. Hamburger JS (before contact modal <script>) ────────────────────────────
HAMBURGER_JS = (
    '<script>\n'
    '// \u2500\u2500 Slide menu cat\u00e9gories \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n'
    'function openCatMenu() {\n'
    "  document.getElementById('slideMenu').classList.add('slide-menu--open');\n"
    "  document.getElementById('slideOverlay').classList.add('slide-overlay--visible');\n"
    "  document.body.style.overflow = 'hidden';\n"
    '}\n'
    'function closeCatMenu() {\n'
    "  document.getElementById('slideMenu').classList.remove('slide-menu--open');\n"
    "  document.getElementById('slideOverlay').classList.remove('slide-overlay--visible');\n"
    "  document.body.style.overflow = '';\n"
    '}\n'
    "document.addEventListener('keydown', e => { if (e.key === 'Escape') closeCatMenu(); });\n"
    '</script>\n\n'
)

if 'function openCatMenu' not in base:
    # Add before the contact modal script block
    CONTACT_SCRIPT_ANCHOR = '<script>\n// \u2500\u2500 Contact Modal'
    if CONTACT_SCRIPT_ANCHOR in base:
        base = base.replace(CONTACT_SCRIPT_ANCHOR, HAMBURGER_JS + CONTACT_SCRIPT_ANCHOR)
        print('hamburger JS added before contact modal script')
    else:
        # Fallback: before </body>
        base = base.replace('</body>', HAMBURGER_JS + '</body>')
        print('hamburger JS added before </body> (fallback)')
else:
    print('hamburger JS already present (function defined)')

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(base)
print('\nbase.html OK — hamburger + slide menu done')