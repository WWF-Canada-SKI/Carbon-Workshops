"""Grassland-palette banners for the Grasslands workshop.

Same grammar as the Forests and Wetlands banners: 1200x360, sky / air /
substrate bands, a wayfinding pill, a centred title and a caption line.

The one deliberate difference is the substrate band. In Wetlands it carries
peat stratigraphy lines; here it carries ROOTS descending through the soil,
because that is the argument of the whole workshop -- in grassland most of
the carbon is below ground, and most of the biomass is root.
"""
import os, random

OUT = "/home/user/Terrestrial_Carbon_Workshops_V1/Grasslands"

DEFS = """<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{sky0}"/><stop offset="100%" stop-color="{sky1}"/>
  </linearGradient>
  <linearGradient id="air" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{air0}"/><stop offset="55%" stop-color="{air1}"/><stop offset="100%" stop-color="{air2}"/>
  </linearGradient>
  <linearGradient id="soil" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%"   stop-color="#4a3421"/><stop offset="14%" stop-color="#3b2a1a"/>
    <stop offset="40%"  stop-color="#4b3826"/><stop offset="72%" stop-color="#6b5843"/>
    <stop offset="100%" stop-color="#8b7a63"/>
  </linearGradient>
</defs>"""


def tussock(x, base, h, fill, op, blades=7):
    """A bunchgrass tussock -- the defining grassland form."""
    out = []
    for i in range(blades):
        dx = (i - blades // 2) * 4
        tip = h * random.uniform(0.55, 1.0)
        lean = dx * random.uniform(1.6, 3.0)
        out.append(f'<path d="M{x+dx:.0f} {base:.0f} Q{x+dx+lean*0.4:.0f} {base-tip*0.62:.0f} '
                   f'{x+dx+lean:.0f} {base-tip:.0f}" stroke="{fill}" stroke-width="2.2" '
                   f'fill="none" stroke-linecap="round" opacity="{op}"/>')
    return "".join(out)


def forb(x, base, h, stem, head, op):
    """A flowering forb -- the colour in a native sward."""
    return (f'<path d="M{x} {base} Q{x-3} {base-h*0.6:.0f} {x+1} {base-h:.0f}" '
            f'stroke="{stem}" stroke-width="1.8" fill="none" opacity="{op}"/>'
            f'<circle cx="{x+1}" cy="{base-h:.0f}" r="3.4" fill="{head}" opacity="{op}"/>')


def oak(x, base, h, w, canopy, trunk, op):
    """A scattered, open-grown oak -- the savannah silhouette.

    Open-grown oaks are BROADER than tall and have irregular, lumpy crowns
    carried on a short thick bole. A single smooth dome on a thin stalk reads
    as a mushroom, which is what the first version of this looked like.
    """
    random.seed(int(x) + int(h))
    bole = h * 0.46
    out = [
        # short, thick, slightly tapered bole
        f'<path d="M{x-5:.0f} {base:.0f} L{x-3:.0f} {base-bole:.0f} '
        f'L{x+3:.0f} {base-bole:.0f} L{x+5:.0f} {base:.0f} Z" fill="{trunk}" opacity="{op}"/>',
        # two low limbs, which is what makes an open-grown oak recognisable
        f'<path d="M{x-2:.0f} {base-bole*0.82:.0f} Q{x-w*0.42:.0f} {base-bole*0.95:.0f} '
        f'{x-w*0.60:.0f} {base-h*0.66:.0f}" stroke="{trunk}" stroke-width="3.4" fill="none" '
        f'opacity="{op}" stroke-linecap="round"/>',
        f'<path d="M{x+2:.0f} {base-bole*0.86:.0f} Q{x+w*0.44:.0f} {base-bole*1.0:.0f} '
        f'{x+w*0.62:.0f} {base-h*0.70:.0f}" stroke="{trunk}" stroke-width="3.0" fill="none" '
        f'opacity="{op}" stroke-linecap="round"/>',
    ]
    # irregular crown from overlapping lobes, wider than tall
    cy = base - h * 0.74
    for dx, dy, rx, ry in [(-w*0.52, 6, w*0.50, h*0.21), (w*0.54, 8, w*0.47, h*0.20),
                           (-w*0.14, -7, w*0.52, h*0.25), (w*0.20, -4, w*0.48, h*0.23),
                           (0, -16, w*0.34, h*0.17)]:
        out.append(f'<ellipse cx="{x+dx:.0f}" cy="{cy+dy:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" '
                   f'fill="{canopy}" opacity="{op}"/>')
    return "".join(out)


def sage(x, base, h, w, fill, op):
    """A big sagebrush / antelope-brush shrub -- interior BC and the dry mixedgrass."""
    out = [f'<ellipse cx="{x}" cy="{base-h*0.55:.0f}" rx="{w:.0f}" ry="{h*0.5:.0f}" '
           f'fill="{fill}" opacity="{op*0.85:.2f}"/>']
    for i in range(4):
        dx = (i - 1.5) * w * 0.45
        out.append(f'<line x1="{x:.0f}" y1="{base:.0f}" x2="{x+dx:.0f}" y2="{base-h*0.7:.0f}" '
                   f'stroke="#6d6350" stroke-width="1.6" opacity="{op}"/>')
    return "".join(out)


def roots(x, top, depth, fill, op, seed_n):
    """A root system descending from a tussock. Fine, branching, and DEEP --
    this is the visual claim the workshop has to earn."""
    random.seed(seed_n)
    out = []
    for i in range(5):
        dx = random.uniform(-16, 16)
        d = depth * random.uniform(0.55, 1.0)
        mid = top + d * 0.5
        out.append(f'<path d="M{x:.0f} {top:.0f} Q{x+dx:.0f} {mid:.0f} {x+dx*2.1:.0f} {top+d:.0f}" '
                   f'stroke="{fill}" stroke-width="{1.7 - i*0.18:.2f}" fill="none" '
                   f'opacity="{op}" stroke-linecap="round"/>')
        # a couple of laterals
        for j in range(2):
            f = random.uniform(0.3, 0.75)
            bx = x + dx * f * 1.4
            by = top + d * f
            out.append(f'<path d="M{bx:.0f} {by:.0f} q{random.uniform(-14,14):.0f} '
                       f'{random.uniform(8,20):.0f} {random.uniform(-22,22):.0f} '
                       f'{random.uniform(14,30):.0f}" stroke="{fill}" stroke-width="0.9" '
                       f'fill="none" opacity="{op*0.8:.2f}" stroke-linecap="round"/>')
    return "".join(out)


def banner(path, title, subtitle, tagtext, accent, extra="", tagfill="#3a2c18",
           sky=("#cfe3ef", "#a8c8de"), air=("#c8cfa8", "#c2bf86", "#b0a86a"),
           groundy=250, seed=7, savannah=True):
    random.seed(seed)
    GRASS = ["#c9b26a", "#b59a52", "#d8c584"]
    GREENS = ["#8a9a54", "#76873f", "#9aa866"]
    ROOTC = "#cbb489"
    art = []

    # far horizon line of low hills
    art.append('<path d="M0 238 Q 180 224 360 236 T 720 232 T 1080 238 L1200 236 L1200 252 L0 252 Z" '
               'fill="#9aa06a" opacity="0.45"/>')

    # scattered oaks on the skyline -- the savannah case
    if savannah:
        for x, h in [(104, 96), (1100, 86), (240, 64)]:
            art.append(oak(x, groundy - 2, h, h * 0.95, "#6f7f45", "#4a3a26", 0.62))

    # sagebrush at the margins -- the interior BC case
    for x in (40, 1158):
        art.append(sage(x, groundy + 4, 40, 22, "#8d9679", 0.8))

    # The sward. Full-height tussocks everywhere except the centre, which is
    # reserved for the title; the centre instead gets a short row, so that no
    # stretch of soil carries roots with nothing growing above it.
    sward_x = []
    for x in range(-10, 1230, 38):
        if 300 < x < 900:
            continue
        art.append(tussock(x, groundy + 6, random.randint(30, 60),
                           GRASS[random.randrange(3)], 0.9))
        sward_x.append(x)
    for x in range(8, 1220, 52):
        if 310 < x < 890:
            continue
        art.append(tussock(x, groundy + 2, random.randint(20, 38),
                           GREENS[random.randrange(3)], 0.75, blades=5))
        sward_x.append(x)
    # the centre row: short enough to clear the subtitle baseline at y=220
    for x in range(306, 900, 33):
        art.append(tussock(x, groundy + 6, random.randint(14, 21),
                           GRASS[random.randrange(3)], 0.85, blades=5))
        art.append(tussock(x + 16, groundy + 2, random.randint(11, 17),
                           GREENS[random.randrange(3)], 0.7, blades=4))
        sward_x.append(x)
    # forbs
    for x in range(26, 1200, 67):
        if 300 < x < 900:
            continue
        art.append(forb(x, groundy + 4, random.randint(26, 46), "#7d8a4a",
                        random.choice(["#e0b23f", "#d98b5a", "#b98bb0", "#e8d98a"]), 0.85))

    # ROOTS -- the point of the whole thing. Deep, reaching most of the band.
    # Every root system descends from a tussock that is actually drawn above it:
    # root density tracks plant density, which is the claim the banner is making.
    sward_x = sorted(set(sward_x))
    anchors, last = [], -999
    for x in sward_x:                      # thin to ~one root system per 96 px
        if x - last >= 90 and 0 <= x <= 1190:
            anchors.append(x)
            last = x
    root_svg = "".join(roots(x, groundy + 6, random.randint(70, 104), ROOTC, 0.55, 100 + i)
                       for i, x in enumerate(anchors))
    # a few that go right to the bottom, to make "metres deep" visible --
    # also anchored, to the plants nearest thirds of the way across
    deep = [min(sward_x, key=lambda s, t=t: abs(s - t)) for t in (210, 640, 1010)]
    root_svg += "".join(roots(x, groundy + 6, 360 - groundy - 8, ROOTC, 0.42, 200 + i)
                        for i, x in enumerate(deep))

    # faint horizon bands in the soil -- horizons, not stratigraphy
    lines, y, step = [], groundy + 26, 22
    while y < 360:
        lines.append(f'<line x1="0" y1="{y:.0f}" x2="1200" y2="{y:.0f}"/>')
        y += step
        step += 6

    pill_w = max(168, 11 * len(tagtext) + 44)
    svg = f"""<svg width="1200" height="360" viewBox="0 0 1200 360" xmlns="http://www.w3.org/2000/svg" role="img">
<title>{title} — Grassland Carbon Workshop</title>
<desc>Illustration of a Canadian grassland — bunchgrass tussocks, forbs, sagebrush and scattered open-grown oaks above a deep soil profile threaded with roots, each root system descending from a plant above it — headed "{title}".</desc>
{DEFS.format(sky0=sky[0], sky1=sky[1], air0=air[0], air1=air[1], air2=air[2])}
<rect x="0" y="0" width="1200" height="120" fill="url(#sky)"/>
<rect x="0" y="120" width="1200" height="{groundy-120}" fill="url(#air)"/>
<rect x="0" y="{groundy}" width="1200" height="{360-groundy}" fill="url(#soil)"/>
<circle cx="1044" cy="54" r="26" fill="#fdf3d8" opacity="0.85"/>
<g opacity="0.22" stroke="#ffffff" stroke-width="2" fill="none" stroke-linecap="round">
  <path d="M0 58 Q 70 42 140 58 T 280 58 T 420 58"/>
  <path d="M700 38 Q 770 24 840 38 T 980 38"/>
</g>
{"".join(art)}
<g stroke="#241a10" stroke-width="1" opacity="0.26">{"".join(lines)}</g>
{root_svg}
{extra}
<rect x="40" y="26" width="{pill_w}" height="32" rx="16" fill="{tagfill}" opacity="0.66"/>
<text x="{40 + pill_w/2:.0f}" y="47" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="600" letter-spacing="1" fill="#f2ead6">{tagtext}</text>
<text x="600" y="186" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="46" font-weight="600" fill="#ffffff">{title}</text>
<text x="600" y="220" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="17" letter-spacing="1" fill="{accent}">{subtitle}</text>
</svg>
"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(svg)
    print("wrote", path.replace(OUT, "Grasslands"), len(svg), "bytes")


PALE = "#f4eed8"

banner(f"{OUT}/01_Background/images/banner_grassland.svg", "Grassland Carbon Workshop",
       "ROOTS &#8226; SHOOTS &#8226; SOILS &#8226; CARBON STOCKS AND MONITORING",
       "WWF-CANADA CARBON MEASUREMENT", PALE, seed=3)

banner(f"{OUT}/01_Background/images/banner_background.svg", "Background",
       "CARBON POOLS IN GRASSLANDS &#8226; ROOTS AND SHOOTS &#8226; DIGGING DEEP FOR BELOW-GROUND CARBON",
       "SECTION 1 OF 5", PALE, seed=11)

# Planning: stratification blocks across the sward
strata = ('<g opacity="0.85">' + "".join(
    f'<rect x="{x}" y="212" width="{w}" height="36" rx="4" fill="none" '
    f'stroke="{c}" stroke-width="2.5" stroke-dasharray="7 5"/>'
    for x, w, c in [(96, 150, "#ffd166"), (958, 132, "#9be6b4")]) + '</g>'
    '<text x="171" y="206" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" '
    'font-size="11" font-weight="600" fill="#ffd166">grazed</text>'
    '<text x="1024" y="206" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" '
    'font-size="11" font-weight="600" fill="#9be6b4">ungrazed</text>')
banner(f"{OUT}/02_Project_Planning/images/banner_planning.svg", "Project Planning",
       "HOW MANY CORES &#8226; STRATIFYING ON MANAGEMENT &#8226; SIZING FOR ROOTS",
       "SECTION 2 OF 5", PALE, extra=strata, seed=5)

# Field methods: a quadrat on the surface and a core beneath it
quad = ('<g opacity="0.95">'
        '<rect x="150" y="236" width="104" height="26" rx="2" fill="none" stroke="#ffd166" stroke-width="2.5"/>'
        '<rect x="196" y="250" width="16" height="96" rx="2" fill="#2e2114" stroke="#d8d2c4" stroke-width="1.6"/>'
        '</g>'
        '<text x="202" y="230" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" '
        'font-size="11" font-weight="600" fill="#ffd166">clip &#38; core</text>')
banner(f"{OUT}/03_Field_Methods/images/banner_field_methods.svg", "Field Methods",
       "CLIP AND WEIGH &#8226; CORING SOIL &#8226; SEPARATING ROOTS FROM SOIL",
       "SECTION 3 OF 5", PALE, extra=quad, seed=17)

# Data interpretation: stacked pools, roots and soil dwarfing shoots
bars = '<g opacity="0.92">' + "".join(
    f'<rect x="{150 + i*30}" y="{338 - h}" width="20" height="{h}" rx="2" fill="{c}" opacity="0.9"/>'
    for i, (h, c) in enumerate([(10, "#9be6b4"), (44, "#cbb489"), (88, "#ffd166")])) + '</g>'
bars += ('<text x="160" y="352" font-family="Helvetica, Arial, sans-serif" font-size="9" '
         'font-weight="600" fill="#f2ead6">shoot</text>'
         '<text x="188" y="352" font-family="Helvetica, Arial, sans-serif" font-size="9" '
         'font-weight="600" fill="#f2ead6">root</text>'
         '<text x="218" y="352" font-family="Helvetica, Arial, sans-serif" font-size="9" '
         'font-weight="600" fill="#f2ead6">soil</text>')
banner(f"{OUT}/04_Data_Interpretation/images/banner_data_interpretation.svg", "Data Interpretation",
       "LAB RESULTS &#8226; ROOT PROCESSING &#8226; CARBON CALCULATOR &#8226; REPORTING",
       "SECTION 4 OF 5", PALE, extra=bars, seed=23)

# Monitoring: two sampling times and the difference between them
random.seed(41)
t1 = [(300, 284), (420, 280), (540, 288), (660, 282), (780, 286), (900, 281)]
t2 = [(300, 268), (420, 262), (540, 272), (660, 264), (780, 266), (900, 259)]
mon = (f'<path d="M{" L".join(f"{x} {y}" for x, y in t1)}" stroke="#d8c584" stroke-width="2.5" '
       f'fill="none" opacity="0.9" stroke-dasharray="6 4"/>'
       f'<path d="M{" L".join(f"{x} {y}" for x, y in t2)}" stroke="#9be6b4" stroke-width="2.5" '
       f'fill="none" opacity="0.95"/>'
       + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="#d8c584"/>' for x, y in t1)
       + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="#9be6b4"/>' for x, y in t2)
       + '<text x="264" y="288" text-anchor="end" font-family="Helvetica, Arial, sans-serif" '
         'font-size="11" font-weight="600" fill="#d8c584">t&#8320;</text>'
         '<text x="264" y="272" text-anchor="end" font-family="Helvetica, Arial, sans-serif" '
         'font-size="11" font-weight="600" fill="#9be6b4">t&#8321;</text>')
banner(f"{OUT}/05_Monitoring/images/banner_monitoring.svg", "Monitoring Supplement",
       "DETECTING CHANGE &#8226; EQUIVALENT SOIL MASS &#8226; SOIL HEALTH INDICATORS",
       "OPTIONAL SUPPLEMENT", "#f6e7c1", extra=mon, tagfill="#2a2013",
       sky=("#2f2a1d", "#403923"), air=("#403923", "#4b4229", "#564a2d"),
       groundy=250, seed=29, savannah=False)
