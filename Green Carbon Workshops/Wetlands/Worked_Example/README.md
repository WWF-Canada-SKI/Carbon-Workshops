# Worked Example — the Mica Bog complex

*One dataset, followed end to end: from field sheets to a reportable carbon stock and an
accumulation rate.*

[← Back to the main guide](../README.md)

---

This folder holds the **completed** version of the workshop's worked example, so you can see what
a finished project looks like before — or while — you do your own.

**👉 [`Wetland_Carbon_Calculator_WorkedExample.xlsx`](Wetland_Carbon_Calculator_WorkedExample.xlsx)**

It follows a **48.3 ha peatland complex** split into three wetland types, with **9 plots**,
**10 cores**, **231 peat sections** and **9 dated horizons** on one core.

> [!NOTE]
> **The example data is constructed for teaching — it is not from a real survey.** Depths, bulk
> densities, LOI values and ages are drawn to be realistic for a boreal bog, a riverine fen and a
> conifer swamp, but no field crew collected them. Use the *structure* as a template; don't cite
> the *numbers*.

---

## The site

| | Site | Type | Area | Character |
|---|---|---|---|---|
| **S1** | Mica Bog | 🟤 Bog | 24.0 ha | Raised *Sphagnum* bog, ombrotrophic, scattered stunted black spruce. Plots `MB-01`–`MB-03` |
| **S2** | Rushing Fen | 🟢 Fen | 15.5 ha | Minerotrophic sedge fen along a creek. Plots `RF-01`–`RF-03` |
| **S3** | Cedar Swamp | 🌲 Swamp | 8.8 ha | Eastern white cedar, ≥25% tree cover. Plots `CS-01`–`CS-03` |

**Total: 48.3 ha.** Reference depth **100 cm**, reported alongside the full profile. Precision
target **±20% at 90% confidence**.

---

## What happened

The team had no depth survey and no prior, so they followed the
[peat guide](../03_Field_Methods/Peat-FINAL-Eng-2026.pdf)'s "one to five plots per site" and took
**three per site**. That is the normal condition of a first campaign.

**Six deliberate teaching cases are built into the data:**

| Core / plot | What it demonstrates |
|---|---|
| **`MB-03-C1`** | **Recovery ratio 0.86** — the chamber did not fill. Material is *missing*, not compressed, so no compaction correction applies |
| **`CS-02-C1`** | **Refusal on buried wood at 104 cm**, mineral contact never reached. Its stock is a **minimum** |
| **`CS-03-C1`** | Only **26 cm** of organic material — **below the 30 cm peatland threshold**. Not a peatland, and that is a finding |
| **`MB-01`** | **Two cores in one plot.** The only plot with replication, and the one whose plot mean you can actually trust |
| **Mineral-contact sections** | Bulk density 0.85–1.15 g/cm³ and LOI 4–11% — the peat signature flipping at the base |
| **`MB-01-C1`** | A **dated core**: 9 horizons from ²¹⁰Pb, ¹³⁷Cs and ¹⁴C, carried through to RERCA and LORCA |

---

## The results

### Per plot (kg C/m²)

| Plot | Site | Peat, full profile | Peat to 100 cm | Vegetation | **Total** |
|---|---|---|---|---|---|
| `MB-01` | S1 | 170.6 | 31.5 | 0.21 | **170.8** |
| `MB-02` | S1 | 181.3 | 31.1 | 0.19 | **181.5** |
| `MB-03` | S1 | 107.0 | 37.1 | 0.36 | **107.3** |
| `RF-01` | S2 | 127.4 | 59.9 | 0.49 | **127.9** |
| `RF-02` | S2 | 135.1 | 57.2 | 0.41 | **135.5** |
| `RF-03` | S2 | 109.7 | 60.0 | 0.37 | **110.1** |
| `CS-01` | S3 | 84.8 | 84.3 | 5.11 | **89.9** |
| `CS-02` | S3 | 89.8 | 85.8 | 3.53 | **93.3** |
| `CS-03` | S3 | 27.1 | 27.1 | 4.13 | **31.2** |

### Per site

| Site | Type | *n* | Mean (kg C/m²) | SD | ± half-width | Achieved | Target | Result |
|---|---|---|---|---|---|---|---|---|
| **S1** | Bog | 3 | 153.2 | 40.1 | ±67.6 | **±44%** | ±20% | ❌ **NOT MET** |
| **S2** | Fen | 3 | 124.5 | 13.0 | ±22.0 | **±18%** | ±20% | ✅ **MET** |
| **S3** | Swamp | 3 | 71.5 | 34.9 | ±58.8 | **±82%** | ±20% | ❌ **NOT MET** |

### Study area

| | |
|---|---|
| **Total area** | 483,000 m² (48.3 ha) |
| **Area-weighted mean** | **129.1 kg C/m²** |
| **Total carbon** | **62,357 t C** |
| **CO₂ equivalent** | 228,850 t CO₂e |
| **Basis** | Full profile, to the mineral contact. 100 cm reported alongside |

---

## Four things this dataset shows better than any amount of prose

### 1 · Most of the carbon is below one metre — and how much depends on the wetland type

| Site | Below 100 cm |
|---|---|
| **S1 — bog** | **78%** |
| **S2 — fen** | **52%** |
| **S3 — swamp** | **2%** |

The bog plots run to 82–83% below a metre. **A survey that stopped at 100 cm would have reported
about a fifth of what is actually in the bog** — and would have been nearly complete for the
swamp. That is why this workshop leads with the full profile and reports the fixed depth
alongside, rather than the other way round.

It also sharpens [Bansal's](../../_Shared/s13157-023-01722-2.pdf) headline figure. Nahlik &
Fennessy found 65% of wetland organic carbon between 30 and 120 cm across a continental sample;
in a deep bog specifically, the shortfall from stopping shallow is worse than that.

### 2 · Vegetation matters exactly where the peat is thin

| Site | Vegetation as % of total |
|---|---|
| **S1 — bog** | **0.2%** |
| **S2 — fen** | **0.3%** |
| **S3 — swamp** | **6.0%** |

In `CS-03`, where the organic layer is only 26 cm, vegetation is **13% of the plot total**. The
rule in [Part 3B](../03_Field_Methods/3B_Vegetation.md) — *measure the trees when the peat is
shallow; skip them defensibly when it is deep* — is this table.

### 3 · Two of three sites missed the precision target, and the cause is diagnosable

It is not bad luck and it is not too few cores. In both failing sites, **one of the three plots
sat near the basin margin**:

| Site | Plot depths to contact | Margin plot |
|---|---|---|
| **S1 — bog** | 352, 366, **214** cm | `MB-03` |
| **S2 — fen** | 182, 196, 158 cm | *(none — laterally uniform)* |
| **S3 — swamp** | 96, 104, **26** cm | `CS-03` |

The fen, with no strong depth gradient, hit **±18%** on three cores. The bog and swamp, with
pronounced centre-to-margin gradients, missed badly because an unstratified mean has to absorb
that gradient as variance.

**The fix is stratification, not more coring.** Splitting each wetland into `centre` and `margin`
and allocating by area would have produced two tighter means per site from the *same nine cores*.
That is [Part 2, Step 2](../02_Project_Planning/README.md#step-2--stratify-your-site).

### 4 · The depth CV predicts the stock CV — so a probe would have caught all of this

| Site | CV of probed depth | CV of measured stock | Ratio |
|---|---|---|---|
| S1 — bog | 0.270 | 0.263 | **0.97** |
| S2 — fen | 0.108 | 0.105 | **0.97** |
| S3 — swamp | 0.570 | 0.518 | **0.91** |

Had the team run a depth survey first, the swamp's CV of ~0.5 would have told them it needed
**21 cores**, not 3 — before a single sample went to a lab.
[Part 2, Step 4](../02_Project_Planning/README.md#the-depth-survey-is-your-variability-prior)
is built on this result.

**Do not pool across types**, though: across all nine plots the depth CV is 0.600 against a stock
CV of 0.406, because carbon density per cm differs between types (**0.49** bog, **0.69** fen,
**0.93** swamp kg C/m² per cm).

---

## The chronology

Core `MB-01-C1` carries **9 dated horizons** — five from ²¹⁰Pb and ¹³⁷Cs in the upper 30 cm, four
from ¹⁴C below.

| | |
|---|---|
| **Basal age** | 6,820 yr at 352 cm |
| **Profile carbon** | 174.4 kg C/m² |
| **LORCA** | **25.6 g C/m²/yr** over 6,820 years |
| **Recent horizon** | 30 cm, 127 yr, 6.77 kg C/m² above it |
| **RERCA** | **53.3 g C/m²/yr** over 127 years |
| **RERCA ÷ LORCA** | **2.09 ×** |

LORCA of 25.6 sits comfortably inside the published range of 4.6–85.8 g C/m²/yr (mean ~20), so
the `LORCA_MIN`/`LORCA_MAX` sanity check passes.

**The ratio of 2.09 fires the guardrail**, which is the point:

> *"RERCA is 2.1× LORCA. This is EXPECTED, not a finding: near-surface peat has not finished
> decomposing, so recent rates always look higher. Do not report it as accelerating
> sequestration."*

### The interval rates are the interesting part

| Depth interval | Age span | Interval CAR (g C/m²/yr) |
|---|---|---|
| 0–6 cm | 14 yr | **94.6** |
| 6–12 cm | 19 yr | 63.7 |
| 12–18 cm | 30 yr | 46.0 |
| 18–24 cm | 33 yr | 41.3 |
| 24–30 cm | 31 yr | 48.2 |
| 30–75 cm | 303 yr | 50.0 |
| 75–150 cm | 1,280 yr | 24.6 |
| 150–240 cm | 2,280 yr | 20.6 |
| 240–352 cm | 2,830 yr | **25.1** |

**That decline from ~95 to ~25 g C/m²/yr is the acrotelm/catotelm transition made numeric.** The
top few centimetres have barely begun decomposing and look extraordinarily productive; by a metre
down, the rate has settled at roughly the long-term average and stays there. Nothing about this
core's behaviour changed — only how much time decomposition has had.

This is the figure worth plotting, and the one that makes the RERCA-vs-LORCA warning intuitive
rather than a rule to memorise. See [Part 5](../05_Chronology_Supplement/).

---

## The QC flags, and what they are telling you

The workbook raises flags on this dataset rather than presenting it as clean. Each is an
instruction:

| Flag | Where | What the team should do |
|---|---|---|
| `Only one core in this plot` | 8 of 9 plots | Note the limitation. `MB-01` is the only replicated plot |
| `Core did not reach the mineral contact` | `CS-02-C1` | Report 89.8 kg C/m² as a **minimum**, or re-core away from the wood |
| `Recovered only 86% of the bore depth` | `MB-03-C1` | Treat the stock as uncertain. **No compaction correction** |
| `Organic depth under 30 cm — not peatland` | `CS-03-C1` | Report it, and say so. It is a real result about the swamp margin |
| `Most of this plot's carbon lies below the reference depth` | `MB-01` | Lead with the full-profile figure |
| `NOT MET: ±44%` / `±82%` | S1, S3 | Post-stratify by landscape position before adding cores |
| `Carbon derived from LOI using the default factor of 0.5, which has not been calibrated locally` | all sections | Run CHN on 10–20 sections and calibrate. Until then, disclose it |

> [!IMPORTANT]
> **Nothing here was hidden to make the example look better.** An under-powered result reported
> honestly is worth more than a confident one that conceals its own uncertainty — and a worked
> example that came out clean would teach nothing about what to do when yours doesn't.

---

## How to use this folder

1. **Open the workbook and read `0. Instructions`**, then work left to right through the tabs.
   Yellow cells were typed in the field, blue came back from the lab, grey is calculated.
2. **Compare it against the [blank calculator](../04_Data_Interpretation/calculators/)** — same
   structure, no data.
3. **Trace one core end to end.** `MB-01-C1` is the one to pick: it appears in `2. Core Log`,
   has 40-odd rows in `3. Peat Data`, is the only dated core in `4. Chronology`, and rolls up
   through `5. Plot Summary` into `6. Site Summary`.
4. **Break something deliberately.** Change a bulk density to 3.0, or delete a section so the
   depths no longer run continuously, and watch which flag fires. That is the fastest way to
   learn what the workbook is checking for.

---

[← Back to the main guide](../README.md) · [4 — Data Interpretation](../04_Data_Interpretation/) · [5 — Chronology Supplement](../05_Chronology_Supplement/)
