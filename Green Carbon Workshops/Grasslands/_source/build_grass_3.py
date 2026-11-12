"""Grassland_Carbon_Calculator.xlsx -- part 3: summaries and the reference tab.

The design point here is that SOIL and ROOTS are checked against SEPARATE
precision targets. Roots are 4-5x more variable than soil carbon, so holding
both to the same target would demand four to five times the cores. See Part 2,
Appendix A10.
"""
import sys, openpyxl
sys.path.insert(0, "/home/user/Terrestrial_Carbon_Workshops_V1/Grasslands/_source")
from grass_style import *   # noqa

wb = openpyxl.load_workbook(OUT)
SD_LAST = 4 + NROW_SOIL
RT_LAST = 4 + NROW_ROOT
VG_LAST = 4 + NROW_VEG
PL_LAST = 4 + NROW_PLOT

# ── 5. Plot Summary ──────────────────────────────────────────────────────────
ps = wb.create_sheet("5. Plot Summary", 5)
COLS = ["Plot ID", "Site ID", "Increments", "Soil C to reporting depth (kg C/m²)",
        "Soil C, full profile (kg C/m²)", "Deepest increment (cm)",
        "Root C (kg C/m²)", "Vegetation C (kg C/m²)",
        "TOTAL to reporting depth (kg C/m²)", "TOTAL, full profile (kg C/m²)",
        "QC flags", "_soil", "_root", "_inc", "_cores", "_rootcores", "_soil2", "_root2",
        "_sr", "_sr2"]
W = [12, 10, 11, 16, 16, 13, 14, 15, 17, 17, 52, 9, 9, 7, 8, 8, 9, 9, 9, 9]
title(ps, "PLOT SUMMARY",
      "One row per plot, calculated for you. Soil carbon is reported on two bases — to the "
      "reporting depth, and to the full depth you actually cored. Root carbon is measured, not "
      "derived from a ratio.", len(COLS))
header_row(ps, 4, COLS, W)
R0, R1 = 5, 4 + NROW_PLOT
for col in range(1, len(COLS) + 1):
    paint(ps, R0, R1, col, "s" if col <= 10 else ("r" if col == 11 else "g"))

for r in range(R0, R1 + 1):
    i = r - 4
    ps.cell(r, 1, f'=IF(INDEX(\'1. Plot & Site Log\'!$A$5:$A${PL_LAST},{i})="","",'
                  f'INDEX(\'1. Plot & Site Log\'!$A$5:$A${PL_LAST},{i}))')
    ps.cell(r, 2, f'=IF($A{r}="","",INDEX(\'1. Plot & Site Log\'!$B$5:$B${PL_LAST},'
                  f'MATCH($A{r},\'1. Plot & Site Log\'!$A$5:$A${PL_LAST},0)))')
    ps.cell(r, 3, f'=IF($A{r}="","",COUNTIFS(\'2. Soil Data\'!$A$5:$A${SD_LAST},$A{r}))')
    # distinct cores in this plot, from the portable first-of-core marker
    ps.cell(r, 15, f'=IF($A{r}="","",SUMIFS(\'2. Soil Data\'!$U$5:$U${SD_LAST},'
                   f'\'2. Soil Data\'!$A$5:$A${SD_LAST},$A{r}))')
    ps.cell(r, 16, f'=IF($A{r}="","",SUMIFS(\'3. Root Biomass\'!$Q$5:$Q${RT_LAST},'
                   f'\'3. Root Biomass\'!$A$5:$A${RT_LAST},$A{r}))')
    # soil to reporting depth, and full profile: summed over the plot's increments,
    # then averaged across the cores in that plot
    ps.cell(r, 4, f'=IF(OR($A{r}="",$C{r}=0,$O{r}=0),"",'
                  f'SUMIFS(\'2. Soil Data\'!$R$5:$R${SD_LAST},'
                  f'\'2. Soil Data\'!$A$5:$A${SD_LAST},$A{r})/$O{r})')
    ps.cell(r, 5, f'=IF(OR($A{r}="",$C{r}=0,$O{r}=0),"",'
                  f'SUMIFS(\'2. Soil Data\'!$P$5:$P${SD_LAST},'
                  f'\'2. Soil Data\'!$A$5:$A${SD_LAST},$A{r})/$O{r})')
    # deepest increment. MAXIFS returns blank in LibreOffice, so use SUMPRODUCT(MAX(...)).
    ps.cell(r, 6, f'=IF($A{r}="","",'
                  f'SUMPRODUCT(MAX((\'2. Soil Data\'!$A$5:$A${SD_LAST}=$A{r})*'
                  f'IF(ISNUMBER(\'2. Soil Data\'!$E$5:$E${SD_LAST}),'
                  f'\'2. Soil Data\'!$E$5:$E${SD_LAST},0))))')
    ps.cell(r, 7, f'=IF(OR($A{r}="",$P{r}=0),"",'
                  f'SUMIFS(\'3. Root Biomass\'!$N$5:$N${RT_LAST},'
                  f'\'3. Root Biomass\'!$A$5:$A${RT_LAST},$A{r})/$P{r})')
    ps.cell(r, 8, f'=IF($A{r}="","",IFERROR(SUMIFS(\'4. Vegetation Data\'!$O$5:$O${VG_LAST},'
                  f'\'4. Vegetation Data\'!$A$5:$A${VG_LAST},$A{r}),""))')
    ps.cell(r, 9, f'=IF($A{r}="","",IF(ISNUMBER($D{r}),$D{r},0)+IF(ISNUMBER($G{r}),$G{r},0)'
                  f'+IF(ISNUMBER($H{r}),$H{r},0))')
    ps.cell(r, 10, f'=IF($A{r}="","",IF(ISNUMBER($E{r}),$E{r},0)+IF(ISNUMBER($G{r}),$G{r},0)'
                   f'+IF(ISNUMBER($H{r}),$H{r},0))')
    ps.cell(r, 11,
            f'=IF($A{r}="","",'
            f'IF($C{r}=0,"No soil increments for this plot — it contributes nothing. ","")'
            f'&IF(AND(ISNUMBER($F{r}),$F{r}<SOIL_REPORTING_DEPTH_CM),'
            f'"Cored shallower than the reporting depth, so the reporting-depth figure is an '
            f'UNDERESTIMATE for this plot. ","")'
            f'&IF(AND(ISNUMBER($G{r}),$G{r}>0,ISNUMBER($F{r})),'
            f'"Root total reaches only "&$F{r}&" cm — the bottom of the core, not the bottom of '
            f'the roots. Report it as a MINIMUM. ","")'
            # The two working boundaries are not equivalent, so they get different
            # flags: one says the sum is defensible, the other says the sum is a
            # double count. "Not agreed" is the state most projects are actually in.
            f'&IF(AND(ISNUMBER($G{r}),$G{r}>0,'
            f'ROOT_SOIL_REPORTING_BOUNDARY="Not agreed with the lab"),'
            f'"Root carbon is being added to a soil stock whose root content was never agreed '
            f'with the lab. The overlap is unknown, not zero — settle '
            f'ROOT_SOIL_REPORTING_BOUNDARY before reporting a combined figure. ","")'
            f'&IF(AND(ISNUMBER($G{r}),$G{r}>0,'
            f'ROOT_SOIL_REPORTING_BOUNDARY="Operational soil fraction"),'
            f'"The soil sample keeps every root the lab\'s standard preparation did not pick '
            f'out, so soil and root pools OVERLAP. Report them separately; do not add them. '
            f'","")'
            f'&IF(ROOT_SOIL_BOUNDARY_SOURCE="",'
            f'"No source recorded for the root/soil boundary. ",""))')
    ps.cell(r, 12, f'=IF(ISNUMBER($D{r}),$D{r},"")')   # reporting-depth basis
    ps.cell(r, 13, f'=IF(ISNUMBER($G{r}),$G{r},"")')
    ps.cell(r, 14, f'=IF(AND(ISNUMBER($D{r}),$A{r}<>""),1,0)')
    # squares, so the Site Summary can compute SD without an array formula
    ps.cell(r, 17, f'=IF(ISNUMBER($D{r}),$D{r}^2,"")')
    ps.cell(r, 18, f'=IF(ISNUMBER($G{r}),$G{r}^2,"")')
    # soil + root per plot, and its square. This is the quantity the study-area
    # total is built from, and the stratified interval needs its WITHIN-site
    # spread -- which is not recoverable from the soil and root SDs separately,
    # because the two are correlated within a plot.
    ps.cell(r, 19, f'=IF($A{r}="","",IF(ISNUMBER($D{r}),$D{r},0)+IF(ISNUMBER($G{r}),$G{r},0))')
    ps.cell(r, 20, f'=IF(ISNUMBER($S{r}),$S{r}^2,"")')
for col in (12, 13, 14, 15, 16, 17, 18, 19, 20):
    ps.column_dimensions[openpyxl.utils.get_column_letter(col)].hidden = True

# ── 6. Site Summary ──────────────────────────────────────────────────────────
ss = wb.create_sheet("6. Site Summary", 6)
COLS = ["Site ID", "Site area (m²)", "Plots",
        "SOIL mean to reporting depth (kg C/m²)", "SOIL SD", "SOIL ± half-width", "SOIL achieved",
        "SOIL target", "SOIL precision",
        "ROOT mean (kg C/m²)", "ROOT SD", "ROOT ± half-width", "ROOT achieved",
        "ROOT target", "ROOT precision",
        "Total carbon (kg C)", "Total (t CO₂e)", "QC flags",
        "_srmean", "_srsd", "_varpart", "_dfpart"]
W = [10, 13, 8, 14, 11, 14, 12, 11, 30, 14, 11, 14, 12, 11, 30, 15, 14, 48, 9, 9, 9, 9]
title(ss, "SITE SUMMARY",
      "Type a Site ID and its area; everything else calculates. Soil is summarised on the "
      "REPORTING-DEPTH basis, so cores of different depths stay comparable. SOIL and ROOTS are "
      "checked against SEPARATE targets, because roots are far more variable and holding both "
      "to the same precision would need four to five times the cores. See Part 2, Appendix A10.",
      len(COLS))
header_row(ss, 4, COLS, W, ["y", "y"] + ["s"] * 20)
R0, R1 = 5, 4 + NROW_SITE
paint(ss, R0, R1, 1, "y"); paint(ss, R0, R1, 2, "y")
for col in range(3, 18):
    paint(ss, R0, R1, col, "s")
paint(ss, R0, R1, 18, "r")
for col in (19, 20, 21, 22):
    paint(ss, R0, R1, col, "g")

PS_LAST = 4 + NROW_PLOT
for r in range(R0, R1 + 1):
    ss.cell(r, 3, f'=IF($A{r}="","",COUNTIFS(\'5. Plot Summary\'!$B$5:$B${PS_LAST},$A{r},'
                  f'\'5. Plot Summary\'!$N$5:$N${PS_LAST},1))')
    # ---- soil block
    ss.cell(r, 4, f'=IF(OR($A{r}="",$C{r}=0),"",'
                  f'AVERAGEIFS(\'5. Plot Summary\'!$L$5:$L${PS_LAST},'
                  f'\'5. Plot Summary\'!$B$5:$B${PS_LAST},$A{r}))')
    # SD from sums of squares: portable, and no CSE array entry needed.
    ss.cell(r, 5, f'=IF(OR($A{r}="",NOT(ISNUMBER($C{r})),$C{r}<2),"",'
                  f'SQRT(MAX(0,(SUMIFS(\'5. Plot Summary\'!$Q$5:$Q${PS_LAST},'
                  f'\'5. Plot Summary\'!$B$5:$B${PS_LAST},$A{r})'
                  f'-$C{r}*$D{r}^2)/($C{r}-1))))')
    ss.cell(r, 6, f'=IF(OR($A{r}="",NOT(ISNUMBER($C{r})),$C{r}<2,NOT(ISNUMBER($E{r}))),"",'
                  f'TINV(1-TARGET_CONFIDENCE,$C{r}-1)*$E{r}/SQRT($C{r}))')
    ss.cell(r, 7, f'=IF(OR(NOT(ISNUMBER($F{r})),NOT(ISNUMBER($D{r})),$D{r}=0),"",$F{r}/$D{r})')
    ss.cell(r, 8, '=TARGET_MARGIN_SOIL')
    ss.cell(r, 9, f'=IF($A{r}="","",IF(OR(NOT(ISNUMBER($C{r})),$C{r}<2),'
                  f'"Cannot be assessed — at least 2 plots are needed for an interval.",'
                  f'IF(NOT(ISNUMBER($G{r})),"",'
                  f'IF($G{r}<=$H{r},"MET: ±"&TEXT($G{r},"0%")&" at "'
                  f'&TEXT(TARGET_CONFIDENCE,"0%")&" confidence",'
                  f'"NOT MET: ±"&TEXT($G{r},"0%")&" against a ±"&TEXT($H{r},"0%")&" target"))))')
    # ---- root block
    ss.cell(r, 10, f'=IF(OR($A{r}="",$C{r}=0),"",IFERROR('
                   f'AVERAGEIFS(\'5. Plot Summary\'!$M$5:$M${PS_LAST},'
                   f'\'5. Plot Summary\'!$B$5:$B${PS_LAST},$A{r}),""))')
    ss.cell(r, 11, f'=IF(OR($A{r}="",NOT(ISNUMBER($C{r})),$C{r}<2,NOT(ISNUMBER($J{r}))),"",'
                   f'SQRT(MAX(0,(SUMIFS(\'5. Plot Summary\'!$R$5:$R${PS_LAST},'
                   f'\'5. Plot Summary\'!$B$5:$B${PS_LAST},$A{r})'
                   f'-$C{r}*$J{r}^2)/($C{r}-1))))')
    ss.cell(r, 12, f'=IF(OR($A{r}="",NOT(ISNUMBER($C{r})),$C{r}<2,NOT(ISNUMBER($K{r}))),"",'
                   f'TINV(1-TARGET_CONFIDENCE,$C{r}-1)*$K{r}/SQRT($C{r}))')
    ss.cell(r, 13, f'=IF(OR(NOT(ISNUMBER($L{r})),NOT(ISNUMBER($J{r})),$J{r}=0),"",$L{r}/$J{r})')
    ss.cell(r, 14, '=TARGET_MARGIN_ROOT')
    ss.cell(r, 15, f'=IF($A{r}="","",IF(OR(NOT(ISNUMBER($C{r})),$C{r}<2),'
                   f'"Cannot be assessed — at least 2 plots are needed for an interval.",'
                   f'IF(NOT(ISNUMBER($M{r})),"No root data for this site.",'
                   f'IF($M{r}<=$N{r},"MET: ±"&TEXT($M{r},"0%")&" at "'
                   f'&TEXT(TARGET_CONFIDENCE,"0%")&" confidence",'
                   f'"NOT MET: ±"&TEXT($M{r},"0%")&" against a ±"&TEXT($N{r},"0%")&" target"))))')
    # ---- totals
    ss.cell(r, 16, f'=IF(OR($A{r}="",NOT(ISNUMBER($B{r}))),"",'
                   f'(IF(ISNUMBER($D{r}),$D{r},0)+IF(ISNUMBER($J{r}),$J{r},0))*$B{r})')
    ss.cell(r, 17, f'=IF(NOT(ISNUMBER($P{r})),"",$P{r}*CO2E_FACTOR/1000)')
    ss.cell(r, 18,
            f'=IF($A{r}="","",'
            f'IF($C{r}=0,"No plots carry this Site ID — check it matches the Plot & Site Log. ","")'
            f'&IF(AND(ISNUMBER($C{r}),$C{r}=1),'
            f'"Only one plot: a mean can be reported but never an uncertainty. ","")'
            f'&IF($B{r}="","No site area, so no total carbon. ","")'
            f'&IF(AND(ISNUMBER($G{r}),ISNUMBER($H{r}),$G{r}>$H{r}),'
            f'"Soil precision target missed — scrutinise the data, then post-stratify on '
            f'management before adding cores. ","")'
            f'&IF(AND(ISNUMBER($M{r}),ISNUMBER($N{r}),$M{r}>$N{r}),'
            f'"Root precision target missed. Roots are genuinely patchy; a wider honest interval '
            f'is better than a tight unearned one. ",""))')
    # ---- hidden: the pieces of the stratified study-area interval ----
    # mean and SD of (soil + root) per plot, within this site
    ss.cell(r, 19, f'=IF(OR($A{r}="",$C{r}=0),"",'
                   f'AVERAGEIFS(\'5. Plot Summary\'!$S$5:$S${PS_LAST},'
                   f'\'5. Plot Summary\'!$B$5:$B${PS_LAST},$A{r}))')
    ss.cell(r, 20, f'=IF(OR($A{r}="",NOT(ISNUMBER($C{r})),$C{r}<2,NOT(ISNUMBER($S{r}))),"",'
                   f'SQRT(MAX(0,(SUMIFS(\'5. Plot Summary\'!$T$5:$T${PS_LAST},'
                   f'\'5. Plot Summary\'!$B$5:$B${PS_LAST},$A{r})'
                   f'-$C{r}*$S{r}^2)/($C{r}-1))))')
    # this site's contribution to Var(stratified mean) = W_h^2 * s_h^2 / n_h
    ss.cell(r, 21, f'=IF(OR(NOT(ISNUMBER($T{r})),NOT(ISNUMBER($B{r})),'
                   f'SUM($B${R0}:$B${R1})=0,NOT(ISNUMBER($C{r})),$C{r}<2),0,'
                   f'($B{r}/SUM($B${R0}:$B${R1}))^2*$T{r}^2/$C{r})')
    # and to the degrees of freedom, sum(n_h - 1)
    ss.cell(r, 22, f'=IF(OR(NOT(ISNUMBER($C{r})),$C{r}<2),0,$C{r}-1)')

for col in (19, 20, 21, 22):
    ss.column_dimensions[openpyxl.utils.get_column_letter(col)].hidden = True

r = R1 + 3
band(ss, r, len(COLS), "  STUDY AREA — all sites combined, weighted by area")
r += 1
ss.cell(r, 1, "Total area (m²)").font = F_SUB
ss.cell(r, 2, f'=IF(SUM($B$5:$B${R1})=0,"",SUM($B$5:$B${R1}))')
r += 1
ss.cell(r, 1, "Total carbon (kg C)").font = F_SUB
ss.cell(r, 2, f'=IF(SUM($P$5:$P${R1})=0,"",SUM($P$5:$P${R1}))')
r += 1
ss.cell(r, 1, "Area-weighted mean (kg C/m²)").font = F_SUB
ss.cell(r, 2, f'=IF(OR(NOT(ISNUMBER($B${r-1})),NOT(ISNUMBER($B${r-2})),$B${r-2}=0),"",'
              f'$B${r-1}/$B${r-2})')
r += 1
ss.cell(r, 1, "Total (t CO₂e)").font = F_SUB
ss.cell(r, 2, f'=IF(NOT(ISNUMBER($B${r-2})),"",$B${r-2}*CO2E_FACTOR/1000)')
R_MEAN = r - 1          # the area-weighted mean row
R_TOTAL = r - 2         # total carbon
R_AREA = r - 3          # total area

# ── The study-area interval ──────────────────────────────────────────────────
# The area-weighted mean above is a STRATIFIED estimate: each site is a stratum,
# weighted by its area. Its variance is the standard one (Cochran 1977, ch. 5):
#     Var = sum_h ( W_h^2 * s_h^2 / n_h ),     W_h = area_h / total area
# with sum_h (n_h - 1) degrees of freedom. Both pieces are accumulated in the
# hidden columns U and V above. Without this the workbook reported a total with
# no interval at all, which is the one thing Part 2 tells you never to do.
r += 2
band(ss, r, len(COLS), "  STUDY-AREA INTERVAL — the sites combined as strata")
r += 1
ss.cell(r, 1, "Standard error (kg C/m²)").font = F_SUB
ss.cell(r, 2, f'=IF(SUM($U${R0}:$U${R1})=0,"",SQRT(SUM($U${R0}:$U${R1})))')
R_SE = r
r += 1
ss.cell(r, 1, "Degrees of freedom").font = F_SUB
ss.cell(r, 2, f'=IF(SUM($V${R0}:$V${R1})=0,"",SUM($V${R0}:$V${R1}))')
R_DF = r
r += 1
ss.cell(r, 1, "± half-width (kg C/m²)").font = F_SUB
ss.cell(r, 2, f'=IF(OR(NOT(ISNUMBER($B${R_SE})),NOT(ISNUMBER($B${R_DF})),$B${R_DF}<1),"",'
              f'TINV(1-TARGET_CONFIDENCE,$B${R_DF})*$B${R_SE})')
R_HALF = r
r += 1
ss.cell(r, 1, "Achieved margin").font = F_SUB
ss.cell(r, 2, f'=IF(OR(NOT(ISNUMBER($B${R_HALF})),NOT(ISNUMBER($B${R_MEAN})),$B${R_MEAN}=0),"",'
              f'$B${R_HALF}/$B${R_MEAN})')
R_ACH = r
r += 1
ss.cell(r, 1, "Study-area precision").font = F_SUB
ss.cell(r, 2, f'=IF(NOT(ISNUMBER($B${R_ACH})),"",'
              f'IF(COUNTIFS($A${R0}:$A${R1},"<>",$C${R0}:$C${R1},"<2")>0,'
              f'"INCOMPLETE — a site with fewer than 2 plots contributes no variance. ","")'
              f'&IF($B${R_ACH}<=TARGET_MARGIN_SOIL,'
              f'"MET: ±"&TEXT($B${R_ACH},"0%")&" at "&TEXT(TARGET_CONFIDENCE,"0%")'
              f'&" confidence",'
              f'"NOT MET: ±"&TEXT($B${R_ACH},"0%")&" against a ±"'
              f'&TEXT(TARGET_MARGIN_SOIL,"0%")&" target"))')
r += 1
ss.cell(r, 1, "Total carbon, ± (kg C)").font = F_SUB
ss.cell(r, 2, f'=IF(OR(NOT(ISNUMBER($B${R_HALF})),NOT(ISNUMBER($B${R_AREA}))),"",'
              f'$B${R_HALF}*$B${R_AREA})')

r += 2
note(ss, r, len(COLS),
     "Basis: soil to the REPORTING DEPTH, plus measured root carbon. The site mean uses the "
     "reporting-depth figure because cores reach different depths, and averaging full-profile "
     "stocks would describe no defined depth — a plot cored shallower would look like real "
     "variability rather than a shorter core. Full-profile figures are on the Plot Summary. "
     "Vegetation is reported "
     "separately on the Plot Summary and is deliberately NOT rolled into this total — it is a "
     "standing crop, not a stock. "
     "The study-area mean weights each site by its AREA, not by how many plots landed in it, "
     "and the interval above propagates the per-site spreads through that same weighting: "
     "Var = sum of W_h² · s_h² / n_h, on sum(n_h − 1) degrees of freedom. Note that individual "
     "sites can miss their own targets while the study-area figure meets its, because "
     "combining strata pools the information — that is what stratifying buys.")

# ── R1. Reference ────────────────────────────────────────────────────────────
rf = wb.create_sheet("R1. Reference")
for col, w in zip("ABCD", (24, 30, 74, 18)):
    rf.column_dimensions[col].width = w
title(rf, "REFERENCE TABLES", "Lookups and the published ranges behind the defaults.", 4)

r = 4
band(rf, r, 4, "CARBON FRACTION OF DRY BIOMASS")
r += 1
note(rf, r, 4, "The workbook defaults to 0.5 for both shoots and roots. Root tissue is often "
                "reported a little lower than shoot tissue. Calibrate against CHN if you can.")
r += 1
header_row(rf, r, ["Factor", "Source", "Note", ""])
for f, src, nt in CARBON_FACTORS:
    r += 1
    rf.cell(r, 1, f).font = F_SUB
    rf.cell(r, 2, src).font = F_N
    rf.cell(r, 3, nt).alignment = WRAP
    rf.row_dimensions[r].height = 26

r += 2
band(rf, r, 4, "BULK DENSITY BASIS — and the double-correction trap")
r += 1
note(rf, r, 4, "Rocks hold no carbon. Labs report bulk density on one of two bases and they are "
                "NOT interchangeable. Correcting twice understates a stony site by as much as a "
                "third; not correcting at all overstates it by the same.")
r += 1
header_row(rf, r, ["Basis", "Meaning", "What the workbook does", ""])
for b, mean, does in [
    ("Fine earth / total volume",
     "Mass of the <2 mm fraction divided by the WHOLE sample volume.",
     "Uses it as-is. Coarse fragments are already accounted for."),
    ("Fine earth / fine-earth volume",
     "Mass of the <2 mm fraction divided by only the volume that fraction occupies.",
     "Multiplies by (1 − coarse fragment %) to convert to a total-volume basis."),
    ("Not confirmed", "You have not asked the lab yet.",
     "Uses the value as-is AND raises a flag. Ask the lab."),
]:
    r += 1
    rf.cell(r, 1, b).font = F_SUB
    rf.cell(r, 2, mean).alignment = WRAP
    rf.cell(r, 3, does).alignment = WRAP
    rf.row_dimensions[r].height = 32

r += 2
band(rf, r, 4, "ROOT DIAMETER CLASSES")
r += 1
note(rf, r, 4, "The ≤2 mm cutoff for 'fine' roots is near-universal and functionally arbitrary — "
                "it lumps absorptive roots that live weeks with transport roots that live years. "
                "The workshop keeps it because a field crew can apply it consistently with a "
                "sieve, not because it is a biological boundary.")
r += 1
header_row(rf, r, ["Class", "Turnover", "Where the carbon goes", "Recovery from a core"])
for cls, turn, goes, rec in [
    ("≤ 2 mm (fine)", "Fast — much of it annual", "Straight into soil organic matter",
     "POOR — the finest pass through the sieve and are lost"),
    ("> 2 mm (coarse)", "Slow", "Stays as biomass for years", "Good"),
]:
    r += 1
    rf.cell(r, 1, cls).font = F_SUB
    for i, v in enumerate((turn, goes, rec), start=2):
        rf.cell(r, i, v).alignment = WRAP
    rf.row_dimensions[r].height = 30

r += 2
band(rf, r, 4, "GRASSLAND TYPES")
r += 1
header_row(rf, r, ["Type", "Character", "What changes in the method", ""])
for t, ch, ch2 in [
    ("Prairie", "Mixed-grass, fescue. Deep dark soils.",
     "The baseline case. Stratify on grazing and management first."),
    ("Aspen parkland", "Grassland matrix with aspen groves.",
     "Shrub/medium plot carries more weight; the boundary with Forests matters."),
    ("Black Oak savannah", "Scattered open-grown oaks; fire-maintained; sandy soils.",
     "Tree protocol applies. Fire history is a stratification variable, not context."),
    ("Interior BC bunchgrass", "Semi-arid; shallow soils; coarse fragments common.",
     "The coarse-fragment correction is mandatory. Shallow-soil method; record depth to refusal."),
]:
    r += 1
    rf.cell(r, 1, t).font = F_SUB
    rf.cell(r, 2, ch).alignment = WRAP
    rf.cell(r, 3, ch2).alignment = WRAP
    rf.row_dimensions[r].height = 30

wb.save(OUT)
print("part 3 written:", wb.sheetnames)
