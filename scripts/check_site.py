"""Check generated pages for broken local links and images before deployment."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys


class References(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.references = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and attrs.get('href'):
            self.references.append(attrs['href'])
        if tag in ('img', 'script') and attrs.get('src'):
            self.references.append(attrs['src'])
        if tag == 'link' and attrs.get('href'):
            self.references.append(attrs['href'])


site = Path(sys.argv[1] if len(sys.argv) > 1 else '_site').resolve()
baseurl = '/Carbon-Workshops'
errors = []
pages = list(site.rglob('*.html'))
if not pages:
    raise SystemExit('No generated HTML pages were found.')
checked = 0
for page in pages:
    parser = References()
    parser.feed(page.read_text(encoding='utf-8'))
    for reference in parser.references:
        parsed = urlsplit(reference)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        path = unquote(parsed.path)
        if path == baseurl or path.startswith(baseurl + '/'):
            path = path[len(baseurl):] or '/'
        target = site / path.lstrip('/') if path.startswith('/') else page.parent / path
        target = target.resolve()
        if target.is_dir():
            target = target / 'index.html'
        checked += 1
        if not target.is_relative_to(site) or not target.is_file():
            errors.append(f'{page.relative_to(site)}: {reference}')
if errors:
    raise SystemExit('Broken internal links or images:\n' + '\n'.join(sorted(set(errors))))
print(f'Checked {checked} internal references across {len(pages)} HTML pages.')
