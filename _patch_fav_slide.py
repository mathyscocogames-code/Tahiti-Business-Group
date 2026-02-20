"""Add Favoris link to slide menu after Toutes les annonces."""

with open('templates/base.html', encoding='utf-8') as f:
    base = f.read()

OLD = ('    <a href="{% url \'liste_annonces\' %}" class="slide-cat-link slide-cat-link--all">'
       '<span class="slide-cat-icon">\U0001f50d</span> Toutes les annonces</a>\n')
NEW = ('    <a href="{% url \'liste_annonces\' %}" class="slide-cat-link slide-cat-link--all">'
       '<span class="slide-cat-icon">\U0001f50d</span> Toutes les annonces</a>\n'
       '    <a href="{% url \'mes_favoris\' %}" class="slide-cat-link">'
       '<span class="slide-cat-icon">\u2764\ufe0f</span> Mes Favoris</a>\n')

if 'mes_favoris' in base:
    print('mes_favoris already in slide menu (bottom-nav already patched)')
elif OLD in base:
    base = base.replace(OLD, NEW, 1)
    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(base)
    print('slide menu: Favoris added')
else:
    print(f'WARNING: anchor not found. OLD in base: {OLD in base}')
    # Debug: show what's actually at line 323 area
    for i, line in enumerate(base.splitlines(), 1):
        if 'slide-cat-link--all' in line:
            print(f'Line {i}: {repr(line)}')