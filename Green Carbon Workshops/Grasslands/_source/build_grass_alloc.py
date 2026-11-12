"""Grassland Sample Allocation Calculator.

Sizes SOIL and ROOT sampling separately, because root biomass is usually the
more variable pool and holding both to the same relative precision makes root
washing dominate the campaign.

The number it returns is the small-sample-adjusted one. Planning starts from the
normal multiplier z, but the interval you will actually report after fieldwork
uses Student's t on n-1 degrees of freedom, which is larger. So the sheet
iterates:

    n_0     = ceil( (z  * CV / E)^2 )
    n_{k+1} = ceil( (t(n_k - 1) * CV / E)^2 )      until it stops moving

and takes the larger value where it oscillates between two. Both the plain
z-based figure and the adjusted one are shown, so the adjustment is never
invisible.

Excel has no closed form for this, so the iteration is unrolled across six
hidden columns. Six passes is far more than enough -- it converges in three or
four for every case in Part 2 -- and unrolling keeps the workbook free of
circular references and macros.

Run:  python3 build_grass_alloc.py
"""
import sys, math, openpyxl
sys.path.insert(0, "/home/user/Terrestrial_Carbon_Workshops_V1/Grasslands/_source")
from grass_style import (F_H, F_SUB, F_N, F_IT, FILL_H, FILL, BOX, WRAP, CTR,
                         header_row, band, note, paint, title, NAVY)
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font
from openpyxl.workbook.defined_name import DefinedName
import tdist

OUT = ("/home/user/Terrestrial_Carbon_Workshops_V1/Grasslands/02_Project_Planning/"
       "Sampling Design Tools/grassland-sample-allocation.xlsx")

NROW = 12          # stratum rows
PASSES = 6         # unrolled iterations of the t adjustment

wb = openpyxl.Workbook()

# ═══════════════════════════════════════════════════════════════════════════
# 0. Instructions
# ═══════════════════════════════════════════════════════════════════════════
ws = wb.active
ws.title = "0. Instructions"
for col, w in zip("ABCD", (30, 64, 22, 40)):
    ws.column_dimensions[col].width = w
title(ws, "GRASSLAND SAMPLE ALLOCATION CALCULATOR",
      "WWF-Canada Carbon Measurement · Grassland Carbon Workshop, Part 2 Step 4", 4)

r = 4
for head, body in [
    ("What this workbook does",
     "Turns a precision target into a number of samples, separately for SOIL and for ROOTS, "
     "and splits that number across your strata by area. It records every assumption you "
     "used, so the design can be defended later."),
    ("Why soil and roots are sized separately",
     "Planned sample size scales with the SQUARE of the coefficient of variation. Root biomass "
     "is usually more variable than soil carbon, so one shared precision target lets root "
     "processing set the size of the whole campaign. Setting a wider, stated target for roots "
     "is usually the better trade."),
    ("The small-sample adjustment",
     "Planning uses the normal multiplier z. The interval you report afterwards uses Student's "
     "t on n-1 degrees of freedom, which is larger. This sheet iterates with t until the "
     "answer stops moving, and shows both figures so the adjustment is visible."),
    ("What it does NOT do",
     "It does not choose your prior, judge whether your strata are meaningful, or replace a "
     "design-specific analysis. It is a planning starting point."),
]:
    ws.cell(r, 1, head).font = F_SUB
    c = ws.cell(r, 2, body); c.alignment = WRAP
    ws.row_dimensions[r].height = 58
    r += 1

r += 1
band(ws, r, 4, "  HOW TO USE IT")
r += 1
for i, step in enumerate([
    "On '1. Design', set your confidence level and the precision target for each pool.",
    "Enter your variability prior (mean and SD, or a CV directly) for each pool, and say where it came from.",
    "On '2. Strata', enter each stratum's name and area in m². The sheet allocates by area.",
    "Read the per-pool sample size and the per-stratum allocation off '3. Result'.",
    "Copy the assumptions statement on '3. Result' into your project record.",
], start=1):
    ws.cell(r, 1, f"Step {i}").font = F_SUB
    ws.cell(r, 2, step).alignment = WRAP
    ws.row_dimensions[r].height = 28
    r += 1

r += 1
note(ws, r, 4,
     "Colour key:  yellow = type here  ·  grey = calculated  ·  green = the answer  "
     "·  orange = a value only you can supply")

# ═══════════════════════════════════════════════════════════════════════════
# 1. Design
# ═══════════════════════════════════════════════════════════════════════════
ds = wb.create_sheet("1. Design")
for col, w in zip("ABCDE", (34, 16, 14, 58, 4)):
    ds.column_dimensions[col].width = w
title(ds, "DESIGN INPUTS", "Everything you choose. Yellow and orange cells only.", 4)

r = 4
band(ds, r, 4, "  CONFIDENCE")
r += 1
ds.cell(r, 1, "Confidence level").font = F_SUB
ds.cell(r, 2, 0.90).fill = FILL["y"]; ds.cell(r, 2).border = BOX
ds.cell(r, 2).number_format = "0%"
ds.cell(r, 4, "0.90 or 0.95. Higher confidence needs more samples.").font = F_IT
CONF = f"'1. Design'!$B${r}"
r += 1
ds.cell(r, 1, "z multiplier").font = F_SUB
ds.cell(r, 2, f"=NORMSINV(1-(1-{CONF})/2)").fill = FILL["g"]
ds.cell(r, 2).border = BOX; ds.cell(r, 2).number_format = "0.000"
ds.cell(r, 4, "Normal multiplier used for the FIRST planning pass only.").font = F_IT
Z = f"'1. Design'!$B${r}"

r += 2
band(ds, r, 4, "  PRECISION TARGET, PER POOL")
r += 1
header_row(ds, r, ["Pool", "Target E", "", "What it means"], None, None)
ds.row_dimensions[r].height = 20
TARG = {}
for pool, default, why in [
    ("Soil carbon", 0.20, "Relative margin of error. 0.20 = the interval reaches ±20% of the mean."),
    ("Root biomass", 0.40, "A wider target here is usually honest, not a failure. State it and report against it."),
]:
    r += 1
    ds.cell(r, 1, pool).font = F_SUB
    c = ds.cell(r, 2, default); c.fill = FILL["y"]; c.border = BOX; c.number_format = "0%"
    ds.cell(r, 4, why).font = F_IT; ds.cell(r, 4).alignment = WRAP
    ds.row_dimensions[r].height = 26
    TARG[pool] = f"'1. Design'!$B${r}"

r += 2
band(ds, r, 4, "  VARIABILITY PRIOR, PER POOL")
r += 1
note(ds, r, 4,
     "Enter EITHER a mean and SD in the same units, OR a CV directly. If a CV is entered it "
     "wins. This is the single input that most changes the answer, and the one the workshop "
     "cannot supply for you.")
r += 1
header_row(ds, r, ["Pool", "Value", "", "Notes"], None, None)
ds.row_dimensions[r].height = 20
CV = {}
for pool in ("Soil carbon", "Root biomass"):
    r += 1
    band(ds, r, 4, f"  {pool}", fill="EDEDED")
    rows = {}
    for lab, dflt, note_txt in [
        ("Prior mean", None, "In whatever unit you measure the pool. Only used to derive the CV."),
        ("Prior SD", None, "Same unit as the mean."),
        ("Prior CV (overrides)", None, "SD ÷ mean. Enter directly if that is what your source reports."),
        ("Source of the prior", None, "Pilot / published study / soil map. Write it down — a reviewer will ask."),
    ]:
        r += 1
        ds.cell(r, 1, lab).font = F_N
        c = ds.cell(r, 2, dflt); c.fill = FILL["o"]; c.border = BOX
        ds.cell(r, 4, note_txt).font = F_IT; ds.cell(r, 4).alignment = WRAP
        ds.row_dimensions[r].height = 24
        rows[lab] = r
    r += 1
    ds.cell(r, 1, "→ CV used").font = F_SUB
    c = ds.cell(r, 2, f'=IF(ISNUMBER($B${rows["Prior CV (overrides)"]}),$B${rows["Prior CV (overrides)"]},'
                      f'IF(AND(ISNUMBER($B${rows["Prior mean"]}),ISNUMBER($B${rows["Prior SD"]}),'
                      f'$B${rows["Prior mean"]}<>0),$B${rows["Prior SD"]}/$B${rows["Prior mean"]},""))')
    c.fill = FILL["g"]; c.border = BOX; c.number_format = "0.00"
    ds.cell(r, 4, "Blank until you supply a prior. Nothing downstream computes without it.").font = F_IT
    CV[pool] = f"'1. Design'!$B${r}"
    r += 1

r += 1
band(ds, r, 4, "  MINIMUM PER STRATUM")
r += 1
ds.cell(r, 1, "Minimum samples per stratum").font = F_SUB
c = ds.cell(r, 2, 3); c.fill = FILL["o"]; c.border = BOX
ds.cell(r, 4, "Draft statistical minimum is 3; 5 is preferred where feasible. The eelgrass "
              "workshop uses 5 as an operational minimum. Confirm the series-wide rule.").font = F_IT
ds.cell(r, 4).alignment = WRAP
ds.row_dimensions[r].height = 40
MINH = f"'1. Design'!$B${r}"

for nm, ref in [("CONF_LEVEL", CONF), ("Z_MULT", Z), ("CV_SOIL", CV["Soil carbon"]),
                ("CV_ROOT", CV["Root biomass"]), ("E_SOIL", TARG["Soil carbon"]),
                ("E_ROOT", TARG["Root biomass"]), ("MIN_PER_STRATUM", MINH)]:
    wb.defined_names.add(DefinedName(nm, attr_text=ref))

# ═══════════════════════════════════════════════════════════════════════════
# 2. Strata
# ═══════════════════════════════════════════════════════════════════════════
st = wb.create_sheet("2. Strata")
COLS = ["Stratum name", "Area (m²)", "Area (ha)", "Share of total",
        "Soil samples", "Root samples", "Notes"]
header_row(st, 4, COLS, [30, 14, 12, 13, 13, 13, 46], ["y", "y"] + [None] * 5)
title(st, "STRATA", "One row per stratum from Part 2 Step 2. Area drives the allocation.", len(COLS))
R0, R1 = 5, 4 + NROW
paint(st, R0, R1, 1, "y"); paint(st, R0, R1, 2, "y")
for col in (3, 4, 5, 6):
    paint(st, R0, R1, col, "g")
paint(st, R0, R1, 7, "y")

TOT = f"SUM($B${R0}:$B${R1})"
for r in range(R0, R1 + 1):
    st.cell(r, 3, f'=IF(NOT(ISNUMBER($B{r})),"",$B{r}/10000)').number_format = "0.00"
    st.cell(r, 4, f'=IF(OR(NOT(ISNUMBER($B{r})),{TOT}=0),"",$B{r}/{TOT})').number_format = "0.0%"
    # allocation: share x total n, rounded UP, then floored at the minimum
    for col, tot_ref in ((5, "'3. Result'!$B$8"), (6, "'3. Result'!$C$8")):
        st.cell(r, col,
                f'=IF(OR($A{r}="",NOT(ISNUMBER($D{r})),NOT(ISNUMBER({tot_ref}))),"",'
                f'MAX(MIN_PER_STRATUM,CEILING($D{r}*{tot_ref},1)))')

r = R1 + 2
st.cell(r, 1, "TOTAL").font = F_SUB
st.cell(r, 2, f'=IF({TOT}=0,"",{TOT})').font = F_SUB
st.cell(r, 3, f'=IF({TOT}=0,"",{TOT}/10000)').number_format = "0.00"
for col in (5, 6):
    L = get_column_letter(col)
    st.cell(r, col, f'=IF(SUM(${L}${R0}:${L}${R1})=0,"",SUM(${L}${R0}:${L}${R1}))').font = F_SUB
r += 2
note(st, r, len(COLS),
     "Allocation is proportional to AREA, rounded up, then raised to the minimum per stratum. "
     "Both of those push the total above the calculated n, which is expected — rounding down "
     "or allowing a 2-sample stratum would leave that stratum without an estimable variance. "
     "Where strata differ greatly in variability or cost, area-proportional allocation is not "
     "optimal; see Appendix A7.")

# ═══════════════════════════════════════════════════════════════════════════
# 3. Result
# ═══════════════════════════════════════════════════════════════════════════
rs = wb.create_sheet("3. Result")
for col, w in zip("ABCDEFGHIJKLMN", (32, 15, 15, 46) + (9,) * 10):
    rs.column_dimensions[col].width = w
title(rs, "RESULT", "The sample size for each pool, and how it was reached.", 4)

rs.cell(4, 2, "SOIL").font = F_H; rs.cell(4, 2).fill = FILL_H; rs.cell(4, 2).alignment = CTR
rs.cell(4, 3, "ROOTS").font = F_H; rs.cell(4, 3).fill = FILL_H; rs.cell(4, 3).alignment = CTR

rows = {
    5: ("CV used", '=IF(ISNUMBER({cv}),{cv},"")', "0.00", "g"),
    6: ("Target E", '={e}', "0%", "g"),
    7: ("Planning n (z only)", '=IF(OR(NOT(ISNUMBER({cv})),NOT(ISNUMBER({e})),{e}=0),"",'
                               'CEILING((Z_MULT*{cv}/{e})^2,1))', "0", "g"),
    8: ("SAMPLE SIZE (t-adjusted)", '=IF(NOT(ISNUMBER(${col}$7)),"",${col}${last})', "0", "s"),
    9: ("Added by the adjustment", '=IF(OR(NOT(ISNUMBER(${col}$7)),NOT(ISNUMBER(${col}$8))),"",'
                                   '${col}$8-${col}$7)', "0", "g"),
}
# ── the unrolled t iteration, hidden ────────────────────────────────────────
# F..K hold passes 1..6 for soil, and rows below for roots. Each pass recomputes
# n from t(previous n - 1). ROUND to 6 dp keeps a stable comparison.
first_pass_col = 6
last_col_letter = get_column_letter(first_pass_col + PASSES - 1)

for row, (label, formula, fmt, fill) in rows.items():
    rs.cell(row, 1, label).font = F_SUB
    for col, cv_ref, e_ref in ((2, "CV_SOIL", "E_SOIL"), (3, "CV_ROOT", "E_ROOT")):
        L = get_column_letter(col)
        f = formula.format(cv=cv_ref, e=e_ref, col=L, last=f"$IT{col}")
        c = rs.cell(row, col, f)
        c.number_format = fmt; c.fill = FILL[fill]; c.border = BOX
        if row == 8:
            c.font = Font(bold=True, size=12, color=NAVY)

# iteration rows: 12 (soil) and 13 (roots), columns F..K
rs.cell(11, 1, "t-iteration (unrolled)").font = F_SUB
rs.cell(11, 4, "Each pass recomputes n from t on the previous n−1 degrees of freedom. "
               "It converges in three or four passes; six is headroom.").font = F_IT
rs.cell(11, 4).alignment = WRAP
for i in range(PASSES):
    rs.cell(11, first_pass_col + i, f"pass {i+1}").font = F_IT
for row, cv_ref, e_ref, src in ((12, "CV_SOIL", "E_SOIL", "$B$7"), (13, "CV_ROOT", "E_ROOT", "$C$7")):
    rs.cell(row, 1, "soil" if row == 12 else "roots").font = F_N
    for i in range(PASSES):
        col = first_pass_col + i
        prev = src if i == 0 else f"${get_column_letter(col-1)}${row}"
        rs.cell(row, col,
                f'=IF(NOT(ISNUMBER({prev})),"",'
                f'CEILING((TINV(1-CONF_LEVEL,MAX(1,{prev}-1))*{cv_ref}/{e_ref})^2,1))'
                ).number_format = "0"

# point row 8 at the last pass
# The iteration does not always reach a fixed point -- for some inputs it settles
# into a two-cycle, alternating between n and n+1. Taking the larger of the last
# two passes is the conservative resolution and is what the Python check below
# reproduces.
penult = get_column_letter(first_pass_col + PASSES - 2)
rs.cell(8, 2, f'=IF(NOT(ISNUMBER($B$7)),"",MAX(${penult}$12,${last_col_letter}$12))').number_format = "0"
rs.cell(8, 3, f'=IF(NOT(ISNUMBER($C$7)),"",MAX(${penult}$13,${last_col_letter}$13))').number_format = "0"
rs.cell(8, 2).fill = FILL["s"]; rs.cell(8, 3).fill = FILL["s"]
rs.cell(8, 2).font = Font(bold=True, size=12, color=NAVY)
rs.cell(8, 3).font = Font(bold=True, size=12, color=NAVY)
for col in range(first_pass_col, first_pass_col + PASSES):
    rs.column_dimensions[get_column_letter(col)].hidden = True

r = 15
band(rs, r, 4, "  FIELD COUNT")
r += 1
rs.cell(r, 1, "Cores to collect").font = F_SUB
rs.cell(r, 2, f"='2. Strata'!$E${R1+2}").fill = FILL["s"]
rs.cell(r, 2).border = BOX; rs.cell(r, 2).number_format = "0"
rs.cell(r, 4, "Soil allocation summed over strata, after rounding and the minimum.").font = F_IT
r += 1
rs.cell(r, 1, "Cores to wash for roots").font = F_SUB
rs.cell(r, 2, f"='2. Strata'!$F${R1+2}").fill = FILL["s"]
rs.cell(r, 2).border = BOX; rs.cell(r, 2).number_format = "0"
rs.cell(r, 4, "Roots come out of the same cores. If this is below the soil count, choose the "
              "subset AT RANDOM before looking at the cores.").font = F_IT
rs.cell(r, 4).alignment = WRAP
rs.row_dimensions[r].height = 30

r += 2
band(rs, r, 4, "  ASSUMPTIONS STATEMENT — copy this into your project record")
r += 1
rs.merge_cells(start_row=r, start_column=1, end_row=r + 3, end_column=4)
c = rs.cell(r, 1,
            f'=IF(OR(NOT(ISNUMBER($B$8)),NOT(ISNUMBER($C$8))),'
            f'"Complete the design inputs to generate this statement.",'
            f'"Sample sizes were calculated at "&TEXT(CONF_LEVEL,"0%")&" confidence. '
            f'Soil carbon was sized to a relative margin of error of "&TEXT(E_SOIL,"0%")&'
            f'" using a coefficient of variation of "&TEXT(CV_SOIL,"0.00")&", giving "&$B$8&'
            f'" samples. Root biomass was sized separately to "&TEXT(E_ROOT,"0%")&'
            f'" using a coefficient of variation of "&TEXT(CV_ROOT,"0.00")&", giving "&$C$8&'
            f'" samples. Planning began from the normal multiplier and was then adjusted for '
            f'small-sample Student''s t until stable. Samples were allocated across strata in '
            f'proportion to area, rounded up, with a minimum of "&MIN_PER_STRATUM&'
            f'" per stratum. Record the source of each variability prior alongside this '
            f'statement.")')
c.alignment = WRAP; c.font = F_N; c.fill = FILL["s"]; c.border = BOX
for rr in range(r, r + 4):
    rs.row_dimensions[rr].height = 22

r += 5
note(rs, r, 4,
     "This is a planning starting point, not a design-specific analysis. It assumes independent "
     "samples and a defensible prior. Paired designs, chronosequences, unequal-variance "
     "comparisons and detectable-change studies all need more than this sheet — see Appendix A10.")

# ═══════════════════════════════════════════════════════════════════════════
# 4. Sensitivity — regenerated, never hand-typed
# ═══════════════════════════════════════════════════════════════════════════
sv = wb.create_sheet("4. Sensitivity")
COLS2 = ["Pool", "CV", "Target E", "Confidence", "n (z only)", "n (t-adjusted)", "Added"]
header_row(sv, 4, COLS2, [26, 10, 11, 12, 13, 15, 10])
title(sv, "SENSITIVITY",
      "What one knob at a time does. These are the figures Part 2 quotes — they are computed "
      "here, so the prose and the calculator cannot disagree.", len(COLS2))


def n_z(cv, e, conf):
    z = tdist.tinv_normal(conf) if hasattr(tdist, "tinv_normal") else None
    if z is None:
        # inverse normal via the t distribution at very high df
        z = tdist.tinv(1 - conf, 100000)
    return math.ceil((z * cv / e) ** 2)


def n_t(cv, e, conf):
    """Fixed-point iteration on n using t(n-1). Where it settles into a
    two-cycle rather than a fixed point, take the larger of the pair."""
    n = n_z(cv, e, conf)
    seq = []
    for _ in range(PASSES):
        n = math.ceil((tdist.tinv(1 - conf, max(1, n - 1)) * cv / e) ** 2)
        seq.append(n)
    return max(seq[-2], seq[-1])


SCEN = [("Soil carbon — relatively uniform", 0.20, 0.20, 0.90),
        ("Soil carbon — moderate variation", 0.30, 0.20, 0.90),
        ("Soil carbon — higher variation", 0.40, 0.20, 0.90),
        ("Roots — lower illustrative variation", 0.50, 0.20, 0.90),
        ("Roots — moderate illustrative variation", 0.70, 0.20, 0.90),
        ("Roots — high illustrative variation", 1.00, 0.20, 0.90),
        ("Roots at a ±30% target", 0.70, 0.30, 0.90),
        ("Roots at a ±40% target", 0.70, 0.40, 0.90),
        ("Soil at 95% confidence", 0.30, 0.20, 0.95)]

r = 5
for label, cv, e, conf in SCEN:
    sv.cell(r, 1, label).font = F_N
    sv.cell(r, 2, cv).number_format = "0.00"
    sv.cell(r, 3, e).number_format = "0%"
    sv.cell(r, 4, conf).number_format = "0%"
    sv.cell(r, 5, n_z(cv, e, conf))
    sv.cell(r, 6, n_t(cv, e, conf)).font = F_SUB
    sv.cell(r, 7, n_t(cv, e, conf) - n_z(cv, e, conf))
    for col in range(1, 8):
        sv.cell(r, col).border = BOX
        sv.cell(r, col).fill = FILL["g" if col < 6 else "s"]
    r += 1

r += 1
note(sv, r, len(COLS2),
     "Values computed by build_grass_alloc.py with the same iteration the '3. Result' tab "
     "unrolls in Excel. Re-run that script after changing the method, and copy these figures "
     "into Part 2 rather than editing either by hand.")

import os
os.makedirs(os.path.dirname(OUT), exist_ok=True)
wb.save(OUT)
print("wrote", OUT)
print(f"{'scenario':<42}{'CV':>6}{'E':>7}{'conf':>7}{'n(z)':>7}{'n(t)':>7}")
for label, cv, e, conf in SCEN:
    print(f"{label:<42}{cv:>6.2f}{e:>7.0%}{conf:>7.0%}{n_z(cv,e,conf):>7}{n_t(cv,e,conf):>7}")
