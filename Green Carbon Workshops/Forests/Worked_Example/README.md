# Worked Example — Moose Ridge, boreal mixedwood

*One dataset, followed end to end: from field sheets to a reportable carbon stock.*

[← Back to the main guide](../README.md)

---

This folder holds the **completed** version of the workshop's worked example, so you can see
what a finished project looks like before (or while) you do your own.

**👉 [`Forest_Carbon_Calculator_WorkedExample.xlsx`](Forest_Carbon_Calculator_WorkedExample.xlsx)**

It follows a **12 ha community woodlot** split into two strata, with **six plots**, **95 trees**,
**49 understory records** and **8 soil cores** sliced into **48 depth increments**.

> [!NOTE]
> **The example data is constructed for teaching — it is not from a real survey.** The species
> mixes, diameters, bulk densities and carbon concentrations are drawn to be realistic for a
> boreal mixedwood and a lowland conifer stand, but no field crew collected them. Use the
> *structure* as a template; don't cite the *numbers*.

---

## The site

| | Stratum | Area | Character |
|---|---|---|---|
| **S1** | Upland mixedwood | 7.2 ha | Aspen, birch, spruce and fir on a well-drained ridge. Plots `MR-01`–`MR-03` |
| **S2** | Lowland conifer | 4.8 ha | Black spruce and larch on wetter ground. Plots `BC-01`–`BC-03` |

Reporting depth: **30 cm**. Precision target: **±20% at 90% confidence**.

---

## What happened

The plan called for **15 plots** ([Part 2, Step 4](../02_Project_Planning/#step-4--decide-how-many-plots)).
The team got **six** into the season — a small crew and a wet July. That gap is the normal
condition of a first campaign, not a failure, and the workbook reports the result honestly
rather than dressing it up.

Three deliberate teaching cases are built into the data:

| Plot / core | What it demonstrates |
|---|---|
| **MR-03** | Laid out on an 11.5° slope **without** the slope allowance — effective plot area corrects to 391 m², not 400 |
| **MR-03-C1** | Hit refusal at **22 cm**, short of the 30 cm reporting depth. Flagged as an underestimate |
| **All cores** | Compaction factors of 1.00–1.14, with the flag explaining what that does and doesn't bias |

---

## The results

**Per plot** (kg C/m², soil to 30 cm):

| Plot | Site | Trees | Understory | Soil | **Total** |
|---|---|---|---|---|---|
| MR-01 | S1 | 4.88 | 0.20 | 10.55 | **15.62** |
| MR-02 | S1 | 6.03 | 0.18 | 10.51 | **16.72** |
| MR-03 | S1 | 4.10 | 0.16 | 9.76 | **14.02** |
| BC-01 | S2 | 1.58 | 0.30 | 11.60 | **13.48** |
| BC-02 | S2 | 1.60 | 0.17 | 10.79 | **12.57** |
| BC-03 | S2 | 1.84 | 0.18 | 10.58 | **12.60** |

**Per site:**

| Site | *n* | Mean | SD | ± half-width | Precision vs target |
|---|---|---|---|---|---|
| S1 — Upland mixedwood | 3 | 15.45 | 1.36 | 2.29 | **MET: ±15% at 90%** |
| S2 — Lowland conifer | 3 | 12.88 | 0.51 | 0.87 | **MET: ±7% at 90%** |

**Study area:** 12 ha · **1,730,828 kg C** · area-weighted mean **14.42 kg C/m²** ·
**6,352 t CO₂e** · soil to **30 cm**.

---

## Three things to read off it

**1 · Soil is 65–85% of the stock.** In the lowland conifer stand the trees are a footnote —
1.6 against 11.6 kg C/m². A trees-only survey there would have reported about an eighth of the
carbon. This is the [Part 1](../01_Background/) point, arriving as a number.

**2 · Stratifying is what made six plots work.** The two strata differ three-fold in tree
carbon but barely at all in soil. Splitting them removed the biggest source of variance from
the estimate, which is why ±15% and ±7% were achievable on three plots each. Pooled as one
site, the same six plots give a visibly wider interval.

**3 · Meeting the target on 3 plots is partly luck.** [Appendix A7](../02_Project_Planning/#a7--proportional-allocation-across-strata)
asks for a 5-plot minimum per stratum for a reason: with *n* = 3 the *t*-multiplier is **2.92**
against 1.645 for large samples, and a single unusual plot moves the mean a long way. The
honest way to report this result is with the *n* stated beside it — which is what the Site
Summary does.

---

## Work alongside it

| You want… | Use this |
|---|---|
| A completed example to follow | this workbook |
| A blank workbook for your own site | [`04_Data_Interpretation/calculators/`](../04_Data_Interpretation/calculators/Forest_Carbon_Calculator.xlsx) |
| Blank printable field sheets | [`03_Field_Methods/datasheets/`](../03_Field_Methods/datasheets/) |
| The planning walkthrough | [Part 2](../02_Project_Planning/) — the Moose Ridge example is threaded through each step |

---

## The thread, end to end

1. **Plan** ([Part 2](../02_Project_Planning/)) — 12 ha, two strata, ±20% at 90%, 15 plots called for.
2. **Collect** ([Part 3](../03_Field_Methods/)) — trees, understory, then soil, in that order.
3. **Analyse** ([Part 4](../04_Data_Interpretation/)) — lab results complete the sheet, and the summaries calculate.

> 📸 **[SCREENSHOTS NEEDED]** — the workbook's Plot Summary and Site Summary tabs as they
> appear when open, so a reader can see the output without downloading the file.
