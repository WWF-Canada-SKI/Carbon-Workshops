# Worked Example — the Ravine Creek grasslands

*One dataset, followed end to end: from field sheets to a reportable carbon stock, an honest
interval, and a clear statement of what it cannot tell you.*

[← Back to the main guide](../README.md)

---

This folder holds the **completed** version of the workshop's worked example, so you can see what a
finished project looks like before — or while — you do your own.

**👉 [`Grassland_Carbon_Calculator_WorkedExample.xlsx`](Grassland_Carbon_Calculator_WorkedExample.xlsx)**

A **94.5 ha** study area split into three sites, with **9 plots**, **9 cores**, **34 soil
increments**, **68 root fractions** and **9 clip-and-weigh quadrats**.

> [!NOTE]
> **The example data is constructed for teaching — it is not from a real survey.** Bulk densities,
> carbon percentages and root masses are drawn to be realistic for southern prairie and a Black Oak
> savannah, but no field crew collected them. Use the *structure* as a template; don't cite the
> *numbers*.

---

## The site

| | Site | Type | Area | Character |
|---|---|---|---|---|
| **S1** | Grazed prairie | 🌾 Prairie | 64.0 ha | Native sward, never cultivated, **season-long grazing**. Plots `GP-01`–`GP-03` |
| **S2** | Ungrazed exclosure | 🌾 Prairie | 9.5 ha | The same sward, **fenced and ungrazed**. Plots `UP-01`–`UP-03` |
| **S3** | Black Oak savannah | 🌳 Savannah | 21.0 ha | Scattered oak, 22–31% canopy, **fire-maintained**, sandier and shallower. Plots `BOS-01`–`BOS-03` |

**The design is deliberate.** S1 and S2 are the *same grassland* under two management regimes — a
grazing contrast, which is the question a prairie partner most often has. S3 is a different
ecosystem entirely, and is there to break things: trees, thin soil, and a core that hits refusal.

---

## What happened

| | |
|---|---|
| **Sampled** | 2026-08-05, a single visit at peak growing season |
| **Soil** | One core per plot, 5 cm internal diameter, increments 0–10, 10–20, 20–30, 30–60 cm |
| **Roots** | Separated from every increment, sieved at **0.5 mm**, split ≤2 mm / >2 mm, **ash-corrected**, dried at 65 °C |
| **Vegetation** | 0.25 m² clip-and-weigh, live and dead separated; 100 m² shrub plot; tree carbon from the Forests calculator where canopy cover warranted it |
| **Reporting depth** | **30 cm**, with the full profile reported alongside |

**Two plots did not go to plan, and that is the point of including them:**

- **`UP-03`** was cored to 30 cm only — the crew ran out of light. It has three increments, not four.
- **`BOS-03`** hit **refusal at 22 cm** on coarse sandy substrate. It is *shallower than the
  reporting depth*, which is the one case that needs a caveat rather than a correction.

---

## The results

### Per plot (kg C/m²)

| Plot | Site | Soil to 30 cm | Soil, full profile | Deepest | Roots | Vegetation |
|---|---|---|---|---|---|---|
| `GP-01` | S1 | 11.151 | 16.064 | 60 cm | 1.337 | 0.110 |
| `GP-02` | S1 | 10.071 | 14.580 | 60 cm | 0.690 | 0.094 |
| `GP-03` | S1 | 10.474 | 15.044 | 60 cm | 0.882 | 0.126 |
| `UP-01` | S2 | 12.937 | 18.535 | 60 cm | 1.594 | 0.220 |
| `UP-02` | S2 | 9.648 | 13.878 | 60 cm | 0.818 | 0.220 |
| `UP-03` | S2 | 11.540 | 11.540 | **30 cm** | 1.067 | 0.222 |
| `BOS-01` | S3 | 6.153 | 8.705 | 60 cm | 0.588 | 2.076 |
| `BOS-02` | S3 | 4.489 | 6.365 | 60 cm | 1.083 | 2.447 |
| `BOS-03` | S3 | 5.148 | 5.148 | **22 cm** | 0.273 | 1.555 |

### Per site

| Site | *n* | Soil to 30 cm | Soil precision | Roots | Root precision |
|---|---|---|---|---|---|
| **S1** grazed prairie | 3 | **10.57 ±0.92** | **MET: ±9%** | 0.969 ±0.560 | NOT MET: ±58% |
| **S2** ungrazed exclosure | 3 | **11.37 ±2.78** | NOT MET: ±24% | 1.159 ±0.668 | NOT MET: ±58% |
| **S3** Black Oak savannah | 3 | **5.26 ±1.41** | NOT MET: ±27% | 0.648 ±0.689 | NOT MET: ±106% |

*±half-widths at 90% confidence. Targets: **±20% soil**, **±40% roots** — deliberately different,
per [Appendix A10](../02_Project_Planning/README.md#a10--why-roots-may-need-more-samples).*

### Study area

| | |
|---|---|
| Total area | **94.5 ha** |
| Total carbon | **9,814.6 t C** *(S1 7,382.4 · S2 1,190.8 · S3 1,241.4)* |
| Area-weighted mean | **10.386 ± 0.727 kg C/m²** |
| Achieved precision | **±7% at 90% confidence — MET** *(6 design df)* |
| CO₂ equivalent | **36,019.5 t CO₂e** |

> [!IMPORTANT]
> **Read the basis, not just the number.** That total is **soil to 30 cm plus measured root
> carbon**. It excludes soil below 30 cm — which for these plots is roughly *another 43%* again —
> and it excludes vegetation entirely, because a standing crop is not a stock. All of this is
> stated on the `6. Site Summary` tab itself.

> [!NOTE]
> **Two of three sites missed their own precision targets, and the study area still meets its.**
> That is not a contradiction — it is what dividing the site up buys you. The study-area figure is
> a **stratified** estimate: each site is a stratum, weighted by area, and the interval combines
> their spreads as `Var = Σ W_h²·s_h²/n_h` on `Σ(n_h − 1) = 6` degrees of freedom. Pooling across
> strata recovers precision that no single site had on its own.
>
> It does **not** rescue the site-level comparisons. S2 against S1 is still undetectable — see
> [point 6](#6--one-target-met-out-of-six-and-every-failure-is-diagnosable) and
> [Part 5](../05_Monitoring/). A tight study-area total and an undetectable difference between two
> of its parts are perfectly consistent, and reporting only the first would be misleading.

---

## Six things this dataset shows better than any amount of prose

### 1 · Soil dominates, roots are the living pool, and shoots are a rounding error

| Site | Soil | Roots | Vegetation | Roots as % of soil+root | Vegetation as % of all three |
|---|---|---|---|---|---|
| **S1** grazed prairie | 10.566 | 0.969 | 0.110 | **8.4%** | **0.9%** |
| **S2** ungrazed exclosure | 11.375 | 1.159 | 0.221 | **9.2%** | **1.7%** |
| **S3** savannah | 5.263 | 0.648 | 2.026 | **11.0%** | **25.5%** |

Across individual plots roots run **5.0% to 19.4%** of soil-plus-root carbon. So roots are a
**small fraction of the carbon** and **the overwhelming majority of the living biomass** — which is
exactly the inversion [Part 1](../01_Background/) argues, and it only shows up because the roots were
*measured* rather than inferred from a ratio.

The savannah's 25.5% vegetation share is the exception, and it is **trees**, not grass — see point 5.

### 2 · The ash correction is not a rounding detail

Across all 68 root fractions, correcting for adhering mineral soil took root mass from
**36.389 g to 32.714 g — a 10.1% reduction.**

**Ten per cent of the root pool was dirt.** Skip that step and every root number in the workshop is
biased high by about that much, in one direction, invisibly. It is one of the
things the [root-processing SOP must define](../04_Data_Interpretation/#13-the-root-chain--and-this-one-is-yours-to-get-right) in Part 4,
and it is the one most often left out.

### 3 · Fine roots are the pool, so the sieve mesh decides the answer

| Diameter class | Root carbon (summed over 9 plots) | Share |
|---|---|---|
| **≤2 mm (fine)** | 6.792 | **81.5%** |
| **>2 mm (coarse)** | 1.538 | 18.5% |

Four-fifths of root carbon is in the fine fraction — the fraction that **passes through a coarse
sieve and is lost.** This dataset used **0.5 mm**. A 2 mm sieve would have thrown away much of that
81.5% and reported a confidently lower number.

Which is why `ROOT_SIEVE_MM` is a `Fill Me In` field rather than a footnote: **a fine-root figure
without its mesh size cannot be interpreted, let alone compared.**

### 4 · 30 cm really is a floor — and so is 60

Mean root carbon by increment, across the nine plots:

| Increment | Root C (kg C/m²) | Per cm | Cumulative |
|---|---|---|---|
| 0–10 cm | 0.396 | 0.0396 | 0.396 |
| 10–20 cm | 0.201 | 0.0201 | 0.598 |
| 20–30 cm | 0.103 | 0.0103 | 0.702 |
| 30–60 cm | 0.224 | **0.0075** | **0.926** |

**24.2% of the root carbon found to 60 cm sits below 30 cm.** Report to 30 cm and you have left a
quarter of the measured root pool out of the number.

And look at the last column: at 30–60 cm the root density is still **19% of what it is at the
surface**. It is declining, but it has not stopped. **These cores did not reach the bottom of the
root systems and neither will yours** — which is why every plot carries the flag *"Root total reaches
only 60 cm — the bottom of the core, not the bottom of the roots. Report it as a MINIMUM."*

The same argument applies to soil: full-profile soil carbon to 60 cm averages **43% more** than the
30 cm figure for the seven plots that got there. The 30 cm number is comparable; it is not complete.

### 5 · Why trees are counted by height, not by canopy cover

The savannah plots have **22%, 28% and 31%** canopy cover. An earlier draft of this workshop
gated the tree protocol on a **25% canopy-cover threshold**, which would have put `BOS-03` at 22%
*below* the line. The crew recorded **1.42 kg C/m²** of tree carbon on it anyway, because there
were visibly trees standing on the plot.

| S3 vegetation mean | kg C/m² |
|---|---|
| As recorded | **2.026** |
| Applying the 25% rule strictly (no tree carbon on `BOS-03`) | **1.553** |
| Difference | **0.473 — 23.4% of the pool** |

**The threshold would have discarded a quarter of the pool, and the carbon was measured.** That is
why the workshop now counts **any tree over 2 m**, with no cover threshold to set: the medium plot
covers 0.5–2 m, so the two protocols meet exactly and a tree either is over 2 m or is not. Savannah
sits on a canopy-cover boundary *by definition*, which is precisely why a canopy-cover rule was the
wrong instrument here.

Canopy cover is still recorded on the sheet — it is useful context, and
[Part 5](../05_Monitoring/) uses it to track woody encroachment. It just no longer decides whether
carbon gets counted.

### 6 · One target met out of six, and every failure is diagnosable

| | |
|---|---|
| **S1 soil, ±9% — met** | Three plots on uniform mid-slope prairie. Soil CV **0.05** |
| **S2 soil, ±24% — missed** | `UP-01` 12.94 against `UP-02` 9.65. Soil CV **0.15**. Real heterogeneity inside a small exclosure |
| **S3 soil, ±27% — missed** | Soil CV **0.16**, and `BOS-03` is an underestimate because it was cored shallow. Fix the caveat before adding plots |
| **All three root targets missed** | Root CVs **0.34, 0.34, 0.63** against soil CVs of **0.05, 0.15, 0.16** |

The root failures are not a mistake. They are [A10](../02_Project_Planning/README.md#a10--why-roots-may-need-more-samples)
happening on real data: **roots are between two and four times as variable as soil at the same
site**, the target was already loosened to ±40% to account for it, and three plots still cannot
deliver it. Closing that gap at S3 would need roughly **five times the cores**.

A ±58% root interval is the honest answer. A ±40% claim would not be.

> [!TIP]
> **Note the soil CVs: 0.05, 0.15 and 0.16.** These are *below* the 0.2–0.4 range Part 2 uses for
> planning — the dataset is constructed, and constructed data is tidier than real grassland. Plan
> with the published range, not with these.

---

## And the thing this dataset cannot do

Two sites, same sward, one grazed and one not. The exclosure holds more soil carbon. That is the
result a partner wants:

| | |
|---|---|
| Ungrazed − grazed | **+0.81 kg C/m²** (+7.7%) |
| 90% confidence interval | **−1.33 to +2.95 kg C/m²** |
| Verdict | **spans zero — not detectable** |

**Three plots per site cannot see a 7.7% difference.** Fourteen plots per group would make the
interval exclude zero; having a real chance of catching it takes **30**.

This is not a flaw in the data. It is the correct answer to a question the design was never sized to
answer — and it is why [Part 5](../05_Monitoring/) exists, and why it says to read it *before*
finalising Part 2 rather than after the second visit.

---

## The QC flags, and what they are telling you

The workbook flags 4 soil rows, both shallow cores, and every plot's root total. Working them in
order:

| Flag | Plots | What it means | What to do |
|---|---|---|---|
| **Bulk-density basis not confirmed with the lab** | `GP-02`, 4 rows | The coarse-fragment correction may be wrong or doubled. This is the [double-correction trap](../04_Data_Interpretation/README.md#-the-coarse-fragment-correction-is-applied-once-or-not-at-all) | **One email.** Highest-value flag in the workbook |
| **Cored shallower than the reporting depth** | `BOS-03` | The 30 cm figure is an **underestimate** for this plot — the soil is not there to measure | Report the site mean with the caveat. Do not extrapolate; do not drop the plot |
| **Root total reaches only *n* cm** | all 9 | The core ended, the roots did not | Report root carbon as a **minimum**, with the depth |
| **Shrub figures are ABOVE-ground only** | `BOS-01`–`03` | Shrub roots are in neither the vegetation pool nor the soil core | **Declare the gap.** It is a known, stated omission |
| **Coarse fragments recorded, basis already accounts for them** | 30 rows | Informational — confirming *no* further correction was applied, which is correct | Nothing. This is the flag you want to see |

> [!NOTE]
> **Two things this constructed dataset does not exercise**, and a real campaign will:
> **dead roots** (every fraction here is recorded Live, so the live/dead path is untested) and a
> **`ROOT_SOIL_REPORTING_BOUNDARY = Operational soil fraction`** case, where fine-root carbon sits
> inside the soil number and the overlap flag fires. Both paths are built and both are worth trying
> by hand — change the setting on the `7. Settings` tab and watch what changes.

---

## How to use this folder

1. **Open the workbook and read it backwards.** Start at `6. Site Summary`, then `5. Plot Summary`,
   then the data tabs. That is the order the numbers depend on each other, and it is the spine of
   the whole workshop.
2. **Change something and watch it move.** Set `ROOT_SOIL_REPORTING_BOUNDARY` to
   `Operational soil fraction`, or back to `Not agreed with the lab`. Set
   `ASH_CORRECTED` to `No`. Change `SOIL_REPORTING_DEPTH_CM` to 60. Each one is a point the workshop
   argues in prose; the workbook lets you see it.
3. **Then take the blank copy.** The clean workbook is at
   [`../04_Data_Interpretation/calculators/`](../04_Data_Interpretation/calculators/) — same
   formulas, no data.

---

## Open items

> 📊 **[REAL DATA]** — the best possible replacement for this folder is a partner's actual dataset,
> even a small one. Failing that, this stays clearly labelled as constructed.
>
> 📸 **[FIGURE NEEDED]** — **root carbon by depth**, plotted. Point 4's table is the clearest single
> illustration of the "30 cm is a floor" argument in the whole workshop and currently exists only as
> numbers.
>
> 📸 **[FIGURE NEEDED]** — the three sites side by side: grazed sward, exclosure, oak savannah.

---

[← Back to the main guide](../README.md) · [4 — Data Interpretation](../04_Data_Interpretation/) · [5 — Monitoring](../05_Monitoring/)
