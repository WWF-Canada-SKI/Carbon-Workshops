import sys; sys.path.insert(0, "/tmp/claude-0/-home-user/af4fc136-c459-5930-bae9-67144880d936/scratchpad")
from build_calc_part1 import *
import openpyxl

N_TREE, N_UNDER, N_SOIL, N_PLOT, N_SITE = 300, 200, 400, 40, 12

wb = openpyxl.Workbook()

# ═══════════════════════════════════════════════════════════ 0. INSTRUCTIONS
ws = wb.active; ws.title = "0. Instructions"
ws.column_dimensions["A"].width = 26
ws.column_dimensions["B"].width = 104
rows = [
 ("FOREST CARBON CALCULATOR", ""),
 ("", "WWF-Canada Carbon Measurement · Forest Carbon Workshop"),
 ("", ""),
 ("What this workbook does", "Turns field measurements of trees, understory and soil into a carbon stock in kg C/m², "
  "then scales plots to sites and to your whole study area. It follows 'Measuring Carbon in Trees' "
  "and 'Measuring Carbon in Non-Peat Soils' (WWF-Canada, 2026)."),
 ("", ""),
 ("COLOUR KEY", ""),
 ("Yellow", "TYPE HERE — field measurements you record."),
 ("Blue", "TYPE HERE — lab results, once they come back."),
 ("Grey", "Calculated for you. Do not type in grey cells."),
 ("Green", "Summary output."),
 ("Red", "A quality-control flag. Read it before trusting the row."),
 ("", ""),
 ("ORDER OF WORK", ""),
 ("1", "Fill '1. Plot & Site Log' FIRST — one row per plot. Everything else joins to it on Plot ID."),
 ("2", "Fill '2. Tree Data', '3. Understory Data' and '4. Soil Data' as the field data comes in."),
 ("3", "Add lab results (blue columns) to '3. Understory Data' and '4. Soil Data' when they return."),
 ("4", "Read '5. Plot Summary' and '6. Site Summary'. Both calculate themselves."),
 ("", ""),
 ("⚠ PLOT IDs MUST MATCH", "Plot ID is the key that joins every sheet. If a Plot ID on the Tree, Understory or Soil "
  "sheet does not appear in the Plot & Site Log, that row's plot area cannot be looked up and its carbon will not "
  "reach the summary. The QC flag column will tell you."),
 ("", ""),
 ("UNITS", ""),
 ("DBH", "centimetres (cm), measured at 1.3 m above ground"),
 ("Tree height", "metres (m)"),
 ("Shrub L / W / H", "metres (m)"),
 ("Depths", "centimetres (cm), measured down from the soil surface"),
 ("Bulk density", "g/cm³ — oven-dry fine earth (<2 mm) ÷ total sample volume (see '4. Soil Data')"),
 ("Carbon content", "per cent of dry mass (%)"),
 ("Carbon stock", "kg C/m² at plot and site level; kg C for totals"),
 ("", ""),
 ("WHERE THE NUMBERS COME FROM", ""),
 ("Tree biomass", "Lambert, Ung & Raulier (2005) and Ung, Bernier & Guo (2008) — Canadian national biomass "
  "equations. See 'R1. Tree Coefficients'."),
 ("Tree roots", "Root:shoot relationships, 'Measuring Carbon in Trees' p.17. See the note on 'R1. Tree Coefficients'."),
 ("Shrub biomass", "Flade et al. (2020). See 'R2. Understory Coefficients'."),
 ("Soil carbon", "'Measuring Carbon in Non-Peat Soils' pp.23–24, Eq 1–4."),
 ("Carbon fraction", "0.5 of dry biomass, and 0.5 of soil organic matter. Set on '8. Settings'."),
 ("", ""),
 ("BEFORE YOU START", "Open '8. Settings' and confirm the reporting depth, the plot sizes your crew actually used, "
  "and your precision target from Part 2 of the workshop."),
]
for i, (a, b) in enumerate(rows, start=1):
    ws.cell(i, 1, a).font = F_SUB if a and not a.isdigit() else F_N
    c = ws.cell(i, 2, b); c.font = F_N; c.alignment = WRAP
ws["A1"].font = Font(bold=True, size=16, color=NAVY)
for r, key in [(7, "y"), (8, "b"), (9, "g"), (10, "s"), (11, "r")]:
    ws.cell(r, 1).fill = FILL[key]
ws.cell(19, 1).fill = FILL["r"]

# ═══════════════════════════════════════════════════════════ 7. SETTINGS
st = wb.create_sheet("8. Settings")
st.column_dimensions["A"].width = 38
st.column_dimensions["B"].width = 16
st.column_dimensions["C"].width = 82
st["A1"] = "SETTINGS"; st["A1"].font = Font(bold=True, size=14, color=NAVY)
st["A2"] = "Everything the calculator assumes lives here. Change it once, and every sheet follows."
st["A2"].font = F_IT
setrows = [
 ("Parameter", "Value", "What it does"),
 ("CARBON_FRACTION_BIOMASS", 0.5, "Fraction of dry plant biomass that is carbon. 0.5 is the IPCC default and the value both protocol guides use."),
 ("CARBON_FRACTION_OM", 0.5, "Fraction of soil organic matter that is carbon, used to convert LOI550 to %C. Non-peat guide, p.22."),
 ("CO2E_FACTOR", 3.67, "Multiply kg C by this to report CO₂ equivalents."),
 ("REPORTING_DEPTH_CM", 30, "The soil depth every core is reported to. Cores are integrated to this depth so that cores of different lengths are comparable. Anything deeper is reported separately. Common choices: 30, 50, 100."),
 ("LARGE_PLOT_AREA_M2", 400, "Default large (tree) plot area. Circular r = 11.28 m, or 20 × 20 m, or 10 × 40 m. Can be overridden per plot on sheet 1."),
 ("MEDIUM_PLOT_AREA_M2", 100, "Default medium (shrub) plot area. 4 × 4 m = 16 m², or 10 × 10 m = 100 m². Override per plot on sheet 1."),
 ("SMALL_PLOT_AREA_M2", 1, "Default small (ground vegetation) plot area. 1 × 1 m = 1 m², or 0.5 × 0.5 m = 0.25 m². Override per plot on sheet 1."),
 ("TARGET_MARGIN", 0.2, "Precision target set in Part 2, Step 4. ±20% of the mean by default."),
 ("TARGET_CONFIDENCE", 0.9, "Confidence level for the target and for all reported intervals."),
 ("BGB_RS_DECIDUOUS_a", 1.576, "Deciduous root biomass: BGB = a × AGB^b. Trees guide p.17."),
 ("BGB_RS_DECIDUOUS_b", 0.615, "Exponent for the deciduous relationship."),
 ("BGB_RS_CONIFER", 0.222, "Conifer root:shoot ratio: BGB = ratio × AGB. Trees guide p.17."),
 ("BGB_FRACTION_MIN", 0.1, "QC bound. The Trees guide states roots are 18–30% of total tree biomass; anything outside 10–40% is flagged."),
 ("BGB_FRACTION_MAX", 0.4, "Upper QC bound for the belowground fraction."),
 ("QC_DBH_MAX_CM", 200, "Flag any DBH above this as a likely transcription error."),
 ("QC_BD_MIN", 0.1, "Minimum plausible bulk density, g/cm³."),
 ("QC_BD_MAX", 2.0, "Maximum plausible bulk density, g/cm³."),
 ("QC_CARBON_PCT_MAX", 60, "Flag any soil carbon above this per cent — organic horizons reach ~50%, mineral soil far less."),
]
for i, (a, b, c) in enumerate(setrows, start=4):
    ca, cb, cc = st.cell(i, 1, a), st.cell(i, 2, b), st.cell(i, 3, c)
    if i == 4:
        for cc2 in (ca, cb, cc):
            cc2.font, cc2.fill, cc2.alignment = F_H, FILL_H, CTR
    else:
        ca.font = Font(bold=True, size=10, name="Consolas")
        cb.fill, cb.border, cb.font = FILL["y"], BOX, F_N
        cc.font, cc.alignment = F_N, WRAP
        st.row_dimensions[i].height = 30
# named ranges
for i, (a, *_rest) in enumerate(setrows[1:], start=5):
    wb.defined_names.add(openpyxl.workbook.defined_name.DefinedName(
        a, attr_text=f"'8. Settings'!$B${i}"))

print("settings + instructions done")
wb.save("/tmp/claude-0/-home-user/af4fc136-c459-5930-bae9-67144880d936/scratchpad/_stage1.xlsx")
