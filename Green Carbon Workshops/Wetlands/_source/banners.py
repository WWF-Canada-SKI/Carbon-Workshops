"""Peatland-palette banners for the Wetlands workshop.
Same grammar as the Forests banners: 1200x360, sky / air / substrate bands,
a wayfinding pill, a centred title and a caption line."""
import os, random

OUT = "/home/user/Terrestrial_Carbon_Workshops_V1/Wetlands"

DEFS = """<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{sky0}"/><stop offset="100%" stop-color="{sky1}"/>
  </linearGradient>
  <linearGradient id="air" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{air0}"/><stop offset="55%" stop-color="{air1}"/><stop offset="100%" stop-color="{air2}"/>
  </linearGradient>
  <linearGradient id="peat" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%"   stop-color="#6b4f2a"/><stop offset="18%" stop-color="#57401f"/>
    <stop offset="45%"  stop-color="#3d2c14"/><stop offset="78%" stop-color="#2a1d0d"/>
    <stop offset="100%" stop-color="#4a4036"/>
  </linearGradient>
</defs>"""


def sedge(x, base, h, fill, op):
    """A tussock of sedge/cottongrass blades."""
    out = []
    for i in range(5):
        dx = (i - 2) * 5
        tip = h * random.uniform(0.62, 1.0)
        out.append(f'<path d="M{x+dx:.0f} {base:.0f} Q{x+dx*2.2:.0f} {base-tip*0.6:.0f} '
                   f'{x+dx*3.4:.0f} {base-tip:.0f}" stroke="{fill}" stroke-width="2.4" '
                   f'fill="none" stroke-linecap="round" opacity="{op}"/>')
    return "".join(out)


def hummock(cx, base, w, h, top, side, op):
    """A Sphagnum hummock: a low dome."""
    return (f'<path d="M{cx-w:.0f} {base:.0f} Q{cx-w*0.55:.0f} {base-h:.0f} {cx:.0f} {base-h:.0f} '
            f'Q{cx+w*0.55:.0f} {base-h:.0f} {cx+w:.0f} {base:.0f} Z" fill="{side}" opacity="{op}"/>'
            f'<path d="M{cx-w*0.72:.0f} {base-h*0.32:.0f} Q{cx:.0f} {base-h*1.12:.0f} '
            f'{cx+w*0.72:.0f} {base-h*0.32:.0f}" stroke="{top}" stroke-width="5" fill="none" '
            f'stroke-linecap="round" opacity="{op}"/>')


def spruce(x, base, h, w, fill, op):
    """A stunted black spruce — the bog/fen silhouette."""
    parts = []
    for i in range(4):
        f = i / 3
        cy = base - h * (0.20 + 0.70 * f)
        hw = w * (1 - 0.70 * f)
        parts.append(f'<path d="M{x-hw:.0f} {cy:.0f} L{x:.0f} {cy-h*0.26:.0f} '
                     f'L{x+hw:.0f} {cy:.0f} Z" fill="{fill}" opacity="{op}"/>')
    parts.append(f'<rect x="{x-2:.0f}" y="{base-h*0.22:.0f}" width="4" height="{h*0.22:.0f}" '
                 f'fill="#3d2f22" opacity="{op}"/>')
    return "".join(parts)


def banner(path, title, subtitle, tagtext, accent, extra="", tagfill="#1d3326",
           sky=("#cfe0e6", "#9fbfc6"), air=("#a9c6c9", "#88aeb2", "#6d9498"),
           groundy=252, seed=7, pools=True):
    random.seed(seed)
    GREENS = ["#4a6b43", "#5e7a4a", "#3f5c3a"]
    MOSS_T = ["#8fae5a", "#a3bd68", "#7d9e50"]
    MOSS_S = ["#6d8a44", "#5d7a3a", "#7a9650"]
    art = []
    # far treeline of stunted spruce
    for x in range(15, 1200, 54):
        art.append(spruce(x, groundy - 6, random.randint(46, 78), 13, "#3a5240", 0.45))
    # hummock-hollow surface, skipping the centre for the title
    for x in range(-10, 1230, 74):
        if 310 < x < 890:
            continue
        i = random.randrange(3)
        art.append(hummock(x, groundy + 8, random.randint(34, 52),
                           random.randint(16, 30), MOSS_T[i], MOSS_S[i], 0.95))
    # sedges
    for x in range(20, 1200, 46):
        if 320 < x < 880:
            continue
        art.append(sedge(x, groundy + 4, random.randint(22, 44),
                         GREENS[random.randrange(3)], 0.8))
    # a few nearer spruce at the edges
    for x in (60, 140, 1080, 1160):
        art.append(spruce(x, groundy + 4, random.randint(92, 132), 20,
                          GREENS[random.randrange(3)], 0.9))
    # peat stratigraphy lines, closer-spaced with depth
    lines, y, step = [], groundy + 20, 10
    while y < 360:
        lines.append(f'<line x1="0" y1="{y}" x2="1200" y2="{y}"/>')
        y += step
        step = max(5, step - 0.7)
    # bog pools
    pool_svg = ""
    if pools:
        pool_svg = "".join(
            f'<ellipse cx="{cx}" cy="{groundy+10}" rx="{rx}" ry="7" fill="#5b7f86" opacity="0.75"/>'
            f'<ellipse cx="{cx}" cy="{groundy+8}" rx="{rx*0.7:.0f}" ry="4" fill="#7ea4a9" opacity="0.5"/>'
            for cx, rx in [(255, 44), (960, 38)])
    pill_w = max(168, 11 * len(tagtext) + 44)
    svg = f"""<svg width="1200" height="360" viewBox="0 0 1200 360" xmlns="http://www.w3.org/2000/svg" role="img">
<title>{title} — Wetland Carbon Workshop</title>
<desc>Illustration of a Canadian peatland — Sphagnum hummocks, sedges and stunted spruce above a deep layered peat profile — headed "{title}".</desc>
{DEFS.format(sky0=sky[0], sky1=sky[1], air0=air[0], air1=air[1], air2=air[2])}
<rect x="0" y="0" width="1200" height="92" fill="url(#sky)"/>
<rect x="0" y="92" width="1200" height="{groundy-92}" fill="url(#air)"/>
<rect x="0" y="{groundy}" width="1200" height="{360-groundy}" fill="url(#peat)"/>
<circle cx="1044" cy="50" r="24" fill="#fdf6e0" opacity="0.8"/>
<g opacity="0.2" stroke="#ffffff" stroke-width="2" fill="none" stroke-linecap="round">
  <path d="M0 52 Q 60 38 120 52 T 240 52 T 360 52"/>
  <path d="M690 34 Q 750 20 810 34 T 930 34"/>
</g>
{"".join(art)}
{pool_svg}
<g stroke="#140d06" stroke-width="1" opacity="0.30">{"".join(lines)}</g>
{extra}
<rect x="40" y="26" width="{pill_w}" height="32" rx="16" fill="{tagfill}" opacity="0.62"/>
<text x="{40 + pill_w/2:.0f}" y="47" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="600" letter-spacing="1" fill="#e8f3ea">{tagtext}</text>
<text x="600" y="186" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="46" font-weight="600" fill="#ffffff">{title}</text>
<text x="600" y="220" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="17" letter-spacing="1" fill="{accent}">{subtitle}</text>
</svg>
"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(svg)
    print("wrote", path.replace(OUT, "Wetlands"), len(svg), "bytes")


PALE = "#e2f0e6"

banner(f"{OUT}/01_Background/images/banner_wetland.svg", "Wetland Carbon Workshop",
       "BOGS &#8226; FENS &#8226; SWAMPS &#8226; MEASURING THE DEEPEST CARBON STORE",
       "WWF-CANADA CARBON MEASUREMENT", PALE, seed=3)

banner(f"{OUT}/01_Background/images/banner_background.svg", "Background",
       "WHAT PEAT IS &#8226; BOGS, FENS AND SWAMPS &#8226; WHY DEPTH DOMINATES",
       "SECTION 1 OF 4", PALE, seed=11)

# Planning: depth-probe grid over the peat
probe = ('<g opacity="0.85">' + "".join(
    f'<line x1="{x}" y1="{252}" x2="{x}" y2="{252 + d}" stroke="#ffd166" stroke-width="2"/>'
    f'<circle cx="{x}" cy="{252 + d}" r="3.5" fill="#ffd166"/>'
    for x, d in [(120, 46), (168, 72), (216, 95), (984, 88), (1032, 60), (1080, 38)]) + '</g>'
    '<text x="168" y="352" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" '
    'font-size="11" font-weight="600" fill="#ffd166">depth survey</text>')
banner(f"{OUT}/02_Project_Planning/images/banner_planning.svg", "Project Planning",
       "HOW MANY CORES &#8226; WHERE THEY GO &#8226; SURVEYING PEAT DEPTH",
       "SECTION 2 OF 4", PALE, extra=probe, seed=5)

# Field methods: a Russian corer chamber lying in the peat
corer = ('<g opacity="0.95">'
         '<rect x="196" y="150" width="14" height="196" rx="3" fill="#d8d2c4" stroke="#8a836f" stroke-width="1.5"/>'
         '<rect x="196" y="252" width="14" height="94" fill="#3d2c14" opacity="0.9"/>'
         '<circle cx="203" cy="146" r="9" fill="#b9b2a0" stroke="#8a836f" stroke-width="1.5"/>'
         '<line x1="186" y1="146" x2="220" y2="146" stroke="#8a836f" stroke-width="3" stroke-linecap="round"/>'
         '</g>'
         '<text x="203" y="128" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" '
         'font-size="11" font-weight="600" fill="#ffd166">50 cm drive</text>')
banner(f"{OUT}/03_Field_Methods/images/banner_field_methods.svg", "Field Methods",
       "SURVEYING DEPTH &#8226; CORING PEAT &#8226; SECTIONING AND PACKAGING",
       "SECTION 3 OF 4", PALE, extra=corer, seed=17)

# Data interpretation: a deepening stock bar
bars = '<g opacity="0.92">' + "".join(
    f'<rect x="{150 + i*26}" y="{336 - h}" width="18" height="{h}" rx="2" fill="#ffd166" opacity="{0.5 + i*0.1:.2f}"/>'
    for i, h in enumerate([16, 30, 48, 66, 84])) + '</g>'
bars += '<g opacity="0.92">' + "".join(
    f'<rect x="{944 + i*26}" y="{336 - h}" width="18" height="{h}" rx="2" fill="#9be6b4" opacity="{0.5 + i*0.11:.2f}"/>'
    for i, h in enumerate([24, 44, 62, 80])) + '</g>'
banner(f"{OUT}/04_Data_Interpretation/images/banner_data_interpretation.svg", "Data Interpretation",
       "LAB RESULTS &#8226; CARBON CALCULATOR &#8226; SCALING AND REPORTING",
       "SECTION 4 OF 4", PALE, extra=bars, seed=23)

# Chronology: an age-depth curve descending through the peat, dated tie points
random.seed(31)
pts = [(300, 262), (430, 278), (560, 296), (690, 314), (820, 330), (950, 344)]
path = "M" + " L".join(f"{x} {y}" for x, y in pts)
chron = (f'<path d="{path}" stroke="#ffd166" stroke-width="2.5" fill="none" opacity="0.9"/>'
         + "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="#ffd166" stroke="#3d2c14" stroke-width="1.5"/>'
                   for x, y in pts)
         + '<text x="300" y="250" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" '
           'font-size="11" font-weight="600" fill="#ffd166">²¹⁰Pb</text>'
           '<text x="950" y="336" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" '
           'font-size="11" font-weight="600" fill="#ffd166">¹⁴C</text>')
banner(f"{OUT}/05_Chronology_Supplement/images/banner_chronology.svg", "Chronology Supplement",
       "DATING THE PEAT &#8226; RERCA AND LORCA &#8226; RATES, NOT JUST STOCKS",
       "OPTIONAL SUPPLEMENT", "#f6e7c1", extra=chron, tagfill="#2b1d0d",
       sky=("#2e2a20", "#413424"), air=("#413424", "#4d3c28", "#57432c"), seed=29, pools=False)
