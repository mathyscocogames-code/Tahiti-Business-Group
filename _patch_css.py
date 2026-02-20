with open('static/css/style.css', encoding='utf-8') as f:
    css = f.read()
OLD = '.slide-cat-link--cta  { color: var(--accent); font-weight: 700; }'
NEW = ('.slide-cat-link--cta   { color: var(--accent); font-weight: 700; }\n'
       '.slide-cat-link--admin { color: #6b7280; font-size: 13px; }')
if '--admin' not in css:
    css = css.replace(OLD, NEW, 1)
    with open('static/css/style.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print('CSS updated')
else:
    print('already present')