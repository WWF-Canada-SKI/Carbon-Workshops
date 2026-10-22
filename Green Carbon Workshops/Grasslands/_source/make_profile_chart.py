"""Depth profile of soil and root carbon, for Part 1's "how deep" section.

Answers the placeholder "a full soil profile beside a 30 cm core, showing
carbon and roots below the conventional reporting depth" with the workshop's
own worked-example data rather than a drawing, so the figure cannot claim
more than the data do. Writes
Grasslands/01_Background/images/soil_profile_vs_30cm.svg.

What it uses, and why:
  - The PRAIRIE plots (S1, S2) only, as in carbon_pools.svg. Of those six,
    UP-03 hit refusal at 30 cm, so the profile is the mean of the FIVE plots
    cored to 60 cm. Mixing a 30 cm plot into the 30-60 cm mean would dilute
    the deep increment with a zero that is not a measurement.
  - Each increment is drawn at its TRUE thickness, and bar length is carbon
    per 10 cm of depth. So each bar's AREA is the stock in that increment,
    and the 30 cm thick bottom increment is not visually inflated by its
    thickness alone.
  - Soil and roots differ by ~10x, so they are two panels with their own
    x-scales (small multiples), never one chart with two axes.
  - One hue, the same as carbon_pools.svg, validated against both surfaces.
    Whether carbon is inside or below a 30 cm core is shown by position and
    a labelled band, not by a second colour.
  - No hover layer: GitHub strips scripts from SVG. Every bar is direct-
    labelled, and the page carries the numbers as a table.
"""
import os, statistics, openpyxl

GRASS = "/home/user/Terrestrial_Carbon_Workshops_V1/Grasslands"
WB = f"{GRASS}/Worked_Example/Grassland_Carbon_Calculator_WorkedExample.xlsx"
OUT = f"{GRASS}/01_Background/images/soil_profile_vs_30cm.svg"

BAR = "#6E8B3D"
INK = "#7a7a7a"
FAINT = "#9a9a9a"
BAND = "#9a9a9a"
CUT = 30
INCS = [(0, 10), (10, 20), (20, 30), (30, 60)]

wb = openpyxl.load_workbook(WB, data_only=True)
ps, sd, rt = wb["5. Plot Summary"], wb["2. Soil Data"], wb["3. Root Biomass"]

prairie = [ps.cell(r, 1).value for r in range(5, 20)
           if ps.cell(r, 2).value in ("S1", "S2")]
soil = {p: {} for p in prairie}
root = {p: {i: 0.0 for i in INCS} for p in prairie}
for r in range(5, 700):
    p = sd.cell(r, 1).value
    if p in soil and isinstance(sd.cell(r, 16).value, (int, float)):
        soil[p][(sd.cell(r, 4).value, sd.cell(r, 5).value)] = sd.cell(r, 16).value
for r in range(5, 1000):
    p = rt.cell(r, 1).value
    if p in root and isinstance(rt.cell(r, 14).value, (int, float)):
        key = (rt.cell(r, 3).value, rt.cell(r, 4).value)
        if key not in root[p]:
            raise SystemExit(f"{p}: unexpected root increment {key}")
        root[p][key] += rt.cell(r, 14).value

full = [p for p in prairie if all(i in soil[p] for i in INCS)]
short = [p for p in prairie if p not in full]
if len(full) != 5:
    raise SystemExit(f"expected 5 prairie plots cored to 60 cm, found {full}")


def mean_profile(d):
    return [statistics.mean(d[p][i] for p in full) for i in INCS]


S, R = mean_profile(soil), mean_profile(root)
share = lambda v: 100 * v[3] / sum(v)

# ── geometry ────────────────────────────────────────────────────────────────
W, H = 760, 470
TOP = 96                        # y of 0 cm
PXCM = 4.6                      # px per cm of depth
yd = lambda d: TOP + d * PXCM
PANELS = [("Soil carbon", S, 58, 250), ("Root carbon", R, 432, 250)]


def bar(x, y, w, h):
    """Square at the axis, 4px rounded at the data end."""
    r = min(4.0, w / 2, h / 2)
    return (f'<path d="M{x:.1f} {y:.1f} H{x + w - r:.1f} A{r} {r} 0 0 1 {x + w:.1f} '
            f'{y + r:.1f} V{y + h - r:.1f} A{r} {r} 0 0 1 {x + w - r:.1f} {y + h:.1f} '
            f'H{x:.1f} Z" fill="{BAR}"/>')


o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
     f'viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d" '
     f'font-family="Helvetica, Arial, sans-serif">',
     '<title id="t">What a 30 cm core leaves behind</title>',
     f'<desc id="d">Two depth profiles, soil carbon and root carbon, averaged over five '
     f'prairie plots cored to 60 centimetres. Each increment is drawn at its true thickness '
     f'with bar length equal to carbon per 10 centimetres of depth. Below 30 centimetres lie '
     f'{share(S):.0f} per cent of the soil carbon and {share(R):.0f} per cent of the root '
     f'carbon in the 0 to 60 centimetre profile. Roots were still present at 60 centimetres, '
     f'so the true totals are larger.</desc>',
     f'<text x="0" y="20" font-size="15" font-weight="600" fill="{INK}">'
     f'What a 30 cm core leaves behind</text>',
     f'<text x="0" y="38" font-size="12.5" fill="{FAINT}">Mean of five prairie plots cored '
     f'to 60 cm · bar length = kg C per m² per 10 cm of depth · area = stock</text>']

# band below the reporting depth, shared by both panels
o.append(f'<rect x="0" y="{yd(CUT):.1f}" width="{W}" height="{yd(60) - yd(CUT):.1f}" '
         f'fill="{BAND}" opacity="0.10"/>')
o.append(f'<line x1="0" y1="{yd(CUT):.1f}" x2="{W}" y2="{yd(CUT):.1f}" stroke="{INK}" '
         f'stroke-width="1.5" stroke-dasharray="6 4"/>')
o.append(f'<text x="{W}" y="{yd(CUT) - 7:.1f}" font-size="12" text-anchor="end" '
         f'fill="{INK}">a 30 cm core stops here</text>')

for name, vals, x0, maxw in PANELS:
    per10 = [v / ((b - a) / 10) for v, (a, b) in zip(vals, INCS)]
    k = maxw / max(per10)
    o.append(f'<text x="{x0}" y="{TOP - 16}" font-size="13.5" font-weight="600" '
             f'fill="{INK}">{name}</text>')
    o.append(f'<line x1="{x0}" y1="{TOP}" x2="{x0}" y2="{yd(60):.1f}" stroke="{FAINT}" '
             f'stroke-width="1"/>')
    for v, p10, (a, b) in zip(vals, per10, INCS):
        y, h = yd(a) + 1, (b - a) * PXCM - 2          # 2px surface gap between fills
        o.append(bar(x0, y, p10 * k, h))
        # the label states what the LENGTH encodes; increment stocks, which the
        # area encodes, are totalled in the summary lines under each panel
        o.append(f'<text x="{x0 + p10 * k + 8:.1f}" y="{y + min(h, 40) / 2 + 4.5:.1f}" '
                 f'font-size="12" fill="{INK}">{p10:.2f}</text>')
    lo, hi = sum(vals[:3]), vals[3]
    o.append(f'<text x="{x0}" y="{yd(60) + 24:.1f}" font-size="12.5" fill="{INK}">'
             f'0–30 cm <tspan font-weight="600">{lo:.2f}</tspan> · 30–60 cm '
             f'<tspan font-weight="600">{hi:.2f}</tspan> kg C/m²</text>')
    o.append(f'<text x="{x0}" y="{yd(60) + 42:.1f}" font-size="12.5" fill="{INK}">'
             f'<tspan font-weight="600">{100 * hi / (lo + hi):.0f}%</tspan> of the 0–60 cm '
             f'total is below 30 cm</text>')

# depth ticks, left of the soil panel
for d in (0, 10, 20, 30, 60):
    o.append(f'<text x="{PANELS[0][2] - 8}" y="{yd(d) + 4:.1f}" font-size="11" '
             f'text-anchor="end" fill="{FAINT}">{d}</text>')
o.append(f'<text x="0" y="{TOP - 16}" font-size="11" fill="{FAINT}">cm</text>')

o.append(f'<text x="0" y="{H - 26}" font-size="12" fill="{FAINT}">Roots were still present '
         f'at 60 cm, so even the 0–60 cm figure is a minimum. {", ".join(short)} hit refusal '
         f'at 30 cm and is not in this mean.</text>')
o.append(f'<text x="0" y="{H - 8}" font-size="12" fill="{FAINT}">Constructed teaching data '
         f'from the Worked Example — not a regional value.</text>')
o.append("</svg>")

open(OUT, "w", encoding="utf-8").write("\n".join(o))
print("wrote", OUT)
for lab, v in (("soil", S), ("roots", R)):
    print(f"  {lab:<6}", " ".join(f"{x:.3f}" for x in v),
          f"| 0-30 {sum(v[:3]):.3f}  30-60 {v[3]:.3f}  below-30 share {share(v):.1f}%")
