# Forest Carbon Workshop — Plan (revised after asset ingest)

*Supersedes the Forests section of [`BUILD_PLAN.md`](../../BUILD_PLAN.md). Written after
reading every uploaded asset plus the LiDAR supplement.*

---

## 1. Headline: the picture changed

Both items I flagged as **blocking** are resolved, and a third asset class arrived that I
hadn't planned for.

| Blocker (from BUILD_PLAN §7) | Status |
|---|---|
| NRCan/Lambert biomass coefficients | ✅ **`DataTemplate_TreesUpdated.xlsx`** — 175-row table, 42 species, Lambert (2005) + Ung (2008), with **both** DBH-only and DBH+height parameter sets |
| Shrub volume → biomass equations | ✅ **`Carbon-Calculator-Medium-Vegetation.xlsx`** — Flade et al. (2020), `y = b·xᵃ`, 6 species + an all-shrub pooled row |
| *(unplanned)* Skill checklists | ✅ 2 checklists — these also close the **"Eelgrass Workshop Skills Checklist"** TODO left open in the source repo |

**Forests is no longer the hardest workshop to build — it's the closest to done.** The
calculation spine (field sheet → allometrics → per-individual carbon) exists and works.
What's missing is *consistency between the pieces* and the *scaling/uncertainty layer*.

That reframes the job from "write a workshop" to "make eight assets behave like one system."

---

## 2. What we now have

### 2a. Uploaded to `Forests/Assets/`

| Asset | What it is | Verdict |
|---|---|---|
| `DataTemplate_TreesUpdated.xlsx` | 2 tabs: `Allometric Coefficeints` (175 rows) + `Large Vegation Data Sheet ` | **Core asset.** Well built — see §3 |
| `Carbon-Calculator-Medium-Vegetation.xlsx` | 2 tabs: `Vegetation Allometric Equations` (Flade 2020) + `Medium Sized Plot Data Sheet` | Good; AGB-only (see §4c) |
| `Carbon-Calculation-Example-Forest-Soil.xlsx` | 2 tabs: `Non-peat soil data` + `Answers_non-peatCore` | **Teaching exercise**, not a blank tool. Has a depth defect (§4d) |
| `Carbon-Calculation-Example-Peat-Soil.xlsx` | 3 tabs: core → site → study area | **Belongs in `Wetlands/`** — most complete scaling chain of the three |
| `Tree-Survey-Datasheet.docx` | Printable field sheet: plot description + 5 survey columns | Matches the tree workbook's input columns |
| `Soil-Carbon-Data-Sheet.docx` | Printable: project/plot/core notes + section table | See §4h — terminology inherited from blue carbon |
| `Forest_Carbon_Skill_Checklist (2).docx` | 5 sections, pre-field → calculations, with Eq 1–5 | Excellent. Use as the model for all three workshops |
| `Soil_Carbon_Skill_Checklist (2).docx` | 5 sections, 3 sampling methods, Eq 1–8 | Excellent. **Supersedes `(1)`** — delete (1) |
| `Soil_Carbon_Skill_Checklist (1).docx` | 131 paras vs 210 in (2); partial | **Redundant — remove** |
| `SamplingDesignTool_GEE` | 2,531 lines. Self-testing rewrite of the sampling tool | See §5 |

### 2b. The LiDAR supplement

`CathalD/ForestScanWorkflow-LiDR-TreeTop-` — a `targets`-based `lidR` pipeline: tiles →
DTM → CHM → structure metrics → individual tree detection → **area-based approach (ABA)**
biomass/carbon map with cross-validated error.

**It already aligns with the Trees protocol, without adjustment:**

| | Trees guide | LiDAR ABA | |
|---|---|---|---|
| Plot | circular **r = 11.28 m** (= 400 m²) | circular **r = 11.28 m**, to match a 20 m pixel (400 m²) | ✅ identical |
| AGB source | Lambert/Ung allometrics from DBH + height | *"species allometric equations, e.g. Lambert et al. (2005)"* | ✅ identical |
| Output | kg C/m² per plot | `agb_mgha` per plot → wall-to-wall map | ✅ unit conversion only |

So the handoff is: **Tree Survey Datasheet → tree workbook → `field_plots.csv` (`agb_mgha`)
→ ABA model → carbon map.** The one genuinely new field requirement is **sub-metre GNSS on
plot centres**, which the current tree datasheet does not ask for.

---

## 3. What's good and should be protected

The tree workbook is better engineered than I expected, and two behaviours are worth keeping
explicitly rather than accidentally:

1. **Automatic model switching.** `AJ = IF(height > 0, DBH+height model, DBH-only model)`.
   A crew that measured height gets the better equation; a crew that didn't still gets a
   number. This is exactly the right design and should be *documented as a feature* in the
   workshop text, because it silently changes which equation ran.
2. **Component-wise biomass.** Wood, bark, branches and foliage are looked up and computed
   separately, then summed — matching the guide's method rather than a single bulk equation.
3. **Self-testing GEE tool.** `SamplingDesignTool_GEE` has a test harness asserting its
   numbers against the Sample Allocation Calculator, and replaced a cubic inverse-normal
   approximation that was under-estimating *z* (and therefore *n*) badly at high confidence.
   Keep the harness when porting to terrestrial priors.
4. **The checklists.** Structure (skill / description / practised ☐ / trainer-confirmed ✔)
   is genuinely good pedagogy and has no eelgrass equivalent. Make it a series-wide pattern.

---

## 4. Defects and inconsistencies to fix

Ordered by how much they affect the reported number.

### 🔴 Scientific — these change the answer

**(a) `All` species silently gets the conifer root:shoot equation.**
`AK` = `IF(tree_type = "Deciduous", 1.576·AGB^0.615, 0.222·AGB)`. The lookup column K is
`"NA"` for the generic `All` row, so `All` falls to the ELSE branch and is treated as
softwood. A user picking the safest-looking generic option gets a hidden species assumption.
*Fix:* make the `All` case explicit — either a third branch with a pooled ratio, or refuse
and prompt for Deciduous/Conifers.

**(b) The two BGB equations are not the same kind of model.**
Hardwood is a power law (`1.576·AGB^0.615`); softwood is a fixed ratio (`0.222·AGB`). They
come from different derivations and are presented as equivalent. At small AGB they diverge
sharply — for a 10 kg tree, hardwood BGB ≈ 6.5 kg (65%), softwood ≈ 2.2 kg (22%). The guide
itself states BGB is 18–30% of total biomass, which the hardwood equation violates at small
sizes. *Fix:* verify both against Paré et al. (2013) / Addo-Danso et al. (2016), state the
applicable DBH range, and flag out-of-range results rather than returning them silently.

**(c) Medium vegetation has no belowground component at all.**
Flade et al. (2020) coefficients are aboveground. The sheet goes straight
`biomass → carbon = biomass/2` with no BGB step, while the tree sheet does apply one. Two
pools in the same workshop, two different definitions of "total biomass."
*Fix:* add a shrub root:shoot (Mokany et al. 2006 is the standard source), or state the
omission prominently so the pools aren't summed as if comparable.

**(d) The forest soil example averages cores integrated to different depths.**
`Answers_non-peatCore!E9 = SUM(F3:F5)/3` averages three cores of **50 cm, 30 cm and 40 cm**.
A deeper core holds more carbon simply for being deeper, so this mean describes no defined
depth. This is a *teaching* workbook, so it teaches the error.
*Fix:* harmonise to a common depth every core reached (the eelgrass workshop's
`PRIMARY_DEPTH_CM` pattern — report the measured depth, and anything deeper separately with
the modelled share stated).

**(e) No coarse-fragment correction anywhere.** Forest mineral soils are stony; carbon stock
must be computed on the fine-earth (<2 mm) fraction. Neither the guide's equations nor the
workbook correct for it, so stock is overestimated on stony sites — which is most of the
Shield. *Fix:* add a `coarse_fragment_pct` column and a fine-earth correction to Eq 1.

**(f) No uncertainty at any step, in any asset.** Eq 1–5 and Eq 1–8 produce point estimates
only — no SE, no CI, no check against the precision target that the *planning* stage spent
a whole section choosing. This is the single biggest gap between these assets and the
eelgrass workshop, and it's also the LiDAR guide's own stated non-negotiable
(*"a carbon number without an uncertainty is not usable"*). See §6.

### 🟠 Consistency — these stop the assets working as one system

**(g) Plot size is stated three different ways across WWF's own documents.**

| Source | Large | Medium | Small |
|---|---|---|---|
| Trees guide | 400 m² (r=11.28 m / 20×20 / 10×40) | — | — |
| Sampling Design guide | 400 m² | **25 m²** (range 16–100) | — |
| Vegetation guide | — | **16–100 m²** | 1 m² |
| `Soil_Carbon_Skill_Checklist (2)` | 20×20 m | **10×10 m (100 m²)** | 1×1 m |
| `SamplingDesignTool_GEE` | `PLOT_M2: 100` | — | — |
| LiDAR ABA | **400 m²** (must match pixel) | — | — |

Every `kg C/m²` divides by plot area, so this is not cosmetic. **Needs one authoritative
table, set once and referenced everywhere.** Recommend 400 / 25 / 1 m² per the Sampling
Design guide, with 400 m² locked for any plot intended to calibrate LiDAR.

**(h) The soil datasheet uses blue-carbon compaction terminology.**
`Soil-Carbon-Data-Sheet.docx` asks for *"Outside Depth"* / *"Inside Depth"* — the eelgrass
push-corer fields. The Non-peat guide measures the same thing but calls it **core length**
and **hole depth** (*"The hole depth is the true depth of the core"*).
*Good news:* this means the eelgrass compaction machinery **does** transfer to non-peat soil
cores — unlike peat cores, where a side-filling Russian corer doesn't compact this way.
*Fix:* rename to the guide's wording, keep the arithmetic.

**(i) Core/plot ID conventions differ across every asset.**
`PE - S2 - P3` (tree header, with spaces) vs `PE-S2-P3` (tree data rows) vs `PE-S3-P4`
(medium veg) vs `WF-01-01` + 4 separate ID columns (forest soil) vs `DB-01-01` (peat) vs
the Peat guide's stated `PE-01-B` = Location–Site–Sample.
Since pools must join on Plot ID for a nested design to produce one total, **one convention
has to win.** Recommend the guide's `Location–Site–Plot` with a documented separator, and a
validation rule that flags mismatches rather than silently returning blanks.

**(j) Typos baked into sheet names, headers and lookups.**
`Coefficeints`, `Coeffiecints`, `Vegation`, `Longtitude`, `measurementts`, `bracnhes`,
`folaige`, `coeffiecnt`, `coeffeicnt`, `LOI5505`. Most are cosmetic, but
**`'Large Vegation Data Sheet '` carries a trailing space** that every cross-sheet formula
depends on — rename carefully, or leave it and document it.

**(k) Neither biomass workbook aggregates to plot level.** Both stop at per-individual
carbon (`M`/`AM`). The checklists describe Eq 1–5 and the soil workbooks implement their
chain, but the tree and shrub workbooks don't. *Fix:* add a Plot Summary tab to each.

**(l) Carbon fraction 0.5 is hardcoded in three places** (`AM=AL*0.5`, `M=L/2`, `K=J/2`).
Consistent, but should be one named parameter with its source stated, so it can be changed
and audited in one place.

### 🟡 Filing

- `Carbon-Calculation-Example-Peat-Soil.xlsx` → move to `Wetlands/`
- `Soil_Carbon_Skill_Checklist (1).docx` → delete (superseded by `(2)`)
- `Forests/Assets/README.md` is empty
- Filenames carry `(1)`/`(2)` download suffixes — rename on filing
- `Non-peat-FINAL-Eng-2026.pdf` still duplicated with `Grasslands/` → `_Shared/`

---

## 5. The GEE sampling tool

Architecturally the cleanest asset here, and the terrestrial port is a **narrow, well-defined
swap** rather than a rewrite:

| Change | Where |
|---|---|
| Priors table | `BCStats.PNW_PRIORS` — 4 marine rows (Janousek 2025) → forest rows (biomass + soil) |
| Default ecosystem | `CONFIG.DEFAULT_ECOSYSTEM: 'Eelgrass'` → `'Forest'` |
| Plot area | `CONFIG.PLOT_M2: 100` → 400, per §4g |
| Depth basis | `DEFAULT_DEPTH_CM: 30` — keep for soil; biomass needs no depth axis |
| Repo links | `CONFIG.REPO` points at a non-existent repo; `LINKS` has two `TODO`s | 
| Branding | Header still reads "Blue Carbon Sampling Design Tool / Coastal Blue Carbon Hub" |
| Stratification layer | Already uses Dynamic World / S2 / SRTM / Satellite Embedding — all fine for forest |

**Keep the `RUN_SELF_TEST` harness.** It is what makes the tool's numbers auditable against
the spreadsheet, and it caught a real error before.

The prior swap needs a source. The forest equivalents of Janousek are:
- **NFI ground plot data** (open.canada.ca) — plot-level biomass by ecozone/stand type
- **Canadian Upland Forest Soil Profile and Carbon Stocks Database** (Shaw et al., NRCan) — soil side
- Kurz et al. (2013), *Environ. Rev.* 21:260–292 — boreal synthesis

---

## 6. The estimator question, now concrete

BUILD_PLAN §5 raised this in the abstract. The assets make it specific: **every uploaded
calculator implements the unweighted protocol arithmetic, and none reports uncertainty.**

Meanwhile the *planning* side of the same workshop (GEE tool, Sample Allocation Calculator)
spends its whole effort choosing a margin of error and confidence level — and then nothing
downstream ever checks whether the campaign hit it. That's a loop the workshop leaves open.

The LiDAR supplement is the outlier: it already requires a cross-validated %RMSE and calls a
carbon number without uncertainty unusable.

**Recommendation, unchanged but now sharper:** keep the protocol arithmetic as the visible,
by-hand path (it is what the printed guides teach, and participants will look for it), and
add **one Plot Summary tab per pool plus one Study Area tab** that carries the stratified
area-weighted mean, its SE, a CI, and a PASS/FAIL against the planning target. That closes
the plan → collect → check loop without contradicting the published guides.

This is a decision about what the workshop teaches, so it's yours — but note that adopting
it makes the three tiers consistent (planning sets a target → field-based summary checks it
→ LiDAR reports %RMSE), and declining it leaves Tier 2 stricter than Tier 1.

---

## 7. Proposed structure for the Forests workshop

Three tiers, so teams self-select by capability — the LiDAR component is **additive, never
required**:

| Tier | Needs | Produces |
|---|---|---|
| **1 — Field** | Crew, DBH tape, rangefinder, auger | Plot/site/study-area carbon from measured plots |
| **2 — LiDAR** *(optional)* | Tier 1 plots **+ LiDAR coverage** + R | Wall-to-wall carbon map with cross-validated error |
| **3 — Analysis** *(deferred)* | R pipeline | Stratified estimate + uncertainty |

```
Forests/
├── README.md                        ← landing; the data-sheet spine, 3 tiers
├── 01_Background/                   ← forest carbon, pools, disturbance regime
├── 02_Project_Planning/
│   ├── README.md                    ← 5 steps; Step 3 becomes multi-pool
│   ├── SamplingDesignTool_GEE       ← forest-prior port
│   └── SampleAllocation_Calculator.xlsx
├── 03_Field_Methods/
│   ├── README.md                    ← trees + soil, sequenced
│   ├── Trees-FINAL-Eng-2026.pdf
│   ├── Non-peat-FINAL-Eng-2026.pdf  (→ _Shared/)
│   ├── datasheets/                  ← Tree-Survey + Soil-Carbon (printable)
│   └── checklists/                  ← Forest + Soil skill checklists
├── 04_Data_Interpretation/
│   ├── README.md                    ← lab, LOI vs CHN, scaling, reporting
│   └── calculators/                 ← tree · medium-veg · soil (blank + worked)
├── 05_LiDAR_Supplement/             ← NEW
│   └── README.md                    ← when it applies, plot rules, handoff, limits
├── Worked_Example/
└── TODO.md
```

**Why `05_` and not a section inside `04_`:** it has its own prerequisites (data coverage,
R, GNSS), its own failure modes (temporal mismatch, model transfer), and most teams won't
run it. Burying it inside Data Interpretation would imply it's part of the normal path.

---

## 8. What the LiDAR supplement page must say

Short page, four jobs:

1. **When it applies** — needs existing LiDAR coverage, ~30–50 plots, sub-metre GNSS, R.
   Without all four, stay at Tier 1.
2. **What changes in the field** — plots must be **circular, 400 m², r = 11.28 m**, centres
   at **sub-metre GNSS**, spread across the **full range of canopy height and density**
   (not randomly — ABA can only interpolate within structure it has seen). This is a
   *different placement rule* from Part 2's probability sampling, and the tension needs
   saying out loud rather than glossing.
3. **The temporal reconciliation** — LiDAR lift date vs plot measurement date, growth
   correction, which plots get dropped. The guide's `max_gap_years = 2` default.
4. **The limits** — models don't transfer between acquisitions or forest types; structure
   proxies without plots are not carbon; report the cross-validated %RMSE.

One addition needed to the **Tree Survey Datasheet**: a **GNSS accuracy / datum** field.
Plot centre position error de-aligns plot and pixel and adds noise that cannot be modelled
out — and the current sheet records lat/long with no accuracy or datum.

---

## 9. Revised task list for Forests

### Assets to fix (I can do these)
- [ ] `All`-species BGB branch (§4a)
- [ ] Add Plot Summary tab to tree and medium-veg workbooks (§4k)
- [ ] Build a **blank** non-peat soil calculator (only the worked example exists)
- [ ] Harmonise IDs, headers, typos, and the plot-size table (§4g, §4i, §4j)
- [ ] Rename soil datasheet compaction fields to guide wording (§4h)
- [ ] Add coarse-fragment column + fine-earth correction (§4e)
- [ ] Add depth harmonisation to the soil chain (§4d)
- [ ] Port `SamplingDesignTool_GEE` to forest priors; keep the test harness (§5)
- [ ] Move peat example → `Wetlands/`; delete checklist `(1)`; de-duplicate the PDF
- [ ] Add GNSS accuracy/datum field to the Tree Survey Datasheet (§8)
- [ ] Write §7's pages

### Still needed from you
- [ ] **Decision:** estimator + uncertainty layer (§6)
- [ ] **Decision:** authoritative plot sizes (§4g)
- [ ] **Decision:** is understory (small vegetation, clip-and-weigh) in scope for Forests?
      If yes, a small-vegetation calculator is missing — only Medium exists
- [ ] **Verify:** the two BGB equations against their sources (§4b) — you're closer to
      this literature than I am
- [ ] Forest slide deck
- [ ] WWF trees/soil video playlist URLs
- [ ] Field photos (plot layout, DBH tape, rangefinder, tagging, soil pit horizons)
- [ ] Worked-example site + real data — is Peawanuck usable? It's the example site
      throughout the guides and both datasheets
- [ ] Forest priors for the GEE tool, or approval to derive them from NFI open data
- [ ] Lab contacts/quotes for the lab directory table

---

## 10. Open questions

1. **Is the LiDAR supplement forest-only, or does it come to Wetlands too?** `lidR` handles
   peatland microtopography and shrub height, but ABA calibration for non-tree carbon is a
   much weaker link. My instinct: forest-only for now.
2. **`TreeTop` Shiny app** — the LiDAR guide mentions it for partners exploring the CHM
   without code. Is it part of this repo's deliverable, or a separate link?
3. **Should the three tiers share one workbook** (tabs for trees/shrubs/soil joined on Plot
   ID) **or stay separate files?** One workbook is better for the "work back from the sheet"
   pedagogy and for summing pools; separate files are easier to hand to different crews.
4. **Peawanuck as the worked example** — real data, or constructed for teaching as the
   eelgrass example is?
