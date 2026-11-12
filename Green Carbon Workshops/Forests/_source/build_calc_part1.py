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


def read_tree_coeffs():
    wb = openpyxl.load_workbook(f"{SRC}/DataTemplate_TreesUpdated.xlsx")
    cs = wb["Allometric Coefficeints"]
    out = []
    for r in range(8, 176):
        sp = cs.cell(r, 1).value
        if not sp:
            continue
        out.append(dict(
            species=str(sp).strip(), species_fr=cs.cell(r, 2).value,
            component=str(cs.cell(r, 3).value or "").strip().lower(),
            a_d=cs.cell(r, 5).value, b_d=cs.cell(r, 6).value,
            a_dh=cs.cell(r, 7).value, b_dh=cs.cell(r, 8).value, c_dh=cs.cell(r, 9).value,
            ref=cs.cell(r, 10).value, ttype=cs.cell(r, 11).value))
    return out


def read_shrub_coeffs():
    wb = openpyxl.load_workbook(f"{SRC}/Carbon-Calculator-Medium-Vegetation.xlsx")
    cs = wb["Vegetation Allometric Equations"]
    out = []
    for r in range(9, 30):
        nm = cs.cell(r, 1).value
        if not nm:
            continue
        out.append(dict(name=str(nm).strip(), sci=cs.cell(r, 2).value,
                        ptype=cs.cell(r, 3).value, comp=cs.cell(r, 4).value,
                        b=cs.cell(r, 5).value, a=cs.cell(r, 6).value,
                        ref=cs.cell(r, 7).value))
    return out
