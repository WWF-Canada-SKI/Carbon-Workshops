"""Stage 3 — chronology summary (RERCA/LORCA), Plot Summary, Site Summary."""
import sys, json; sys.path.insert(0, "/home/user/Terrestrial_Carbon_Workshops_V1/Wetlands/_source")
from wet_style import *
import openpyxl

SCR = "/tmp/claude-0/-home-user/af4fc136-c459-5930-bae9-67144880d936/scratchpad/wet"
Q = json.load(open(f"{SCR}/_wrows.json"))
wb = openpyxl.load_workbook(f"{SCR}/_w2.xlsx")
F1, NP, NC, NPE, NCH = Q["F1"], Q["N_PLOT"], Q["N_CORE"], Q["N_PEAT"], Q["N_CHRON"]
PL, CL, PD, CH = "'1. Plot & Site Log'", "'2. Core Log'", "'3. Peat Data'", "'4. Chronology'"
def rg(sh, col, n): return f"{sh}!${col}${F1}:${col}${F1+n-1}"
PKEY, PSITE, PAREA = rg(PL,'A',NP), rg(PL,'B',NP), rg(PL,'O',NP)
CKEY, CPLOT = rg(CL,'A',NC), rg(CL,'B',NC)
CFULL, CREF = rg(CL,'R',NC), rg(CL,'S',NC)
ch_core, ch_dep, ch_age, ch_cum, ch_rec = (rg(CH,'A',NCH), rg(CH,'B',NCH), rg(CH,'C',NCH),
                                           rg(CH,'F',NCH), rg(CH,'J',NCH))

# ═════════════════════════ chronology summary block, on sheet 4
ws = wb["4. Chronology"]
B0 = F1 + NCH + 2
band(ws, B0, 11, "  ACCUMULATION RATES — one row per core, calculated from the horizons above")
ws.cell(B0+1, 1, "LORCA is the whole-profile average: all the carbon in the core divided by the age at its base. "
                 "RERCA covers only the recent, Pb-210/Cs-137-dated part near the surface. They answer different "
                 "questions and are not interchangeable — read the flag in the last column before comparing them.").font = F_IT
ws.merge_cells(start_row=B0+1, start_column=1, end_row=B0+1, end_column=11)
ws.cell(B0+1, 1).alignment = WRAP; ws.row_dimensions[B0+1].height = 32
SH = B0 + 2
hdr = ["Core ID", "Basal age (yr)", "Profile carbon (kg C/m²)", "LORCA (g C/m²/yr)",
       "Recent horizon depth (cm)", "Recent horizon age (yr)", "Carbon above it (kg C/m²)",
       "RERCA (g C/m²/yr)", "RERCA ÷ LORCA", "QC flags", "Notes"]
header_row(ws, SH, hdr, widths=[13, 12, 15, 14, 14, 14, 15, 14, 12, 52, 24])
NSUM = 30
for i, k in enumerate(["g"]*9 + ["g", "y"], start=1):
    paint(ws, SH+1, SH+NSUM, i, "s" if i in (4, 8) else k)
sf = {
 1: f'=IF(INDEX({CKEY},ROW()-{SH})="","",INDEX({CKEY},ROW()-{SH}))',
 2: f'=IF($A{{r}}="","",IF(SUMPRODUCT(({ch_core}=$A{{r}})*{ch_age})=0,"",SUMPRODUCT(MAX(({ch_core}=$A{{r}})*{ch_age}))))',
 3: f'=IF($A{{r}}="","",IFERROR(INDEX({CFULL},MATCH($A{{r}},{CKEY},0)),""))',
 4: '=IF(OR(NOT(ISNUMBER($B{r})),NOT(ISNUMBER($C{r})),$B{r}=0),"",$C{r}*1000/$B{r})',
 5: f'=IF($A{{r}}="","",IF(SUMPRODUCT(({ch_core}=$A{{r}})*{ch_rec}*{ch_dep})=0,"",SUMPRODUCT(MAX(({ch_core}=$A{{r}})*{ch_rec}*{ch_dep}))))',
 6: f'=IF(NOT(ISNUMBER($E{{r}})),"",SUMIFS({ch_age},{ch_core},$A{{r}},{ch_dep},$E{{r}}))',
 7: f'=IF(NOT(ISNUMBER($E{{r}})),"",SUMIFS({ch_cum},{ch_core},$A{{r}},{ch_dep},$E{{r}}))',
 8: '=IF(OR(NOT(ISNUMBER($F{r})),NOT(ISNUMBER($G{r})),$F{r}=0),"",$G{r}*1000/$F{r})',
 9: '=IF(OR(NOT(ISNUMBER($H{r})),NOT(ISNUMBER($D{r})),$D{r}=0),"",$H{r}/$D{r})',
 10: ('=IF($A{r}="","",'
      'IF(NOT(ISNUMBER($B{r})),"No dated horizons for this core — LORCA cannot be calculated. ","")'
      '&IF(AND(ISNUMBER($B{r}),NOT(ISNUMBER($E{r}))),"No Pb-210 or Cs-137 horizon — RERCA cannot be calculated. ","")'
      f'&IF(IFERROR(INDEX({rg(CL,"L",NC)},MATCH($A{{r}},{CKEY},0)),"")="No","Core did not reach the mineral contact, so LORCA is based on a partial profile and is a MINIMUM. ","")'
      '&IF(AND(ISNUMBER($I{r}),$I{r}>1.2),"RERCA is "&TEXT($I{r},"0.0")&"x LORCA. This is EXPECTED, not a finding: near-surface peat has not finished decomposing, so recent rates always look higher. Do not report it as accelerating sequestration. ","")'
      '&IF(AND(ISNUMBER($D{r}),OR($D{r}<LORCA_MIN,$D{r}>LORCA_MAX)),"LORCA outside the published range of "&LORCA_MIN&"-"&LORCA_MAX&" g C/m2/yr — check the basal age and the profile carbon. ",""))'),
}
for col, t in sf.items():
    for r in range(SH+1, SH+NSUM+1):
        ws.cell(r, col, t.format(r=r))

# ═════════════════════════ 5. PLOT SUMMARY
ws = wb.create_sheet("5. Plot Summary", 5)
ws["A1"] = "PLOT SUMMARY"; ws["A1"].font = Font(bold=True, size=14, color=NAVY)
ws["A2"] = ("One row per plot, calculated for you. Peat is the mean of the cores taken in that plot. If the site "
            "is a swamp, or you surveyed shrubs and ground layer, enter that carbon in the yellow column — it "
            "comes from the Forests calculator, which this workshop does not duplicate.")
ws["A2"].font = F_IT; ws.merge_cells("A2:J2"); ws["A2"].alignment = WRAP; ws.row_dimensions[2].height = 32
hdr = ["Plot ID", "Site ID", "Cores in plot", "Peat, full profile (kg C/m²)",
       "Peat to reference depth (kg C/m²)", "Vegetation carbon (kg C/m²)",
       "TOTAL, full profile (kg C/m²)", "QC flags", "_num", "_inc"]
header_row(ws, 4, hdr, widths=[13, 10, 11, 16, 17, 15, 17, 46, 9, 7])
f = {
 1: f'=IF(INDEX({PKEY},ROW()-4)="","",INDEX({PKEY},ROW()-4))',
 2: f'=IF($A{{r}}="","",INDEX({PSITE},MATCH($A{{r}},{PKEY},0)))',
 3: f'=IF($A{{r}}="","",COUNTIFS({CPLOT},$A{{r}}))',
 4: f'=IF(OR($A{{r}}="",$C{{r}}=0),"",IFERROR(AVERAGEIFS({CFULL},{CPLOT},$A{{r}}),""))',
 5: f'=IF(OR($A{{r}}="",$C{{r}}=0),"",IFERROR(AVERAGEIFS({CREF},{CPLOT},$A{{r}}),""))',
 7: '=IF($A{r}="","",IF(ISNUMBER($D{r}),$D{r},0)+IF(ISNUMBER($F{r}),$F{r},0))',
 8: ('=IF($A{r}="","",'
     'IF($C{r}=0,"No cores for this plot — it contributes nothing to the site mean. ","")'
     '&IF(AND($C{r}>0,$C{r}<2),"Only one core in this plot. Bansal et al. recommend three or more per wetland. ","")'
     '&IF(AND(ISNUMBER($D{r}),ISNUMBER($E{r}),$D{r}>$E{r}*1.5),"Most of this plot\'s carbon lies below the reference depth — make sure your reporting says which number you are quoting. ",""))'),
 9: '=IF(ISNUMBER($G{r}),$G{r},0)',
 10: '=IF(AND(ISNUMBER($G{r}),$A{r}<>""),1,0)',
}
for col, t in f.items():
    for r in range(5, 5+NP): ws.cell(r, col, t.format(r=r))
for i in range(1, 11):
    paint(ws, 5, 4+NP, i, "y" if i == 6 else ("s" if i == 7 else "g"))
ws.column_dimensions["I"].hidden = True; ws.column_dimensions["J"].hidden = True
ws.freeze_panes = "C5"
PS = "'5. Plot Summary'"
PS_SITE, PS_NUM, PS_INC = f"{PS}!$B$5:$B${4+NP}", f"{PS}!$I$5:$I${4+NP}", f"{PS}!$J$5:$J${4+NP}"

# ═════════════════════════ 6. SITE SUMMARY
ws = wb.create_sheet("6. Site Summary", 6)
ws["A1"] = "SITE SUMMARY"; ws["A1"].font = Font(bold=True, size=14, color=NAVY)
ws["A2"] = ("Type a Site ID and its area; everything else calculates. This is where the loop from Part 2 closes: "
            "the precision you asked for when you sized the campaign is checked against the precision you "
            "achieved. Totals are on the FULL-PROFILE basis.")
ws["A2"].font = F_IT; ws.merge_cells("A2:N2"); ws["A2"].alignment = WRAP; ws.row_dimensions[2].height = 32
hdr = ["Site ID", "Site area (m²)", "Plots", "Mean (kg C/m²)", "SD", "Standard error",
       "t (two-sided)", "± half-width (kg C/m²)", "Achieved margin", "Target margin",
       "Precision", "Total carbon (kg C)", "Total (t CO₂e)", "QC flags"]
header_row(ws, 4, hdr, widths=[13, 14, 8, 14, 11, 12, 11, 15, 13, 12, 22, 15, 14, 42])
NS, SR = 14, 5
for i, k in enumerate(["y", "y"] + ["g"]*12, start=1): paint(ws, SR, SR+NS-1, i, k)
sf = {
 3: f'=IF($A{{r}}="","",SUMIFS({PS_INC},{PS_SITE},$A{{r}}))',
 4: f'=IF(OR($A{{r}}="",NOT(ISNUMBER($C{{r}})),$C{{r}}=0),"",SUMIFS({PS_NUM},{PS_SITE},$A{{r}})/$C{{r}})',
 5: (f'=IF(OR($A{{r}}="",NOT(ISNUMBER($C{{r}})),$C{{r}}<2),"",'
     f'SQRT(SUMPRODUCT(({PS_SITE}=$A{{r}})*{PS_INC}*({PS_NUM}-$D{{r}})^2)/($C{{r}}-1)))'),
 6: '=IF(OR(NOT(ISNUMBER($E{r})),NOT(ISNUMBER($C{r})),$C{r}<2),"",$E{r}/SQRT($C{r}))',
 7: '=IF(OR($A{r}="",NOT(ISNUMBER($C{r})),$C{r}<2),"",TINV(1-TARGET_CONFIDENCE,$C{r}-1))',
 8: '=IF(OR(NOT(ISNUMBER($F{r})),NOT(ISNUMBER($G{r}))),"",$G{r}*$F{r})',
 9: '=IF(OR(NOT(ISNUMBER($H{r})),NOT(ISNUMBER($D{r})),$D{r}=0),"",$H{r}/$D{r})',
 10: '=IF($A{r}="","",TARGET_MARGIN)',
 11: ('=IF(NOT(ISNUMBER($I{r})),IF($A{r}="","","Cannot be assessed — at least 2 plots are needed for an interval."),'
      'IF($I{r}<=$J{r},"MET: ±"&TEXT($I{r},"0%")&" at "&TEXT(TARGET_CONFIDENCE,"0%")&" confidence",'
      '"NOT MET: ±"&TEXT($I{r},"0%")&" against a ±"&TEXT($J{r},"0%")&" target"))'),
 12: '=IF(OR($A{r}="",NOT(ISNUMBER($B{r})),NOT(ISNUMBER($D{r}))),"",$D{r}*$B{r})',
 13: '=IF(NOT(ISNUMBER($L{r})),"",$L{r}*CO2E_FACTOR/1000)',
 14: ('=IF($A{r}="","",'
      'IF($C{r}=0,"No plots carry this Site ID — check it matches the Plot & Site Log. ","")'
      '&IF(AND($C{r}>0,$C{r}<2),"Only one plot: a mean can be reported but never an uncertainty. ","")'
      '&IF($B{r}="","No site area, so no total carbon. ","")'
      '&IF(AND(ISNUMBER($I{r}),$I{r}>$J{r}),"Wider than planned. Peatland carbon varies more than forest carbon does, largely through depth — more cores, or stratifying by microform and depth, would tighten it. ",""))'),
}
for col, t in sf.items():
    for r in range(SR, SR+NS): ws.cell(r, col, t.format(r=r))
B0 = SR + NS + 2
band(ws, B0, 14, "  STUDY AREA — all sites combined, weighted by area")
labs = [("Total area (m²)", f'=IF(SUM($B${SR}:$B${SR+NS-1})=0,"",SUM($B${SR}:$B${SR+NS-1}))'),
        ("Total carbon (kg C)", f'=IF(SUM($L${SR}:$L${SR+NS-1})=0,"",SUM($L${SR}:$L${SR+NS-1}))'),
        ("Area-weighted mean (kg C/m²)", f'=IF(OR($B${B0+1}="",$B${B0+2}=""),"",$B${B0+2}/$B${B0+1})'),
        ("Total (t CO₂e)", f'=IF($B${B0+2}="","",$B${B0+2}*CO2E_FACTOR/1000)')]
for i, (lab, fo) in enumerate(labs, start=1):
    ws.cell(B0+i, 1, lab).font = F_SUB
    c = ws.cell(B0+i, 2, fo); c.fill, c.border, c.font = FILL["s"], BOX, Font(bold=True, size=10)
ws.cell(B0+6, 1, "Basis: FULL PROFILE, to the mineral contact.").font = F_SUB
ws.cell(B0+7, 1, "Reference depth reported alongside:").font = F_SUB
ws.cell(B0+7, 2, '=REFERENCE_DEPTH_CM&" cm"').font = F_N
ws.cell(B0+8, 1, "Note: the study-area mean weights each site by its area, which is right when sites differ in "
                 "size. It does NOT propagate the per-site uncertainties into a study-area interval — that needs "
                 "the stratified estimator described in Part 4.").font = F_IT
ws.merge_cells(start_row=B0+8, start_column=1, end_row=B0+8, end_column=11)
ws.cell(B0+8, 1).alignment = WRAP; ws.row_dimensions[B0+8].height = 30
ws.freeze_panes = "C5"

order = ['0. Instructions','1. Plot & Site Log','2. Core Log','3. Peat Data','4. Chronology',
         '5. Plot Summary','6. Site Summary','7. Settings','R1. Reference']
wb._sheets = [wb[n] for n in order]; wb.active = 0
wb.save("/home/user/Terrestrial_Carbon_Workshops_V1/Wetlands/04_Data_Interpretation/calculators/Wetland_Carbon_Calculator.xlsx")
json.dump(dict(SH=SH, NSUM=NSUM), open(f"{SCR}/_wsum.json","w"))
print("stage 3 ok — chronology summary at row", SH, "· sheets:", wb.sheetnames)
