import sys; sys.path.insert(0, "/tmp/claude-0/-home-user/af4fc136-c459-5930-bae9-67144880d936/scratchpad")
from build_calc_part1 import *
import openpyxl
from openpyxl.worksheet.datavalidation import DataValidation

SCR = "/tmp/claude-0/-home-user/af4fc136-c459-5930-bae9-67144880d936/scratchpad"
wb = openpyxl.load_workbook(f"{SCR}/_stage1.xlsx")
N_TREE, N_UNDER, N_SOIL, N_PLOT, N_SITE = 300, 200, 400, 40, 12
ORDER = ["wood", "bark", "branches", "foliage"]

# ═════════════════════════════════════════════ R1. TREE COEFFICIENTS
tc = read_tree_coeffs()
by_sp = {}
for x in tc:
    by_sp.setdefault(x["species"], {})[x["component"]] = x
species_list = list(by_sp.keys())

rc = wb.create_sheet("R1. Tree Coefficients")
rc["A1"] = "TREE ALLOMETRIC COEFFICIENTS"; rc["A1"].font = Font(bold=True, size=14, color=NAVY)
notes = [
 "Lambert, M.-C., Ung, C.-H. & Raulier, F. (2005). Canadian national tree aboveground biomass equations. Can. J. For. Res. 35:1996–2018.",
 "Ung, C.-H., Bernier, P. & Guo, X.-J. (2008). Canadian national biomass equations: new parameter estimates that include British Columbia data. Can. J. For. Res. 38:1123–1232.",
 "Biomass (kg) of one component = a × DBH^b            when only DBH was measured",
 "Biomass (kg) of one component = a × DBH^b × height^c  when height was also measured",
 "Every species has exactly four components, always in this order: wood, bark, branches, foliage. '2. Tree Data' relies on that order — do not re-sort or insert rows.",
 "TREE_TYPE drives the belowground equation. 'All' is deliberately left generic: see the note below.",
]
for i, n in enumerate(notes, start=2):
    rc.cell(i, 1, n).font = F_IT
rc.cell(9, 1, "⚠ On the generic 'All' row: the Trees guide gives one root equation for hardwoods and another for softwoods, and "
              "nothing for a mixed or unknown species. Choosing 'All' therefore has no defensible root:shoot value. The calculator "
              "averages the two relationships and raises a flag. Pick a species, or 'Deciduous'/'Conifers', wherever you can.").font = Font(italic=True, size=9, color="AA3333")
rc.row_dimensions[9].height = 30
rc.merge_cells("A9:J9"); rc["A9"].alignment = WRAP

hdr = ["Species (EN)", "Essence (FR)", "Component", "a (DBH only)", "b (DBH only)",
       "a (DBH+H)", "b (DBH+H)", "c (DBH+H)", "Reference", "Tree type"]
header_row(rc, 11, hdr, widths=[26, 24, 12, 13, 13, 13, 13, 13, 14, 13])
r = 12
sp_start = {}
for sp in species_list:
    sp_start[sp] = r
    for comp in ORDER:
        x = by_sp[sp][comp]
        tt = x["ttype"] if x["ttype"] not in (None, "NA") else "All"
        for ci, v in enumerate([sp, x["species_fr"], comp, x["a_d"], x["b_d"],
                                x["a_dh"], x["b_dh"], x["c_dh"], x["ref"], tt], start=1):
            cc = rc.cell(r, ci, v); cc.font, cc.border = F_N, BOX
            if ci == 3: cc.font = Font(size=10, color="666666")
        r += 1
TC_LAST = r - 1
rc.freeze_panes = "A12"

# One row per species, for the dropdown and the single-MATCH lookup
rc.cell(11, 12, "SPECIES LIST (dropdown source)").font = F_SUB
rc.column_dimensions["L"].width = 26
for i, sp in enumerate(species_list):
    rc.cell(12 + i, 12, sp).font = F_N
SP_FIRST, SP_LAST = 12, 12 + len(species_list) - 1

# ═════════════════════════════════════════════ R2. UNDERSTORY COEFFICIENTS
sc = read_shrub_coeffs()
uc = wb.create_sheet("R2. Understory Coefficients")
uc["A1"] = "UNDERSTORY ALLOMETRIC COEFFICIENTS"; uc["A1"].font = Font(bold=True, size=14, color=NAVY)
for i, n in enumerate([
  "Flade, L. et al. (2020). Allometric equations for shrub and short-stature tree aboveground biomass.",
  "Biomass (g) = b × x^a, then divided by 1000 to give kg. Coefficients were derived in grams.",
  "x is the MODEL PARAMETER: for a short-statured tree it is the stem diameter at 0.30 m (cm); for a shrub it is "
  "crown volume L × W × H (m³). The two are different quantities — the sheet picks the right one from 'Plant type'.",
  "⚠ These are ABOVE-ground equations only. No belowground component is included for understory. See '3. Understory Data'.",
], start=2):
    uc.cell(i, 1, n).font = F_IT
header_row(uc, 7, ["Common name", "Scientific name", "Plant type", "Component", "b", "a", "Reference"],
           widths=[24, 26, 12, 12, 12, 12, 20])
for i, x in enumerate(sc):
    for ci, v in enumerate([x["name"], x["sci"], x["ptype"], x["comp"], x["b"], x["a"], x["ref"]], start=1):
        cc = uc.cell(8 + i, ci, v); cc.font, cc.border = F_N, BOX
UC_FIRST, UC_LAST = 8, 8 + len(sc) - 1
uc.cell(7, 9, "NAME LIST (dropdown source)").font = F_SUB
uc.column_dimensions["I"].width = 24
for i, x in enumerate(sc):
    uc.cell(8 + i, 9, x["name"]).font = F_N
UN_FIRST, UN_LAST = 8, 8 + len(sc) - 1
uc.freeze_panes = "A8"

wb.save(f"{SCR}/_stage2.xlsx")
import json
json.dump(dict(TC_LAST=TC_LAST, SP_FIRST=SP_FIRST, SP_LAST=SP_LAST,
               UC_FIRST=UC_FIRST, UC_LAST=UC_LAST, UN_FIRST=UN_FIRST, UN_LAST=UN_LAST,
               n_species=len(species_list), n_shrub=len(sc)),
          open(f"{SCR}/_refs.json", "w"))
print("R1 rows 12..%d (%d species) · R2 rows %d..%d (%d taxa)" % (TC_LAST, len(species_list), UC_FIRST, UC_LAST, len(sc)))
