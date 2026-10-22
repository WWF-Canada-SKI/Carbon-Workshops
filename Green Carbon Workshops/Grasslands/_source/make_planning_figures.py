"""The Part 2 planning diagrams.

Seven schematic SVGs, written to Grasslands/02_Project_Planning/images/.

One file has to read on both GitHub themes, so every figure uses a transparent
background, the muted ink `#898781` that the dataviz reference palette uses in
both light and dark mode, and a categorical set validated against BOTH the light
and the dark surface:

    node scripts/validate_palette.js "#3987e5,#d95926,#199e70,#c98500" --mode light
    node scripts/validate_palette.js "#3987e5,#d95926,#199e70,#c98500" --mode dark

Both pass all six checks. Every category is also directly labelled, so identity
never rests on colour alone.

The figures are deliberately bare: the drawing and its identifying labels
only. Titles, notes and explanation live in the page text under each figure,
where they can be edited without regenerating anything.

Run:  python3 make_planning_figures.py
"""
import os, math, random

OUT = ("/home/user/Terrestrial_Carbon_Workshops_V1/Grasslands/"
       "02_Project_Planning/images")

C1, C2, C3, C4 = "#3987e5", "#d95926", "#199e70", "#c98500"
INK = "#898781"          # muted ink, identical in both modes
FAINT = "#a5a49e"
LINE = "#b9b8b1"
FONT = 'font-family="Helvetica, Arial, sans-serif"'


def svg(w, h, title, desc, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d" {FONT}>\n'
            f'<title id="t">{esc(title)}</title>\n<desc id="d">{esc(desc)}</desc>\n'
            f'{body}\n</svg>\n')


def esc(s):
    """XML-escape text content. '<' in labels like 'veg < 0.5 m' is otherwise
    an unclosed tag, and the whole file fails to parse."""
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def txt(x, y, s, size=13, fill=INK, anchor="start", weight="normal"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}">{esc(s)}</text>')


def write(name, content):
    os.makedirs(OUT, exist_ok=True)
    open(f"{OUT}/{name}", "w", encoding="utf-8").write(content)
    print("  wrote", name)


# ═══════════════════════════════════════════════════════════════════════════
# sampling_explainer.svg — why a sample stands in for the whole
# ═══════════════════════════════════════════════════════════════════════════
def sampling_explainer():
    b = []
    gx, gy, cell, n = 20, 20, 26, 13
    # the true surface: a carbon field, shown as a faint value grid
    for i in range(n):
        for j in range(8):
            v = 0.32 + 0.5 * math.exp(-((i - 4) ** 2 + (j - 3) ** 2) / 26) \
                     + 0.28 * math.exp(-((i - 10) ** 2 + (j - 5) ** 2) / 16)
            b.append(f'<rect x="{gx+i*cell}" y="{gy+j*cell}" width="{cell-2}" '
                     f'height="{cell-2}" rx="2" fill="{C3}" opacity="{0.10+0.55*min(v,1):.2f}"/>')
    # the sample
    for i, j in [(1, 1), (4, 5), (7, 2), (10, 6), (3, 3), (11, 3), (6, 6), (9, 0)]:
        cx, cy = gx + i * cell + cell / 2 - 1, gy + j * cell + cell / 2 - 1
        b.append(f'<circle cx="{cx}" cy="{cy}" r="7" fill="none" stroke="{C2}" stroke-width="2.5"/>')
    # the estimate
    mid = gy + 4 * cell
    ex = gx + n * cell + 44
    b.append(f'<path d="M{gx+n*cell+8} {mid} h26" stroke="{LINE}" stroke-width="2" marker-end="url(#a)"/>')
    b.append(f'<line x1="{ex}" y1="{mid}" x2="{ex+200}" y2="{mid}" stroke="{LINE}" stroke-width="2"/>')
    b.append(f'<rect x="{ex+50}" y="{mid-12}" width="100" height="24" rx="4" fill="{C2}" opacity="0.22"/>')
    b.append(f'<line x1="{ex+100}" y1="{mid-16}" x2="{ex+100}" y2="{mid+16}" stroke="{C2}" stroke-width="3"/>')
    b.append(txt(ex + 100, mid + 36, "estimate", 12, INK, anchor="middle"))
    b.append(txt(ex + 100, mid + 52, "± margin of error", 12, FAINT, anchor="middle"))
    b.insert(0, f'<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" '
                f'markerWidth="6" markerHeight="6" orient="auto">'
                f'<path d="M0 0 L10 5 L0 10 z" fill="{LINE}"/></marker></defs>')
    write("sampling_explainer.svg", svg(
        640, 250, "Probability-based sampling",
        "A grid of carbon values across a study area with eight sampled plots circled, and an "
        "arrow to the estimate and its margin of error.", "\n".join(b)))


# ═══════════════════════════════════════════════════════════════════════════
# sample_size_explorer_static.svg — the static fallback, three frames
# ═══════════════════════════════════════════════════════════════════════════
def explorer_static():
    random.seed(4)
    frames = [(3, 0.42, "3 samples"), (9, 0.24, "9 samples"), (25, 0.14, "25 samples")]
    b, fw, x0, y0, h = [], 230, 24, 74, 120
    b.append(txt(x0, 28, "What more samples buy", 14, INK, weight="600"))
    b.append(txt(x0, 46, "Each panel: the running estimate (bar) and its interval (band) against the simulated true mean (dashed).",
                 11.5, FAINT))
    for k, (n, rel, lab) in enumerate(frames):
        ox = x0 + k * (fw + 16)
        true_y = y0 + h * 0.42
        b.append(f'<rect x="{ox}" y="{y0}" width="{fw}" height="{h}" rx="4" '
                 f'fill="none" stroke="{LINE}" stroke-width="1"/>')
        est = 0.46 if k == 0 else (0.43 if k == 1 else 0.42)
        ey = y0 + h * est
        band = h * rel
        b.append(f'<rect x="{ox+30}" y="{ey-band/2}" width="{fw-60}" height="{band}" '
                 f'rx="3" fill="{C1}" opacity="0.20"/>')
        b.append(f'<line x1="{ox+30}" y1="{ey}" x2="{ox+fw-30}" y2="{ey}" '
                 f'stroke="{C1}" stroke-width="2.5"/>')
        b.append(f'<line x1="{ox+12}" y1="{true_y}" x2="{ox+fw-12}" y2="{true_y}" '
                 f'stroke="{INK}" stroke-width="1.5" stroke-dasharray="5 4"/>')
        b.append(txt(ox + fw / 2, y0 + h + 20, lab, 12.5, INK, anchor="middle", weight="600"))
        b.append(txt(ox + fw / 2, y0 + h + 36, f"±{rel*100:.0f}% (illustrative)", 11.5, FAINT, anchor="middle"))
    b.append(txt(x0, y0 + h + 66,
                 "A more variable pool — roots rather than soil — needs more samples to reach the same relative precision.",
                 12, INK))
    write("sample_size_explorer_static.svg", svg(
        760, 268, "Sample size and precision",
        "Three panels showing an estimate and its confidence band at three, nine and "
        "twenty-five samples. The band narrows as sample size grows while the simulated "
        "true mean stays fixed.", "\n".join(b)))


# ═══════════════════════════════════════════════════════════════════════════
# step1_grassland_boundary.svg
# ═══════════════════════════════════════════════════════════════════════════
def step1():
    b = ['<g transform="translate(-16,-42)">']
    b.append(f'<path d="M40 70 L430 62 L470 176 L392 268 L96 262 L36 168 Z" fill="{C3}" '
             f'opacity="0.16" stroke="{C3}" stroke-width="2.5"/>')
    for d in ("M150 120 q30 -22 62 -4 q20 30 -10 44 q-44 10 -52 -40 z",
              "M330 190 l40 -14 l24 30 l-30 26 l-36 -14 z"):
        b.append(f'<path d="{d}" fill="{C2}" opacity="0.30" stroke="{C2}" stroke-width="1.8"/>')
    b.append(txt(182, 168, "wetland", 11, C2, anchor="middle"))
    b.append(txt(356, 236, "rock outcrop", 11, C2, anchor="middle"))
    b.append(f'<path d="M36 214 L470 198" stroke="{C2}" stroke-width="9" opacity="0.30"/>')
    b.append(txt(96, 192, "road", 11, C2))
    b.append(f'<path d="M58 78 L64 258" stroke="{C4}" stroke-width="2" stroke-dasharray="8 5"/>')
    b.append(txt(70, 256, "fence line", 11, C4))
    b.append("</g>")
    write("step1_grassland_boundary.svg", svg(
        470, 240, "Study area boundary",
        "A project boundary polygon containing a wetland, a rock outcrop and a road, with a "
        "fence line crossing it.", "\n".join(b)))


# ═══════════════════════════════════════════════════════════════════════════
# step2_stratification.svg
# ═══════════════════════════════════════════════════════════════════════════
def step2():
    b = ['<g transform="translate(-24,-42)">']
    for lab, col, d, lx, ly in [
        ("Restored 20 yr", C3, "M40 70 L230 64 L242 176 L52 182 Z", 142, 128),
        ("Restored 10 yr", C1, "M230 64 L430 58 L446 168 L242 176 Z", 336, 122),
        ("Unrestored", C4, "M52 182 L242 176 L446 168 L412 268 L92 262 Z", 244, 228),
    ]:
        b.append(f'<path d="{d}" fill="{col}" opacity="0.20" stroke="{col}" stroke-width="2.5"/>')
        b.append(txt(lx, ly, lab, 12, col, anchor="middle", weight="600"))
    b.append("</g>")
    write("step2_stratification.svg", svg(
        440, 240, "Strata in the study area",
        "The study area divided into three strata: restored 20 years, restored 10 years, and "
        "unrestored.", "\n".join(b)))


# ═══════════════════════════════════════════════════════════════════════════
# step3_carbon_pools.svg
# ═══════════════════════════════════════════════════════════════════════════
def step3():
    """Pools, with roots under every plant and a rough stock beside every pool.

    Stocks are ROUGH, in kg C per m2, chosen to give a sense of scale only:
      trees, tree roots   Sothe et al. (2022): Canadian forest means, above-ground 4.1,
                          roots 1.3 (forest averages; scattered savannah trees hold less)
      ground vegetation   Bremer (2008) via Bork & Badiou (2017): Canadian temperate
      and its roots       grassland plants + litter hold 3-12 t C/ha (0.3-1.2 kg C/m2),
                          split with the report's "up to 85%+" root allocation
      soil, 0-30 cm       Bhatti et al. (2002) via Bork & Badiou (2017): 84-110 t C/ha
      shrubs              no per-area value: Flade et al. (2020) give per-plant equations
    The page text under the figure carries the citations.
    """
    b, g = [], 176                                       # ground line
    R = "#8a6a4a"                                         # roots
    def bubble(x, y, w, lines, anchor_x=None):
        h = 14 + 13 * (len(lines) - 1)
        out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h + 6}" rx="7" fill="none" '
               f'stroke="{INK}" stroke-width="1"/>']
        for i, (t, bold) in enumerate(lines):
            out.append(txt(x + w / 2, y + 15 + 13 * i, t, 10.5 if i == 0 else 10,
                           INK if i == 0 else FAINT, anchor="middle",
                           weight="bold" if bold else "normal"))
        return "\n".join(out)
    def roots(x, depth, spread, n, width=1.6):
        out = []
        for i in range(n):
            dx = spread * (2 * i / max(1, n - 1) - 1)
            out.append(f'<path d="M{x} {g} q{dx * 0.3:.1f} {depth * 0.5:.1f} {dx:.1f} {depth:.1f}" '
                       f'stroke="{R}" stroke-width="{width}" fill="none" opacity="0.8"/>')
        return "\n".join(out)

    b.append(f'<line x1="20" y1="{g}" x2="630" y2="{g}" stroke="{LINE}" stroke-width="2"/>')
    # tree, deep roots
    b.append(f'<line x1="90" y1="{g}" x2="90" y2="{g-74}" stroke="{C4}" stroke-width="4"/>')
    b.append(f'<ellipse cx="90" cy="{g-88}" rx="40" ry="26" fill="{C3}" opacity="0.35"/>')
    b.append(roots(90, 92, 42, 7, 2.2))
    b.append(bubble(40, 14, 100, [("Tree", True), ("≈ 4.1", False)]))
    b.append(bubble(40, g + 100, 100, [("Tree roots", True), ("≈ 1.3", False)]))
    # shrub, medium roots
    b.append(f'<path d="M222 {g} q-4 -32 14 -40 q22 4 16 40 z" fill="{C3}" opacity="0.45"/>')
    b.append(roots(232, 58, 26, 6, 1.6))
    b.append(bubble(182, 82, 100, [("Shrub", True), ("no value yet", False)]))
    b.append(bubble(182, g + 70, 100, [("Shrub roots", True), ("no value yet", False)]))
    # sward + quadrat, dense fine roots
    for i in range(16):
        x = 318 + i * 7
        b.append(f'<path d="M{x} {g} q2 -12 5 -18" stroke="{C3}" stroke-width="1.6" fill="none" opacity="0.8"/>')
        b.append(f'<path d="M{x+2} {g} q{(-1)**i * 2} 20 {(-1)**i * 3} {34 + (i % 4) * 6}" '
                 f'stroke="{R}" stroke-width="1" fill="none" opacity="0.7"/>')
    b.append(f'<rect x="314" y="{g-30}" width="120" height="30" fill="none" stroke="{C2}" '
             f'stroke-width="2" stroke-dasharray="5 3"/>')
    b.append(bubble(314, 104, 120, [("Ground vegetation", True), ("≈ 0.05–0.2", False)]))
    b.append(bubble(314, g + 64, 120, [("Grass roots", True), ("≈ 0.25–1.0", False)]))
    # core
    cx = 500
    b.append(f'<rect x="{cx}" y="{g}" width="30" height="128" fill="{C1}" opacity="0.16" stroke="{C1}" stroke-width="2"/>')
    for d, lab in [(0, "0–10"), (26, "10–20"), (52, "20–30"), (78, "30–60"), (104, "60–100")]:
        b.append(f'<line x1="{cx}" y1="{g+d}" x2="{cx+30}" y2="{g+d}" stroke="{C1}" stroke-width="1.2"/>')
        b.append(txt(cx + 38, g + d + 17, f"{lab} cm", 10.5, FAINT))
    b.append(bubble(466, 104, 112, [("Soil, 0–30 cm", True), ("≈ 8–11", False)]))
    b.append(txt(20, 346, "Rough stocks in kg C per m². Sources under the figure.", 10.5, FAINT))
    write("step3_carbon_pools.svg", svg(
        640, 356, "Carbon pools",
        "A grassland cross-section with a tree, a shrub and ground vegetation inside a small "
        "quadrat, each with roots, and a soil core divided into depth increments from 0 to 100 "
        "centimetres. Rough stocks in kilograms of carbon per square metre: tree about 4.1, tree "
        "roots about 1.3, shrub and shrub roots no value yet, ground vegetation about 0.05 to 0.2, "
        "grass roots about 0.25 to 1.0, soil 0 to 30 centimetres about 8 to 11.",
        "\n".join(b)))


# ═══════════════════════════════════════════════════════════════════════════
# step5_sampling_strategies.svg
# ═══════════════════════════════════════════════════════════════════════════
def step5_strategies():
    random.seed(7)
    b, fw, fh, x0, y0 = [], 168, 150, 8, 8
    panels = []
    panels.append(("Random", [(random.uniform(.1, .9), random.uniform(.1, .9)) for _ in range(9)], None))
    panels.append(("Systematic", [(0.2 + 0.3 * i, 0.2 + 0.3 * j) for i in range(3) for j in range(3)], None))
    strat = []
    for k in range(3):
        for _ in range(3):
            strat.append((random.uniform(.08, .92), k / 3 + random.uniform(.05, .28)))
    panels.append(("Stratified random", strat, "bands"))
    paired = []
    for k in range(4):
        y = 0.16 + k * 0.22
        paired += [(0.3, y), (0.7, y)]
    panels.append(("Paired", paired, "split"))
    for k, (lab, pts, deco) in enumerate(panels):
        ox = x0 + k * (fw + 16)
        b.append(f'<rect x="{ox}" y="{y0}" width="{fw}" height="{fh}" rx="4" fill="none" '
                 f'stroke="{LINE}" stroke-width="1"/>')
        if deco == "bands":
            for i, col in enumerate((C3, C1, C4)):
                b.append(f'<rect x="{ox+1}" y="{y0+1+i*(fh-2)/3}" width="{fw-2}" '
                         f'height="{(fh-2)/3}" fill="{col}" opacity="0.12"/>')
        if deco == "split":
            b.append(f'<line x1="{ox+fw/2}" y1="{y0}" x2="{ox+fw/2}" y2="{y0+fh}" '
                     f'stroke="{C2}" stroke-width="2" stroke-dasharray="6 4"/>')
        for px, py in pts:
            b.append(f'<circle cx="{ox+px*fw:.1f}" cy="{y0+py*fh:.1f}" r="4" fill="{C1}" opacity="0.85"/>')
        b.append(txt(ox + fw / 2, y0 + fh + 20, lab, 12, INK, anchor="middle", weight="600"))
    write("step5_sampling_strategies.svg", svg(
        736, 186, "Sampling strategies",
        "Four panels of sample placement: random, systematic grid, stratified random, and "
        "paired across a boundary.", "\n".join(b)))


# ═══════════════════════════════════════════════════════════════════════════
# step5_nested_plot_layout.svg
# ═══════════════════════════════════════════════════════════════════════════
def nested_plot():
    b, cx, cy = ['<g transform="translate(-100,-44)">'], 240, 176
    b.append(f'<circle cx="{cx}" cy="{cy}" r="112" fill="{C3}" opacity="0.08" stroke="{C3}" stroke-width="2"/>')
    b.append(txt(cx, cy - 118, "large plot", 11.5, C3, anchor="middle"))
    b.append(f'<rect x="{cx-56}" y="{cy-56}" width="112" height="112" fill="{C1}" opacity="0.10" stroke="{C1}" stroke-width="2"/>')
    b.append(txt(cx, cy - 64, "medium plot", 11.5, C1, anchor="middle"))
    b.append(f'<rect x="{cx-44}" y="{cy+6}" width="34" height="34" fill="{C2}" opacity="0.22" stroke="{C2}" stroke-width="2"/>')
    b.append(txt(cx - 27, cy + 56, "quadrat", 11, C2, anchor="middle"))
    b.append(f'<circle cx="{cx+34}" cy="{cy+24}" r="6" fill="{C4}"/>')
    b.append(txt(cx + 34, cy + 46, "core", 11, C4, anchor="middle"))
    b.append(f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="{INK}"/>')
    b.append("</g>")
    write("step5_nested_plot_layout.svg", svg(
        280, 250, "Nested plot layout",
        "Plan view of a nested plot: a large circular plot, a medium square plot inside it, a "
        "small quadrat, and a soil core beside the quadrat.", "\n".join(b)))


# ═══════════════════════════════════════════════════════════════════════════
# permanent_vs_single_use.svg
# ═══════════════════════════════════════════════════════════════════════════
def perm_vs_single():
    b, fw, fh, y0 = [], 200, 196, 8
    for k, (lab, perm) in enumerate([("Single-use", False), ("Permanent", True)]):
        ox = 8 + k * (fw + 24)
        col = C2 if not perm else C3
        b.append(f'<rect x="{ox}" y="{y0}" width="{fw}" height="{fh}" rx="5" fill="none" '
                 f'stroke="{LINE}" stroke-width="1"/>')
        b.append(txt(ox + 14, y0 + 24, lab, 13.5, col, weight="600"))
        px, py, half = ox + 84, y0 + 108, 44
        b.append(f'<rect x="{px-half}" y="{py-half}" width="{2*half}" height="{2*half}" '
                 f'fill="{col}" opacity="0.10" stroke="{col}" stroke-width="2"/>')
        b.append(f'<rect x="{px-30}" y="{py-12}" width="24" height="24" fill="{C1}" '
                 f'opacity="0.28" stroke="{C1}" stroke-width="1.5"/>')
        b.append(txt(px - 18, py + 30, "quadrat", 9.5, C1, anchor="middle"))
        if perm:
            b.append(f'<circle cx="{px+half+26}" cy="{py+18}" r="6" fill="{C4}"/>')
            b.append(f'<path d="M{px+half+2} {py+18} h16" stroke="{C4}" stroke-width="1.2" '
                     f'stroke-dasharray="3 3"/>')
            b.append(txt(px + half + 26, py + 40, "core", 10, C4, anchor="middle"))
            b.append(f'<circle cx="{px-half}" cy="{py+half}" r="4.5" fill="{col}"/>')
            b.append(txt(px - half, py + half + 18, "marker", 9.5, col, anchor="middle"))
        else:
            b.append(f'<circle cx="{px+20}" cy="{py+6}" r="6" fill="{C4}"/>')
            b.append(txt(px + 20, py + 28, "core", 10, C4, anchor="middle"))
    write("permanent_vs_single_use.svg", svg(
        440, 212, "Single-use and permanent plots",
        "Two panels. Single-use: the core is taken inside the vegetation plot. Permanent: the "
        "core is taken outside the vegetation plot, and the plot has a marker.", "\n".join(b)))


if __name__ == "__main__":
    print("Part 2 figures →", OUT)
    sampling_explainer()
    explorer_static()
    step1()
    step2()
    step3()
    step5_strategies()
    nested_plot()
    perm_vs_single()
