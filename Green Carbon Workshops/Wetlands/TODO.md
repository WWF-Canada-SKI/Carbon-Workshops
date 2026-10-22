# Wetland Workshop TODO — gaps to fill

Everything the workshop still needs. Grouped by page. Most items are things only you can
supply — photos, videos, real data, lab quotes — or decisions to make.

Legend: 📸 image · 🔗 link · ✍️ writing · 📊 data · 📄 asset · ❓ decision · 🛠 build

---

## Decisions outstanding

- [ ] ❓ **Is a Canadian wetland regional protocol coming?** Forests pairs with
  [`SO-StLawrence-Eng-2026.pdf`](../Forests/01_Background/SO-StLawrence-Eng-2026.pdf).
  [Part 1](01_Background/) currently says plainly that no wetland equivalent is in the folder and
  treats the depth survey as doing that work empirically. If one exists, it belongs in
  `01_Background/` and Part 1's closing section should point at it.
- [ ] ❓ **Marshes** — currently accepted as a wetland type in the calculator and mentioned in
  [Part 1](01_Background/), but out of scope for the method (usually mineral, shallow organic
  horizons). Confirm, or write them in properly.
- [ ] ❓ **Dead wood and litter in swamps** — declared out of scope in
  [Part 3B](03_Field_Methods/3B_Vegetation.md), same as in Forests. Confirm, or find a protocol.
  Flooded swamps kill trees standing, so this pool is not negligible there.
- [ ] ❓ **Default reference depth** — set to **100 cm** (`REFERENCE_DEPTH_CM`), the coastal-carbon
  convention. 30, 50 and 200 cm are all in use. Confirm 100 is the right default for a Canadian
  peatland audience.
- [ ] ❓ **Worked example** — keep the constructed Mica Bog dataset, or replace with real data?
  Peawanuck appears throughout the WWF guides.
- [ ] ❓ **Minimum cores per stratum** — [Part 2](02_Project_Planning/) states **3** (Forests uses
  5) on the grounds that 3 is the honest floor for a peatland campaign and matches Bansal's
  "three or more". Confirm.

## Landing page (`README.md`)

- [ ] 📸 The three wetland types side by side, showing the water-source difference: rain on a
  raised bog, groundwater feeding a fen, a treed swamp.
- [ ] 📸 Cross-section through a raised bog — peat thickening from the lagg margin to the dome
  centre, with coring points and the mineral contact marked.

## Part 1 — Background (`01_Background/`)

- [ ] 📸 Peatland carbon-cycle slide: atmosphere, vegetation, acrotelm, catotelm, and the methane
  pathway out.
- [ ] 📸 Stacked bar adding peat to the Canadian pools figure from
  [Forests Part 1](../Forests/01_Background/) — the small-footprint / tall-bar point.
- [ ] ✍️ Slide deck for Part 1 (`.pptx` + `.pdf`).
- [ ] 🔗 **WWF peat coring video** — the guide states it has "a corresponding video". Playlist URL
  needed here and in [Part 3](03_Field_Methods/).
- [ ] 📊 Confirm the Canadian peatland area and stock figures against primary sources before
  quoting any in the slide deck. Part 1 currently uses only Bansal's global figures, which are
  cited.

## Part 2 — Project Planning (`02_Project_Planning/`)

- [ ] 🛠 **Build the wetland sampling-design tool.** The
  [Forests tool is a placeholder](02_Project_Planning/Sampling%20Design%20Tools/) — its priors are
  forest values and its plot size is 400 m². Needs: peatland priors, **100 m² plots**,
  stratification by wetland type and landscape position, and the **t-floor from
  [A9](02_Project_Planning/README.md#a9--plan-with-z-floor-it-with-t)** reported beside the
  Cochran figure. **Keep the `RUN_SELF_TEST` harness.**
- [ ] 🛠 **Prior carbon scoping tool** — a larger version is in development. The existing Forests
  script already loads **CanPeat** (`projects/north-star-project-470316/assets/peat_profiles`) and
  **WoSIS**, which is the peatland prior source; it needs filtering to organic soils and
  summarising over an AOI.
- [ ] 📊 **Derive real peatland priors** — mean and CV by wetland type from CanPeat, plus a
  defensible map-CV inflation factor. Part 2 currently recommends deriving the prior from your own
  depth survey, which is better anyway, but a fallback is still needed for scoping.
- [ ] 📄 A **sample allocation spreadsheet**, so a team can size a campaign without Earth Engine.
  The maths is in Appendix A.
- [ ] 📸 Screenshots: a stratified peatland complex in the tool; a depth-probe grid with
  interpolated depth contours; a 10 × 10 m plot with its 121 probe points and chosen coring point.
- [ ] 📸 A depressional wetland from above with concentric vegetation zones marked, plus a
  cross-section showing the depocentre and the hummock–hollow surface.
- [ ] ✍️ Slide deck for Part 2.

## Part 3 — Field Methods (`03_Field_Methods/`)

**Field photos are the biggest single gap in the workshop.** Your Frame A/B/C images already
appear in the peat guide's appendix credited to you, so those may be yours to reuse at higher
resolution.

- [ ] 📸 **Russian corer in the open and closed positions**, side by side, with the serrated edge
  visible. This is the single most useful photo on the page — [3A](03_Field_Methods/3A_Peat_Coring.md)
  describes it in words because there is no image.
- [ ] 📸 The **two-person lift** at extraction step 5.
- [ ] 📸 A core being **carried horizontally**.
- [ ] 📸 A **revealed core on the tarp** with the whiteboard in frame — what a good core photo
  looks like.
- [ ] 📸 **Frame A/B/C at higher resolution**: the *Sphagnum* green→brown transition; mucky→lighter
  peat with wood; the peat→mineral contact.
- [ ] 📸 A **close vertical section through the *Sphagnum* surface** with a scale bar, for the
  double-counting boundary in [3B](03_Field_Methods/3B_Vegetation.md).
- [ ] 📸 A **filled 11 × 11 depth grid** for one plot, with the median contour and chosen coring
  point marked, beside the two-tape layout in the field.
- [ ] 📸 An example **14-photo series** from a bog, a fen and a swamp.
- [ ] 🔗 WWF peat coring video, at the coring steps.
- [ ] ✍️ Slide deck for Part 3.
- [ ] 📄 A **vegetation datasheet** for swamp work, or confirm that routing to the
  [Forests tree datasheet](../Forests/03_Field_Methods/datasheets/Tree-Survey-Datasheet.docx) is
  enough.

## Part 4 — Data Interpretation (`04_Data_Interpretation/`)

- [ ] 💰 **Lab quotes** — per-sample cost and turnaround for bulk density, LOI₅₅₀ and CHN from two
  or three Canadian labs, **including which bulk-density basis each reports** and whether their
  volume calculation assumes a full or half cylinder. This is the number teams ask for first and
  the one the workshop cannot currently answer.
- [ ] 📊 **A local LOI→carbon calibration**, from CHN on a subset of real Canadian peat. The
  default 0.5 is disclosed as uncalibrated everywhere it is used; a real regression would let the
  workshop recommend a number rather than a convention.
- [ ] ✍️ Slide deck for Part 4.
- [ ] 🛠 **R analysis pipeline for stocks** — *deferred by agreement.* The workshop stops at the
  spreadsheet. When it lands it should read the same workbook and reproduce the same numbers.
- [ ] 🗺 **Community led carbon mapping** — an R-based analysis turning plot measurements into a
  carbon map with uncertainty, as a baseline communities can hold and re-map against.
  **Series-wide**, not wetland-specific; a placeholder sits in
  [Part 4](04_Data_Interpretation/README.md). The workflow is to be supplied and then documented
  the way [Part 5](05_Chronology_Supplement/) documents `SedimentChronologies_R` — read
  file-by-file and verified against its current head, not its README.

## Part 5 — Chronology Supplement (`05_Chronology_Supplement/`)

- [ ] 💰 **Lab costs** — per-sample gamma (²¹⁰Pb + ¹³⁷Cs) and AMS ¹⁴C pricing, Canadian labs. Cost
  × 20–30 samples × 3 replicate cores decides whether a project can do this at all.
- [ ] 📸 A **real ²¹⁰Pb/¹³⁷Cs activity profile** from a Canadian peatland — excess ²¹⁰Pb, supported
  background and the ¹³⁷Cs peak marked, beside the resulting age–depth model. Bansal's Fig. 19a is
  the model.
- [ ] 🧪 **A real dated peat core** to replace the constructed chronology in the worked example.

### `SedimentChronologies_R` — recorded, not fixed

The [supplement](05_Chronology_Supplement/) documents these; this workshop does not modify the
repository. All verified directly against its current head.

- [ ] 🛠 **One `select()` fixes two of them.** Script `01`'s write of `01_activity_profile.csv`
  drops `dry_bulk_density_g_cm3` and `cs137_dpm_g`, which the input template already carries.
  Adding them would make `car_factor` compute instead of returning NA for every row, and would let
  the ¹³⁷Cs validation section run at all — the one cross-check the peatland ²¹⁰Pb-mobility caveat
  most requires.
- [ ] 🛠 `bg_value`/`bg_error` are assigned only in the no-Ra-226 branch of `01` and `03`, then
  used unconditionally. A core **with** ²²⁶Ra data errors out; one without runs.
- [ ] 🛠 Related: supported ²¹⁰Pb is treated as a scalar downstream, while the ²²⁶Ra branch
  correctly makes it per-depth.
- [ ] 🛠 All four scripts default `data_file` to `example_pb210_data.csv`; the repo ships
  `template_pb210_data.csv`.
- [ ] 🛠 `05_RERCA_Report.qmd` line 272 derives calendar years from `Sys.Date()` rather than the
  coring year. `03_serac.R` already uses `coring_year` correctly.
- [ ] 🛠 `02_rplum.R` reads `crs_ages.csv`; `01` writes `01_crs_ages.csv`. The overlay never draws.
- [ ] 🛠 `readline()` in `01` and `03` blocks non-interactive runs.
- [ ] 🛠 The README lists `03_serac.R` as CRS/CIC/CFCS; it calls `c("CRS", "CFCS")`.
- [ ] 📐 **LORCA scripts** — `rbacon`/`rplum` with ¹⁴C calibration. `LORCA/` is a README today, and
  `02_rplum.R` is closer to whole-core capability than that folder suggests, since Plum already
  accepts ²¹⁰Pb, ¹³⁷Cs, ¹⁴C and calendar ages in one model.

## Worked Example (`Worked_Example/`)

- [ ] 📊 Replace the constructed dataset with real data, or keep and label clearly *(it is
  currently labelled clearly)*.
- [ ] 📸 A plot of the **interval CAR decay** — 94.6 → 25.1 g C/m²/yr down the profile. It is the
  clearest single illustration of the acrotelm/catotelm idea in the whole workshop and currently
  exists only as a table.

## Series-level

- [x] ✅ **Grasslands** — the third ecosystem in
  [`BUILD_PLAN.md`](../BUILD_PLAN.md). **Written**, including an optional
  [Part 5 on monitoring](../Grasslands/05_Monitoring/). Its own gaps are in
  [`Grasslands/TODO.md`](../Grasslands/TODO.md).
- [x] ✅ **Series landing page** at the repository root, tying Forests, Wetlands and Grasslands
  together.
- [ ] 🔗 WWF video playlist URLs, across all workshops.
- [ ] 📊 Verify the two Forests root:shoot equations against Paré (2013) / Addo-Danso (2016) —
  carried over unchanged from the source workbooks and used by
  [3B](03_Field_Methods/3B_Vegetation.md) for swamp trees.

---

## Verified and closed

Kept as a record of what has been checked, so it is not re-litigated.

- [x] ✅ **Calculator** — zero error cells blank and filled; all 10 core stocks reproduce against
  an independent Python recomputation.
- [x] ✅ **Part 2 figures** — every sample-size number computed before being written, asserted
  against a fresh recomputation using a scipy-free two-sided *t*-inverse validated to four
  decimals against published tables.
- [x] ✅ **Datasheet fields** — every field a crew fills in matches the calculator's column names,
  asserted field-for-field.
- [x] ✅ **Links** — all relative links and anchors across the repository resolve.
- [x] ✅ **The guide's Eq 5 units** — the printed parenthetical says g/cm², the left-hand side and
  step-6 prose say kg/m², and the guide's own example spreadsheet uses kg/m². The workshop uses
  the correct form and documents the discrepancy in
  [Part 4](04_Data_Interpretation/README.md).
- [x] ✅ **`SedimentChronologies_R` findings** — all ten issues verified against the repository's
  current head, not from memory.
