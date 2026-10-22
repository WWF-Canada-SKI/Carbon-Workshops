# Grassland Workshop TODO — gaps to fill

Everything the workshop still needs. Grouped by page, with the **blocking** items first.

Most items are things only you can supply — references, photos, real data, lab quotes — or
decisions to make.

Legend: 📸 image · 🔗 link · ✍️ writing · 📊 data · 📄 asset · ❓ decision · 🛠 build · 📚 reference

---

## ⭐ The short list — what would help most, in order

If you only do four things from this file, do these.

| # | What | Why it matters |
|---|---|---|
| **1** | 📚 **Root-methods references** (see [below](#root-methods-references--the-big-one)) | Every claim in the root sections is currently written at a level the method itself supports, with **nothing cited**. These pages cannot ship as authoritative until they are |
| **2** | 📊 **A Canadian grassland carbon reference** | Part 1 is written with few numbers rather than invented ones (the Sothe et al. national comparison was removed). It needs a citable source for the root:shoot relationship, soil carbon per unit area, and remaining native grassland area |
| **3** | ❓ **The tree-cover threshold** — at what canopy cover does the Forests tree protocol apply? | Savannah sits right on this boundary by definition. Proposed **≥ 25%**, matching the Wetlands swamp rule. Set it in the calculator's `Fill Me In` tab |
| **4** | 🔗 **The Community led carbon mapping repository** | Part 4's mapping section is a placeholder until this lands |

---

## Root-methods references — the big one

The decision to **measure** root biomass rather than apply a root:shoot ratio is the scientific
centrepiece of this workshop. It is also the part with **no citations yet**, because academic
domains are blocked from the build environment by an organisation policy denial (403 at the egress
proxy — not retryable).

**Easiest route: drop the PDFs into [`_source/`](_source/) or [`../_Shared/`](../_Shared/).**
That is what made page-level citation of Bansal et al. possible throughout the Wetlands workshop,
and it is why those pages hold up.

Candidates, in rough order of usefulness — **none verified from this session**, so treat the
citations themselves as unconfirmed until checked:

- [ ] 📚 **Freschet et al. (2021)**, *A starting guide to root ecology*, New Phytologist
  232:973–1122 — the current comprehensive standard for sampling, processing and traits.
- [ ] 📚 **McCormack et al. (2015)**, *Redefining fine roots…*, New Phytologist 207:505–518 — the
  argument that a 2 mm cutoff lumps functionally different roots.
- [ ] 📚 **Addo-Danso, Prescott & Smith (2016)**, *Methods for estimating root biomass and
  production…*, Forest Ecology and Management 359:332–351 — method bias. Also listed in
  [`../Forests/TODO.md`](../Forests/TODO.md).
- [ ] 📚 **Jackson et al. (1996)**, *A global analysis of root distributions…*, Oecologia
  108:389–411 — depth distribution, for quantifying what a 30 cm core misses.
- [ ] 📚 **Milchunas (2009)**, *Estimating root production…*, Ecosystems 12:1381–1402 —
  grassland-specific method bias.
- [ ] 📚 **Böhm (1979)** *Methods of Studying Root Systems* · **Smit et al. (2000)** *Root Methods:
  A Handbook* — the classic monographs.
- [ ] 📚 **New Phytologist 2004**, DOI `10.1111/j.1469-8137.2004.01201.x` — you linked this; it
  could not be resolved here, so its relevance is unknown.
- [ ] 📚 **ScienceDirect 2026**, PII `S2949790626001643` — likewise. You linked `#fig3`
  specifically, so that figure presumably matters.

**What I need from each:** the sieving and washing procedure, live/dead separation criteria,
**ash correction**, drying temperature, and whatever they say about systematic losses of the
finest roots.

---

## Decisions outstanding

- [ ] ❓ **Tree-cover threshold for the Forests protocol.** Proposed **≥ 25%** (matching Wetlands
  swamps). Savannah is the case that makes this matter.
- [ ] ❓ **Fine roots: in the soil pool, or reported separately?** The calculator supports both via
  `ROOT_SOIL_REPORTING_BOUNDARY`, alongside `ROOT_SOIL_BOUNDARY_SOURCE` for who agreed it and
  under which method. Default is **`Not agreed with the lab`** — deliberately, since that is the
  real starting state. Settle it with the laboratory and set it.
- [ ] ❓ **Root sieve mesh.** Default **2 mm** for the fine/coarse split; a second, finer mesh
  (0.5 mm or 0.2 mm) determines how much fine root you actually recover. State what you use.
- [ ] ❓ **Default reporting depth.** Set to **30 cm minimum**, with deeper increments reported
  alongside. Confirm 30 is right as the floor for your partners' reporting needs.
- [ ] ❓ **Minimum cores per stratum.** Wetlands uses 3, Forests 5. Roots are more variable than
  soil carbon, so the root minimum may need to be higher than the soil one.
- [ ] ❓ **Worked example** — keep a constructed dataset, or replace with real data from a partner
  site?

---

## Landing page (`README.md`)

- [ ] 📸 The four grassland types side by side — prairie, parkland, savannah, interior BC.
- [ ] 📸 The three pools on one axis (shoot / root / soil), making the point that the visible pool
  is the smallest.

## Part 1 — Background (`01_Background/`)

- [ ] 📊 **The numbers.** This page is written without them on purpose. Wanted, with sources:
  root:shoot relationship for Canadian grassland **with a range**; grassland soil carbon per unit
  area for the prairie / savannah / interior BC cases; area of remaining native grassland in
  Canada.
- [ ] 📸 Grassland carbon-cycle slide, with the root→soil pathway drawn thick.
- [ ] 📸 Soil profiles under each of the four types, showing how differently carbon is distributed.
- [ ] 🔗 **A grassland regional protocol**, if one exists in the WWF series. Forests has
  [`SO-StLawrence-Eng-2026.pdf`](../Forests/01_Background/SO-StLawrence-Eng-2026.pdf); there is no
  grassland equivalent in this folder and Part 1 says so.
- [ ] ✍️ Slide deck for Part 1.
- [ ] 🔗 WWF vegetation video playlist URL.

## Part 2 — Project Planning (`02_Project_Planning/`)

- [ ] 🛠 **Build the grassland sampling-design tool.** The
  [Forests tool is a placeholder here](02_Project_Planning/Sampling%20Design%20Tools/) — forest
  priors, 400 m² plots. Needs grassland priors, the right plot sizes, stratification on management,
  and **separate sizing for soil and for roots**. Keep the `RUN_SELF_TEST` harness.
- [ ] 📊 **Grassland SOC priors** — mean and CV by type and region. AAFC / CanSIS for Canadian
  coverage, SoilGrids 250 m as fallback, with the same map-CV-inflation warning used in the other
  two workshops.
- [ ] 📊 **A root-biomass CV prior.** Roots are more spatially variable than soil carbon, which is
  why they get their own sample-size calculation — but the workshop currently states that
  qualitatively. A published CV would let Part 2 give a number.
- [ ] 📸 Screenshots of the tool: a stratified site, the sample-size output.
- [ ] ✍️ Slide deck for Part 2.

## Part 3 — Field Methods (`03_Field_Methods/`)

- [ ] 📸 **Root washing in progress** — the sieve stack with roots on it. This is the photo that
  would do most work on the page, because it is the step people have not done before.
- [ ] 📸 A **quadrat in place** before and after clipping.
- [ ] 📸 **Soil auger / corer** in grassland, and a core laid out with depth increments marked.
- [ ] 📸 A **root sample sorted by diameter class**, with a scale.
- [ ] 📸 Drying oven and balance setup.
- [ ] 📄 A **vegetation datasheet** — this gap is shared with Forests, which never got an
  understory sheet either. One `.docx` can serve both workshops.
- [ ] ✍️ Slide deck for Part 3.

## Part 4 — Data Interpretation (`04_Data_Interpretation/`)

- [ ] 🔗 ⭐ **The Community led carbon mapping repository.** Until it arrives the mapping section
  is a marked placeholder. When it lands it gets documented the way the LiDAR and
  SedimentChronologies supplements were — read file-by-file and verified against its current head,
  not its README.
- [ ] 💰 **Lab quotes** — cost and turnaround for bulk density, LOI₅₅₀, CHN, **and root
  processing** if the lab does it. Include **which bulk-density basis** each lab reports.
- [ ] 📊 **A local LOI→carbon calibration** for grassland soils, from CHN on a subset.
- [ ] ✍️ Slide deck for Part 4.

## Part 5 — Monitoring (`05_Monitoring/`)

*Written. Every figure on the page was computed and is asserted by a re-runnable check — the gaps
below are references and real data, not arithmetic.*

- [ ] 📊 **A Canadian grassland carbon accrual rate** — ⭐ **the most valuable single number missing
  from this workshop.** The years-to-detectability table in
  [Step 2](05_Monitoring/README.md#step-2--minimum-detectable-difference) scales directly off it,
  and it currently uses 0.3 / 0.5 / 1.0 t C/ha/yr as **brackets, not measurements**. A defensible
  rate for prairie restoration or grazing management turns that table from an illustration into
  planning guidance.
- [ ] 📚 **FAO LEAP (2019)** guidelines — sampling design and **equivalent soil mass**. The ESM
  procedure in [Step 4](05_Monitoring/README.md#step-4--equivalent-soil-mass) is written from first
  principles, with worked arithmetic that is independently checkable, and is **not yet cited**.
- [ ] 📚 **Herrick et al.**, *Monitoring Manual for Grassland, Shrubland and Savanna Ecosystems*
  (Jornada) — core indicator method sheets and the soil aggregate stability test. This is the
  bridge to your partners' soil-health indicator work, and
  [Step 6](05_Monitoring/README.md#step-6--soil-health-indicators-and-carbon-stocks)'s indicator
  table needs it.
- [ ] 📚 **FAO SOC Mapping Cookbook (2nd ed.)** — validation and uncertainty chapters.
- [ ] 📚 **ESM method literature** — spline-based alternatives to the linear interpolation used
  here, and the debate over how to choose the reference mass.
- [ ] 📊 **A real repeat-measurement dataset**, if a partner has one. Detecting change is far easier
  to teach from a case where it was actually attempted, ESM included.
- [ ] 🛠 **Two-visit ESM comparison** — not built, and it does not belong in the workbook: it needs
  two workbooks side by side, per-plot matching and interpolation within increments. Fully specified
  in [Step 4](05_Monitoring/README.md#step-4--equivalent-soil-mass), with worked figures
  (+8% bulk density → a spurious **+3.5%** carbon "gain"; −7% → a spurious **−5.0%** "loss"; ESM
  returns exactly zero for both) to test any implementation against. Belongs with the R pipeline.
- [ ] ✍️ Slide deck for Part 5.
- [ ] 📸 A figure for the **paired-versus-independent** argument — 113 plots against 13–24 is the
  most consequential number in the supplement and is currently a table.

## Worked Example (`Worked_Example/`)

*Written, with every figure asserted against the recalculated workbook.*

- [ ] 📊 Real data from a partner site, or keep the constructed dataset clearly labelled *(it is
  currently labelled clearly)*.
- [ ] 📸 A plot of **root mass by depth**, showing how slowly it declines — the figure that makes
  the "30 cm is a floor" argument land. **24.2%** of the root carbon found to 60 cm sits below
  30 cm, and root density at 30–60 cm is still **19%** of the surface value.
- [ ] 📸 The three sites side by side: grazed sward, exclosure, oak savannah.
- [ ] 📊 **Two paths the constructed dataset does not exercise** — **dead roots** (every fraction is
  recorded Live) and a **`ROOT_SOIL_REPORTING_BOUNDARY = Operational soil fraction`** case, where
  the overlap flag fires. Both are built; neither is demonstrated. A revised dataset could cover both.

---

## Series-level

- [ ] ✍️ Update the root [`README.md`](../README.md) status table when this workshop is complete.
- [ ] 📊 Verify the two Forests root:shoot equations against their sources — used by savannah and
  parkland tree measurement here.
- [ ] 🔗 WWF video playlist URLs across all three workshops.
- [ ] 💰 Still outstanding from Wetlands: **corer photos** and **lab quotes**.
