"""Build Forest_Carbon_Calculator.xlsx — shared setup + reference tabs."""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

SRC = "/home/user/Terrestrial_Carbon_Workshops_V1/Forests/_source"

# ── house style ──────────────────────────────────────────────────────────────
NAVY   = "1B4332"          # headers
YELLOW = "FFF2CC"          # type here
GREY   = "EDEDED"          # calculated
BLUE   = "DDEBF7"          # lab result
GREEN  = "E2EFDA"          # summary
RED    = "FCE4E4"          # flag

F_H   = Font(bold=True, color="FFFFFF", size=10)
F_SUB = Font(bold=True, color=NAVY, size=10)
F_N   = Font(size=10)
F_IT  = Font(italic=True, size=9, color="666666")
FILL_H = PatternFill("solid", fgColor=NAVY)
FILL = {k: PatternFill("solid", fgColor=v) for k, v in
        dict(y=YELLOW, g=GREY, b=BLUE, s=GREEN, r=RED).items()}
THIN = Side(style="thin", color="BFBFBF")
BOX  = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
CTR  = Alignment(horizontal="center", vertical="center", wrap_text=True)


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
    ws.row_dimensions[row].height = 42
    ws.freeze_panes = ws.cell(row + 1, 1)


def band(ws, row, ncols, text, fill=GREEN):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=ncols)
    c = ws.cell(row, 1, text)
    c.font = F_SUB
    c.fill = PatternFill("solid", fgColor=fill)
    c.alignment = Alignment(vertical="center")
    ws.row_dimensions[row].height = 20


def paint(ws, r0, r1, col, key):
    for r in range(r0, r1 + 1):
        c = ws.cell(r, col)
        c.fill, c.border, c.font = FILL[key], BOX, F_N



# ── house additions for the wetland workbook ─────────────────────────────────
VON_POST = [
 ("H1", "Completely undecomposed", "Clear, colourless water squeezes out. Plant remains easily identifiable."),
 ("H2", "Almost undecomposed", "Clear, yellowish water. Plant remains still identifiable."),
 ("H3", "Very weakly decomposed", "Slightly turbid brown water. No peat escapes between the fingers."),
 ("H4", "Weakly decomposed", "Strongly turbid brown water. No peat escapes. Residue mushy."),
 ("H5", "Moderately decomposed", "Very turbid water with a little peat escaping. Plant structure evident but indistinct."),
 ("H6", "Fairly well decomposed", "About one third of the peat escapes between the fingers. Residue very mushy."),
 ("H7", "Strongly decomposed", "About half escapes. Plant structure barely discernible."),
 ("H8", "Very strongly decomposed", "About two thirds escapes. Only resistant remains, such as roots and fibres, left."),
 ("H9", "Almost completely decomposed", "Nearly all escapes as a fairly uniform paste."),
 ("H10", "Completely decomposed", "All the peat escapes between the fingers. No free water visible."),
]

WETLAND_TYPES = [
 ("Bog", "Ombrotrophic \u2014 rain and snow only", "Acidic, nutrient-poor. Sphagnum, ericaceous shrubs, stunted black spruce."),
 ("Fen", "Minerotrophic \u2014 groundwater carrying minerals", "Less acidic. Sedges, brown mosses, tamarack."),
 ("Swamp", "Variable; standing or moving water", "At least 25% tree cover. Organic depth shallow to very deep. Measure trees too."),
 ("Marsh", "Standing or slowly moving surface water", "Emergent herbaceous vegetation. Often mineral, not peat."),
 ("Other", "", "Describe it in the notes."),
]

LOI_FACTORS = [
 ("This workshop / WWF peat guide", 0.50, "Peat organic matter taken as 50% carbon. The default here."),
 ("van Bemmelen (historical)", 0.58, "Long-standing general factor. Pribyl (2010) considers it too high for many soils."),
 ("Braun et al. (2020)", 0.53, "Freshwater coastal wetlands, Lake Michigan."),
 ("Ouyang & Lee (2020)", 0.52, "Salt marsh."),
 ("Baustian et al. (2017)", 0.47, "All Louisiana soils."),
 ("Fourqurean et al. (2012)", 0.43, "Global seagrass sediments."),
 ("Ouyang & Lee (2020)", 0.21, "Mangrove \u2014 the low end, and a warning against assuming a universal factor."),
 ("Craft et al. (1991)", None, "0.4\u20130.6 depending on organic matter content and soil age, North Carolina salt marsh."),
]
