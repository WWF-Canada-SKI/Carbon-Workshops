> 🗄️ **Archived.** This walkthrough used constructed Tsawwassen data and the earlier analysis pipeline
> (now in `04_Data_Interpretation/DataAnalysisWorkflow/advanced/`). It is kept for reference only — the
> current Part 4 follows the published Cowichan cores through the shared workflow and Options A and B.
> See [Part 4](../../04_Results/) and the [archive note](README.md).

# Worked example — Part 4: Analysing the Tsawwassen cores

*How one team went from six bags of wet sediment to a defensible carbon number.*

[← Worked example overview](../README.md) · [Back to Part 4 — Data Interpretation](../../04_Results/)

---

The team from [Part 2](../02_Project_Planning.md) collected their cores. This is what
happened to them next — one core followed all the way through, then the whole campaign.

> ⚠️ **This is constructed teaching data.** The site and layout are realistic and the values
> sit within published ranges for BC salt marsh and eelgrass, but they are **not field
> measurements** and must not be cited as such.

---

## What came back from the field

Six cores — three in **salt marsh** (`WWF-01-A/C/D`) and three in **eelgrass**
(`WWF-01-B/E/F`) — arrived as 32 labelled bags, plus two field sheets: the *Plot &
Core Log* and the *Sample Data* tab.

The plan from [Part 2](../02_Project_Planning.md) called for 23 cores. Weather and tides being
what they are, the team got six in their first season and intend to return for the rest.
That is worth stating plainly, because it changes how the results below should be read —
and the workflow is built to say so rather than quietly present an under-powered number as
a finished one.

Take core **`WWF-01-A`**. The corer was driven **65 cm** into the sediment but only **58 cm**
of core came out, so the team recorded both numbers. That pair is the whole compaction
record, and without it the core cannot be placed back on real depths.

The core was extruded and cut into six slices, thicker with depth because the interesting
change is near the surface:

| Slice | Depth in the tube (cm) | Description |
|---|---|---|
| 1 | 0–5 | Dense live root mat, dark brown silty clay |
| 2 | 5–10 | Root mat thinning, dark brown silty clay |
| 3 | 10–15 | Fine roots, dark grey-brown silt |
| 4 | 15–25 | Occasional root fragments, grey silty clay |
| 5 | 25–40 | Grey silt, faint organic banding, few roots |
| 6 | 40–58 | Firm grey silt grading to fine sand at base |

## Sending it to the lab

Each slice was weighed wet, dried at 60 °C to constant mass, weighed again, and sent for
**dry bulk density** and **organic carbon**. The team asked for elemental analysis rather
than loss-on-ignition, because eelgrass sediments here are sandy and low in organic matter,
where LOI is least reliable.

What came back, for core `WWF-01-A`:

| Slice | Depth (cm) | Bulk density (g/cm³) | Organic carbon (g/kg) |
|---|---|---|---|
| 1 | 0–5 | 0.42 | 62 |
| 2 | 5–10 | 0.48 | 54 |
| 3 | 10–15 | 0.55 | 43 |
| 4 | 15–25 | 0.63 | 32 |
| 5 | 25–40 | 0.72 | 23 |
| 6 | 40–58 | 0.81 | 16 |

Carbon falls and density rises with depth, which is the expected pattern: the surface is
young, root-rich and light; the base is compacted mineral sediment.

## Putting the core back on real depths

58 cm of core came out of a 65 cm hole, so the sediment was compressed by a factor of
**65 ÷ 58 = 1.121**. Every slice sat deeper in the ground than it did in the tube.

Correcting for that stretches the depths — slice 6 moves from 40–58 cm to **44.8–65.0 cm**
— and thins the bulk density by the same factor, from 0.81 to **0.723 g/cm³**. The two
cancel exactly, which they must: the tube holds precisely the sediment that came out of the
hole. Core `WWF-01-A` contains **10.61 kg C/m²** before the correction and 10.61 kg C/m²
after. What changes is *where* that carbon is, not how much.

> This is the step most often got wrong. Stretching depths without thinning density inflates
> every stock by the compaction factor — 8–14% across these six cores. The workflow
> asserts the total is unchanged and stops if it is not.

## Making six different cores comparable

The cores are not the same length: the marsh cores reach 58–72 cm in the ground, the
eelgrass cores only 26–35 cm. They were also sliced at different thicknesses. Before
anything can be averaged they have to be put on the same depth intervals — done with a
mass-preserving spline, which redistributes carbon onto standard bins without inventing or
losing any.

Below the base of each core there is nothing to measure, so the profile is **modelled**:
carbon declining toward a non-zero floor, because eelgrass sediments retain recalcitrant
carbon at depth rather than decaying to nothing.

That leaves two honest numbers instead of one:

- **0–25 cm** — every one of the six cores physically reached this depth. Fully measured.
- **0–50 cm** — the deepest interval *every* core can support. For the marsh cores this is
  still entirely measured; for the eelgrass cores, a substantial share of it is modelled,
  and the workflow reports that share per core.

Anything deeper would mean averaging a 100 cm marsh core against a 50 cm eelgrass core and
calling the result one number.

## The estimate

Each stratum's mean is weighted by its **area** — 1.8 ha of marsh, 3.2 ha of eelgrass — not
by how many cores landed in it. Both strata got three cores, but the eelgrass covers nearly
twice the ground, so it carries nearly twice the weight.

| | Salt marsh | Eelgrass |
|---|---|---|
| Cores | 3 | 3 |
| Area | 1.8 ha (36%) | 3.2 ha (64%) |
| Mean stock 0–25 cm | 5.17 ± 0.25 kg C/m² | 2.00 ± 0.41 kg C/m² |

**Area-weighted result: 3.14 kg C/m², or 31.4 ± 2.7 Mg C/ha, to 25 cm.**
Across the 5 ha inlet, **157 Mg C**.

To 50 cm, **51.5 ± 3.8 Mg C/ha**.

The marsh holds **2.6 times** the carbon of the eelgrass per square metre to 25 cm
(difference 3.17 kg C/m²). Note that with three cores per stratum this comparison has low
power — the contrast is large and consistent, but a formal test on 4 degrees of freedom
proves little either way, and a non-significant result here would not be evidence that the
strata are equal.

Whole-core totals, which need no depth model, run wider still: the marsh cores average
**10.33 kg C/m²** against **2.23 kg C/m²** in the eelgrass, a ~4.6 : 1 contrast. That is a
different quantity — the marsh cores are roughly twice as long, and standardising to 25 cm
removes the extra length, which is why the depth-standardised ratio is the smaller one. In
both cases the marsh sediment is far richer in carbon even though it is less dense:
concentration wins over density.

## Did the campaign work?

The plan called for **±20% at 90% confidence** and for 23 cores. The team collected six,
and those six delivered **±18.6%**.

**The target was met** — narrowly. That sentence, not the point estimate, is what a reviewer
checks first, and the word "narrowly" belongs in it: the estimate rests on **4 degrees of
freedom**, and against a ±10% target the same data would have failed. A survey that misses
its target has not failed either; it has costed the next season. What would be a failure is
reporting the point estimate as though the target had been met.

Worth seeing what stratifying bought. Running the same Cochran formula from
[Part 2](../../02_Project_Planning/#appendix-a--a-brief-lesson-in-sampling-logic) at this
campaign's own ±20% target, with the variability read off three different bases — the
planning prior, these six cores treated as one population, and these six cores within their
strata:

| Basis for the variability | $CV$ | Implied cores at ±20% |
|---|---|---|
| Planning prior — regional eelgrass, all sources of spread | 0.68 | 30 |
| Observed, ignoring strata | 0.50 | 17 |
| Observed, within strata — what stratifying actually buys | 0.19 | 2 |

<!-- These three rows are computed from the per-core 0-25 cm stocks in section 2 above,
     using the Cochran formula in Part 2 Appendix A2-A3 (N = 500, z = 1.645). They are
     reproducible from the published table; they are not separate pipeline output. -->

Planning used the conservative figure, which is the right way to be wrong: an under-powered
survey costs another field season. But **stratifying the meadow cut the effective
variability by more than half**, because most of the variation at this site is *between*
marsh and eelgrass, not within either. The design absorbed it before the statistics had to —
which is why six well-placed cores go further here than six scattered ones would.

Do not read the bottom row as "two cores would have done". It is the variance term alone,
and it ignores everything else a design has to survive: the 5-core-per-stratum minimum from
Part 2, cores lost to refusal or weather, and the fact that you cannot know the within-strata
$CV$ until after you have sampled. It is an argument for stratifying, not for sampling less.

## What the prior added

The regional prior — 82 *Zostera marina* cores from 11 comparable estuaries — says
**21.7 ± 7.9 Mg C/ha**. Combined with the fieldwork it gives **30.4 ± 2.6 Mg C/ha**, and it
earned **11%** of the weight.

How much weight the prior earns is itself the finding, and it moves with your sample size.
Eleven percent means most of the answer still comes from the fieldwork — which is what a
campaign of this size should produce — but it is a good deal more than a full campaign would
have conceded, because the prior describes *meadows of this kind* while your cores describe
*this one*. That is the mechanism working as intended: it leans in hardest when your own
data is thinnest, and steps back as you collect more.

> The synthesis contains three eelgrass cores from Tsawwassen itself. They were **excluded**
> from the prior — otherwise those cores would count once as prior and again as evidence,
> and the result would look more certain than it is.

## What happened next

The team reported **157 Mg C in the top 25 cm of a 5 ha inlet, ±18.6% at 90% confidence**,
alongside the 2.6 : 1 marsh-to-eelgrass contrast — which is the number that actually matters
for management, because it says which habitat is worth protecting per hectare.

Four things they flagged in the report:

1. The **stratum areas** drive the site total, and came from a drawn boundary rather than a
   survey. Tightening them tightens the total.
2. The 0–50 cm figure is **partly modelled** in the eelgrass stratum. Longer cores there
   would replace inference with measurement.
3. This is a **stock**, not a sequestration rate. Saying how fast carbon is accumulating
   needs dated cores, which this campaign did not collect.
4. The campaign is **six cores against a plan of 23**. The estimate stands on its own
   interval, but the next season's coring is what will tighten it — and the workflow prints
   how many more cores that would take.

---

**→ Run it yourself:** the analysis lives in
[`04_Data_Interpretation/DataAnalysisWorkflow/`](../../resources.md#pending-materials).
`source("run_pipeline.R")` reproduces every number on this page.
