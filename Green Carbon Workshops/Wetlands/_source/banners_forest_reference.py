import os, random
OUT = "/home/user/Terrestrial_Carbon_Workshops_V1/Forests"

DEFS = """<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{sky0}"/><stop offset="100%" stop-color="{sky1}"/>
  </linearGradient>
  <linearGradient id="air" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{air0}"/><stop offset="55%" stop-color="{air1}"/><stop offset="100%" stop-color="{air2}"/>
  </linearGradient>
  <linearGradient id="soil" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#6b5436"/><stop offset="30%" stop-color="#5a4429"/>
    <stop offset="70%" stop-color="#3d2c1a"/><stop offset="100%" stop-color="#241a0f"/>
  </linearGradient>
</defs>"""

def conifer(x, base, h, w, fill, op):
    """Layered conifer silhouette."""
    parts = []
    tiers = 4
    for i in range(tiers):
        f = i / (tiers - 1)
        cy = base - h * (0.18 + 0.72 * f)
        hw = w * (1 - 0.68 * f)
        th = h * 0.30
        parts.append(f'<path d="M{x - hw:.0f} {cy:.0f} L{x:.0f} {cy - th:.0f} L{x + hw:.0f} {cy:.0f} Z" fill="{fill}" opacity="{op}"/>')
    parts.append(f'<rect x="{x - 3:.0f}" y="{base - h * 0.20:.0f}" width="6" height="{h * 0.20:.0f}" fill="#4a3728" opacity="{op}"/>')
    return "".join(parts)

def broadleaf(x, base, h, w, fill, op):
    r = w * 0.55
    cy = base - h * 0.68
    return (f'<rect x="{x - 3:.0f}" y="{cy:.0f}" width="6" height="{base - cy:.0f}" fill="#4a3728" opacity="{op}"/>'
            f'<ellipse cx="{x:.0f}" cy="{cy:.0f}" rx="{r:.0f}" ry="{r * 0.82:.0f}" fill="{fill}" opacity="{op}"/>'
            f'<ellipse cx="{x - r * 0.45:.0f}" cy="{cy + r * 0.22:.0f}" rx="{r * 0.55:.0f}" ry="{r * 0.48:.0f}" fill="{fill}" opacity="{op}"/>'
            f'<ellipse cx="{x + r * 0.45:.0f}" cy="{cy + r * 0.18:.0f}" rx="{r * 0.52:.0f}" ry="{r * 0.45:.0f}" fill="{fill}" opacity="{op}"/>')

def banner(path, title, subtitle, tag, tagfill, tagtext, accent, extra="",
           sky=("#d3e6f4", "#9dc5de"), air=("#a9cfe4", "#7fb4d0", "#5e97b8"),
           groundy=268, seed=7):
    random.seed(seed)
    GREENS = ["#1b4332", "#2d6a4f", "#40916c", "#276749"]
    trees = []
    # far ridge
    for x in range(20, 1200, 46):
        h = random.randint(70, 105)
        trees.append(conifer(x, groundy, h, 22, "#20503c", 0.40))
    # mid band, skipping the centre so the title stays legible
    for x in range(10, 1200, 62):
        if 300 < x < 900:
            continue
        h = random.randint(105, 165)
        g = GREENS[random.randrange(len(GREENS))]
        if random.random() < 0.3:
            trees.append(broadleaf(x, groundy, h, 46, g, 0.88))
        else:
            trees.append(conifer(x, groundy, h, 30, g, 0.9))
    horizons = "".join(
        f'<line x1="0" y1="{y}" x2="1200" y2="{y}"/>' for y in range(groundy + 16, 360, 17))
    svg = f"""<svg width="1200" height="360" viewBox="0 0 1200 360" xmlns="http://www.w3.org/2000/svg" role="img">
<title>{title} — Forest Carbon Workshop</title>
<desc>Illustration of a Canadian forest stand above a layered soil profile, headed "{title}".</desc>
{DEFS.format(sky0=sky[0], sky1=sky[1], air0=air[0], air1=air[1], air2=air[2])}
<rect x="0" y="0" width="1200" height="96" fill="url(#sky)"/>
<rect x="0" y="96" width="1200" height="{groundy - 96}" fill="url(#air)"/>
<rect x="0" y="{groundy}" width="1200" height="{360 - groundy}" fill="url(#soil)"/>
<circle cx="1046" cy="52" r="25" fill="#fff4d6" opacity="0.85"/>
<g opacity="0.22" stroke="#ffffff" stroke-width="2" fill="none" stroke-linecap="round">
  <path d="M0 54 Q 60 40 120 54 T 240 54 T 360 54"/>
  <path d="M690 36 Q 750 22 810 36 T 930 36"/>
</g>
{"".join(trees)}
<g stroke="#1d140b" stroke-width="1" opacity="0.33">{horizons}</g>
{extra}
<rect x="40" y="28" width="{max(168, 11 * len(tagtext) + 44)}" height="32" rx="16" fill="{tagfill}" opacity="0.6"/>
<text x="{40 + max(168, 11 * len(tagtext) + 44) / 2:.0f}" y="49" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="600" letter-spacing="1" fill="#eaf7ef">{tagtext}</text>
<text x="600" y="190" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="46" font-weight="600" fill="#ffffff">{title}</text>
<text x="600" y="224" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="17" letter-spacing="1" fill="{accent}">{subtitle}</text>
</svg>
"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(svg)
    print("wrote", path.replace(OUT, "Forests"), len(svg), "bytes")

DARK = "#12331f"
PALE = "#dff0e4"

# Landing banner — no section tag, wider subtitle
banner(f"{OUT}/01_Background/images/banner_forest.svg",
       "Forest Carbon Workshop",
       "TREES &#8226; SOILS &#8226; UNDERSTORY &#8226; FROM PLANNING TO CARBON STOCK",
       None, DARK, "WWF-CANADA CARBON MEASUREMENT", PALE, seed=3)

banner(f"{OUT}/01_Background/images/banner_background.svg",
       "Background",
       "WHAT FOREST CARBON IS &#8226; WHICH POOLS MATTER &#8226; KEY REFERENCES",
       None, DARK, "SECTION 1 OF 4", PALE, seed=11)

# Planning — add plot-grid overlay
grid = ('<g opacity="0.5" stroke="#ffd166" stroke-width="2" fill="none">'
        '<rect x="150" y="292" width="80" height="46"/><rect x="960" y="292" width="80" height="46"/>'
        '<circle cx="1080" cy="315" r="24"/></g>'
        '<g fill="#ffd166" opacity="0.85">'
        + "".join(f'<circle cx="{x}" cy="{y}" r="4"/>' for x, y in
                  [(170, 305), (210, 325), (190, 315), (980, 305), (1020, 325), (1000, 312)]) + '</g>')
banner(f"{OUT}/02_Project_Planning/images/banner_planning.svg",
       "Project Planning",
       "HOW MANY PLOTS &#8226; WHERE THEY GO &#8226; WHICH POOLS TO MEASURE",
       None, DARK, "SECTION 2 OF 4", PALE, extra=grid, seed=5)

# Field methods — DBH tape on a trunk + soil core
field = ('<g opacity="0.95">'
         '<rect x="222" y="150" width="16" height="188" rx="3" fill="#e8e2d5" stroke="#8a836f" stroke-width="1.5"/>'
         '<rect x="222" y="268" width="16" height="70" fill="#3d2c1a" opacity="0.92"/>'
         '<rect x="222" y="150" width="16" height="18" fill="#c9c2b0"/></g>'
         '<g stroke="#ffd166" stroke-width="3" fill="none" opacity="0.9">'
         '<ellipse cx="985" cy="214" rx="26" ry="8"/></g>'
         '<text x="985" y="196" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" '
         'font-size="12" font-weight="600" fill="#ffd166">DBH 1.3 m</text>')
banner(f"{OUT}/03_Field_Methods/images/banner_field_methods.svg",
       "Field Methods",
       "MEASURING TREES &#8226; SAMPLING SOIL &#8226; SURVEYING UNDERSTORY",
       None, DARK, "SECTION 3 OF 4", PALE, extra=field, seed=17)

# Data interpretation — rising bar chart
bars = '<g opacity="0.9">' + "".join(
    f'<rect x="{150 + i * 26}" y="{330 - h}" width="18" height="{h}" rx="2" fill="#ffd166" opacity="{0.55 + i * 0.09:.2f}"/>'
    for i, h in enumerate([18, 30, 44, 58, 76])) + '</g>'
bars += ('<g opacity="0.9">' + "".join(
    f'<rect x="{940 + i * 26}" y="{330 - h}" width="18" height="{h}" rx="2" fill="#9be6b4" opacity="{0.5 + i * 0.1:.2f}"/>'
    for i, h in enumerate([22, 38, 52, 70])) + '</g>')
banner(f"{OUT}/04_Data_Interpretation/images/banner_data_interpretation.svg",
       "Data Interpretation",
       "LAB RESULTS &#8226; CARBON CALCULATORS &#8226; SCALING AND REPORTING",
       None, DARK, "SECTION 4 OF 4", PALE, extra=bars, seed=23)

# LiDAR supplement — scan lines / point cloud
random.seed(41)
pts = "".join(
    f'<circle cx="{random.randint(20, 1180)}" cy="{random.randint(110, 262)}" r="{random.choice([1, 1, 2])}" fill="#7ee3ff" opacity="{random.uniform(0.3, 0.85):.2f}"/>'
    for _ in range(320))
beams = '<g stroke="#7ee3ff" stroke-width="1.5" opacity="0.35">' + "".join(
    f'<line x1="600" y1="18" x2="{x}" y2="266"/>' for x in range(120, 1120, 96)) + '</g>'
banner(f"{OUT}/05_LiDAR_Supplement/banner_lidar.svg",
       "LiDAR Supplement",
       "CANOPY STRUCTURE &#8226; AREA-BASED APPROACH &#8226; WALL-TO-WALL CARBON",
       None, "#0b2b3a", "OPTIONAL SUPPLEMENT", "#cdf0fb",
       extra=beams + pts, sky=("#0e2d3d", "#123b4f"), air=("#123b4f", "#0f3244", "#0a2331"), seed=29)
