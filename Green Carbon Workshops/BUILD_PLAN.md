# Terrestrial Carbon Workshops — Build Plan

*How the Blue Carbon Eelgrass Workshop gets converted into three distinct terrestrial
workshops: **Forests**, **Grasslands**, **Wetlands**.*

Status: planning draft. Nothing built yet. The R analysis pipeline is **explicitly deferred**
to a later phase and is not costed here.

---

## 1. What this plan is based on

**Source workshop** — `CathalD/BlueCarbon_EelgrassWorkshop_V2`, read in full:

| Component | Size | Nature |
|---|---|---|
| `README.md` (landing) | ~120 lines | Framing, data-sheet spine, TLDR formula |
| `01_Background/` | 277 lines + slide deck | Concepts, carbon curves, 3 GIFs |
| `02_Project_Planning/` | 803 lines | 5-step sampling design + Appendix A (sampling theory) |
| `03_Field_Methods/` | 572 lines | Equipment, 5 coring steps, compaction, datasheet |
| `04_Data_Interpretation/` | 419 lines | Digitizing, lab prep, labs, lab methods, reporting |
| `Worked_Example/` | 415 lines + xlsx | Tsawwassen Beach, 6 cores, end to end |
| Sampling Design Tools | 3 GEE scripts | Boundary → strata → allocation → coordinates |
| Spreadsheets | 2 workbooks | Sample Allocation (7 tabs), Digital Data Sheet (4 tabs) |

**Target protocols** — already in this repo, 4 unique documents across 3 folders:

| Protocol | Pages | Forests | Grasslands | Wetlands |
|---|---|:---:|:---:|:---:|
| `Trees-FINAL-Eng-2026.pdf` | 24 | ✅ | — | — |
| `Non-peat-FINAL-Eng-2026.pdf` | 28 | ✅ | ✅ | — |
| `Vegetation-FINAL-Eng-2026.pdf` | 24 | *(understory, optional)* | ✅ | ✅ |
| `Peat-FINAL-Eng-2026.pdf` | 32 | — | — | ✅ |

`Non-peat` is byte-identical in Forests/ and Grasslands/; `Vegetation` is byte-identical in
Grasslands/ and Wetlands/. That duplication is the first thing the repo layout should fix.

---

## 2. The one structural finding that drives everything else

**The eelgrass workshop is single-pool. All three terrestrial workshops are multi-pool.**

The eelgrass workshop's entire pedagogy is *"start from the data sheet and work backwards."*
That works because there is exactly one data sheet, one field method (push core), one
measurement chain (`SOC × bulk density × thickness`), and one number at the end.

Terrestrial ecosystems do not have that. All four protocols independently describe a
**nested / integrated plot design**, where separate plots for each carbon pool overlap in
the same place:

| | Large plot (400 m²) | Medium plot (16–100 m²) | Small plot (1 m²) | Soil |
|---|---|---|---|---|
| **Forests** | Trees >2 m — DBH + height | *(optional understory)* | *(optional)* | Non-peat core / pit |
| **Grasslands** | — | Shrubs 0.5–2 m — volume | Clip-and-weigh <0.5 m | Non-peat core / pit |
| **Wetlands** | *(treed swamps)* | Shrubs 0.5–2 m | Clip-and-weigh + sphagnum surface core | Peat core |

Consequences, in order of how much rework each causes:

1. **The "one data sheet" spine becomes 2–3 linked sheets per ecosystem.**
   *Recommendation:* keep **one workbook per ecosystem**, with a tab per pool, joined on
   `Plot ID`. This preserves the eelgrass teaching device (one sheet you work back from)
   while handling multiple pools honestly. The landing-page table becomes "what each tab
   captures / filled in during / covered in".
2. **Part 2 Step 3 ("Choose what to measure") stops being a one-line answer.** In eelgrass
   it is "sediment, obviously." Here it is a genuine design decision with a cost/benefit —
   and it is where the three workshops diverge most.
3. **Part 3 is not one method, it is 2–3 methods** that must be sequenced (non-destructive
   vegetation surveys **before** destructive soil coring — all four protocols say this).
4. **Part 4 sums pools**, so it needs a per-pool → per-plot → per-site → per-study-area
   chain, not a single core-total chain.
5. **Permanent plots vs destructive sampling** is a live constraint the eelgrass workshop
   never has to address. It belongs in Part 2.

---

## 3. Asset inventory — transfers, edits, builds

### 3a. Transfers essentially unchanged (build once, share across all three)

| Asset | Why it transfers | Action |
|---|---|---|
| `Sampling-Design-Eng-2026.pdf` | **Already ecosystem-generic — and actually written terrestrial-first.** It references "Measuring Carbon in Trees", nested plot design, 400 m² large plots, and the Sample Allocation Calculator by name. It fits here *better* than it fits eelgrass. | Copy from eelgrass repo → `_Shared/` |
| `Lab-Guide-Eng-2026.pdf` | The "Supplemental Guide: Laboratory Analysis" that all four protocols point to. Generic. | Copy → `_Shared/` |
| Sample Allocation Calculator (`.xlsx`) | Sheets 1, 2, 4, 5 (sample size, stratified split, precision check, sensitivity) are pure sampling statistics — no ecosystem content. Only **Sheet 3 (Priors)** is blue-carbon-specific. | Copy → `_Shared/`, rewrite Sheet 3 per ecosystem |
| Part 2 → *Background: what sampling is* | Probability sampling, estimate/confidence/margin-of-error. Ecosystem-free. | Copy verbatim |
| Part 2 → **Appendix A** (A1–A8, ~200 lines) | Cochran's formula, FPC, precision→n inversion, proportional allocation, UNFCCC A6.4 crosswalk, post-hoc precision check. Pure statistics. | Copy verbatim |
| Part 1 → carbon equilibrium / pulse-press GIFs | Net ecosystem carbon balance, pulse vs press disturbance. **More apt for terrestrial than for eelgrass** — fire, harvest, insect outbreak, drainage are textbook pulse/press. | Copy, rewrite captions |
| Carbon Accumulation Visualizer | Generic ecosystem carbon curve tool. | Link as-is |
| Repo skeleton, nav, banner SVGs, callout/table idioms | Layout only. | Copy, recolour per ecosystem |
| 4-step framing (design → collect → analyse → calculate) + the two jobs ("making the data useful" / "collecting the data") | The workshop's organising spine. | Keep identical — it is what makes the three feel like one series |

### 3b. Needs per-ecosystem rewriting (same skeleton, new content)

| Section | What changes |
|---|---|
| Landing `README.md` | Ecosystem framing, national C-stock figure, the TLDR formula (different per pool), data-sheet tab table |
| `01_Background` | What the ecosystem is, why its carbon matters, which pool dominates, disturbance regime, allochthonous/autochthonous replaced by the relevant carbon-input story |
| `02` Step 1 — study area | Same logic, different remote-sensing basis for boundaries |
| `02` Step 2 — stratify | Same logic; strata are now stand type / age class / drainage / peat depth |
| `02` Step 3 — choose pools | **Largest rewrite.** Becomes multi-pool with a nested-plot diagram |
| `02` Step 5 — "For X specifically" | Replaces "For eelgrass specifically" (shore-parallel transects) with the ecosystem's own layout logic |
| `03_Field_Methods` | **Rebuilt from scratch** per ecosystem from the protocol PDFs |
| `04` lab sections | Carbon conversion factor, LOI applicability, coarse fragments, what the lab returns — all differ |
| `Worked_Example` | New site, new numbers, new sheet |

### 3c. Must be built new (no eelgrass equivalent)

- Field data sheets (paper PDF + digital workbook) per ecosystem
- Per-ecosystem priors for the sample-size calculator
- Per-ecosystem slide decks
- GEE sampling tool variants (ecosystem masks + priors)
- Worked examples

---

## 4. Per-ecosystem plans

### 4.1 🌲 FORESTS

**Pools:** trees (dominant, ~immediate) + non-peat soil (largest but slow-changing)
+ optional understory.

#### Assets needed

| # | Asset | Source | Who supplies |
|---|---|---|---|
| F1 | `Trees-FINAL-Eng-2026.pdf` | ✅ in repo | — |
| F2 | `Non-peat-FINAL-Eng-2026.pdf` | ✅ in repo | — |
| F3 | Sampling Design + Lab guides | eelgrass repo | me (copy) |
| F4 | **Tree datasheet (auto-calculating)** — the "accompanying datasheet" the Trees guide references on p.16 | WWF Learning Library | **you** ⭐ |
| F5 | **NRCan biomass calculator access / coefficient table** — `AGB = B_i1·DBH^B_i2·H^B_i3` is useless without the species coefficients | NRCan | **you** ⭐ |
| F6 | Soil datasheet (core + pit variants) | WWF Learning Library | **you** |
| F7 | Forest workshop slide deck | — | **you** |
| F8 | WWF forest/trees video playlist URL | wwf.ca/carbon-measurement | **you** |
| F9 | Field photos — plot layout, DBH tape, rangefinder, tagging, soil pit face with horizons | your field archive | **you** |
| F10 | Worked-example site + real numbers | — | **you** |
| F11 | Sample Allocation Calculator w/ forest priors | adapt | me |
| F12 | GEE sampling tool — forest variant | port | me |

#### Documents & literature to base the page content on

**Method authority (cited in the Trees guide, use directly):**
- Lambert, Ung & Raulier (2005) — *Canadian national tree aboveground biomass equations*, CJFR 35:1996–2018 — **the source of the AGB coefficients**
- Ung, Bernier & Guo (2008) — updated national parameter estimates incl. BC, CJFR 38
- Paré et al. (2013) — stand-scale biomass, nutrient contents **and associated uncertainties**, CJFR 43:599–608 — the uncertainty reference
- Addo-Danso, Prescott & Smith (2016) — root biomass methods review, *For. Ecol. Manage.* 359:332–351 — for the BGB/root:shoot discussion
- NRCan (2008) — *Canada's National Forest Inventory Ground Sampling Guidelines* — PSP tagging, plot standards
- BC Ministry of Forests (2024) — Provincial monitoring ground sampling procedures
- Halbritter et al. (2020) — ClimEx handbook, *MEE* 11:22–37

**For priors (the Janousek-equivalent):**
- **Canada's National Forest Inventory ground plot data** (open.canada.ca) — the best national prior source; gives plot-level biomass by ecozone/stand type
- **Canadian Upland Forest Soil Profile and Carbon Stocks Database** (Shaw et al., NRCan) — the soil-side prior
- Kurz et al. (2013) — *Carbon in Canada's boreal forest: a synthesis*, Environ. Rev. 21:260–292

#### Scientific issues to resolve before writing

1. **The BGB equations in the guide are inconsistent in form.**
   Hardwood: `BGB = 1.576 × AGB^0.615` (a power law). Softwood: `BGB = 0.222 × AGB` (a fixed
   root:shoot ratio). These come from different derivations and are being presented side by
   side as if equivalent. Verify both against Addo-Danso (2016) / Paré (2013) and state the
   uncertainty. The guide itself says BGB is 18–30% of total biomass — a range wide enough
   that this is a headline uncertainty, not a footnote.
2. **Allometric error is the forest analogue of the eelgrass corer-diameter bias**, and it is
   bigger. The eelgrass workshop's best teaching moment ("measure your actual internal
   diameter — it propagates as systematic bias into every bulk density") maps directly onto
   "species misidentification + allometric model choice propagates into every tree." Use that
   slot the same way.
3. **Coarse fragments.** Forest mineral soils contain rocks >2 mm. The Non-peat guide's
   scaling equations (Eq 1–4) do **not** correct for them, so stock is overestimated wherever
   the soil is stony. Add a fine-earth-fraction correction — this is a real defensibility gap.
4. **Slope correction** (Trees guide Appendix): `adjusted distance = horizontal / cos(angle)`.
   Easy to get wrong and it changes plot area, hence every per-m² figure.
5. **Carbon fraction of 0.5** for tree biomass is the IPCC default; the defensible move is to
   state it, not hide it.

---

### 4.2 🌾 GRASSLANDS

**Pools:** soil (overwhelmingly dominant) + medium vegetation (shrubs) + small vegetation
(herbaceous, clip-and-weigh).

#### Assets needed

| # | Asset | Source | Who supplies |
|---|---|---|---|
| G1 | `Vegetation-FINAL-Eng-2026.pdf` | ✅ in repo | — |
| G2 | `Non-peat-FINAL-Eng-2026.pdf` | ✅ in repo | — |
| G3 | Sampling Design + Lab guides | eelgrass repo | me (copy) |
| G4 | **Vegetation datasheet (auto-calculating)** — referenced in the Vegetation guide p.15 | WWF Learning Library | **you** ⭐ |
| G5 | **Shrub volume → biomass equations** — the guide defers these to "the Appendix", which is not in the extractable text | WWF / source refs | **you** ⭐ |
| G6 | Soil datasheet | WWF Learning Library | **you** |
| G7 | Grassland slide deck | — | **you** |
| G8 | WWF vegetation video playlist URL | wwf.ca/carbon-measurement | **you** |
| G9 | Field photos — quadrat, clip-and-weigh, drying oven, soil auger | your archive | **you** |
| G10 | Worked-example site + numbers | — | **you** |
| G11 | Calculator w/ grassland priors | adapt | me |
| G12 | GEE tool — grassland variant | port | me |

#### Documents & literature

**Method authority:**
- Vegetation guide + Non-peat guide (in repo)
- Halbritter et al. (2020) ClimEx handbook — standardised herbaceous biomass protocols
- Billings et al. (2021) — *Soil organic carbon is not just for soil scientists*, Ecol. Appl. 31:e02290 (cited in the Peat guide, applies here)
- Davis et al. (2018) — review of SOC measurement protocols, *Sustainability* 10:53

**Needed and not yet in the repo:**
- **Mokany, Raison & Prokushkin (2006)** — *Critical analysis of root:shoot ratios in terrestrial biomes*, GCB 12:84–96 — **essential**, because grassland root:shoot is 2–8, not the 0.2–0.3 the Trees guide uses
- A Canadian prairie/rangeland carbon reference (e.g. Bork lab, U Alberta; or AAFC rangeland C work)

**For priors:**
- AAFC / Canadian Soil Information Service (CanSIS) SOC data for grassland soil landscapes
- SoilGrids 250m as a fallback covariate-based prior

#### Scientific issues to resolve before writing

1. **Belowground is the story, and the guides barely cover it.** The Vegetation guide's
   clip-and-weigh gives you **aboveground herbaceous biomass only**. In grassland, root
   biomass typically exceeds shoot biomass several-fold, and soil carbon dwarfs both. A
   grassland workshop that leads with clip-and-weigh gets the emphasis backwards. Lead with
   soil; treat AGB as the small, seasonal component it is.
2. **Herbaceous AGB is not a "stock" in the eelgrass sense.** It is a standing crop that
   turns over annually and varies several-fold within a season. The guide says sample at
   peak growing season — say plainly *why*, and say that a single clip-and-weigh is not
   comparable to a soil carbon stock. This is the most likely place for a workshop
   participant to draw a wrong conclusion.
3. **Grazing / management is the dominant stratification variable** — more so than
   vegetation cover. Step 2 should say so.
4. **Coarse fragments** — same gap as forests.
5. **Bulk density in grassland topsoil is compaction-sensitive** (trampling, machinery).
   Measure it, don't take it from a table.

---

### 4.3 💧 WETLANDS

**Pools:** peat (overwhelmingly dominant) + vegetation (incl. living sphagnum, which needs
its own surface-coring method).

#### Assets needed

| # | Asset | Source | Who supplies |
|---|---|---|---|
| W1 | `Peat-FINAL-Eng-2026.pdf` | ✅ in repo | — |
| W2 | `Vegetation-FINAL-Eng-2026.pdf` | ✅ in repo | — |
| W3 | Sampling Design + Lab guides | eelgrass repo | me (copy) |
| W4 | **Peat datasheet** | WWF Learning Library | **you** ⭐ |
| W5 | Vegetation datasheet (shared with Grasslands) | WWF Learning Library | **you** |
| W6 | Wetland slide deck | — | **you** |
| W7 | WWF peat video playlist URL | wwf.ca/carbon-measurement | **you** |
| W8 | Field photos — Russian corer open/closed, core laid on tarp, sphagnum transition, peat→mineral contact. **The Peat guide's Appendix frames A/B/C are credited to you**, so these may already be yours to reuse | your archive | **you** |
| W9 | Worked-example site + numbers (Peawanuck is used throughout the guides as the example site) | — | **you** |
| W10 | Calculator w/ peatland priors | adapt | me |
| W11 | GEE tool — wetland variant | port | me |

#### Documents & literature

**Method authority (all cited in the Peat guide):**
- **Bansal et al. (2023)** — *Practical Guide to Measuring Wetland Carbon Pools and Fluxes*, Wetlands 43:105 — the single most important supporting reference
- De Vleeschouwer, Chambers & Swindles (2010) — coring and sub-sampling of peatlands, *Mires and Peat* 7
- Shotyk & Noernberg (2020) — peat core sampling/handling, CJSS 100:363–380
- Dettmann et al. (2022) — *How to take volume-based peat samples down to mineral soil?*, Geoderma 427:116132 — directly relevant to the bulk-density problem below
- Jandl et al. (2014) — SOC monitoring uncertainty, *STOTEN* 468–469:376–383
- Petrokofsky et al. (2012) — comparison of C stock methods, *Environ. Evidence* 1:6
- Canadian Soil Classification System — peat as the organic (O) horizon

**For priors:**
- Canadian peatland carbon databases (Vitt et al. boreal peatland database; CanSIS organic soils)
- Hugelius et al. — northern peatland carbon stocks
- PEATMAP / Global Peatland Database for spatial extent

#### Scientific issues to resolve before writing

1. **The eelgrass compaction correction does not transfer.** The eelgrass workshop's whole
   Step 3 is push-corer compaction (`compaction_factor = outside_depth / inside_depth`). A
   **side-filling Russian/Macaulay corer does not compact that way** — it rotates a chamber
   into undisturbed peat. Its failure mode is the opposite: **incomplete chamber filling**,
   and smearing at the chamber edge. The workshop must replace, not adapt, this section —
   and say explicitly why the blue-carbon compaction maths is absent.
2. **Peat depth is the dominant uncertainty, not %C or bulk density.** Peat is ~90%+ organic
   matter at ~50% C, so %C is nearly constant. Stock ≈ depth × bulk density. That makes the
   guide's **depth survey** (probe at every 1 m intersection in a 10×10 m plot; 10–25 m grid
   across the site) the highest-value measurement in the whole workshop. Sampling design
   should be **depth-stratified**, and Part 2 should say so — this is a genuine departure
   from the eelgrass design logic and the most defensible single change.
3. **Bulk density from a side-filling corer is hard** — chamber volume is only nominal.
   Dettmann et al. (2022) exists precisely for this. Flag it; don't let the workshop imply
   BD falls out of the corer for free.
4. **Vegetation must be surveyed before peat coring** — destructive sampling ordering. All
   four protocols say this; it belongs in Part 2, not buried in Part 3.
5. **Living vs dead sphagnum** — the Vegetation guide's surface-coring method requires
   separating living (colourful) from actively-decomposing (discoloured) sphagnum in the lab.
   Double-counting here inflates both the vegetation and the peat pool.
6. **Water table depth** should be recorded — it governs whether the site is a sink or a
   source, and it is the main thing a management decision would act on.

---

## 5. Cross-cutting decision: which estimator?

This one needs your call before Part 2 and Part 4 can be written, for all three ecosystems.

**The four protocol PDFs and the eelgrass workshop use different estimators.**

| | Protocol guides (Trees Eq 1–5, Peat Eq 1–8, Veg Eq 1–5) | Eelgrass workshop |
|---|---|---|
| Plot → site | Unweighted mean of plot means | Stratified, **area-weighted** |
| Site → study area | Sum of site totals ÷ sum of site areas | Design-based (Horvitz–Thompson) |
| Finite population correction | None | Yes |
| **Uncertainty** | **None. No SE, no CI, at any step.** | SE, CI, and a PASS/FAIL against the precision target |

They agree only when plots are allocated exactly proportional to stratum area. Otherwise they
diverge, and the guides give no way to report uncertainty at all — which is awkward given the
guides themselves spend a whole section on choosing a margin of error during planning.

**My recommendation:** keep the workshop's stratified, design-based estimator as the method,
and present the guides' Eq 1–5 as the **by-hand special case** — exactly the way the eelgrass
workshop already handles the field-guide formula in its "How the carbon-stock formula relates
to the field guide" fold-out. That keeps the workshop consistent with WWF's published guides
while still producing a defensible interval.

**But it is your call**, because it changes what the workshop teaches. The alternative —
follow the printed guides exactly — is simpler and matches what a participant would find in
the PDF, at the cost of reporting point estimates with no uncertainty.

---

## 6. Proposed repository layout

```
Terrestrial_Carbon_Workshops_V1/
├── README.md                      ← series landing page; routes to the 3 workshops
├── BUILD_PLAN.md                  ← this file
├── _Shared/                       ← assets genuinely identical across all three
│   ├── Sampling-Design-Eng-2026.pdf
│   ├── Lab-Guide-Eng-2026.pdf
│   ├── SampleAllocation_Calculator.xlsx
│   └── images/                    ← banner templates, sampling-theory GIFs
├── Forests/
│   ├── README.md                  ← workshop landing
│   ├── 01_Background/
│   ├── 02_Project_Planning/       ← + Sampling Design Tools (forest GEE variant)
│   ├── 03_Field_Methods/          ← Trees + Non-peat protocols live here
│   ├── 04_Data_Interpretation/
│   ├── Worked_Example/
│   └── TODO.md
├── Grasslands/   (same structure)
└── Wetlands/     (same structure)
```

Notes:
- Each ecosystem folder stays **independently usable** — someone running a peatland workshop
  should never need to read forest material. Only genuinely identical files go in `_Shared/`,
  linked by relative path (works fine on GitHub).
- This also resolves the current byte-identical duplication of `Non-peat` and `Vegetation`.
- `TODO.md` per ecosystem, mirroring the eelgrass repo's — it proved to be the most useful
  file in that repo for tracking what only you can supply.

---

## 7. What I need from you (upload checklist)

Ordered by how much is blocked without it.

### ⭐ Blocking — the workshop can't be written around them without these

1. **The auto-calculating datasheets** the protocols keep referencing
   ("*Please see the accompanying datasheet, which automatically calculates the carbon
   stock*" — Trees p.16; also Vegetation p.15). One per pool: trees, vegetation, non-peat
   soil, peat. These are the terrestrial equivalent of the eelgrass digital data sheet, and
   the whole "work back from the sheet" pedagogy hangs off them.
2. **NRCan biomass calculator** — link or exported coefficient table. Forests is unwritable
   without the species coefficients.
3. **Shrub volume → biomass equations** — the Vegetation guide defers them to an Appendix
   that isn't in the text layer I can extract.

### High value — needed for the pages to look and read like the eelgrass workshop

4. Slide decks (one per ecosystem)
5. WWF video playlist URLs (each guide says "this guide and its corresponding video")
6. Field photos per ecosystem (the eelgrass repo's TODO shows photos were the long pole there too)
7. Worked-example sites + real data — Peawanuck appears throughout the guides as the example site; is that usable?

### Useful — improves defensibility, not blocking

8. Any prior datasets you already have (NFI extracts, CanSIS/CUFSPCD pulls, peatland databases)
9. Lab quotes/contacts for the lab directory table (still empty in the eelgrass repo too)

**Where to put them:** drop each into the matching ecosystem folder — `Forests/`,
`Grasslands/`, `Wetlands/` — and anything shared into `_Shared/`. I'll file them into the
right subfolder as the structure gets built.

---

## 8. Suggested phasing

| Phase | What | Depends on |
|---|---|---|
| **0** | Repo skeleton, `_Shared/`, series landing page, de-duplicate the protocol PDFs, per-ecosystem `TODO.md` | nothing — can start now |
| **1** | Part 2 (Project Planning) for all three. ~60% is shared statistics; the ecosystem-specific parts are Steps 2, 3 and 5 | estimator decision (§5) |
| **2** | Part 1 (Background) ×3 | slide decks |
| **3** | Part 3 (Field Methods) ×3 — the largest single build, straight from the protocol PDFs | photos, videos |
| **4** | Part 4 (Data Interpretation) ×3 — lab-facing only, no pipeline | datasheets ⭐ |
| **5** | Worked examples ×3 | real data |
| **6** | GEE sampling tool variants | phase 1 |
| **7** | *(deferred)* R analysis pipeline ×3 | everything above |

Phase 0 and 1 can begin as soon as you've made the §5 estimator call. Phases 2–5 unblock as
assets land.

---

## 9. Open questions for you

1. **Estimator** (§5) — stratified/design-based, or follow the printed guides exactly?
2. **Understory in Forests** — include the Vegetation protocol as an optional 3rd pool, or
   keep Forests to trees + soil and send people to Grasslands for the vegetation method?
3. **Worked-example sites** — one real site per ecosystem, or one constructed teaching
   dataset per ecosystem (as the eelgrass one is: "constructed for teaching — not from a
   real survey")?
4. **Do the three share a landing page and voice**, presented as one series, or should each
   read as a fully standalone workshop that happens to share a layout?
5. **Wetlands scope** — bogs and fens only, or include treed swamps (which would pull the
   Trees protocol into Wetlands as a 4th pool)?
