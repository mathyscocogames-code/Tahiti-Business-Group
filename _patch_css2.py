"""Add spinner + fav button CSS to style.css."""

with open('static/css/style.css', encoding='utf-8') as f:
    css = f.read()

if 'btn-spinner' in css:
    print('CSS: already patched')
    exit(0)

ADDITIONS = """

/* ═══════════════════════════════════════════════════════════════
   JOUR 13 — SPINNERS · FAVORIS · UX POLISH
   ═══════════════════════════════════════════════════════════════ */

/* ── Loading spinner ─────────────────────────────────────────── */
@keyframes tbg-spin { to { transform: rotate(360deg); } }

.btn-spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid currentColor;
  border-top-color: transparent;
  border-radius: 50%;
  animation: tbg-spin .6s linear infinite;
  vertical-align: -3px;
  margin-right: 6px;
}

/* ── Favoris button ─────────────────────────────────────────── */
.fav-btn { transition: background .2s, color .2s, border-color .2s; }
.fav-btn.fav-active,
[data-fav-pk].fav-active {
  color: #e11d48;
}

/* ── Scroll-to-top ajustement monochrome ──────────────────────── */
/* Already in main.js - just ensure it's above bottom-nav on mobile */
@media (max-width: 767px) {
  /* Scroll-to-top is injected at bottom-6 left-6 — fine above bottom nav */
}

/* ── Toast style harmonisé ───────────────────────────────────── */
.toast {
  position: fixed;
  bottom: 80px; /* above bottom nav */
  right: 16px;
  background: #111827;
  color: #fff;
  padding: 12px 18px;
  border-radius: 0;
  font-size: 13px;
  font-weight: 600;
  z-index: 9999;
  box-shadow: 0 8px 32px rgba(0,0,0,.25);
  max-width: 280px;
  transition: opacity .3s, transform .3s;
}
.toast.success { border-left: 3px solid #10b981; }
.toast.error   { border-left: 3px solid #ef4444; }
.toast.info    { border-left: 3px solid #6b7280; }

/* ── Messages Django harmonisés B&W ─────────────────────────── */
.bg-green-50.border-green-200 {
  background: #f9fafb !important;
  border-color: #111827 !important;
  color: #111827 !important;
}
.bg-red-50.border-red-200 {
  background: #fff5f5 !important;
  border-color: #ef4444 !important;
  color: #7f1d1d !important;
}

/* ── Admin stats bar chart ──────────────────────────────────── */
.stat-bar {
  display: flex;
  align-items: flex-end;
  height: 120px;
  gap: 3px;
  padding-bottom: 4px;
}
.stat-bar__col {
  flex: 1;
  background: #111827;
  border-radius: 2px 2px 0 0;
  min-height: 2px;
  transition: opacity .2s;
}
.stat-bar__col:hover { opacity: .7; }
"""

css += ADDITIONS
with open('static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
print('CSS: spinner + fav + toast added')