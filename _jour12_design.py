"""Jour 12 — Design monochrome + Libre Baskerville + article-card."""

with open('static/css/style.css', encoding='utf-8') as f:
    css = f.read()

if 'article-card' in css:
    print('Design already applied')
    exit(0)

# ── 1. Override CSS custom properties → monochrome ──────────────────────────
OLD_VARS = """:root {
  --bg:        #ffffff;
  --bg-alt:    #f8f9fa;
  --bg-alt2:   #f0f2f5;
  --surface:   #ffffff;
  --text:      #1a1a1a;
  --text-sub:  #6b7280;
  --text-hint: #9ca3af;
  --border:    #e5e7eb;
  --border-md: #d1d5db;
  --primary:   #1a6cf1;
  --primary-h: #1558cc;
  --accent:    #059669;
  --accent-h:  #047857;
  --danger:    #ef4444;
  --warning:   #f59e0b;
  --shadow-sm: 0 1px 3px rgba(0,0,0,.08);
  --shadow:    0 4px 16px rgba(0,0,0,.08);
  --shadow-lg: 0 12px 40px rgba(0,0,0,.12);
  --radius:    14px;
  --radius-sm: 8px;
  --radius-lg: 20px;
}"""

NEW_VARS = """:root {
  --bg:        #ffffff;
  --bg-alt:    #f8f9fa;
  --bg-alt2:   #f0f2f5;
  --surface:   #ffffff;
  --text:      #111827;
  --text-sub:  #374151;
  --text-hint: #6b7280;
  --border:    #d1d5db;
  --border-md: #9ca3af;
  --primary:   #111827;
  --primary-h: #000000;
  --accent:    #111827;
  --accent-h:  #000000;
  --danger:    #ef4444;
  --warning:   #f59e0b;
  --shadow-sm: 0 1px 3px rgba(0,0,0,.10);
  --shadow:    0 4px 16px rgba(0,0,0,.12);
  --shadow-lg: 0 12px 40px rgba(0,0,0,.20);
  --radius:    14px;
  --radius-sm: 8px;
  --radius-lg: 20px;
}"""

if OLD_VARS in css:
    css = css.replace(OLD_VARS, NEW_VARS, 1)
    print('CSS variables updated to monochrome')
else:
    print('WARNING: CSS variables block not found — check style.css manually')

# ── 2. Append monochrome overrides + article-card ────────────────────────────
ADDITIONS = """

/* ════════════════════════════════════════════════════════════════════
   JOUR 12 — DESIGN MONOCHROME + TYPOGRAPHIE LIBRE BASKERVILLE
   ════════════════════════════════════════════════════════════════════ */

/* ── Typographie premium ─────────────────────────────────────────── */
h1, h2, h3, h4, h5, h6 {
  font-family: 'Libre Baskerville', Georgia, 'Times New Roman', serif;
  letter-spacing: -.02em;
}
body, p, input, textarea, select, button, a, label, span, li {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* ── Override Tailwind : fonds colorés → gris très clair ─────────── */
.bg-blue-50, .bg-blue-100,
.bg-emerald-50, .bg-emerald-100,
.bg-amber-50,  .bg-amber-100,
.bg-green-50,  .bg-green-100  { background-color: #f9fafb !important; }

/* ── Override Tailwind : boutons colorés → noir ─────────────────── */
.bg-blue-600,   .bg-blue-700,
.bg-emerald-600,.bg-emerald-700,
.bg-amber-500,  .bg-amber-600,
.bg-green-600,  .bg-green-700   { background-color: #111827 !important; }

.hover\\:bg-blue-700:hover, .hover\\:bg-blue-800:hover,
.hover\\:bg-blue-50:hover,
.hover\\:bg-emerald-700:hover,  .hover\\:bg-emerald-500:hover,
.hover\\:bg-amber-600:hover,    .hover\\:bg-amber-400:hover { background-color: #000 !important; }

/* ── Override Tailwind : textes colorés → noir ───────────────────── */
.text-blue-600,   .text-blue-700,   .text-blue-800,
.text-emerald-600,.text-emerald-700,
.text-amber-600,  .text-amber-700,
.text-green-600,  .text-green-700   { color: #111827 !important; }

.hover\\:text-blue-800:hover    { color: #000 !important; }

/* ── Override Tailwind : bordures colorées → gris ───────────────── */
.border-blue-200,    .border-blue-300,    .border-blue-400,
.border-emerald-100, .border-emerald-200, .border-emerald-300, .border-emerald-400,
.border-amber-200,   .border-amber-300,   .border-amber-400,
.border-blue-500 { border-color: #d1d5db !important; }

.hover\\:border-blue-300:hover, .hover\\:border-blue-400:hover,
.hover\\:border-emerald-400:hover,
.hover\\:border-amber-400:hover { border-color: #111827 !important; }

/* ── Override Tailwind : gradients colorés → noir ───────────────── */
.bg-gradient-to-r {
  background: linear-gradient(to right, #1a1a1a, #000000) !important;
}

/* ── Badges colorés dans rubriques → monochrome ─────────────────── */
.bg-amber-100.text-amber-700,
.bg-blue-50.text-blue-700,
.bg-emerald-50.text-emerald-700,
.bg-emerald-100.text-emerald-700 {
  background-color: #f3f4f6 !important;
  color: #111827 !important;
}

/* ── Exceptions : pubs conservent leurs couleurs ────────────────── */
/* Les pubs utilisent des classes custom (.billboard-*, .pub-slot)  */
/* pas de classes Tailwind colorées → aucun conflit                 */

/* ═══════════════════════════════════════════════════════════════════
   ARTICLE CARDS — Rubriques (Promo / Info / Nouveauté)
   ═══════════════════════════════════════════════════════════════════ */
.article-card {
  display: block;
  background: #ffffff;
  border: 2px solid #111827;
  border-radius: 0;
  overflow: hidden;
  cursor: pointer;
  text-decoration: none;
  color: inherit;
  transition: transform .25s ease, box-shadow .25s ease, border-color .2s;
}
.article-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 14px 44px rgba(0,0,0,.18);
  border-color: #000;
  text-decoration: none;
  color: inherit;
}

.article-card__image {
  width: 100%;
  height: 150px;
  background: #f3f4f6;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #e5e7eb;
}
.article-card__image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: grayscale(100%);
  transition: filter .35s ease;
}
.article-card:hover .article-card__image img {
  filter: grayscale(0%);
}
.article-card__emoji {
  font-size: 52px;
  line-height: 1;
  filter: grayscale(30%);
  transition: filter .3s ease;
}
.article-card:hover .article-card__emoji {
  filter: grayscale(0%);
}

.article-card__body  { padding: 16px 18px 14px; }
.article-card__badge {
  display: inline-block;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: .08em;
  text-transform: uppercase;
  border: 1px solid #111827;
  color: #111827;
  padding: 2px 7px;
  margin-bottom: 9px;
}
.article-card__title {
  font-family: 'Libre Baskerville', Georgia, serif;
  font-size: 14px;
  font-weight: 700;
  color: #000;
  line-height: 1.35;
  margin-bottom: 7px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.article-card__desc {
  font-size: 12px;
  color: #4b5563;
  line-height: 1.5;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.article-card__meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 11px;
  color: #9ca3af;
  border-top: 1px solid #e5e7eb;
  padding-top: 10px;
}
.article-card__cta {
  font-size: 11px;
  font-weight: 700;
  color: #111827;
  text-decoration: underline;
  text-underline-offset: 2px;
  white-space: nowrap;
}
.article-card:hover .article-card__cta { color: #000; }

/* ── Rubrique grid ───────────────────────────────────────────────── */
.rubrique-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
}
@media (max-width: 640px) {
  .rubrique-grid { grid-template-columns: 1fr; }
}

/* ── Section header rubriques ────────────────────────────────────── */
.rubrique-section-header {
  display: flex;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #111827;
}
.rubrique-section-header h2 {
  font-family: 'Libre Baskerville', Georgia, serif;
  font-size: 20px;
  font-weight: 700;
  color: #000;
  margin: 0;
}
.rubrique-section-badge {
  font-size: 9px;
  font-weight: 700;
  letter-spacing: .08em;
  text-transform: uppercase;
  border: 1px solid #111827;
  padding: 2px 7px;
  color: #111827;
}
.rubrique-section-link {
  margin-left: auto;
  font-size: 12px;
  font-weight: 700;
  color: #111827;
  text-decoration: underline;
  text-underline-offset: 3px;
}
"""

css = css + ADDITIONS
with open('static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
print('Style.css updated with monochrome design + article-card')