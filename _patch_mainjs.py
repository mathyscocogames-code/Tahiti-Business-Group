"""Append form spinners + favoris logic to main.js."""

with open('static/js/main.js', encoding='utf-8') as f:
    js = f.read()

if 'initFormSpinners' in js:
    print('main.js: already patched')
    exit(0)

ADDITIONS = r"""

// ── Form loading spinners ──────────────────────────────────────
function initFormSpinners() {
  document.querySelectorAll('form').forEach(form => {
    const btn = form.querySelector('button[type="submit"]');
    if (!btn || btn.dataset.noSpinner) return;
    form.addEventListener('submit', function() {
      if (!form.checkValidity()) return;
      const orig = btn.innerHTML;
      btn.disabled = true;
      btn.innerHTML = '<span class="btn-spinner"></span> Envoi\u2026';
      // Safety reset after 10s
      setTimeout(() => { btn.disabled = false; btn.innerHTML = orig; }, 10000);
    });
  });
}

// ── Favoris (localStorage) ─────────────────────────────────────
const FAV_KEY = 'tbg_favoris';

function getFavoris() {
  try { return JSON.parse(localStorage.getItem(FAV_KEY) || '[]'); }
  catch { return []; }
}

function initFavorisCards() {
  document.querySelectorAll('[data-fav-pk]').forEach(btn => {
    if (btn.closest('.fav-btn')) return; // detail page handled separately
    const pk = String(btn.dataset.favPk);
    if (getFavoris().includes(pk)) btn.classList.add('fav-active');
    btn.addEventListener('click', function(e) {
      e.preventDefault(); e.stopPropagation();
      const list = getFavoris();
      const idx  = list.indexOf(pk);
      if (idx >= 0) {
        list.splice(idx, 1);
        btn.classList.remove('fav-active');
        showToast('Retiré des favoris', 'info');
      } else {
        list.push(pk);
        btn.classList.add('fav-active');
        showToast('Ajouté aux favoris \u2764\ufe0f', 'success');
      }
      localStorage.setItem(FAV_KEY, JSON.stringify(list));
    });
  });
}

// ── Admin stats link in slide menu (for staff) ─────────────────
// (handled server-side via is_staff check in template)

"""

# Append additions before the last DOMContentLoaded block
OLD_INIT = "// ── Main init ──────────────────────────────────────────────────\ndocument.addEventListener('DOMContentLoaded', () => {\n  initLazyImages();\n  initAutoDismissMessages();\n  initCardAnimations();\n  initPhotoGallery();\n  initSearchAutoSubmit();\n  initScrollToTop();\n  initPrixInput();\n  initSectionReveals();"

NEW_INIT = (
    "// ── Main init ──────────────────────────────────────────────────\n"
    "document.addEventListener('DOMContentLoaded', () => {\n"
    "  initLazyImages();\n"
    "  initAutoDismissMessages();\n"
    "  initCardAnimations();\n"
    "  initPhotoGallery();\n"
    "  initSearchAutoSubmit();\n"
    "  initScrollToTop();\n"
    "  initPrixInput();\n"
    "  initSectionReveals();\n"
    "  initFormSpinners();\n"
    "  initFavorisCards();"
)

js = js + ADDITIONS
js = js.replace(OLD_INIT, NEW_INIT, 1)

with open('static/js/main.js', 'w', encoding='utf-8') as f:
    f.write(js)
print('main.js: spinners + favoris added')