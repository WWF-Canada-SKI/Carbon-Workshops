"""Wetland_Carbon_Calculator.xlsx — stage 1: Instructions, Settings, Reference."""
import sys; sys.path.insert(0, "/home/user/Terrestrial_Carbon_Workshops_V1/Wetlands/_source")
from wet_style import *
import openpyxl

SCR = "/tmp/claude-0/-home-user/af4fc136-c459-5930-bae9-67144880d936/scratchpad/wet"
wb = openpyxl.Workbook()

# ═══════════════════════════════════════════════════════ 0. INSTRUCTIONS
ws = wb.active; ws.title = "0. Instructions"
ws.column_dimensions["A"].width = 27
ws.column_dimensions["B"].width = 104
rows = [
 ("WETLAND CARBON CALCULATOR", ""),
 ("", "WWF-Canada Carbon Measurement · Wetland Carbon Workshop"),
 ("", ""),
 ("What this workbook does", "Turns peat core measurements into a carbon stock in kg C/m², scales cores to plots, "
  "sites and your whole study area, and — if you have dated the core — converts the same carbon into "
  "accumulation rates. It follows 'Measuring Carbon in Peat Soils' (WWF-Canada, 2024), with the additions "
  "noted at the bottom of this sheet."),
 ("", ""),
 ("COLOUR KEY", ""),
 ("Yellow", "TYPE HERE — field measurements you record."),
 ("Blue", "TYPE HERE — lab results, once they come back."),
 ("Grey", "Calculated for you. Do not type in grey cells."),
 ("Green", "Summary output."),
 ("Red", "A quality-control flag. Read it before trusting the row."),
 ("", ""),
 ("ORDER OF WORK", ""),
 ("1", "Fill '1. Plot & Site Log' FIRST — one row per plot. Everything joins to it on Plot ID."),
 ("2", "Fill '2. Core Log' — one row per core. Everything in the peat sheet joins to it on Core ID."),
 ("3", "Fill '3. Peat Data' — one row per section, as the core is sectioned."),
 ("4", "Add lab results (blue columns) to '3. Peat Data' when they return."),
 ("5", "OPTIONAL: if the core has been dated, fill '4. Chronology' to get accumulation rates."),
 ("6", "Read '5. Plot Summary' and '6. Site Summary'. Both calculate themselves."),
 ("", ""),
 ("⚠ IDs MUST MATCH", "Plot ID joins the Core Log to the Plot & Site Log; Core ID joins the Peat Data and the "
  "Chronology to the Core Log. A mismatch means that row's carbon never reaches the summary. Every sheet has a "
  "QC flags column that tells you when this happens."),
 ("", ""),
 ("UNITS", ""),
 ("Depths", "centimetres (cm), measured down from the peat surface"),
 ("Bulk density", "g/cm³ — oven-dry mass ÷ sample volume (see the basis note on '3. Peat Data')"),
 ("Carbon content", "per cent of dry mass (%)"),
 ("Carbon stock", "kg C/m² at core, plot and site level; kg C for totals"),
 ("Accumulation rate", "g C/m²/yr — note the unit change: 1 kg C/m² per 1,000 yr = 1 g C/m²/yr"),
 ("Age", "years before the year the core was taken"),
 ("", ""),
 ("TWO STOCK NUMBERS, AND WHY", ""),
 ("Full profile", "Stock over the whole peat profile, to the mineral contact. THIS IS THE HEADLINE NUMBER — it is "
  "what the peatland actually holds, and what the peatland literature reports."),
 ("To reference depth", "Stock integrated to a fixed depth (100 cm by default, set on '7. Settings'). Reported "
  "alongside so your numbers stay comparable with projects that sampled to a standard depth. Cores that stop "
  "short of it are flagged."),
 ("Why both", "Bansal et al. (2023) found 65% of wetland organic carbon sat between 30 and 120 cm. Report only a "
  "shallow fixed depth and you miss most of the store; report only full profiles and cores of different depths "
  "cannot be compared. So the workbook gives you both."),
 ("", ""),
 ("WHAT'S BEYOND THE PRINTED GUIDE", ""),
 ("Uncertainty", "Site means carry a standard deviation, standard error and confidence interval, checked against "
  "the precision target you set in Part 2. The guide's Eq 1–8 give point estimates only."),
 ("Eq 5 correction", "The guide's printed Eq 5 has its right-hand side in g/cm² and its left-hand side in kg/m². "
  "This workbook uses the correct form — summing the kg/m² core values — which is also what the guide's own "
  "example spreadsheet does."),
 ("Carbon fraction", "Settable on '7. Settings', defaulting to the guide's 0.5. See 'R1. Reference' for why that "
  "is a convention rather than a constant."),
 ("Accumulation rates", "The guide raises them in its introduction and its glossary but gives no method. "
  "'4. Chronology' supplies one — see Part 5 of the workshop."),
]
for i, (a, b) in enumerate(rows, start=1):
    ca = ws.cell(i, 1, a); ca.font = F_SUB if a and not a.isdigit() else F_N
    c = ws.cell(i, 2, b); c.font = F_N; c.alignment = WRAP
ws["A1"].font = Font(bold=True, size=16, color=NAVY)
for r, key in [(7, "y"), (8, "b"), (9, "g"), (10, "s"), (11, "r")]:
    ws.cell(r, 1).fill = FILL[key]
ws.cell(21, 1).fill = FILL["r"]

# ═══════════════════════════════════════════════════════ 7. SETTINGS
st = wb.create_sheet("7. Settings")
st.column_dimensions["A"].width = 30
st.column_dimensions["B"].width = 15
st.column_dimensions["C"].width = 88
st["A1"] = "SETTINGS"; st["A1"].font = Font(bold=True, size=14, color=NAVY)
st["A2"] = "Everything the calculator assumes lives here. Change it once and every sheet follows."
st["A2"].font = F_IT
setrows = [
 ("Parameter", "Value", "What it does"),
 ("CARBON_FRACTION_OM", 0.5, "Fraction of peat organic matter that is carbon, used to convert LOI550 to %C. The peat guide's value. See 'R1. Reference' — published factors run 0.21–0.58 and local calibration against CHN is recommended."),
 ("OM_FACTOR_IS_LOCAL", "No", "Set to Yes once you have calibrated the factor above against elemental analysis on a subset of your own samples. Leaving it No raises an advisory flag, not an error."),
 ("CO2E_FACTOR", 3.67, "Multiply kg C by this to report CO₂ equivalents."),
 ("REFERENCE_DEPTH_CM", 100, "The fixed depth reported alongside the full profile, so cores of different depths stay comparable. 100 cm is the coastal-carbon convention; 30, 50 and 200 cm are also used."),
 ("PEATLAND_MIN_DEPTH_CM", 30, "Organic horizon depth at or above which the guide classes a site as peatland. Cores shallower than this are flagged for interpretation, not rejected."),
 ("PLOT_AREA_M2", 100, "Area each plot represents. The peat guide works in 10 × 10 m plots with one coring site per plot."),
 ("TARGET_MARGIN", 0.2, "Precision target set in Part 2, Step 4. ±20% of the mean by default."),
 ("TARGET_CONFIDENCE", 0.9, "Confidence level for the target and for all reported intervals."),
 ("QC_BD_MIN", 0.02, "Minimum plausible bulk density, g/cm³. Set LOW deliberately: surface Sphagnum peat runs 0.02–0.05, and a mineral-soil threshold would reject most real peat."),
 ("QC_BD_MAX", 1.2, "Maximum plausible bulk density for peat, g/cm³. Values above this usually mean the mineral contact has been passed."),
 ("QC_CARBON_PCT_MAX", 60, "Flag carbon above this per cent. Peat runs roughly 45–55%; higher usually means organic matter has been entered instead of carbon."),
 ("QC_RECOVERY_MIN", 0.9, "Minimum acceptable ratio of core length recovered to bore depth. Below this, the corer chamber probably did not fill completely."),
 ("LORCA_MIN", 4, "Lower sanity bound for long-term accumulation, g C/m²/yr. Published peatland values run roughly 4.6–85.8, mean ~20."),
 ("LORCA_MAX", 90, "Upper sanity bound for long-term accumulation, g C/m²/yr."),
]
for i, (a, b, c) in enumerate(setrows, start=4):
    ca, cb, cc = st.cell(i, 1, a), st.cell(i, 2, b), st.cell(i, 3, c)
    if i == 4:
        for x in (ca, cb, cc): x.font, x.fill, x.alignment = F_H, FILL_H, CTR
    else:
        ca.font = Font(bold=True, size=10, name="Consolas")
        cb.fill, cb.border, cb.font = FILL["y"], BOX, F_N
        cc.font, cc.alignment = F_N, WRAP
        st.row_dimensions[i].height = 32
for i, (a, *_r) in enumerate(setrows[1:], start=5):
    wb.defined_names.add(openpyxl.workbook.defined_name.DefinedName(a, attr_text=f"'7. Settings'!$B${i}"))

# ═══════════════════════════════════════════════════════ R1. REFERENCE
rf = wb.create_sheet("R1. Reference")
rf.column_dimensions["A"].width = 16
rf.column_dimensions["B"].width = 34
rf.column_dimensions["C"].width = 84
r = 1
rf.cell(r, 1, "REFERENCE TABLES").font = Font(bold=True, size=14, color=NAVY); r += 2

rf.cell(r, 1, "VON POST HUMIFICATION SCALE").font = F_SUB; r += 1
rf.cell(r, 1, "Squeeze a handful of wet peat and watch what comes out between your fingers. Subjective, rapid, and "
              "the standard field descriptor of how decomposed peat is. Stanek & Silc (1977); Malterer et al. (1992).").font = F_IT
rf.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3); rf.cell(r, 1).alignment = WRAP
rf.row_dimensions[r].height = 28; r += 1
header_row(rf, r, ["Class", "Degree of decomposition", "What you see when you squeeze it"], widths=[16, 34, 84])
r += 1
VP_FIRST = r
for code, deg, desc in VON_POST:
    for ci, v in enumerate([code, deg, desc], start=1):
        c = rf.cell(r, ci, v); c.font, c.border, c.alignment = F_N, BOX, WRAP
    r += 1
VP_LAST = r - 1
rf.cell(r, 1, "H1–H3 is fibric peat (Oi); H4–H6 hemic, or mucky peat (Oe); H7–H10 sapric, or muck (Oa). "
              "Carbon content per unit mass falls as decomposition advances, while bulk density rises.").font = F_IT
rf.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3); rf.cell(r, 1).alignment = WRAP
rf.row_dimensions[r].height = 26; r += 3

rf.cell(r, 1, "WETLAND TYPES").font = F_SUB; r += 1
header_row(rf, r, ["Type", "Water source", "Notes"], widths=[16, 34, 84]); r += 1
WT_FIRST = r
for a, b, c in WETLAND_TYPES:
    for ci, v in enumerate([a, b, c], start=1):
        cc = rf.cell(r, ci, v); cc.font, cc.border, cc.alignment = F_N, BOX, WRAP
    r += 1
WT_LAST = r - 1
r += 2

rf.cell(r, 1, "PUBLISHED ORGANIC-MATTER → CARBON CONVERSION FACTORS").font = F_SUB; r += 1
rf.cell(r, 1, "The factor is NOT universal. Bansal et al. (2023) recommend determining a local SOM:SOC ratio on a "
              "subset of samples run through BOTH loss-on-ignition and a CHN elemental analyser, and publishing the "
              "relationship. The workbook's default is the peat guide's 0.5; change it on '7. Settings' once you "
              "have your own.").font = F_IT
rf.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3); rf.cell(r, 1).alignment = WRAP
rf.row_dimensions[r].height = 40; r += 1
header_row(rf, r, ["Factor", "Source", "System"], widths=[16, 34, 84]); r += 1
for src, fac, note in LOI_FACTORS:
    for ci, v in enumerate([("0.4–0.6" if fac is None else fac), src, note], start=1):
        cc = rf.cell(r, ci, v); cc.font, cc.border, cc.alignment = F_N, BOX, WRAP
    r += 1
rf.freeze_panes = "A2"

wb.save(f"{SCR}/_w1.xlsx")
import json
json.dump(dict(VP_FIRST=VP_FIRST, VP_LAST=VP_LAST, WT_FIRST=WT_FIRST, WT_LAST=WT_LAST),
          open(f"{SCR}/_wref.json", "w"))
print("stage 1 ok — von Post rows %d-%d, wetland types %d-%d" % (VP_FIRST, VP_LAST, WT_FIRST, WT_LAST))
