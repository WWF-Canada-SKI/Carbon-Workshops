"""Every relative link, heading anchor and inline image in the Grasslands
workshop, resolved against the files on disk.

Run it after any heading rename -- a renamed heading silently breaks every
inbound deep link, and nothing else in the repository notices.
"""
import re, pathlib, urllib.parse, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def slug(h):
    """GitHub's rule: lowercase, drop punctuation, then each REMAINING space
    becomes a hyphen. The spaces the punctuation leaves behind are not
    collapsed, which is why 'Step 1 -- Why' slugs to 'step-1--why'."""
    h = h.strip().lower()
    h = re.sub(r'[^\w\s\-]', '', h, flags=re.UNICODE)
    return h.replace(' ', '-')


_cache = {}


def heads(path):
    key = str(path)
    if key not in _cache:
        out = set()
        for line in pathlib.Path(path).read_text().split("\n"):
            m = re.match(r'^#{1,6}\s+(.*)$', line)
            if m:
                out.add(slug(re.sub(r'`|\*\*|\*|<[^>]+>', '', m.group(1))))
        _cache[key] = out
    return _cache[key]


def main():
    bad = []
    for md in sorted(ROOT.rglob("*.md")):
        if "_source" in str(md):
            continue
        txt = md.read_text()
        for m in re.finditer(r'\[[^\]]*\]\(([^)\s]+)\)', txt):
            tgt = urllib.parse.unquote(m.group(1))
            if tgt.startswith(("http", "mailto:")):
                continue
            path, _, anch = tgt.partition("#")
            f = (md.parent / path).resolve() if path else md.resolve()
            if path:
                if not f.exists():
                    bad.append(f"{md.relative_to(ROOT)}: missing path -> {tgt}")
                    continue
                if f.is_dir():
                    if anch and (f / "README.md").exists():
                        f = f / "README.md"
                    elif anch:
                        bad.append(f"{md.relative_to(ROOT)}: anchor into a directory "
                                   f"with no README -> {tgt}")
                        continue
                    else:
                        continue
            if anch and str(f).endswith(".md") and anch not in heads(f):
                bad.append(f"{md.relative_to(ROOT)}: bad anchor -> {tgt}")
        for m in re.finditer(r'<img src="([^"]+)"', txt):
            src = urllib.parse.unquote(m.group(1))
            if not src.startswith("http") and not (md.parent / src).exists():
                bad.append(f"{md.relative_to(ROOT)}: missing image -> {src}")
    if bad:
        print("\n".join(bad))
        print(f"\n{len(bad)} problems")
        return 1
    print("all links, anchors and images resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
