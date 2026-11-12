"""Grassland_Carbon_Calculator.xlsx -- part 2: the data tabs.
1. Plot & Site Log · 2. Soil Data · 3. Root Biomass · 4. Vegetation Data
"""
import sys, openpyxl
sys.path.insert(0, "/home/user/Terrestrial_Carbon_Workshops_V1/Grasslands/_source")
from grass_style import *   # noqa

wb = openpyxl.load_workbook(OUT)

# ── 1. Plot & Site Log ───────────────────────────────────────────────────────
pl = wb.create_sheet("1. Plot & Site Log", 1)
COLS = ["Plot ID", "Site ID", "Study area", "Date", "Location", "Latitude", "Longitude",
        "GNSS accuracy (m)", "Datum", "Elevation (m)", "Grassland type", "Management",
        "Grazing regime", "Years since fire", "Cultivation history", "Restoration year",
        "Native or seeded", "Canopy cover (%)", "Slope position", "Notes"]
W = [12, 10, 12, 12, 22, 11, 11, 11, 10, 11, 18, 22, 14, 12, 22, 13, 18, 12, 14, 34]
title(pl, "PLOT & SITE LOG",
      "ONE ROW PER PLOT. Fill this in first — everything joins to it on Plot ID. "
      "Management, grazing and fire are not optional context: they are the stratification "
      "variables, and they are what lets you post-stratify if your interval comes out wide.",
      len(COLS))
header_row(pl, 4, COLS, W, ["y"] * len(COLS))
for col in range(1, len(COLS) + 1):
    paint(pl, 5, 4 + NROW_PLOT, col, "y")
dv(pl, 11, 5, 4 + NROW_PLOT, GRASSLAND_TYPES)
dv(pl, 12, 5, 4 + NROW_PLOT, MANAGEMENT)
dv(pl, 13, 5, 4 + NROW_PLOT, GRAZING)
dv(pl, 15, 5, 4 + NROW_PLOT, CULTIVATION)
dv(pl, 17, 5, 4 + NROW_PLOT, NATIVE_SEEDED)

# ── 2. Soil Data ─────────────────────────────────────────────────────────────
sd = wb.create_sheet("2. Soil Data", 2)
COLS = ["Plot ID", "Core ID", "Increment #", "Top depth (cm)", "Bottom depth (cm)",
        "Thickness (cm)", "Corer internal diameter (cm)", "Depth driven (cm)",
        "Length recovered (cm)", "Recovery ratio", "Coarse fragments (% vol)",
        "Bulk density basis", "Bulk density (g/cm³)", "Organic carbon (%)",
        "BD used (g/cm³)", "Stock, increment (kg C/m²)",
        "Thickness within reporting depth (cm)", "Stock to reporting depth (kg C/m²)",
        "QC flags", "Notes", "_first_of_core"]
W = [12, 12, 11, 11, 12, 11, 12, 12, 12, 11, 13, 20, 13, 12, 12, 15, 15, 15, 46, 30, 8]
FILLS = ["y","y","y","y","y","g","y","y","y","g","y","o","b","b","g","g","g","g","r","y","g"]
title(sd, "SOIL DATA",
      "ONE ROW PER DEPTH INCREMENT PER CORE. Record the ACTUAL top and bottom depths, not the "
      "ones you planned — a truncated increment scaled as a full one is a silent error. "
      "Bulk density and carbon come back from the lab.", len(COLS))
header_row(sd, 4, COLS, W, FILLS)
R0, R1 = 5, 4 + NROW_SOIL
for col, f in enumerate(FILLS, start=1):
    paint(sd, R0, R1, col, f)
dv(sd, 12, R0, R1, BD_BASIS)

for r in range(R0, R1 + 1):
    # thickness
    sd.cell(r, 6, f'=IF(OR($D{r}="",$E{r}=""),"",$E{r}-$D{r})')
    # recovery ratio
    sd.cell(r, 10, f'=IF(OR(NOT(ISNUMBER($H{r})),NOT(ISNUMBER($I{r})),$H{r}=0),"",$I{r}/$H{r})')
    # BD used: correct for coarse fragments ONLY when the lab reported fine-earth/fine-earth volume
    sd.cell(r, 15,
            f'=IF(NOT(ISNUMBER($M{r})),"",'
            f'IF($L{r}="Fine earth / fine-earth volume",'
            f'$M{r}*(1-IF(ISNUMBER($K{r}),$K{r},0)/100),$M{r}))')
    # stock for the increment, kg C/m2  = BD (g/cm3) * (%C/100) * thickness (cm) * 10
    sd.cell(r, 16,
            f'=IF(OR(NOT(ISNUMBER($O{r})),NOT(ISNUMBER($N{r})),NOT(ISNUMBER($F{r}))),"",'
            f'$O{r}*($N{r}/100)*$F{r}*10)')
    # thickness lying within the reporting depth
    sd.cell(r, 17,
            f'=IF(OR(NOT(ISNUMBER($D{r})),NOT(ISNUMBER($E{r}))),"",'
            f'MAX(0,MIN($E{r},SOIL_REPORTING_DEPTH_CM)-MIN($D{r},SOIL_REPORTING_DEPTH_CM)))')
    sd.cell(r, 18,
            f'=IF(OR(NOT(ISNUMBER($O{r})),NOT(ISNUMBER($N{r})),NOT(ISNUMBER($Q{r}))),"",'
            f'$O{r}*($N{r}/100)*$Q{r}*10)')
    # QC flags
    sd.cell(r, 19,
            f'=IF(AND($A{r}="",$B{r}="",$D{r}=""),"",'
            f'IF(AND($A{r}<>"",COUNTIF(\'1. Plot & Site Log\'!$A$5:$A${4+NROW_PLOT},$A{r})=0),'
            f'"Plot ID not in the Plot & Site Log. ","")'
            f'&IF(AND(ISNUMBER($D{r}),ISNUMBER($E{r}),$E{r}<=$D{r}),'
            f'"Bottom depth is not below top depth. ","")'
            f'&IF($L{r}="Not confirmed","Bulk-density basis not confirmed with the lab — the '
            f'coarse-fragment correction may be wrong or doubled. ","")'
            # The row records what the lab actually reported for THIS sample; the
            # setting records what the project agreed with the lab in writing. They
            # should be the same, and a disagreement is worth catching before it
            # propagates into every stock on the sheet.
            f'&IF(LAB_BULK_DENSITY_BASIS="Not confirmed",'
            f'"No lab bulk-density basis is on file in Settings (LAB_BULK_DENSITY_BASIS), so '
            f'nothing checks this row. ","")'
            f'&IF(AND($L{r}<>"",LAB_BULK_DENSITY_BASIS<>"Not confirmed",'
            f'$L{r}<>LAB_BULK_DENSITY_BASIS),'
            f'"This row\'s bulk-density basis disagrees with the lab method on file. One of "'
            f'&"the two is wrong, and the coarse-fragment correction follows the row. ","")'
            f'&IF(AND(ISNUMBER($M{r}),OR($M{r}<QC_BD_MIN,$M{r}>QC_BD_MAX)),'
            f'"Bulk density outside the plausible range for a mineral grassland soil. ","")'
            f'&IF(AND(ISNUMBER($N{r}),$N{r}>QC_CARBON_PCT_MAX),'
            f'"Organic carbon above the QC ceiling — check units, and whether this is an '
            f'organic horizon. ","")'
            f'&IF(AND(ISNUMBER($J{r}),$J{r}<QC_RECOVERY_MIN),'
            f'"Recovered less than the QC minimum of the depth driven — the increments may not '
            f'sit where you think. Do NOT stretch them back out. ","")'
            f'&IF(AND(ISNUMBER($K{r}),$K{r}>0,$L{r}="Fine earth / total volume"),'
            f'"Coarse fragments recorded and the lab basis already accounts for them — no '
            f'further correction applied, which is correct. ",""))')
    # portable "is this the first row for this Core ID?" marker.
    # COUNTIFS over an expanding range works in Excel and LibreOffice alike;
    # UNIQUE()/FILTER() are Excel-365 only and silently break elsewhere.
    sd.cell(r, 21, f'=IF($B{r}="",0,IF(COUNTIFS($B$5:$B{r},$B{r})=1,1,0))')

# ── 3. Root Biomass ──────────────────────────────────────────────────────────
rt = wb.create_sheet("3. Root Biomass", 3)
COLS = ["Plot ID", "Core ID", "Top depth (cm)", "Bottom depth (cm)", "Diameter class",
        "Live or dead", "Oven-dry mass (g)", "Ash fraction (0–1)", "Sieve mesh (mm)",
        "Corrected mass (g)", "Corer internal diameter (cm)", "Core area (cm²)",
        "Root mass (g/m²)", "Root carbon (kg C/m²)", "QC flags", "Notes", "_first_of_core"]
W = [12, 12, 11, 12, 16, 12, 13, 13, 12, 13, 12, 12, 13, 14, 46, 30, 8]
FILLS = ["y","y","y","y","y","y","b","b","y","g","g","g","g","g","r","y","g"]
title(rt, "ROOT BIOMASS",
      "ONE ROW PER INCREMENT PER DIAMETER CLASS PER LIVE/DEAD STATE. This is MEASURED root "
      "mass, not a root:shoot ratio. Mass is oven-dry at 60–70 °C — not the 105 °C used for "
      "soil bulk density. Ash fraction corrects for mineral soil still clinging to the roots "
      "after washing; without it root mass is systematically too high.", len(COLS))
header_row(rt, 4, COLS, W, FILLS)
R0, R1 = 5, 4 + NROW_ROOT
for col, f in enumerate(FILLS, start=1):
    paint(rt, R0, R1, col, f)
dv(rt, 5, R0, R1, ROOT_CLASS)
dv(rt, 6, R0, R1, ROOT_STATE)

SD_LAST = 4 + NROW_SOIL
for r in range(R0, R1 + 1):
    # ash-corrected mass, only when the correction was actually applied
    rt.cell(r, 10,
            f'=IF(NOT(ISNUMBER($G{r})),"",'
            f'IF(AND(ASH_CORRECTED="Yes",ISNUMBER($H{r})),$G{r}*(1-$H{r}),$G{r}))')
    # corer diameter, looked up from the soil data for this core
    rt.cell(r, 11,
            f'=IF($B{r}="","",IFERROR(AVERAGEIFS(\'2. Soil Data\'!$G$5:$G${SD_LAST},'
            f'\'2. Soil Data\'!$B$5:$B${SD_LAST},$B{r}),""))')
    # core cross-sectional area, cm2
    rt.cell(r, 12, f'=IF(NOT(ISNUMBER($K{r})),"",PI()*($K{r}/2)^2)')
    # g per m2
    rt.cell(r, 13,
            f'=IF(OR(NOT(ISNUMBER($J{r})),NOT(ISNUMBER($L{r})),$L{r}=0),"",$J{r}/$L{r}*10000)')
    # kg C per m2
    rt.cell(r, 14,
            f'=IF(NOT(ISNUMBER($M{r})),"",$M{r}*CARBON_FRACTION_ROOT/1000)')
    rt.cell(r, 15,
            f'=IF(AND($A{r}="",$B{r}="",$G{r}=""),"",'
            f'IF(AND($B{r}<>"",COUNTIFS(\'2. Soil Data\'!$B$5:$B${SD_LAST},$B{r})=0),'
            f'"Core ID not found in Soil Data, so the corer diameter cannot be looked up. ","")'
            f'&IF(ASH_CORRECTED<>"Yes",'
            f'"Root mass is NOT ash-corrected, so it includes adhering mineral soil and is too '
            f'high. Set ASH_CORRECTED once you have done it. ","")'
            f'&IF(AND(ASH_CORRECTED="Yes",NOT(ISNUMBER($H{r}))),'
            f'"Ash correction is switched on but no ash fraction is given for this row. ","")'
            f'&IF($I{r}="","Sieve mesh not recorded — a fine-root figure cannot be interpreted '
            f'without it. ","")'
            f'&IF(AND(ISNUMBER($H{r}),$H{r}>0.5),'
            f'"Ash fraction above 0.5 — over half this sample was mineral soil. Re-wash. ","")'
            f'&IF($F{r}="Not separated","Live and dead not separated. Fine for a stock, but "'
            f'&"note it in reporting. ",""))')
    rt.cell(r, 17, f'=IF($B{r}="",0,IF(COUNTIFS($B$5:$B{r},$B{r})=1,1,0))')

# ── 4. Vegetation Data ───────────────────────────────────────────────────────
vg = wb.create_sheet("4. Vegetation Data", 4)
# Phenology is recorded in three separate fields, not one yes/no. The stage is
# an observation; whether the plot is comparable is a judgement against the
# project's own written rule (COMPARABLE_SEASON_RULE); and removal by grazing or
# mowing is a third, independent fact about what is standing there. Collapsing
# them loses the reason a plot is or is not comparable, which is the part a
# reader needs.
COLS = ["Plot ID", "Sampling date", "Phenological stage", "Recent grazing / removal",
        "Comparable-season criterion met?", "Small plot area (m²)",
        "Clip dry mass — LIVE (g)", "Clip dry mass — DEAD (g)",
        "Herbaceous carbon (kg C/m²)", "Medium plot area (m²)",
        "Shrub biomass, total (kg)", "Shrub carbon (kg C/m²)",
        "Canopy cover (%)", "Tree carbon (kg C/m²) — from Forests calculator",
        "TOTAL vegetation (kg C/m²)", "QC flags", "Notes"]
W = [12, 13, 20, 19, 18, 13, 15, 15, 15, 13, 14, 14, 12, 30, 15, 52, 30]
FILLS = ["y","y","y","y","y","y","b","b","g","y","b","g","y","y","g","r","y"]
title(vg, "VEGETATION DATA",
      "ONE ROW PER PLOT. This is a STANDING CROP, not a stock — it grows from nothing each "
      "spring and is gone by autumn, so it is reported in its own column and never merged into "
      "the soil figure. Record the stage you found it at, not the stage you wanted.",
      len(COLS))
header_row(vg, 4, COLS, W, FILLS)
R0, R1 = 5, 4 + NROW_VEG
for col, f in enumerate(FILLS, start=1):
    paint(vg, R0, R1, col, f)
dv(vg, 3, R0, R1, PHENOLOGICAL_STAGES)
dv(vg, 4, R0, R1, RECENT_REMOVAL)
dv(vg, 5, R0, R1, COMPARABLE_SEASON)

for r in range(R0, R1 + 1):
    # herbaceous: (live + dead) g over the quadrat area -> g/m2 -> kg C/m2
    vg.cell(r, 9,
            f'=IF(OR(NOT(ISNUMBER($F{r})),$F{r}=0,'
            f'AND(NOT(ISNUMBER($G{r})),NOT(ISNUMBER($H{r})))),"",'
            f'(IF(ISNUMBER($G{r}),$G{r},0)+IF(ISNUMBER($H{r}),$H{r},0))'
            f'/$F{r}*CARBON_FRACTION_BIOMASS/1000)')
    # shrubs: kg over the medium plot -> kg C/m2
    vg.cell(r, 12,
            f'=IF(OR(NOT(ISNUMBER($K{r})),NOT(ISNUMBER($J{r})),$J{r}=0),"",'
            f'$K{r}*CARBON_FRACTION_BIOMASS/$J{r})')
    vg.cell(r, 15,
            f'=IF($A{r}="","",IF(ISNUMBER($I{r}),$I{r},0)+IF(ISNUMBER($L{r}),$L{r},0)'
            f'+IF(ISNUMBER($N{r}),$N{r},0))')
    vg.cell(r, 16,
            f'=IF($A{r}="","",'
            f'IF(COUNTIF(\'1. Plot & Site Log\'!$A$5:$A${4+NROW_PLOT},$A{r})=0,'
            f'"Plot ID not in the Plot & Site Log. ","")'
            f'&IF(COMPARABLE_SEASON_RULE="",'
            f'"No comparable-season rule is written down in Settings, so no plot can say "'
            f'&"whether it met one. ","")'
            f'&IF($E{r}="No",'
            f'"Did NOT meet the project comparable-season rule. Usable on its own, but do not "'
            f'&"pool it with plots that did, or compare it to another visit. ","")'
            f'&IF($E{r}="Not assessed",'
            f'"Comparability against the season rule has not been assessed for this plot. ","")'
            f'&IF($C{r}="Unknown",'
            f'"Phenological stage unknown — a standing crop with no stage attached cannot be "'
            f'&"interpreted or repeated. ","")'
            f'&IF($B{r}="","No sampling date. A clip-and-weigh without a date cannot be '
            f'interpreted. ","")'
            f'&IF(OR($D{r}="Grazing — heavy",$D{r}="Hayed / mown",$D{r}="Burned"),'
            f'"Standing material was removed before clipping, so this is what SURVIVED, not "'
            f'&"what grew. Report it as such. ","")'
            f'&IF($D{r}="Unknown",'
            f'"Recent removal unknown — the clip cannot be separated from grazing loss. ","")'
            f'&IF(AND(ISNUMBER($M{r}),$M{r}>0,NOT(ISNUMBER($N{r}))),'
            f'"Canopy cover is recorded but no tree carbon is entered — any tree over 2 m "'
            f'&"goes through the Forests protocol. ","")'
            f'&IF(AND(ISNUMBER($K{r}),$K{r}>0),'
            f'"Shrub figures are ABOVE-ground only; shrub roots are in neither this pool nor "'
            f'&"the soil core. Declare the gap. ",""))')

wb.save(OUT)
print("part 2 written:", wb.sheetnames)
