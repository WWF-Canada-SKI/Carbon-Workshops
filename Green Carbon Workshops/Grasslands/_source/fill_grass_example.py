"""Fill Grassland_Carbon_Calculator.xlsx with a constructed teaching dataset.

Three sites, nine plots. The numbers are drawn to be realistic for Canadian
grassland but no field crew collected them -- this is a teaching dataset.

Deliberate teaching cases:
  UP-03   cored only to 30 cm, so the full-profile figure equals the
          reporting-depth figure and the plot flags as a minimum
  BOS-03  hits refusal at 22 cm on an interior-BC-style shallow profile,
          with a truncated final increment
  GP-02   lab bulk-density basis left "Not confirmed"
  BOS-*   canopy cover at or above the threshold, so tree carbon is entered
  roots   made genuinely patchy, so soil MEETS its target and roots do NOT
          at the same n -- which is the whole argument of Part 2, A10
"""
import sys, openpyxl, random
sys.path.insert(0, "/home/user/Terrestrial_Carbon_Workshops_V1/Grasslands/_source")
from grass_style import OUT

SRC = OUT
DST = ("/home/user/Terrestrial_Carbon_Workshops_V1/Grasslands/Worked_Example/"
       "Grassland_Carbon_Calculator_WorkedExample.xlsx")

random.seed(11)
wb = openpyxl.load_workbook(SRC)

# ── sites and plots ──────────────────────────────────────────────────────────
PLOTS = [
    # plot, site, type, management, grazing, fire, native, canopy%
    ("GP-01", "S1", "Prairie", "Never cultivated", "Season-long", 12, "Native sward", 0),
    ("GP-02", "S1", "Prairie", "Never cultivated", "Season-long", 12, "Native sward", 0),
    ("GP-03", "S1", "Prairie", "Never cultivated", "Season-long", 12, "Native sward", 0),
    ("UP-01", "S2", "Prairie", "Never cultivated", "None", 12, "Native sward", 0),
    ("UP-02", "S2", "Prairie", "Never cultivated", "None", 12, "Native sward", 0),
    ("UP-03", "S2", "Prairie", "Never cultivated", "None", 12, "Native sward", 0),
    ("BOS-01", "S3", "Black Oak savannah", "Never cultivated", "None", 3, "Native sward", 28),
    ("BOS-02", "S3", "Black Oak savannah", "Never cultivated", "None", 3, "Native sward", 31),
    ("BOS-03", "S3", "Black Oak savannah", "Never cultivated", "None", 9, "Native sward", 22),
]

pl = wb["1. Plot & Site Log"]
for i, (p, s, typ, mgmt, graz, fire, nat, cov) in enumerate(PLOTS):
    r = 5 + i
    lat = 50.90 + i * 0.004
    lon = -104.62 - i * 0.005
    vals = [p, s, "RC", "2026-08-05", f"{typ} unit", round(lat, 4), round(lon, 4),
            0.5, "WGS84", 580 - i * 3, typ, mgmt, graz, fire, nat, cov,
            "Mid slope", ""]
    for c, v in enumerate(vals, start=1):
        pl.cell(r, c, v)

# ── soil increments ──────────────────────────────────────────────────────────
# (top, bottom, BD, OC%) profiles per site, before per-plot jitter
PROFILE = {
    "S1": [(0, 10, 1.02, 4.60), (10, 20, 1.18, 2.85), (20, 30, 1.27, 1.95), (30, 60, 1.36, 1.15)],
    "S2": [(0, 10, 0.94, 5.40), (10, 20, 1.12, 3.25), (20, 30, 1.24, 2.15), (30, 60, 1.33, 1.28)],
    "S3": [(0, 10, 1.31, 2.05), (10, 20, 1.43, 1.25), (20, 30, 1.49, 0.80), (30, 60, 1.52, 0.52)],
}
CF = {"S1": 2, "S2": 2, "S3": 11}          # coarse fragment % by site

# Per-plot multipliers on soil carbon, chosen to give realistic between-plot
# variability: S1 tight enough to MEET a +/-20% target at n=3, S2 and S3 not.
# Random jitter alone produced a CV near 0.01 and an absurd +/-1% interval.
PLOT_SOIL = {"GP-01": 1.05, "GP-02": 0.96, "GP-03": 0.99,
             "UP-01": 1.14, "UP-02": 0.82, "UP-03": 1.04,
             "BOS-01": 1.12, "BOS-02": 0.79, "BOS-03": 1.09}
DIAM = 5.0                                  # corer internal diameter, cm

sd = wb["2. Soil Data"]
row = 5
soil_rows = []
for p, s, *_ in PLOTS:
    prof = list(PROFILE[s])
    if p == "UP-03":
        prof = prof[:3]                     # cored only to 30 cm
    if p == "BOS-03":
        prof = prof[:2] + [(20, 22, 1.51, 0.72)]   # refusal on bedrock at 22 cm
    core = f"{p}-C1"
    for k, (top, bot, bd, oc) in enumerate(prof):
        m = PLOT_SOIL[p]
        j = random.uniform(-0.03, 0.03)
        bd_j = round(bd * (1 + j * 0.4), 3)
        oc_j = round(oc * m * (1 + j), 3)
        driven = bot
        recovered = bot if p != "GP-03" else round(bot * 0.94, 1)
        basis = "Not confirmed" if p == "GP-02" else "Fine earth / total volume"
        vals = [p, core, k + 1, top, bot, None, DIAM, driven, recovered, None,
                CF[s], basis, bd_j, oc_j]
        for c, v in enumerate(vals, start=1):
            if v is not None:
                sd.cell(row, c, v)
        if p == "BOS-03" and k == 2:
            sd.cell(row, 20, "Refusal on bedrock at 22 cm.")
        soil_rows.append((p, s, top, bot, bd_j, oc_j))
        row += 1

# ── roots ────────────────────────────────────────────────────────────────────
# g/m2 by depth, before jitter. Roots decline steeply but not to nothing.
ROOTMASS = {  # (top): (fine g/m2, coarse g/m2)
    0:  (900, 190),
    10: (430,  95),
    20: (240,  55),
    30: (210,  48),
}
SITE_ROOT = {"S1": 0.72, "S2": 1.00, "S3": 0.58}   # grazing suppresses root mass
# per-plot multipliers, chosen so roots are MUCH patchier than soil
PLOT_ROOT = {"GP-01": 1.34, "GP-02": 0.71, "GP-03": 0.95,
             "UP-01": 1.22, "UP-02": 0.62, "UP-03": 1.16,
             "BOS-01": 0.78, "BOS-02": 1.45, "BOS-03": 0.60}

AREA = 3.14159265 * (DIAM / 2) ** 2         # cm2
rt = wb["3. Root Biomass"]
row = 5
for p, s, top, bot, _bd, _oc in soil_rows:
    fine, coarse = ROOTMASS[top]
    mult = SITE_ROOT[s] * PLOT_ROOT[p]
    thick_scale = (bot - top) / 10.0
    for cls, gm2 in (("<=2 mm (fine)", fine), (">2 mm (coarse)", coarse)):
        g_per_core = gm2 * mult * thick_scale * AREA / 10000.0
        g_per_core *= random.uniform(0.90, 1.10)
        ash = round(random.uniform(0.06, 0.14), 3)
        # entered mass is BEFORE ash correction, as it comes off the balance
        entered = round(g_per_core / (1 - ash), 4)
        vals = [p, f"{p}-C1", top, bot, cls, "Live", entered, ash, 0.5]
        for c, v in enumerate(vals, start=1):
            rt.cell(row, c, v)
        row += 1

# ── vegetation ───────────────────────────────────────────────────────────────
VEG = {  # plot: (clip live g, clip dead g, shrub kg, tree kg C/m2)
    "GP-01": (34, 21, 0, None), "GP-02": (29, 18, 0, None), "GP-03": (38, 25, 0, None),
    "UP-01": (62, 48, 0, None), "UP-02": (58, 52, 0, None), "UP-03": (67, 44, 0, None),
    "BOS-01": (41, 19, 3.2, 1.94), "BOS-02": (36, 22, 4.1, 2.31),
    "BOS-03": (44, 17, 2.6, 1.42),
}
vg = wb["4. Vegetation Data"]
for i, (p, s, *_rest) in enumerate(PLOTS):
    cov = _rest[5]
    live, dead, shrub, tree = VEG[p]
    r = 5 + i
    # Phenology now occupies three columns (C-E), so the areas and masses sit
    # two columns further right than they did.
    vals = [p, "2026-08-05", "Peak standing biomass", "None observed", "Yes",
            0.25, live, dead, None, 100,
            shrub if shrub else None, None, cov, tree]
    for c, v in enumerate(vals, start=1):
        if v is not None:
            vg.cell(r, c, v)

# ── site summary inputs ──────────────────────────────────────────────────────
ss = wb["6. Site Summary"]
for i, (sid, area) in enumerate([("S1", 640000), ("S2", 95000), ("S3", 210000)]):
    ss.cell(5 + i, 1, sid)
    ss.cell(5 + i, 2, area)

# ── settings the example confirms ────────────────────────────────────────────
st = wb["7. Settings"]
CONFIRMED = {
    "ASH_CORRECTED": "Yes",
    # The example is built on the root-separated case: roots were sieved out of
    # the soil-carbon sample by the project's own procedure, which is what makes
    # its combined soil + root figure legitimate.
    "ROOT_SOIL_REPORTING_BOUNDARY": "Root-separated soil",
    "ROOT_SOIL_BOUNDARY_SOURCE": "Example lab agreement, method GC-SOC-02, 2026-05-14",
    "LAB_BULK_DENSITY_BASIS": "Fine earth / total volume",
    "LAB_METHOD_REFERENCE": "Example lab, methods GC-SOC-02 / GC-BD-01, confirmed 2026-05-14",
    "COMPARABLE_SEASON_RULE": "Clipped within 14 days of peak standing biomass, judged from "
                              "phenology on site; plots grazed or hayed in the preceding "
                              "30 days are excluded from pooled means.",
}
for r in range(5, 40):
    name = st.cell(r, 1).value
    if name in CONFIRMED:
        st.cell(r, 2, CONFIRMED[name])

import os
os.makedirs(os.path.dirname(DST), exist_ok=True)
wb.save(DST)
print("worked example written:", DST.split("/")[-1])
