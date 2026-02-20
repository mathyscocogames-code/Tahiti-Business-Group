"""Jour 7 — base.html: messages badge + modal + JS"""

with open('templates/base.html', encoding='utf-8') as f:
    base = f.read()

# ── 1. Remove top "Voir tout →" link from index section header
# (already done in jour6, but let's ensure)

# ── 2. Add Messages icon+badge after Déposer button (inside auth block)
OLD_DEPOSER_BLOCK = (
    '        <a href="{% url \'deposer_annonce\' %}" '
    'class="hidden sm:inline-flex items-center gap-1.5 bg-emerald-500 hover:bg-emerald-600 '
    'text-white font-bold px-4 py-2 rounded-xl text-sm transition shadow-sm">\n'
    '          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">\n'
    '            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4"/>\n'
    '          </svg>\n'
    '          D\u00e9poser\n'
    '        </a>\n'
    '\n'
    '        {% if user.is_authenticated %}'
)

NEW_DEPOSER_BLOCK = (
    '        <a href="{% url \'deposer_annonce\' %}" '
    'class="hidden sm:inline-flex items-center gap-1.5 bg-emerald-500 hover:bg-emerald-600 '
    'text-white font-bold px-4 py-2 rounded-xl text-sm transition shadow-sm">\n'
    '          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">\n'
    '            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4"/>\n'
    '          </svg>\n'
    '          D\u00e9poser\n'
    '        </a>\n'
    '\n'
    '        {% if user.is_authenticated %}\n'
    '        <!-- Messages badge -->\n'
    '        <a href="{% url \'mes_messages\' %}" '
    'class="relative flex items-center justify-center w-9 h-9 rounded-xl hover:bg-gray-100 transition flex-shrink-0" '
    'title="Mes messages">\n'
    '          <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">\n'
    '            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" '
    'd="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>\n'
    '          </svg>\n'
    '          {% if unread_count %}\n'
    '          <span class="msg-badge absolute -top-0.5 -right-0.5 bg-red-500 text-white rounded-full w-4 h-4 flex items-center justify-center font-bold leading-none" style="font-size:9px">\n'
    '            {{ unread_count }}\n'
    '          </span>\n'
    '          {% endif %}\n'
    '        </a>'
)

if OLD_DEPOSER_BLOCK in base:
    base = base.replace(OLD_DEPOSER_BLOCK, NEW_DEPOSER_BLOCK)
    print('base.html: messages badge added')
else:
    print('WARNING: deposer block not found — badge not added')

# ── 3. Add modal container + JS just before </body>
MODAL_HTML = '''
<!-- ═══ CONTACT MODAL ═══ -->
<div id="contactModal" class="modal-overlay" style="display:none" onclick="if(event.target===this)closeContact()">
  <div class="modal-box">
    <div class="modal-header">
      <span class="font-bold text-gray-900 text-sm">\u2709\ufe0f Contacter le vendeur</span>
      <button onclick="closeContact()" class="modal-close-btn" aria-label="Fermer">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>
    </div>
    <div id="modalContent" class="modal-body">
      <div class="text-center py-10 text-gray-400">
        <div class="text-4xl mb-2">&#x1F4AC;</div>Chargement\u2026
      </div>
    </div>
  </div>
</div>

<script>
// \u2500\u2500 Contact Modal \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
function openContact(url) {
  const modal = document.getElementById('contactModal');
  const content = document.getElementById('modalContent');
  modal.style.display = 'flex';
  document.body.style.overflow = 'hidden';
  content.innerHTML = '<div class="text-center py-10 text-gray-400"><div class="text-4xl mb-2">&#x1F4AC;</div>Chargement\u2026</div>';
  fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(r => r.json())
    .then(data => {
      if (data.error) { closeContact(); return; }
      content.innerHTML = data.html;
      const t = document.getElementById('chatThread');
      if (t) t.scrollTop = t.scrollHeight;
      const form = document.getElementById('contactForm');
      if (form) form.addEventListener('submit', submitContact);
    })
    .catch(() => {
      content.innerHTML = '<div class="text-center py-8 text-red-400">Erreur de chargement</div>';
    });
}

function closeContact() {
  document.getElementById('contactModal').style.display = 'none';
  document.body.style.overflow = '';
}

function submitContact(e) {
  e.preventDefault();
  const form = e.target;
  const url  = form.dataset.url;
  const btn  = form.querySelector('button[type=submit]');
  btn.disabled = true;
  fetch(url, {
    method: 'POST',
    body: new FormData(form),
    headers: { 'X-Requested-With': 'XMLHttpRequest' }
  })
    .then(r => r.json())
    .then(data => {
      if (data.success) {
        let t = document.getElementById('chatThread');
        if (!t) {
          t = document.createElement('div');
          t.id = 'chatThread';
          t.className = 'chat-thread';
          form.before(t);
          // Remove empty state if present
          const empty = t.previousSibling;
        }
        t.insertAdjacentHTML('beforeend', data.html);
        t.scrollTop = t.scrollHeight;
        form.querySelector('textarea').value = '';
        // Clear badge since we just sent a message
        const badge = document.querySelector('.msg-badge');
        if (badge) badge.remove();
      }
      btn.disabled = false;
    })
    .catch(() => { btn.disabled = false; });
}

document.addEventListener('keydown', e => { if (e.key === 'Escape') closeContact(); });
</script>
'''

if '</body>' in base:
    base = base.replace('</body>', MODAL_HTML + '\n</body>')
    print('base.html: modal + JS added before </body>')
else:
    print('WARNING: </body> not found in base.html')

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(base)
print('base.html OK')

# ── 4. index.html — remove top "Voir tout →" small link
with open('templates/ads/index.html', encoding='utf-8') as f:
    idx = f.read()

idx = idx.replace(
    '        <a href="{% url \'liste_annonces\' %}" class="text-sm text-blue-600 hover:text-blue-800 font-medium transition">Voir tout \u2192</a>\n',
    ''
)

with open('templates/ads/index.html', 'w', encoding='utf-8') as f:
    f.write(idx)
print('index.html: top "Voir tout" link removed')

print('\nAll done!')