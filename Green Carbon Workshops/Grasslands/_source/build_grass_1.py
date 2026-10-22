"""Grassland_Carbon_Calculator.xlsx -- part 1: instructions, settings,
reference and the Fill Me In index. Creates the workbook."""
import sys, openpyxl
sys.path.insert(0, "/home/user/Terrestrial_Carbon_Workshops_V1/Grasslands/_source")
from grass_style import *   # noqa
from openpyxl.workbook.defined_name import DefinedName

wb = openpyxl.Workbook()

# ── 0. Instructions ──────────────────────────────────────────────────────────
ws = wb.active
ws.title = "0. Instructions"
for col, w in zip("ABCD", (26, 62, 22, 46)):
    ws.column_dimensions[col].width = w
title(ws, "GRASSLAND CARBON CALCULATOR",
      "WWF-Canada Carbon Measurement · Grassland Carbon Workshop", 4)

r = 4
ws.cell(r, 1, "What this workbook does").font = F_SUB
ws.cell(r, 2, "Turns soil cores, separated roots and clipped vegetation into a carbon "
              "stock in kg C/m², scales plots to sites and to your study area, and checks "
              "the precision you achieved against the target you set in Part 2.").alignment = WRAP
ws.row_dimensions[r].height = 46

r += 2
band(ws, r, 4, "COLOUR KEY")
keys = [("Yellow", "y", "TYPE HERE — field measurements you record."),
        ("Blue", "b", "TYPE HERE — lab results, once they come back."),
        ("Orange", "o", "NEEDS YOUR INPUT — a value this workshop cannot supply. "
                        "Every one has a working default and a flag that stays lit until you replace it. "
                        "They are all listed on '8. Fill Me In'."),
        ("Grey", "g", "Calculated for you. Do not type in grey cells."),
        ("Green", "s", "Summary — calculated."),
        ("Red", "r", "A QC flag. Read it; it is an instruction, not a decoration.")]
for name, key, desc in keys:
    r += 1
    c = ws.cell(r, 1, name); c.fill, c.border, c.font = FILL[key], BOX, F_N
    ws.cell(r, 2, desc).alignment = WRAP
    ws.row_dimensions[r].height = 30 if key != "o" else 46

r += 2
band(ws, r, 4, "FILL THE TABS IN THIS ORDER — each one joins to the ones above it")
order = [
    ("1. Plot & Site Log", "One row per plot. Everything keys to Plot ID, so fill this first."),
    ("2. Soil Data", "One row per depth increment per core. Joins on Plot ID and Core ID."),
    ("3. Root Biomass", "One row per increment per diameter class per live/dead state."),
    ("4. Vegetation Data", "One row per plot. Clip-and-weigh, shrubs, and tree carbon carried "
                           "across from the Forests calculator."),
    ("5. Plot Summary", "Calculated. One row per plot."),
    ("6. Site Summary", "Calculated, except Site ID and site area. Soil and roots are "
                        "checked against SEPARATE precision targets."),
    ("7. Settings", "Everything the workbook assumes. Orange rows need you."),
    ("8. Fill Me In", "Every orange cell in one list, with what happens if you leave it."),
    ("R1. Reference", "Lookup tables — carbon fractions, grassland types, the bulk-density "
                      "basis question."),
]
for name, desc in order:
    r += 1
    ws.cell(r, 1, name).font = F_SUB
    ws.cell(r, 2, desc).alignment = WRAP
    ws.row_dimensions[r].height = 30

r += 2
band(ws, r, 4, "THREE THINGS THIS WORKBOOK WILL NOT LET YOU SKIP", fill=ORANGE)
warns = [
    ("Roots and soil carbon can be double counted",
     "Soil carbon analysis conventionally removes visible roots, but fine roots stay in the "
     "sample. If root carbon is then added to a soil stock that already contains it, the same "
     "carbon is counted twice. ROOT_SOIL_REPORTING_BOUNDARY records which roots the soil "
     "sample no longer contains; until it is agreed with the lab, the Plot Summary refuses to "
     "add the two pools."),
    ("30 cm is a floor, not a total",
     "Native grassland roots reach metres. A root total whose deepest increment is simply the "
     "bottom of the core is a MINIMUM, and the Plot Summary flags it as one."),
    ("A standing crop is not a stock",
     "Clipped vegetation grows from nothing each spring and is gone by autumn. It is reported "
     "in its own column and never merged into the soil figure."),
]
for head, body in warns:
    r += 1
    ws.cell(r, 1, head).font = F_WARN
    ws.cell(r, 2, body).alignment = WRAP
    ws.row_dimensions[r].height = 58

# ── 7. Settings ──────────────────────────────────────────────────────────────
st = wb.create_sheet("7. Settings")
for col, w in zip("ABC", (32, 12, 96)):
    st.column_dimensions[col].width = w
title(st, "SETTINGS",
      "Everything the calculator assumes lives here. Change it once and every sheet follows. "
      "Orange rows are values only you can supply.", 3)

header_row(st, 4, ["Parameter", "Value", "What it does"])
SETTINGS = [
    ("CARBON_FRACTION_BIOMASS", 0.5, "o",
     "Fraction of dry ABOVE-GROUND plant biomass that is carbon. 0.5 is the convention used "
     "across this series."),
    ("CARBON_FRACTION_ROOT", 0.5, "o",
     "Fraction of dry ROOT biomass that is carbon. Set equal to the shoot value by default; "
     "published root values often run a little lower. See 'R1. Reference'."),
    ("CO2E_FACTOR", 3.67, "g", "Multiply kg C by this to report CO₂ equivalents."),
    ("SOIL_REPORTING_DEPTH_CM", 30, "o",
     "The fixed depth every core is reported to, ALONGSIDE the full profile. 30 cm is the IPCC "
     "default and what makes your number comparable. It is a floor, not the total."),
    ("ROOT_SOIL_REPORTING_BOUNDARY", "Not agreed with the lab", "o",
     "WHICH roots the soil-carbon sample no longer contains, agreed with the lab in writing "
     "before sampling. 'Root-separated soil' = roots removed by the project's defined procedure, "
     "so soil and root pools may be added. 'Operational soil fraction' = the lab removed only "
     "what its standard preparation picks out, so finer roots are already inside the soil "
     "number and an overlapping root estimate must NOT be added to it."),
    ("ROOT_SOIL_BOUNDARY_SOURCE", "", "o",
     "Who agreed the boundary above, under which written method, and on what date. A boundary "
     "with no source is an assumption, not a method."),
    ("ROOT_SIEVE_MM", 0.5, "o",
     "Finest sieve mesh used to recover roots, mm. Roots finer than this are lost, so the "
     "fine-root figure is a known underestimate and cannot be interpreted without this number."),
    ("ASH_CORRECTED", "No", "o",
     "Was root mass corrected for adhering mineral soil by ashing a subsample? Uncorrected root "
     "mass is systematically too high."),
    ("ROOT_DRY_TEMP_C", 65, "o",
     "Temperature roots were dried at. Roots dry at 60–70 °C; soil bulk density at 105 °C."),
    ("COMPARABLE_SEASON_RULE", "", "o",
     "The project's OWN rule for when two clip-and-weigh samples count as comparable, written "
     "out — the phenological stage, the window around it, and what disqualifies a plot. Each "
     "plot then records whether it met the rule, on '4. Vegetation Data'. A blank here means "
     "no plot can honestly answer that question."),
    ("LAB_BULK_DENSITY_BASIS", "Not confirmed", "o",
     "The volume the LAB divides dry mass by when it reports bulk density. 'total volume' = "
     "the whole cored volume, coarse fragments included, so no further coarse-fragment "
     "correction belongs in this workbook. 'fine-earth volume' = stones already excluded, so "
     "the workbook applies the correction. Getting this wrong corrects once too often or not "
     "at all, and Soil Data flags every row that disagrees with it."),
    ("LAB_METHOD_REFERENCE", "", "o",
     "Laboratory, method code or SOP number, and the date the bulk-density basis and the "
     "root/soil boundary above were confirmed. This is the record the two settings point to."),
    ("SMALL_PLOT_AREA_M2", 0.25, "g",
     "Default clip-and-weigh quadrat area. 0.25 m², or a circle of radius 0.28 m."),
    ("MEDIUM_PLOT_AREA_M2", 100, "g", "Default medium (shrub) plot area. 16–100 m²."),
    ("LARGE_PLOT_AREA_M2", 400, "g", "Default large (tree) plot area."),
    ("TARGET_MARGIN_SOIL", 0.2, "o",
     "Precision target for SOIL carbon, as a fraction of the mean."),
    ("TARGET_MARGIN_ROOT", 0.4, "o",
     "Precision target for ROOT biomass. Deliberately looser than soil — roots are far more "
     "variable, so the same target would need four to five times the cores. See Part 2, A10."),
    ("TARGET_CONFIDENCE", 0.9, "g", "Confidence level for the targets and all reported intervals."),
    ("QC_BD_MIN", 0.6, "g", "Minimum plausible bulk density for a mineral grassland soil, g/cm³."),
    ("QC_BD_MAX", 1.8, "g", "Maximum plausible bulk density, g/cm³. Above this suggests a "
                            "compacted or mis-measured sample."),
    ("QC_CARBON_PCT_MAX", 20, "g",
     "Flag soil organic carbon above this per cent. Grassland topsoil usually runs 2–8%; much "
     "higher suggests an organic horizon or a units error."),
    ("QC_RECOVERY_MIN", 0.9, "g",
     "Minimum acceptable ratio of core length recovered to depth driven."),
]
r = 5
for name, val, fill, desc in SETTINGS:
    st.cell(r, 1, name).font = F_SUB
    c = st.cell(r, 2, val); c.fill, c.border, c.font = FILL[fill], BOX, F_N
    st.cell(r, 3, desc).alignment = WRAP
    st.row_dimensions[r].height = 34
    wb.defined_names.add(DefinedName(name, attr_text=f"'7. Settings'!$B${r}"))
    r += 1

# Controlled lists, keyed by name rather than row number so the block survives
# a setting being inserted above it.
_ROW = {name: 5 + i for i, (name, *_rest) in enumerate(SETTINGS)}
dv(st, 2, _ROW["ROOT_SOIL_REPORTING_BOUNDARY"], _ROW["ROOT_SOIL_REPORTING_BOUNDARY"],
   ROOT_SOIL_BOUNDARY_OPTIONS)
dv(st, 2, _ROW["ASH_CORRECTED"], _ROW["ASH_CORRECTED"], ["Yes", "No"])
dv(st, 2, _ROW["LAB_BULK_DENSITY_BASIS"], _ROW["LAB_BULK_DENSITY_BASIS"], BD_BASIS)

# ── 8. Fill Me In ────────────────────────────────────────────────────────────
fm = wb.create_sheet("8. Fill Me In")
for col, w in zip("ABCDE", (32, 18, 54, 14, 62)):
    fm.column_dimensions[col].width = w
title(fm, "FILL ME IN",
      "Every value in this workbook that only you can supply, in one list. Each has a working "
      "default, so the workbook computes from the moment you open it — but the defaults are "
      "assumptions, and each one stays flagged until you replace it.", 5)

header_row(fm, 4, ["What", "Where it lives", "What it is", "Default",
                   "What happens if you leave it"])
r = 5
for name, tab, what, default, consequence in FILL_ME_IN:
    fm.cell(r, 1, name).font = F_SUB
    fm.cell(r, 2, tab).font = F_N
    fm.cell(r, 3, what).alignment = WRAP
    c = fm.cell(r, 4, default); c.fill, c.border, c.font = FILL["o"], BOX, F_N
    fm.cell(r, 5, consequence).alignment = WRAP
    fm.row_dimensions[r].height = 42
    r += 1

r += 1
band(fm, r, 5, "PLANNING PRIORS — not used in any calculation, recorded so the design is "
                "auditable", fill=ORANGE)
r += 1
fm.cell(r, 1, "Regional SOC prior — mean (kg C/m²)").font = F_SUB
paint(fm, r, r, 4, "o")
r += 1
fm.cell(r, 1, "Regional SOC prior — CV").font = F_SUB
paint(fm, r, r, 4, "o")
r += 1
fm.cell(r, 1, "Regional root CV prior").font = F_SUB
paint(fm, r, r, 4, "o")
r += 1
fm.cell(r, 1, "Source of the above").font = F_SUB
paint(fm, r, r, 4, "o")
r += 1
note(fm, r, 5, "Part 2 sizes the campaign from these. A CV read off a modelled map understates "
                "plot-scale variance and must be inflated — or replaced with a pilot estimate — "
                "before it sizes anything.")

wb.save(OUT)
print("part 1 written:", wb.sheetnames)
