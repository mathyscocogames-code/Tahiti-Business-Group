"""Add rubriques import + data to ads/views.py index()."""

with open('ads/views.py', encoding='utf-8') as f:
    src = f.read()

# 1. Add import after the .models import line
OLD_IMPORT = 'from .models import Annonce, Message, CATEGORIES, SOUS_CATEGORIES'
NEW_IMPORT = (
    'from .models import Annonce, Message, CATEGORIES, SOUS_CATEGORIES\n'
    'from rubriques.models import ArticlePromo, ArticleInfo, ArticleNouveaute'
)
if 'ArticlePromo' not in src:
    src = src.replace(OLD_IMPORT, NEW_IMPORT, 1)
    print('import added')
else:
    print('import already present')

# 2. Update index() context to include rubriques data
OLD_INDEX_RETURN = (
    "    return render(request, 'ads/index.html', {\n"
    "        'annonces_recentes': annonces_recentes,\n"
    "        'annonces_par_cat':  annonces_par_cat,\n"
    "        'categories':        CATEGORIES,\n"
    "        'total_count':       total_count,\n"
    "    })"
)
NEW_INDEX_RETURN = (
    "    promos_home     = ArticlePromo.objects.filter(statut='valide').select_related('pro_user')[:4]\n"
    "    infos_home      = ArticleInfo.objects.filter(statut='valide').select_related('auteur')[:4]\n"
    "    nouveautes_home = ArticleNouveaute.objects.filter(statut='valide').select_related('pro_user')[:4]\n"
    "    return render(request, 'ads/index.html', {\n"
    "        'annonces_recentes': annonces_recentes,\n"
    "        'annonces_par_cat':  annonces_par_cat,\n"
    "        'categories':        CATEGORIES,\n"
    "        'total_count':       total_count,\n"
    "        'promos_home':       promos_home,\n"
    "        'infos_home':        infos_home,\n"
    "        'nouveautes_home':   nouveautes_home,\n"
    "    })"
)
if 'promos_home' not in src:
    src = src.replace(OLD_INDEX_RETURN, NEW_INDEX_RETURN, 1)
    print('index context updated')
else:
    print('index context already updated')

with open('ads/views.py', 'w', encoding='utf-8') as f:
    f.write(src)
print('ads/views.py OK')