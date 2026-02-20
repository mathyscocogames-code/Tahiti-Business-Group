"""Patch ads/detail.html — add favoris, WhatsApp, phone, share, signaler."""

with open('templates/ads/detail.html', encoding='utf-8') as f:
    html = f.read()

if 'fav-btn' in html:
    print('detail.html: already patched')
    exit(0)

# ── 1. Add OG blocks for sharing ────────────────────────────────────────────
OG_ANCHOR = "{% block content %}"
OG_BLOCKS = (
    "{% block og_title %}{{ annonce.titre }} — TBG{% endblock %}\n"
    "{% block og_desc %}{{ annonce.description|truncatewords:25 }}{% endblock %}\n"
    "{% block og_image %}{% if annonce.photos %}{{ annonce.photos.0 }}{% endif %}{% endblock %}\n\n"
)
if '{% block og_title %}' not in html:
    html = html.replace(OG_ANCHOR, OG_BLOCKS + OG_ANCHOR, 1)

# ── 2. Replace vendeur section to add phone/WhatsApp links ──────────────────
OLD_TEL = (
    "            {% if annonce.user.tel %}"
    "<div class=\"text-blue-600 font-bold mt-1\">📞 {{ annonce.user.tel }}</div>"
    "{% endif %}"
)
NEW_TEL = (
    "            {% if annonce.user.tel %}\n"
    "            <div class=\"flex flex-wrap gap-2 mt-2\">\n"
    "              <a href=\"tel:{{ annonce.user.tel }}\"\n"
    "                 class=\"inline-flex items-center gap-1.5 bg-gray-900 text-white text-xs font-bold px-3 py-1.5 hover:bg-black transition\">\n"
    "                📞 {{ annonce.user.tel }}\n"
    "              </a>\n"
    "              {% if annonce.user.whatsapp %}\n"
    "              <a href=\"https://wa.me/{{ annonce.user.whatsapp|urlencode }}\"\n"
    "                 target=\"_blank\" rel=\"noopener\"\n"
    "                 class=\"inline-flex items-center gap-1.5 bg-green-600 text-white text-xs font-bold px-3 py-1.5 hover:bg-green-700 transition\">\n"
    "                💬 WhatsApp\n"
    "              </a>\n"
    "              {% else %}\n"
    "              <a href=\"https://wa.me/68989610613?text={{ annonce.titre|urlencode }}%20sur%20TBG\"\n"
    "                 target=\"_blank\" rel=\"noopener\"\n"
    "                 class=\"inline-flex items-center gap-1.5 bg-green-600 text-white text-xs font-bold px-3 py-1.5 hover:bg-green-700 transition\">\n"
    "                💬 WhatsApp TBG\n"
    "              </a>\n"
    "              {% endif %}\n"
    "            </div>\n"
    "            {% endif %}"
)
if OLD_TEL in html:
    html = html.replace(OLD_TEL, NEW_TEL, 1)
    print('detail.html: phone/WhatsApp patched')
else:
    print('WARNING: tel anchor not found')

# ── 3. Add action bar (favoris + share + signaler) after Titre & Prix card ──
PRIX_CARD_END = '      <!-- Description -->'
ACTION_BAR = '''\
      <!-- Action bar: Favoris · Partager · Signaler -->
      <div class="flex flex-wrap gap-2">
        <!-- Favoris -->
        <button class="fav-btn inline-flex items-center gap-1.5 border-2 border-gray-900 text-gray-900 text-xs font-bold px-4 py-2.5 hover:bg-gray-100 transition"
                data-fav-pk="{{ annonce.pk }}"
                aria-label="Ajouter aux favoris">
          <span class="fav-icon">♡</span>
          <span class="fav-label">Favoris</span>
        </button>
        <!-- Partager -->
        <button onclick="shareAnnonce()" class="inline-flex items-center gap-1.5 border border-gray-300 text-gray-600 text-xs font-semibold px-4 py-2.5 hover:border-gray-900 hover:text-gray-900 transition">
          🔗 Partager
        </button>
        <!-- WhatsApp share -->
        <a href="https://wa.me/?text={{ annonce.titre|urlencode }}%20%E2%80%94%20{{ request.build_absolute_uri|urlencode }}"
           target="_blank" rel="noopener"
           class="inline-flex items-center gap-1.5 border border-gray-300 text-gray-600 text-xs font-semibold px-4 py-2.5 hover:border-gray-900 hover:text-gray-900 transition">
          💬 WhatsApp
        </a>
        <!-- Signaler -->
        <a href="{% url 'signaler_annonce' annonce.pk %}"
           class="inline-flex items-center gap-1.5 border border-red-200 text-red-500 text-xs font-semibold px-4 py-2.5 hover:border-red-400 hover:text-red-700 transition ml-auto">
          🚨 Signaler
        </a>
      </div>

      <!-- Description -->
'''

if PRIX_CARD_END in html and 'fav-btn' not in html:
    html = html.replace(PRIX_CARD_END, ACTION_BAR, 1)
    print('detail.html: action bar added')
else:
    print('WARNING: description anchor not found or already patched')

# ── 4. Update extra_js block ─────────────────────────────────────────────────
OLD_JS = '''{% block extra_js %}
<script>
function switchPhoto(el, src) {
  document.getElementById('mainPhoto').src = src;
  document.querySelectorAll('.photo-thumb').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
}
</script>
{% endblock %}'''

NEW_JS = '''{% block extra_js %}
<script>
function switchPhoto(el, src) {
  document.getElementById('mainPhoto').src = src;
  document.querySelectorAll('.photo-thumb').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
}

// Partager via Web Share API ou copier le lien
function shareAnnonce() {
  const url  = location.href;
  const text = document.querySelector('h1') ? document.querySelector('h1').textContent.trim() : document.title;
  if (navigator.share) {
    navigator.share({ title: text, url: url }).catch(() => {});
  } else {
    navigator.clipboard.writeText(url).then(() => {
      showToast && showToast('Lien copié !', 'success');
    }).catch(() => {
      prompt('Copiez ce lien :', url);
    });
  }
}

// Favoris sur la page de détail
document.addEventListener('DOMContentLoaded', function() {
  const btn = document.querySelector('.fav-btn[data-fav-pk]');
  if (!btn) return;
  const pk = btn.dataset.favPk;
  const icon  = btn.querySelector('.fav-icon');
  const label = btn.querySelector('.fav-label');

  function isFav() {
    return (JSON.parse(localStorage.getItem('tbg_favoris') || '[]')).includes(pk);
  }
  function update() {
    if (isFav()) {
      icon.textContent  = '❤️';
      label.textContent = 'Sauvegardé';
      btn.style.background = '#111827';
      btn.style.color = '#fff';
    } else {
      icon.textContent  = '♡';
      label.textContent = 'Favoris';
      btn.style.background = '';
      btn.style.color = '';
    }
  }
  update();
  btn.addEventListener('click', function() {
    const list = JSON.parse(localStorage.getItem('tbg_favoris') || '[]');
    const idx = list.indexOf(pk);
    if (idx >= 0) {
      list.splice(idx, 1);
      typeof showToast !== 'undefined' && showToast('Retiré des favoris', 'info');
    } else {
      list.push(pk);
      typeof showToast !== 'undefined' && showToast('Ajouté aux favoris ❤️', 'success');
    }
    localStorage.setItem('tbg_favoris', JSON.stringify(list));
    update();
  });
});
</script>
{% endblock %}'''

if OLD_JS in html:
    html = html.replace(OLD_JS, NEW_JS, 1)
    print('detail.html: JS updated')
else:
    print('WARNING: JS block not matched exactly')

with open('templates/ads/detail.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('detail.html: OK')