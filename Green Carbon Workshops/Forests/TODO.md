# Forest Workshop TODO — gaps to fill

Everything the workshop still needs. Grouped by page. Most items are things only you can
supply — photos, videos, real data, lab quotes — or decisions to make.

Legend: 📸 image · 🔗 link · ✍️ writing · 📊 data · 📄 asset · ❓ decision · 🛠 build

---

## Decisions outstanding

- [ ] ❓ **Medium plot size** — the guides say 16 m², 25 m² and 100 m² in different places. The
  workbook takes it per-plot so nothing breaks, but the workshop text should recommend one.
  Currently written as "4 × 4 m or 10 × 10 m".
- [ ] ❓ **Is understory in scope by default**, or opt-in? Currently written as optional, with
  [3C](03_Field_Methods/3C_Understory.md) opening on "is this worth doing?".
- [ ] ❓ **Dead wood and litter** — currently declared out of scope in
  [Part 1](01_Background/). Confirm, or find a protocol.
- [ ] ❓ **Worked example** — keep the constructed Moose Ridge dataset, or replace with real data
  (Peawanuck appears throughout the WWF guides and both datasheets)?

## Landing page (`README.md`)

- [ ] 📸 The nested plot diagram from the protocol guides — one centre, large/medium/small plots
  overlapping, soil point offset outside.

## Part 1 — Background (`01_Background/`)

- [ ] 📸 Forest carbon-cycle slide (pools as boxes, fluxes as arrows).
- [ ] 📸 Stacked bar comparing Canadian pools — the 10:1 soil-to-tree point.
- [ ] 📸 Three carbon-curve animations. The eelgrass repo's `download (Null).gif`,
  `download (pulse).gif` and `download.gif` can be reused with forest captions.
- [ ] 📸 Soil pit face with horizons visible and a tape for scale.
- [ ] ✍️ Slide deck for Part 1 (`.pptx` + `.pdf`), as the eelgrass workshop has.
- [ ] 🔗 The other regional protocols, as they become available.
- [ ] 📊 Confirm the Canadian pool figures (21 Gt forest biomass, 208 Gt non-peat soil to 1 m,
  0.2 Gt non-treed) against their primary sources rather than the guides' introductions.

## Part 2 — Project Planning (`02_Project_Planning/`)

- [ ] 📄 **Forest Sample Allocation Calculator** spreadsheet — the forest counterpart to the blue
  carbon one, so teams can size a campaign without opening Earth Engine. Maths is in Appendix A;
  the blue carbon workbook is in [`_source/`](_source/) as a starting point.
- [ ] 🛠 **Port the GEE sampling tool to forest priors** — swap `PNW_PRIORS` (Janousek marine
  values) for Sothe-derived forest and soil figures, change `DEFAULT_ECOSYSTEM`, set
  `PLOT_M2` to 400, fix the dead `CONFIG.REPO` link, and re-brand from "Blue Carbon Sampling
  Design Tool". **Keep the `RUN_SELF_TEST` harness.**
- [ ] 📊 Derive the forest priors themselves — mean and SD over representative AOIs from the
  Sothe layers, plus a defensible CV inflation factor (currently written as "at least 1.5×").
- [ ] 📸 Screenshots: boundary drawn in the tool; a stratified site; the sample-size output.
- [ ] ❓ Confirm the soil plot footprint is 100 m² for the purposes of *N* (taken from the soil
  checklist's 10 × 10 m plot).

## Part 3 — Field Methods (`03_Field_Methods/`)

- [ ] 📸 **Many field photos.** Each page marks its own; the big ones are: crew laying out a
  circular plot · marked plot centre · flagged plot before measurement · DBH tape at 1.3 m ·
  rangefinder height shot · soil probe at refusal · corer and recovered core · core laid out and
  sliced · labelled bags · sieved coarse fragments · quadrat and clippers · clipped samples
  before and after drying.
- [ ] 📸 Nested plot diagram, and the 1 m depth-survey grid figure.
- [ ] 📸 The dichotomous key from the Trees guide (p.13).
- [ ] 🔗 **WWF video playlist URLs** — each guide has a corresponding video. Link them at the
  step they belong to.
- [ ] 📄 **Understory Survey datasheet** — the set currently has Tree and Soil only.
- [ ] 🛠 Update `Tree-Survey-Datasheet.docx`: add **GNSS accuracy** and **datum** fields (required
  for the LiDAR supplement), and a **circumference vs diameter** tick box.
- [ ] 🛠 Update `Soil-Carbon-Data-Sheet.docx`: rename "Outside Depth"/"Inside Depth" to the
  Non-peat guide's **hole depth** / **core length recovered**, and add a **coarse fragments**
  column to the section table.
- [ ] 📚 **Understory allometry beyond Flade et al.** The current list is 6 northern shrub taxa
  plus a pooled equation — thin for southern Canada. Needs sources from outside the WWF guides.

## Part 4 — Data Interpretation (`04_Data_Interpretation/`)

- [ ] 📊 **Lab directory table** — real labs: website, contact, analyses, cost per sample,
  "quoted on" date. Ask each which **bulk density basis** they report.
- [ ] 📸 Paper datasheet next to the digitized tab.
- [ ] 📸 Filled-in lab submission manifest.
- [ ] 📸 A one-page results summary figure.
- [ ] ✍️ Expand "Communicating with partners" — worked language and a one-page template.
- [ ] ✍️ Full citation for **Flade et al. (2020)** — journal, volume, DOI.
- [ ] 📊 **Verify the two root:shoot equations** against Paré et al. (2013) / Addo-Danso et al.
  (2016). The deciduous power law and the conifer fixed ratio come from different derivations
  and diverge sharply at small stem sizes; the workbook flags anything outside 10–40% but the
  underlying relationships should be checked.

## Part 5 — LiDAR Supplement (`05_LiDAR_Supplement/`)

- [ ] 🛠 **Add an ABA export tab to the calculator** that builds `field_plots.csv` directly —
  projected coordinates, `agb_mgha` from above-ground biomass only, correct units. Three
  documented traps make a manual conversion risky.
- [ ] 📸 Canopy height model with plot locations overlaid, beside the resulting carbon map.
- [ ] 📸 The 20 m pixel / 11.28 m plot geometry figure.
- [ ] ❓ Is **TreeTop** (the Shiny CHM explorer) part of this deliverable or a separate link?
- [ ] ❓ Does the supplement extend to Wetlands, or stay forest-only?

## Workbook (`04_Data_Interpretation/calculators/`)

- [x] ✅ Built and verified — filled with the six-plot example and recalculated in LibreOffice
  with zero error cells.
- [ ] 🛠 Add a **Study Area** interval. The study-area mean is area-weighted, but per-site
  uncertainties are not propagated into a combined interval — that needs the stratified
  estimator, which is noted on the tab and deferred with the R pipeline.
- [ ] ❓ Confirm the default `REPORTING_DEPTH_CM` of 30 cm.
- [ ] 🛠 Consider a **species picker by region** — 42 species is a long dropdown for a crew who
  will only meet a dozen.

## Deferred

- [ ] 🔴 **R analysis pipeline** — the forest counterpart to the eelgrass
  `DataAnalysisWorkflow/`: stratified design-based estimation, depth harmonisation, and a
  rendered report. Deferred by agreement; the workbook covers the arithmetic in the meantime.
- [ ] 🗺 **Community led carbon mapping** — an R-based analysis turning plot measurements into a
  carbon map with uncertainty, as a baseline communities can hold and re-map against.
  **Series-wide**, not forest-specific; a placeholder sits in
  [Part 4](04_Data_Interpretation/README.md). The workflow is to be supplied and then documented
  here, the way [Part 5](05_LiDAR_Supplement/) documents the LiDAR pipeline — read file-by-file
  and verified against its head, not its README.
