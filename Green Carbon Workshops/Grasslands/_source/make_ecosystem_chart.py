"""Grassland carbon in national context, for Part 1.

Writes Grasslands/01_Background/images/ecosystem_carbon_comparison.svg.

National values are from Sothe et al. (2022), Large soil carbon storage in
terrestrial ecosystems of Canada, Global Biogeochemical Cycles 36,
e2021GB007213, Table 1 and Section 3.2. They are modelled 250 m means of
ORGANIC carbon. The worked-example values are read from the workbook through
make_pool_chart.load_pools(), so they cannot drift from the data.

Design notes:
  - Sothe et al. give no grassland-specific figure. The one like-for-like
    comparison the paper supports is soil to 30 cm: its national 0-30 cm
    mean against the worked example's 0-30 cm soil. Every other bar is
    labelled with its own pool and depth, and the bars are GROUPED by
    what is measured and to what depth, so a reader never has to guess
    whether two bars are on the same basis.
  - One unit (kg C per m2) and one axis. Values span 0.97 to 109, so the
    grassland plant bar is a sliver; that is the finding, not a flaw, and
    every bar is direct-labelled. A log axis would hide it.
  - Two series, two hues, validated as a pair against both surfaces with
    the dataviz validator: #4A78B5 for the paper, #6E8B3D (the pool
    chart's colour) for the worked example. Identity is also carried by a
    legend and by the label text, so it never rests on colour alone.
  - Text stays in ink, never the series colour. No hover: GitHub strips
    scripts from SVG, and the page carries the numbers as a table.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_pool_chart import load_pools, INK, FAINT

GRASS = "/home/user/Terrestrial_Carbon_Workshops_V1/Grasslands"
OUT = f"{GRASS}/01_Background/images/ecosystem_carbon_comparison.svg"

PAPER = "#4A78B5"      # Sothe et al. (2022)
EXAMPLE = "#6E8B3D"    # this workshop's worked example

# Sothe et al. (2022), Table 1 means, kg C/m2
FOREST_AGB, FOREST_BGB, FOREST_DPM = 4.13, 1.28, 0.78
SOIL_30_CANADA = 13.2
SOIL_100_CANADA = 36.4
SOIL_100_PEAT = 81.0
SOIL_100_HUDSON = 109.0     # Hudson Plains ecozone, Section 3.2

pools = dict(load_pools())
soil30 = pools["Soil, 0–30 cm"]
plants = pools["Roots, 0–30 cm"] + pools["Shoots"]

GROUPS = [
    ("Plant carbon", [
        ("Forests: trees, roots, dead wood", FOREST_AGB + FOREST_BGB + FOREST_DPM, PAPER),
        ("Grassland: roots to 30 cm, shoots", plants, EXAMPLE),
    ]),
    ("Soil organic carbon, 0–30 cm", [
        ("Canada, national mean", SOIL_30_CANADA, PAPER),
        ("Grassland, worked example", soil30, EXAMPLE),
    ]),
    ("Soil organic carbon, 0–1 m", [
        ("Canada, national mean", SOIL_100_CANADA, PAPER),
        ("Peatlands", SOIL_100_PEAT, PAPER),
        ("Hudson Plains ecozone", SOIL_100_HUDSON, PAPER),
    ]),
]

W = 760
X0, MAXW = 250, 430
BARH, GAP, HEAD = 22, 8, 30
vmax = max(v for _, rows in GROUPS for _, v, _ in rows)
k = MAXW / vmax


def fmt(v):
    """No more precision than the source gives: the paper reports 81 and 109."""
    return f"{v:.0f}" if v >= 50 else f"{v:.1f}"


def bar(x, y, w, h, fill):
    """Square at the baseline, 4px rounded at the data end."""
    if w < 2:
        return f'<rect x="{x}" y="{y}" width="2" height="{h}" fill="{fill}"/>'
    r = min(4.0, w / 2)
    return (f'<path d="M{x:.1f} {y:.1f} H{x + w - r:.1f} A{r} {r} 0 0 1 {x + w:.1f} '
            f'{y + r:.1f} V{y + h - r:.1f} A{r} {r} 0 0 1 {x + w - r:.1f} {y + h:.1f} '
            f'H{x:.1f} Z" fill="{fill}"/>')


body, y = [], 78
for head, rows in GROUPS:
    body.append(f'<text x="0" y="{y + 14}" font-size="13" font-weight="600" '
                f'fill="{INK}">{head}</text>')
    y += HEAD
    for label, v, col in rows:
        body.append(f'<text x="{X0 - 12}" y="{y + BARH / 2 + 4.5:.1f}" font-size="13" '
                    f'text-anchor="end" fill="{INK}">{label}</text>')
        body.append(bar(X0, y, v * k, BARH, col))
        body.append(f'<text x="{X0 + max(v * k, 2) + 8:.1f}" y="{y + BARH / 2 + 4.5:.1f}" '
                    f'font-size="13" font-weight="600" fill="{INK}">{fmt(v)}</text>')
        y += BARH + GAP
    y += 10
H = y + 30

desc = ("Horizontal bar chart of carbon per square metre. Plant carbon: forest trees, roots "
        "and dead wood, national mean, "
        f"{FOREST_AGB + FOREST_BGB + FOREST_DPM:.1f}; grassland roots to 30 cm and shoots, worked "
        f"example, {plants:.1f}. "
        f"Soil organic carbon to 30 cm: Canada {SOIL_30_CANADA}; grassland worked example "
        f"{soil30:.1f}. Soil organic carbon to 1 m: Canada {SOIL_100_CANADA}, peatlands "
        f"{SOIL_100_PEAT:.0f}, Hudson Plains ecozone {SOIL_100_HUDSON:.0f}. National values "
        "from Sothe et al. 2022; grassland values are constructed teaching data.")

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
       f'viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d" '
       f'font-family="Helvetica, Arial, sans-serif">',
       '<title id="t">Grassland carbon in national context</title>',
       f'<desc id="d">{desc}</desc>',
       f'<text x="0" y="20" font-size="15" font-weight="600" fill="{INK}">'
       f'Grassland carbon in national context</text>',
       f'<text x="0" y="38" font-size="12.5" fill="{FAINT}">kg C per m² · grouped by what is '
       f'measured and to what depth</text>',
       # legend: a swatch plus a word for each series
       f'<rect x="0" y="50" width="12" height="12" rx="2" fill="{PAPER}"/>',
       f'<text x="18" y="60" font-size="12.5" fill="{INK}">Sothe et al. (2022), modelled '
       f'national means</text>',
       f'<rect x="300" y="50" width="12" height="12" rx="2" fill="{EXAMPLE}"/>',
       f'<text x="318" y="60" font-size="12.5" fill="{INK}">This workshop\'s worked example '
       f'(constructed data)</text>',
       *body,
       f'<text x="0" y="{H - 10}" font-size="12" fill="{FAINT}">The paper reports no '
       f'grassland-specific value; soil to 30 cm is the only like-for-like pair.</text>',
       "</svg>"]
open(OUT, "w", encoding="utf-8").write("\n".join(svg))
print("wrote", OUT)
for head, rows in GROUPS:
    print(" ", head)
    for label, v, _ in rows:
        print(f"    {label:<28} {v:7.2f}")
