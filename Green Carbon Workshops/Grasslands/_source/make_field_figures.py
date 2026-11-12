"""The Part 3 field-methods diagrams.

Seven schematic SVGs, written to Grasslands/03_Field_Methods/images/.

Palette, escaping and the both-themes constraint are shared with the Part 2
figures — see make_planning_figures.py for why the colours are what they are.
Where a figure here covers the same ground as a Part 2 one, the two are
deliberately different: Part 2 shows the DESIGN decision in plan view, Part 3
shows what the crew actually does on the ground.

Run:  python3 make_field_figures.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_planning_figures import C1, C2, C3, C4, INK, FAINT, LINE, svg, txt, esc

OUT = ("/home/user/Terrestrial_Carbon_Workshops_V1/Grasslands/"
       "03_Field_Methods/images")


def write(name, content):
    os.makedirs(OUT, exist_ok=True)
    open(f"{OUT}/{name}", "w", encoding="utf-8").write(content)
    print("  wrote", name)


def arrow_defs(col=LINE, ident="ar"):
    return (f'<defs><marker id="{ident}" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="6" markerHeight="6" orient="auto">'
            f'<path d="M0 0 L10 5 L0 10 z" fill="{col}"/></marker></defs>')


# ═══════════════════════════════════════════════════════════════════════════
# field_workflow_order.svg
# ═══════════════════════════════════════════════════════════════════════════
def workflow_order():
    """The plot diagram only.

    The page already carries the numbered step list in text directly below this
    figure, so repeating it in a legend column would just be the same nine lines
    twice. What the list cannot show is WHERE on the plot each step happens, and
    that is all this figure does.
    """
    b = [arrow_defs()]
    b.append(txt(20, 26, "Where each step happens on the plot", 13.5, INK, weight="600"))
    b.append(txt(20, 44, "Numbers match the sequence below.", 11, FAINT))
    cx, cy = 250, 226
    b.append(f'<circle cx="{cx}" cy="{cy}" r="140" fill="{C3}" opacity="0.07" '
             f'stroke="{C3}" stroke-width="1.6" stroke-dasharray="6 5"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{INK}"/>')
    b.append(txt(cx, cy + 19, "plot centre", 11, INK, anchor="middle"))
    # approach path
    b.append(f'<path d="M24 372 Q 110 356 {cx-92} {cy+92}" stroke="{FAINT}" stroke-width="1.6" '
             f'fill="none" stroke-dasharray="7 5" marker-end="url(#ar)"/>')
    b.append(txt(20, 392, "approach on one path — keep traffic off the plot", 11, FAINT))
    # order of travel
    b.append(f'<path d="M{cx+38} {cy-84} A 94 94 0 1 1 {cx-72} {cy-58}" stroke="{FAINT}" '
             f'stroke-width="1.2" fill="none" stroke-dasharray="3 5" opacity="0.8" '
             f'marker-end="url(#ar)"/>')
    stations = [
        (1, cx,       cy - 106, "mark + GPS",        C3, True),
        (2, cx + 100, cy - 56,  "lay out plots",     C3, False),
        (3, cx + 118, cy + 32,  "photograph",        C3, False),
        (4, cx + 62,  cy + 104, "site + management", C3, False),
        (5, cx - 68,  cy + 100, "trees, shrubs",     C3, False),
        (6, cx - 116, cy + 26,  "clip quadrat",      C2, False),
        (7, cx - 96,  cy - 64,  "core, offset",      C2, True),
    ]
    for n, x, y, lab, col, above in stations:
        b.append(f'<circle cx="{x}" cy="{y}" r="15" fill="{col}" opacity="0.18" '
                 f'stroke="{col}" stroke-width="1.8"/>')
        b.append(txt(x, y + 5, str(n), 13, col, anchor="middle", weight="600"))
        b.append(txt(x, y - 23 if above else y + 32, lab, 11, INK, anchor="middle"))
    # key
    b.append(f'<circle cx="26" cy="414" r="5.5" fill="{C3}" opacity="0.18" '
             f'stroke="{C3}" stroke-width="1.6"/>')
    b.append(txt(39, 418, "non-destructive (1–5)", 11, FAINT))
    b.append(f'<circle cx="196" cy="414" r="5.5" fill="{C2}" opacity="0.18" '
             f'stroke="{C2}" stroke-width="1.6"/>')
    b.append(txt(209, 418, "destructive (6–7)", 11, FAINT))
    b.append(txt(20, 442, "Steps 8 and 9 — sectioning and bagging — happen off the plot.",
                 10.5, FAINT))
    write("field_workflow_order.svg", svg(
        500, 456, "Where each step of the plot visit happens",
        "A plot diagram with seven numbered stations arranged in the order they are worked, "
        "clockwise from marking and GPS at the top: laying out plots, photographing, recording "
        "site conditions, measuring trees and shrubs, then clipping the quadrat and taking an "
        "offset core. The first five are green, the last two orange. The crew approaches on a "
        "single path from outside. Sectioning and bagging happen off the plot.",
        "\n".join(b)))


# ═══════════════════════════════════════════════════════════════════════════
# permanent_vs_single_use_field.svg
# ═══════════════════════════════════════════════════════════════════════════
def perm_field():
    b = [arrow_defs(FAINT)]
    b.append(txt(24, 28, "Where the destructive samples go", 14, INK, weight="600"))
    b.append(txt(24, 46, "Same plot, two designs. The difference is whether the measured "
                         "vegetation has to survive the visit.", 11.5, FAINT))
    fw, fh, y0 = 344, 240, 70
    for k, perm in enumerate((False, True)):
        ox = 24 + k * (fw + 24)
        col = C2 if not perm else C3
        lab = "Single-use" if not perm else "Permanent"
        b.append(f'<rect x="{ox}" y="{y0}" width="{fw}" height="{fh}" rx="5" fill="none" '
                 f'stroke="{LINE}" stroke-width="1"/>')
        b.append(txt(ox + 14, y0 + 24, lab, 13.5, col, weight="600"))
        px, py, half = ox + 110, y0 + 140, 58
        # vegetation area
        b.append(f'<rect x="{px-half}" y="{py-half}" width="{2*half}" height="{2*half}" '
                 f'rx="4" fill="{col}" opacity="0.10" stroke="{col}" stroke-width="2"/>')
        b.append(txt(px, py - half - 12, "vegetation measured here", 10.5, FAINT,
                     anchor="middle"))
        # marker, labelled to its left so nothing stacks above the square
        b.append(f'<circle cx="{px-half}" cy="{py-half}" r="4.5" fill="{col}"/>')
        b.append(txt(px - half - 14, py - half + 3.5, "marker", 10, col, anchor="end"))
        # clip quadrat and core — inside the square, or outside the exclusion line
        qx = px - 26 if not perm else px + 100
        crx = px + 26 if not perm else px + 100
        cry = py + 30 if not perm else py + 34
        b.append(f'<rect x="{qx-14}" y="{py-42}" width="28" height="28" fill="{C1}" '
                 f'opacity="0.28" stroke="{C1}" stroke-width="1.5"/>')
        b.append(txt(qx, py - 50, "clip", 10, C1, anchor="middle"))
        b.append(f'<circle cx="{crx}" cy="{cry}" r="6" fill="{C4}"/>')
        if perm:   # label beside the dot, clear of the traffic arrow coming in below
            b.append(txt(crx + 11, cry + 4, "core", 10, C4))
        else:
            b.append(txt(crx, cry + 20, "core", 10, C4, anchor="middle"))
        if perm:
            b.append(f'<rect x="{px-half-8}" y="{py-half-8}" width="{2*half+16}" '
                     f'height="{2*half+16}" rx="6" fill="none" stroke="{C2}" '
                     f'stroke-width="1.6" stroke-dasharray="5 4"/>')
            # the offset is the gap between the exclusion line and the core
            b.append(f'<path d="M{px+half+8} {cry} H {crx-8}" stroke="{C4}" stroke-width="1.2" '
                     f'stroke-dasharray="3 3"/>')
            b.append(txt((px + half + crx) / 2 + 6, cry - 12, "offset", 10, C4, anchor="middle"))
            traffic = (f'M{ox+14} {y0+fh-28} Q {px} {y0+fh-10} {crx-6} {cry+18}')
            cap = "keep destructive work outside this line"
        else:
            traffic = (f'M{ox+14} {y0+fh-28} Q {px-half-20} {y0+fh-36} {crx-14} {cry+8}')
            cap = "destructive work inside, after the survey"
        b.append(f'<path d="{traffic}" stroke="{FAINT}" stroke-width="1.5" fill="none" '
                 f'stroke-dasharray="6 4" marker-end="url(#ar)"/>')
        b.append(txt(ox + 14, y0 + fh - 12, "crew traffic", 10, FAINT))
        b.append(txt(ox + fw - 14, y0 + fh - 12, cap, 10.5, C2, anchor="end"))
    write("permanent_vs_single_use_field.svg", svg(
        760, 330, "Destructive sampling in permanent and single-use plots",
        "Two field layouts. In the single-use plot the clip quadrat and core sit inside the "
        "vegetation area, taken after the survey. In the permanent plot both sit outside a "
        "marked exclusion line, with the offset recorded, and crew traffic is routed around the "
        "area that will be re-measured.", "\n".join(b)))


# ═══════════════════════════════════════════════════════════════════════════
# photo_series.svg
# ═══════════════════════════════════════════════════════════════════════════
def photo_series():
    import math
    b = [arrow_defs(C1)]
    b.append(txt(24, 28, "The photograph series", 14, INK, weight="600"))
    b.append(txt(24, 46, "One convention, so frames can be compared between plots, crews and "
                         "visits.", 11.5, FAINT))
    cx, cy, R = 214, 192, 84
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{LINE}" '
             f'stroke-width="1" stroke-dasharray="4 4"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{INK}"/>')
    dirs = [("N", 0), ("E", 90), ("S", 180), ("W", 270)]
    frame = 3
    for name, deg in dirs:
        a = math.radians(deg - 90)
        ex, ey = cx + R * math.cos(a), cy + R * math.sin(a)
        b.append(f'<line x1="{cx}" y1="{cy}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{C1}" '
                 f'stroke-width="2" marker-end="url(#ar)"/>')
        lx, ly = cx + (R + 26) * math.cos(a), cy + (R + 26) * math.sin(a)
        b.append(txt(lx, ly + 4, name, 12.5, C1, anchor="middle", weight="600"))
        b.append(txt(lx, ly + 20, f"{frame}–{frame+2}", 10, FAINT, anchor="middle"))
        frame += 3
    # the three angles
    ax = 396
    b.append(txt(ax, 92, "Three frames per direction", 13, INK, weight="600"))
    for i, (lab, dy) in enumerate([("45° up", -22), ("horizontal", 0), ("45° down", 22)]):
        yy = 132 + i * 34
        b.append(f'<line x1="{ax}" y1="{yy}" x2="{ax+56}" y2="{yy+dy}" stroke="{C1}" '
                 f'stroke-width="2" marker-end="url(#ar)"/>')
        b.append(txt(ax + 72, yy + dy * 0.5 + 4, lab, 12, INK))
    # the full frame list, so the numbers on the compass have somewhere to come from
    for i, (dx, s2) in enumerate([(0, "Frames 1–2   straight down, then straight up"),
                                  (0, "Frames 3–14  three per direction, as above"),
                                  (0, "Frames 15–16  the quadrat overhead, before"),
                                  (78, "and after clipping")]):
        b.append(txt(ax + dx, 240 + i * 18, s2, 11.5, INK))
    b.append(txt(ax, 330, "16 frames per plot.", 12, C1, weight="600"))
    # filename convention
    b.append(txt(24, 344, "Every frame carries a board, or a first frame with the same fields:",
                 11.5, FAINT))
    b.append(f'<rect x="24" y="356" width="712" height="30" rx="4" fill="{C1}" opacity="0.08"/>')
    b.append(txt(36, 376, "GRASS-01 · P04 · 2026-07-18 · N-horizontal · frame 03 · initials",
                 12.5, INK))
    b.append(txt(24, 404, "Record the filenames on the plot log and keep the originals — a "
                          "renamed copy loses the camera timestamp.", 11.5, FAINT))
    write("photo_series.svg", svg(
        760, 418, "The plot photograph series",
        "A plot centre with arrows to the four cardinal directions, three frames each at "
        "45 degrees up, horizontal and 45 degrees down, plus one straight down and one straight "
        "up, and two overhead frames of the quadrat before and after clipping. Below, the "
        "filename convention.", "\n".join(b)))


# ═══════════════════════════════════════════════════════════════════════════
# nested_vegetation_plots.svg
# ═══════════════════════════════════════════════════════════════════════════
def nested_veg():
    b = []
    b.append(txt(24, 28, "The nested vegetation plots", 14, INK, weight="600"))
    b.append(txt(24, 46, "Each plot size holds one height class, and each pool is divided by "
                         "ITS OWN area before the pools are combined.", 11.5, FAINT))
    cx, cy = 200, 206
    # plan view — each nested shape named for the class it holds; the areas are
    # given once, on the height ladder, rather than repeated here
    b.append(f'<circle cx="{cx}" cy="{cy}" r="110" fill="{C3}" opacity="0.07" '
             f'stroke="{C3}" stroke-width="2"/>')
    b.append(txt(cx, cy - 120, "trees", 11.5, C3, anchor="middle", weight="600"))
    b.append(f'<rect x="{cx-56}" y="{cy-56}" width="112" height="112" rx="3" fill="{C1}" '
             f'opacity="0.10" stroke="{C1}" stroke-width="2"/>')
    b.append(txt(cx - 48, cy - 42, "shrubs", 11, C1, weight="600"))
    b.append(f'<rect x="{cx-44}" y="{cy+12}" width="32" height="32" fill="{C2}" '
             f'opacity="0.24" stroke="{C2}" stroke-width="2"/>')
    b.append(txt(cx - 62, cy + 32, "ground", 11, C2, anchor="end", weight="600"))
    b.append(f'<circle cx="{cx+44}" cy="{cy+28}" r="6" fill="{C4}"/>')
    b.append(f'<path d="M{cx-8} {cy+28} h42" stroke="{C4}" stroke-width="1.2" '
             f'stroke-dasharray="3 3"/>')
    b.append(txt(cx + 18, cy + 17, "offset", 9.5, C4, anchor="middle"))
    b.append(f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="{INK}"/>')
    b.append(txt(cx, cy + 140, "The core is offset from the quadrat, and the offset is "
                               "recorded.", 11, FAINT, anchor="middle"))
    # height-class column
    x, g = 384, 318
    b.append(f'<line x1="{x}" y1="{g}" x2="{x+340}" y2="{g}" stroke="{LINE}" stroke-width="1.5"/>')
    for h, lab, col, size in [(106, "trees &gt; 2 m", C3, "400 m²"),
                              (60, "shrubs 0.5–2 m", C1, "16–100 m²"),
                              (22, "ground &lt; 0.5 m", C2, "0.25 m²")]:
        b.append(f'<line x1="{x}" y1="{g-h}" x2="{x+340}" y2="{g-h}" stroke="{LINE}" '
                 f'stroke-width="0.8" stroke-dasharray="3 4"/>')
        b.append(f'<text x="{x+4}" y="{g-h-7}" font-size="12" fill="{col}" '
                 f'font-weight="600" font-family="system-ui, sans-serif">{lab}</text>')
        b.append(txt(x + 336, g - h - 7, size, 11, FAINT, anchor="end"))
    b.append(txt(x + 4, g + 18, "ground level — the datum for the clip height", 11, FAINT))
    b.append(txt(x, 92, "Measured in this order", 13, INK, weight="600"))
    for i, s2 in enumerate(["trees — non-destructive",
                            "shrubs — non-destructive",
                            "quadrat — destructive, last"]):
        col = C2 if i == 2 else INK
        b.append(txt(x, 116 + i * 22, f"{i+1}.  {s2}", 12, col,
                     weight="600" if i == 2 else "normal"))
    write("nested_vegetation_plots.svg", svg(
        760, 366, "Nested vegetation plots and height classes",
        "A plan view of the large, medium and small plots nested around the plot centre with a "
        "soil core offset from the quadrat, beside an elevation showing the three height classes "
        "— trees over two metres, shrubs from half a metre to two metres, and ground vegetation "
        "below half a metre — with the plot area used for each.", "\n".join(b)))


# ═══════════════════════════════════════════════════════════════════════════
# core_offset_and_traffic.svg
# ═══════════════════════════════════════════════════════════════════════════
def core_offset():
    b = [arrow_defs(FAINT)]
    b.append(txt(24, 28, "Where the core goes, and where the crew does not", 14, INK, weight="600"))
    b.append(txt(24, 46, "The core has to sample soil nobody knelt on, and miss the quadrat "
                         "another measurement needs.", 11.5, FAINT))
    cx, cy = 250, 190
    b.append(f'<rect x="{cx-140}" y="{cy-110}" width="280" height="220" rx="6" fill="none" '
             f'stroke="{LINE}" stroke-width="1"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="{INK}"/>')
    b.append(txt(cx, cy - 12, "plot centre", 10.5, INK, anchor="middle"))
    # quadrat + kneel zone
    qx, qy = cx - 62, cy - 30
    b.append(f'<circle cx="{qx}" cy="{qy+30}" r="46" fill="{C2}" opacity="0.08"/>')
    b.append(txt(qx, qy + 88, "kneeling / trampled", 10, C2, anchor="middle"))
    b.append(f'<rect x="{qx-22}" y="{qy-22}" width="44" height="44" fill="{C2}" '
             f'opacity="0.26" stroke="{C2}" stroke-width="2"/>')
    b.append(txt(qx, qy - 30, "clipped quadrat", 10.5, C2, anchor="middle"))
    # core
    crx, cry = cx + 68, cy + 34
    b.append(f'<circle cx="{crx}" cy="{cry}" r="7" fill="{C4}"/>')
    b.append(txt(crx, cry + 22, "core", 10.5, C4, anchor="middle"))
    b.append(f'<path d="M{cx+4} {cy+2} L{crx-8} {cry-4}" stroke="{C4}" stroke-width="1.4" '
             f'stroke-dasharray="4 3"/>')
    # annotation parked below the core, where nothing else is drawn
    b.append(txt(cx + 68, cy + 80, "recorded offset", 10, C4, anchor="middle"))
    b.append(txt(cx + 68, cy + 93, "bearing + distance", 9.5, FAINT, anchor="middle"))
    # avoid
    for ax, ay, lab in [(cx - 96, cy + 72, "old core hole"), (cx + 96, cy - 78, "burrow")]:
        b.append(f'<circle cx="{ax}" cy="{ay}" r="9" fill="none" stroke="{FAINT}" '
                 f'stroke-width="1.6" stroke-dasharray="3 3"/>')
        b.append(f'<path d="M{ax-6} {ay-6} l12 12 M{ax+6} {ay-6} l-12 12" stroke="{FAINT}" '
                 f'stroke-width="1.4"/>')
        b.append(txt(ax, ay + 22, lab, 9.5, FAINT, anchor="middle"))
    # traffic
    b.append(f'<path d="M{cx-150} {cy+130} Q {cx-20} {cy+120} {crx-14} {cry+14}" '
             f'stroke="{FAINT}" stroke-width="1.6" fill="none" stroke-dasharray="7 5" '
             f'marker-end="url(#ar)"/>')
    b.append(txt(cx - 148, cy + 148, "approach from the core side, not across the quadrat",
                 10.5, FAINT))
    x = 452
    b.append(txt(x, 92, "Avoid", 13, INK, weight="600"))
    for i, s in enumerate(["the clipped quadrat", "where anyone knelt", "wheel tracks",
                           "burrows and ant nests", "previous core holes"]):
        yy = 112 + i * 24
        b.append(f'<path d="M{x+1} {yy-5} l11 11 M{x+12} {yy-5} l-11 11" stroke="{C2}" '
                 f'stroke-width="1.8" fill="none"/>')
        b.append(txt(x + 22, 116 + i * 24, s, 12, INK))
    b.append(txt(x, 254, "— unless the design deliberately", 11.5, FAINT))
    b.append(txt(x, 271, "targets one of them, in which", 11.5, FAINT))
    b.append(txt(x, 288, "case say so on the sheet.", 11.5, FAINT))
    write("core_offset_and_traffic.svg", svg(
        760, 366, "Core placement and crew traffic",
        "A plot showing the clipped quadrat with its trampled surround, the core placed at a "
        "recorded offset away from it, a burrow and an old core hole marked as places to avoid, "
        "and the crew approach path routed to the core side rather than across the quadrat.",
        "\n".join(b)))


# ═══════════════════════════════════════════════════════════════════════════
# core_sectioning_grassland.svg
# ═══════════════════════════════════════════════════════════════════════════
def sectioning():
    b = [arrow_defs(LINE)]
    b.append(txt(24, 28, "Sectioning the core, and where each fraction goes", 14, INK, weight="600"))
    b.append(txt(24, 46, "Record the depths you actually recovered, not the ones you planned.",
                 11.5, FAINT))
    # the tray
    tx, ty, tw = 40, 106, 300
    b.append(f'<rect x="{tx-14}" y="{ty-42}" width="{tw+28}" height="222" rx="5" fill="none" '
             f'stroke="{LINE}" stroke-width="1"/>')
    b.append(txt(tx, ty - 24, "depth-marked tray — keep the core oriented", 10.5, FAINT))
    b.append(txt(tx, ty - 2, "TOP", 10, C4, weight="600"))
    b.append(txt(tx + tw - 26, ty - 2, "BASE", 10, C4, weight="600"))
    incs = [(0, 10, "0–10"), (10, 20, "10–20"), (20, 30, "20–30"), (30, 60, "30–60"),
            (60, 84, "60–84")]
    total = 84
    for top, bot, lab in incs:
        x0 = tx + tw * top / total
        w = tw * (bot - top) / total
        shade = 0.10 + 0.05 * incs.index((top, bot, lab))
        b.append(f'<rect x="{x0:.1f}" y="{ty+10}" width="{w-2:.1f}" height="44" rx="2" '
                 f'fill="{C4}" opacity="{shade:.2f}" stroke="{C4}" stroke-width="1.2"/>')
        b.append(txt(x0 + w / 2, ty + 70, lab, 10.5, INK, anchor="middle"))
    b.append(txt(tx + tw / 2, ty + 88, "cm below surface", 10, FAINT, anchor="middle"))
    b.append(f'<rect x="{tx + tw*60/total:.1f}" y="{ty+10}" width="{tw*24/total-2:.1f}" '
             f'height="44" rx="2" fill="none" stroke="{C2}" stroke-width="2"/>')
    b.append(txt(tx + tw * 72 / total, ty + 116, "refusal at 84 cm —", 10.5, C2, anchor="middle"))
    b.append(txt(tx + tw * 72 / total, ty + 130, "record 84, never 100", 10.5, C2, anchor="middle"))
    b.append(txt(tx, ty + 160, "Clean the blade and tray between every interval.", 10.5, FAINT))
    # routing
    sx = 392
    b.append(txt(sx, 92, "One interval, four destinations", 13, INK, weight="600"))
    dests = [("soil carbon", C1), ("bulk density", C4), ("roots", C3), ("archive", FAINT)]
    for i, (lab, col) in enumerate(dests):
        yy = 126 + i * 40
        b.append(f'<rect x="{sx+58}" y="{yy-16}" width="150" height="28" rx="4" fill="{col}" '
                 f'opacity="0.14" stroke="{col}" stroke-width="1.4"/>')
        b.append(txt(sx + 133, yy + 3, lab, 11.5, INK, anchor="middle"))
        b.append(f'<path d="M{sx+30} {192} Q {sx+44} {yy} {sx+56} {yy-2}" stroke="{LINE}" '
                 f'stroke-width="1.4" fill="none" marker-end="url(#ar)"/>')
    b.append(f'<rect x="{sx-6}" y="176" width="36" height="32" rx="3" fill="{C4}" '
             f'opacity="0.22" stroke="{C4}" stroke-width="1.6"/>')
    b.append(txt(sx + 12, 222, "10–20 cm", 10, INK, anchor="middle"))
    b.append(txt(sx, 300, "The same material cannot serve every destructive", 11.5, FAINT))
    b.append(txt(sx, 317, "analysis. Agree the split and the minimum masses", 11.5, FAINT))
    b.append(txt(sx, 334, "with the laboratory before the field day.", 11.5, FAINT))
    write("core_sectioning_grassland.svg", svg(
        760, 356, "Sectioning the core and routing the fractions",
        "An oriented core laid on a depth-marked tray with five increments from 0 to 84 "
        "centimetres, the deepest one ending at refusal and marked to be recorded as 84 rather "
        "than the planned 100. Beside it, one interval routed to four destinations: soil carbon, "
        "bulk density, roots and archive.", "\n".join(b)))


# ═══════════════════════════════════════════════════════════════════════════
# root_processing_workflow.svg
# ═══════════════════════════════════════════════════════════════════════════
def root_workflow():
    b = [arrow_defs(LINE)]
    b.append(txt(24, 28, "Root separation — the draft sequence", 14, INK, weight="600"))
    b.append(txt(24, 46, "Each step has a record attached to it. The soil stream and the root "
                         "stream must never merge again.", 11.5, FAINT))
    steps = [("field-moist\nsubsample", "mass + ID"),
             ("soak /\ndisaggregate", "solution, time"),
             ("nested\nsieves", "every mesh"),
             ("sort roots\nfrom debris", "rule, operator"),
             ("diameter\nclasses", "boundary"),
             ("dry to\nconstant mass", "temp, criterion"),
             ("weigh", "balance ID"),
             ("ash\ncorrection", "subsample, ash")]
    x0, y0, bw, gap = 28, 100, 78, 12
    for i, (lab, rec) in enumerate(steps):
        x = x0 + i * (bw + gap)
        b.append(f'<rect x="{x}" y="{y0}" width="{bw}" height="60" rx="5" fill="{C3}" '
                 f'opacity="0.12" stroke="{C3}" stroke-width="1.5"/>')
        for j, line in enumerate(lab.split("\n")):
            b.append(txt(x + bw / 2, y0 + 26 + j * 14, line, 10.5, INK, anchor="middle"))
        b.append(txt(x + bw / 2, y0 - 8, rec, 9.5, FAINT, anchor="middle"))
        if i < len(steps) - 1:
            b.append(f'<path d="M{x+bw+1} {y0+30} h{gap-4}" stroke="{LINE}" stroke-width="1.6" '
                     f'marker-end="url(#ar)"/>')
    # the two streams. The soil residue leaves at the sieve; the roots carry on
    # through the remaining steps, so the two connectors start in different places.
    sy = 214
    sieve_x = x0 + 2 * (bw + gap) + bw / 2
    last_x = x0 + 7 * (bw + gap) + bw / 2
    b.append(f'<path d="M{sieve_x} {y0+60} V 186 H {x0+150} V {sy-4}" stroke="{C4}" '
             f'stroke-width="1.6" fill="none" marker-end="url(#ar)"/>')
    b.append(f'<path d="M{last_x} {y0+60} V 186 H {x0+486} V {sy-4}" stroke="{C3}" '
             f'stroke-width="1.6" fill="none" marker-end="url(#ar)"/>')
    b.append(f'<rect x="{x0}" y="{sy}" width="300" height="52" rx="5" fill="{C4}" '
             f'opacity="0.12" stroke="{C4}" stroke-width="1.5"/>')
    b.append(txt(x0 + 14, sy + 22, "SOIL stream — root-free residue", 12, INK, weight="600"))
    b.append(txt(x0 + 14, sy + 40, "to soil carbon, under the agreed boundary", 10.5, FAINT))
    b.append(f'<rect x="{x0+336}" y="{sy}" width="300" height="52" rx="5" fill="{C3}" '
             f'opacity="0.12" stroke="{C3}" stroke-width="1.5"/>')
    b.append(txt(x0 + 350, sy + 22, "ROOT stream — by class and depth", 12, INK, weight="600"))
    b.append(txt(x0 + 350, sy + 40, "to 3. Root Biomass", 10.5, FAINT))
    b.append(f'<path d="M{x0+300} {sy+26} h30" stroke="{C2}" stroke-width="2" '
             f'stroke-dasharray="4 4"/>')
    b.append(txt(x0 + 318, sy + 16, "✕", 13, C2, anchor="middle"))
    b.append(txt(x0 + 318, sy + 72, "never recombined", 10, C2, anchor="middle"))
    # the caveat
    b.append(f'<rect x="24" y="306" width="712" height="66" rx="5" fill="{C2}" opacity="0.10" '
             f'stroke="{C2}" stroke-width="1.4"/>')
    b.append(txt(40, 328, "DRAFT — not a validated SOP.", 12.5, C2, weight="600"))
    b.append(txt(40, 346, "Mesh sizes, diameter boundary, live/dead rule, drying temperature "
                          "and the ash method all need a", 11, INK))
    b.append(txt(40, 362, "specialist review and primary references before field use.",
                 11, INK))
    write("root_processing_workflow.svg", svg(
        760, 388, "Root separation workflow (draft)",
        "An eight-step sequence from field-moist subsample through soaking, nested sieves, "
        "sorting, diameter classes, drying, weighing and ash correction, each with the record it "
        "requires. It splits into a soil stream and a root stream which are marked as never "
        "recombined, and carries a banner stating that this is a draft rather than a validated "
        "standard operating procedure.", "\n".join(b)))


if __name__ == "__main__":
    print("Part 3 figures →", OUT)
    workflow_order()
    perm_field()
    photo_series()
    nested_veg()
    core_offset()
    sectioning()
    root_workflow()
