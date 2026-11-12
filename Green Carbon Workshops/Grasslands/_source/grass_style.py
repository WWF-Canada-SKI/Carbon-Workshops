"""Shared style and reference data for Grassland_Carbon_Calculator.xlsx.

Forked from Wetlands/_source/wet_style.py. The one structural addition is
ORANGE -- "NEEDS YOUR INPUT" -- a fourth colour in the key for values the
workshop cannot supply and must not invent. Every orange cell carries a
working default so the workbook computes end to end from the moment it is
opened, and a QC advisory that fires while the default is still in place.
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUT = ("/home/user/Terrestrial_Carbon_Workshops_V1/Grasslands/"
       "04_Data_Interpretation/calculators/Grassland_Carbon_Calculator.xlsx")

# ── house style ──────────────────────────────────────────────────────────────
NAVY   = "4A3421"          # headers -- grassland soil brown
YELLOW = "FFF2CC"          # type here (field)
GREY   = "EDEDED"          # calculated
BLUE   = "DDEBF7"          # lab result
GREEN  = "E2EFDA"          # summary
RED    = "FCE4E4"          # flag
ORANGE = "FBE2D5"          # NEEDS YOUR INPUT

F_H   = Font(bold=True, color="FFFFFF", size=10)
F_SUB = Font(bold=True, color=NAVY, size=10)
F_N   = Font(size=10)
F_IT  = Font(italic=True, size=9, color="666666")
F_WARN = Font(bold=True, color="9C4221", size=10)
FILL_H = PatternFill("solid", fgColor=NAVY)
FILL = {k: PatternFill("solid", fgColor=v) for k, v in
        dict(y=YELLOW, g=GREY, b=BLUE, s=GREEN, r=RED, o=ORANGE).items()}
THIN = Side(style="thin", color="BFBFBF")
BOX  = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
CTR  = Alignment(horizontal="center", vertical="center", wrap_text=True)

CULTIVATION = ["Never cultivated", "Cultivated, reseeded", "Cultivated, abandoned",
               "Long-term tame pasture", "Unknown"]

NROW_PLOT = 60      # rows on 1. Plot & Site Log
NROW_SOIL = 600     # rows on 2. Soil Data
NROW_ROOT = 900     # rows on 3. Root Biomass
NROW_VEG  = 60      # rows on 4. Vegetation Data
NROW_SITE = 20      # rows on 6. Site Summary


def header_row(ws, row, labels, widths=None, fills=None):
    for i, lab in enumerate(labels, start=1):
        c = ws.cell(row, i, lab)
        c.font, c.fill, c.border, c.alignment = F_H, FILL_H, BOX, CTR
    if widths:
        for i, w in enumerate(widths, start=1):
            ws.column_dimensions[get_column_letter(i)].width = w
    if fills:
        for i, f in enumerate(fills, start=1):
            if f:
                ws.cell(row + 1, i).fill = FILL[f]
    ws.row_dimensions[row].height = 46
    ws.freeze_panes = ws.cell(row + 1, 1)


def band(ws, row, ncols, text, fill=GREEN):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=ncols)
    c = ws.cell(row, 1, text)
    c.font = F_SUB
    c.fill = PatternFill("solid", fgColor=fill)
    c.alignment = Alignment(vertical="center", wrap_text=True)
    ws.row_dimensions[row].height = 20


def note(ws, row, ncols, text):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=ncols)
    c = ws.cell(row, 1, text)
    c.font, c.alignment = F_IT, WRAP
    ws.row_dimensions[row].height = 30


def paint(ws, r0, r1, col, key):
    for r in range(r0, r1 + 1):
        c = ws.cell(r, col)
        c.fill, c.border, c.font = FILL[key], BOX, F_N


def dv(ws, col, r0, r1, options):
    """A dropdown. Kept short -- Excel's inline list has a 255-char limit."""
    v = DataValidation(type="list", formula1='"' + ",".join(options) + '"',
                       allow_blank=True)
    ws.add_data_validation(v)
    v.add(f"{get_column_letter(col)}{r0}:{get_column_letter(col)}{r1}")


def title(ws, text, subtitle, ncols):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=ncols)
    c = ws.cell(1, 1, text)
    c.font = Font(bold=True, size=14, color=NAVY)
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=ncols)
    c = ws.cell(2, 1, subtitle)
    c.font, c.alignment = F_IT, WRAP
    ws.row_dimensions[2].height = 32


# ── reference data ───────────────────────────────────────────────────────────

GRASSLAND_TYPES = ["Prairie", "Aspen parkland", "Black Oak savannah",
                   "Interior BC bunchgrass", "Other"]

MANAGEMENT = ["Never cultivated", "Cultivated and reseeded", "Long-term tame pasture",
              "Hayed", "Unknown"]

GRAZING = ["None", "Season-long", "Rotational", "Heavy", "Unknown"]

NATIVE_SEEDED = ["Native sward", "Tame or introduced", "Mixed", "Unknown"]

BD_BASIS = ["Fine earth / total volume", "Fine earth / fine-earth volume", "Not confirmed"]

# Which roots the soil-carbon sample no longer contains. This is a method
# boundary, not a yes/no: the two working answers imply different arithmetic,
# and "not agreed" is a real and common third state that has to be visible.
ROOT_SOIL_BOUNDARY_OPTIONS = [
    "Not agreed with the lab",
    "Root-separated soil",
    "Operational soil fraction",
]

# Phenology is recorded as the stage observed, not as a yes/no on someone
# else's idea of peak. Whether the plot is comparable is a separate judgement
# against the project's own written rule.
PHENOLOGICAL_STAGES = [
    "Emergence / early vegetative",
    "Vegetative",
    "Peak standing biomass",
    "Flowering / anthesis",
    "Seed set / senescing",
    "Dormant / cured",
    "Unknown",
]

RECENT_REMOVAL = [
    "None observed",
    "Grazing — light",
    "Grazing — moderate",
    "Grazing — heavy",
    "Hayed / mown",
    "Burned",
    "Unknown",
]

COMPARABLE_SEASON = ["Yes", "No", "Not assessed"]

ROOT_CLASS = ["<=2 mm (fine)", ">2 mm (coarse)"]
ROOT_STATE = ["Live", "Dead", "Not separated"]

VEG_COMPONENTS = ["Clip-and-weigh", "Shrub (medium plot)", "Tree (large plot)"]

# Published organic-matter -> carbon conversion factors, for the reference tab.
CARBON_FACTORS = [
    ("0.50", "This workshop / WWF guides", "Dry plant biomass taken as 50% carbon. The default here."),
    ("0.45-0.50", "Commonly reported for roots", "Root tissue carbon fraction is often reported a little BELOW shoot tissue."),
    ("0.58", "van Bemmelen (historical)", "Long-standing general soil factor; considered too high for many soils."),
    ("0.40-0.60", "Varies with material and decomposition", "Which is why a local calibration against CHN is worth doing."),
]

# Every orange cell in the workbook, for the Fill Me In tab.
# (setting name, tab, what it is, default, what happens if left alone)
FILL_ME_IN = [
    ("CARBON_FRACTION_BIOMASS", "7. Settings",
     "Fraction of dry above-ground plant biomass that is carbon.",
     "0.5", "A generic default. Fine for most purposes; calibrate if you have CHN on plant tissue."),
    ("CARBON_FRACTION_ROOT", "7. Settings",
     "Fraction of dry root biomass that is carbon.",
     "0.5", "Set equal to the shoot value by default. Published root values often run a little lower."),
    ("ROOT_SOIL_REPORTING_BOUNDARY", "7. Settings",
     "Which roots the soil-carbon sample no longer contains, agreed with the lab.",
     "Not agreed with the lab",
     "Until it is agreed, soil and root pools cannot be added: the overlap between them is unknown, not zero."),
    ("ROOT_SOIL_BOUNDARY_SOURCE", "7. Settings",
     "Who agreed that boundary, under which written method, and when.",
     "(blank)", "A boundary with no source is an assumption. Reviewers cannot check it and neither can you, later."),
    ("ROOT_SIEVE_MM", "7. Settings",
     "Finest sieve mesh used to recover roots, in mm.",
     "0.5", "Roots finer than the mesh are lost. Without this number the fine-root figure cannot be interpreted."),
    ("ASH_CORRECTED", "7. Settings",
     "Was root mass corrected for adhering mineral soil by ashing?",
     "No", "Uncorrected root mass is systematically TOO HIGH, badly so in clay soils."),
    ("ROOT_DRY_TEMP_C", "7. Settings",
     "Temperature roots were dried at, in degrees C.",
     "65", "Roots dry at 60-70 C; soil bulk density at 105 C. Confusing the two biases root mass."),
    ("COMPARABLE_SEASON_RULE", "7. Settings",
     "The project's written rule for when two clip-and-weigh samples are comparable.",
     "(blank)", "Each plot is asked whether it met the rule. With no rule written down, that question has no answer."),
    ("LAB_BULK_DENSITY_BASIS", "7. Settings",
     "The volume the lab divides dry mass by when reporting bulk density.",
     "Not confirmed",
     "The coarse-fragment correction is applied once, twice or never. Every Soil Data row that disagrees is flagged."),
    ("LAB_METHOD_REFERENCE", "7. Settings",
     "Laboratory, method or SOP number, and the date those two were confirmed.",
     "(blank)", "The two settings above point at this record. Without it they are unsourced claims."),
    ("SOIL_REPORTING_DEPTH_CM", "7. Settings",
     "The fixed depth every core is reported to, alongside the full profile.",
     "30", "30 cm is the comparability depth. It is a FLOOR, not the total."),
    ("TARGET_MARGIN_SOIL", "7. Settings",
     "Precision target for soil carbon, as a fraction of the mean.",
     "0.2", "Set in Part 2. The Site Summary checks achieved precision against it."),
    ("TARGET_MARGIN_ROOT", "7. Settings",
     "Precision target for root biomass, as a fraction of the mean.",
     "0.4", "Deliberately looser than soil: roots are far more variable, so the same target would need 4-5x the cores."),
    ("Regional SOC prior (mean)", "8. Fill Me In",
     "Expected soil carbon for your region, kg C/m2, used when planning.",
     "(none)", "Planning only -- does not affect any calculated result. Without it, Part 2's sample size is a guess."),
    ("Regional SOC prior (CV)", "8. Fill Me In",
     "Expected coefficient of variation for soil carbon in your region.",
     "(none)", "As above. A map-derived CV must be inflated before use -- see Part 2."),
    ("Regional root CV prior", "8. Fill Me In",
     "Expected coefficient of variation for root biomass.",
     "(none)", "Roots typically 0.5-1.0+. Drives the separate root sample size."),
    ("Lab bulk-density basis", "2. Soil Data",
     "Which basis your lab reports bulk density on. Column L, per row.",
     "Not confirmed", "Getting this wrong understates a stony site by up to a third -- or double-corrects it."),
]
