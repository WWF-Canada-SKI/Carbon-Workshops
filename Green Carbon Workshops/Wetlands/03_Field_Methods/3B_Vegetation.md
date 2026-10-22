[← 3A — Peat Coring](3A_Peat_Coring.md) · [← 3 — Field Methods](README.md) · [Back to main guide](../README.md) · Next: [4 — Data Interpretation →](../04_Data_Interpretation/)

---

# 3B — Vegetation *(optional)*

*Trees in swamps, shrubs and the ground layer — and the one trap that is specific to peatlands:
counting the same moss twice.*

**Sources:** [Forests Part 3A — Trees](../../Forests/03_Field_Methods/3A_Trees.md) and
[3C — Understory](../../Forests/03_Field_Methods/3C_Understory.md), which this page routes to.
Wetland-specific content from [Bansal et al. (2023)](../../_Shared/s13157-023-01722-2.pdf) and the
[peat guide](Peat-FINAL-Eng-2026.pdf).

---

## Is this page for you?

<table>
<tr>
<td width="50%">

**Read it if:**

- Tree cover is **≥ 25%** — you are in a **swamp**, and trees are a real pool
- You are reporting a **total ecosystem** carbon stock, not just soil
- A standard or funder requires **all pools**
- You are working in a **bog** and harvesting living *Sphagnum* — then read
  [the trap](#the-sphagnum-double-counting-trap) at minimum, even if you skip the rest

</td>
<td width="50%">

**Skip it if:**

- You are reporting **soil carbon** only, and saying so
- Tree cover is negligible and vegetation is a fraction of a percent of the stock
- Budget is tight. **Peat first, always** — a complete peat dataset with no vegetation beats a
  partial version of both

</td>
</tr>
</table>

> [!NOTE]
> **Whatever you choose, say so.** "Total carbon stock" and "soil carbon stock" are different
> numbers, and a report that does not name which it gives is the report a reviewer sends back.
> Vegetation excluded is fine; vegetation silently excluded is not.

---

## How much is actually here?

Worth being honest about the magnitudes before you spend a day on it.

| Pool | In a deep-peat bog | In a treed swamp on shallow peat |
|---|---|---|
| **Peat** | >99% | 80–95% |
| **Trees** | ~0 | **5–20%** — worth measuring |
| **Shrubs** | <1% | 1–2% |
| **Ground layer / moss** | <1% | <1% |

*Indicative, from the pool ratios in [Part 1](../01_Background/) and the peat-depth range. Your
own numbers will differ — the point is the ordering, not the exact percentages.*

The pattern: **the shallower the peat, the more the vegetation matters.** In the
[worked example](../Worked_Example/), the swamp site has 26–104 cm of peat and by far the largest
relative vegetation contribution; the bog, at 214–366 cm, barely registers it.

> [!TIP]
> **This gives you a decision rule.** Probe the depth first
> ([3A, Stage 1](3A_Peat_Coring.md#stage-1--the-depth-survey)). If peat is deeper than about 2 m,
> vegetation is inside your peat measurement's own uncertainty and you can defensibly skip it
> — **as long as you report a soil stock, not a total.** If peat is under a metre and there are
> trees, measure them.

---

## Trees — route to the Forests protocol

**The protocol is identical.** A black spruce in a swamp is measured the same way as a black
spruce on a ridge, and runs through the same allometric equations.

**👉 [Forests Part 3A — Trees](../../Forests/03_Field_Methods/3A_Trees.md)**

| | |
|---|---|
| **Plot** | **400 m²** large plot, centred on — or containing — your 100 m² peat plot |
| **Measure** | Species, **DBH at 1.3 m**, height (or a subsample of heights) |
| **Equations** | Lambert et al. (2005) and Ung et al. (2008): $\text{Biomass} = a \cdot DBH^{b}$ or $a \cdot DBH^{b} \cdot H^{c}$, over wood, bark, branches and foliage |
| **Below-ground** | Published root:shoot ratios — deciduous $BGB = 1.576 \cdot AGB^{0.615}$, conifer $BGB = 0.222 \cdot AGB$ |
| **Enter into** | The [Forests calculator](../../Forests/04_Data_Interpretation/calculators/)'s `3. Tree Data` tab |

### Five things that are different in a swamp

| | |
|---|---|
| **1. Footing, not forestry, is the constraint** | Measuring DBH while standing on a floating hummock is the hard part. Allow **twice** the time per plot you would in an upland stand |
| **2. Buttressed and multi-stemmed bases** | Eastern white cedar and black ash in swamps often fork below 1.3 m. Follow the Forests protocol's rule, apply it **consistently**, and note which stems you counted as one tree |
| **3. Hummock bases shift where 1.3 m starts** | A tree on a 40 cm hummock — is DBH measured from the hummock top or the surrounding hollow? **Measure from the ground at the stem base** (the hummock top, for a tree growing on one) and write the convention on the sheet |
| **4. Stunted trees fall outside the equations' range** | A 150-year-old bog spruce can be 4 cm DBH. Canadian allometric equations are fitted mostly on merchantable stems, and extrapolating below their fitted range is unreliable. **Record the DBH, flag it, and say in your reporting that small-stem biomass is extrapolated** |
| **5. Standing dead is common** | Flooded swamps kill trees standing. That carbon is **dead wood**, not live biomass, and neither this workshop nor Forests covers it. Count and note them so the gap is visible |

> [!WARNING]
> **Below-ground tree biomass and peat carbon can overlap.** Tree roots grow **down into the
> peat**, and peat samples containing live roots include root carbon that the root:shoot ratio is
> also counting.
>
> The overlap is small in deep peat — roots are concentrated in the top 30–50 cm, which is a small
> share of a 3 m profile — but it is **not** small in a shallow-peat swamp where roots reach a
> large fraction of the profile.
>
> **What to do:** pick out and discard **visible live roots** from peat sections before analysis,
> note that you did, and state the residual double-counting as a known limitation. Do not attempt
> a numerical correction — there isn't a defensible one at this level of effort.

---

## Shrubs and ground vegetation — route to Forests

**👉 [Forests Part 3C — Understory](../../Forests/03_Field_Methods/3C_Understory.md)**

| | |
|---|---|
| **Medium plots** | **16 m² (4 × 4) or 100 m² (10 × 10)** — shrubs |
| **Small plots** | **1 m² or 0.25 m² (0.5 × 0.5)** — ground layer, herbs, moss |
| **Shrub method** | Non-destructive allometrics from Flade et al. (2020): $y = b \cdot x^{a}$, where $x$ is stem diameter at 0.3 m for tree-form species, or crown **L × W × H** for shrubs |
| **Ground layer** | **Clip and weigh.** Harvest the quadrat, dry, weigh, apply a carbon fraction |
| **Enter into** | The [Forests calculator](../../Forests/04_Data_Interpretation/calculators/)'s `4. Understory Data` tab |

### Peatland-specific notes

- **Ericaceous shrubs are the bog understory** — Labrador tea, leatherleaf, bog laurel,
  sheep laurel. Flade et al. covers bog birch and alder among others; check whether your species
  is in the coefficient table on the calculator's `R2. Understory Coefficients` tab before you
  rely on an allometric, and **clip-and-weigh** if it is not.
- **Sedges and graminoids** in fens are best done by **clip and weigh**, not allometrics.
- **Seasonality matters more here than in a forest.** A sedge fen's above-ground biomass peaks
  late in the growing season and is near zero in spring. Record the **date**, and do not compare
  a June harvest with a September one.
- **Don't harvest where you will core.** Offset the clip quadrats from the coring point, or core
  first at a *different* plot. The ordering rule in [the overview](README.md) applies within a
  plot: vegetation before peat.

---

## The *Sphagnum* double-counting trap

This is the one genuinely peatland-specific hazard on this page, and it is easy to walk into.

<table>
<tr>
<td width="55%">

**The situation.** In a *Sphagnum* bog there is no boundary between vegetation and soil — there is
a **gradient**. The top few centimetres are living green moss. Below that it browns. Below that it
is unambiguously peat. No line is drawn on the ground.

**The trap.** Your peat core starts at the **peat surface** — which in practice means the top of
the moss, or wherever you decided the surface was. So the core has **already counted** the brown
transitional material. If you then harvest a moss quadrat that reaches down into the brown layer
and add it as "vegetation carbon", **you have counted the same carbon twice.**

**How big is it?** Small in absolute terms — a few tenths of a kg C/m². But it is a **systematic**
error in a known direction, and it is free to avoid.

</td>
<td width="45%">

```
   ▓▓▓  living green Sphagnum     ┐
   ▓▓▓  (capitula + a few cm)     │ VEGETATION
   ───────────────────────────────┤ ← the boundary
   ░░░  brown, dead but fibrous   │
   ░░░  (H1–H2, still recognisable)│
   ▒▒▒  brown peat (H3–H4)        │ PEAT — in the core
   ▒▒▒                            │
   ███  darker peat (H5+)         │
   ███            ...             ┘
```

> 📸 **[FIELD PHOTO NEEDED]** — a close vertical section through the *Sphagnum* surface showing
> the green → brown transition with a scale bar. This is the peat guide's **Frame A** transition.

</td>
</tr>
</table>

### The rule: the core starts where the harvest stops

**Pick a boundary, write it down, use it at every plot.** Three defensible choices:

| Option | The boundary | Pros | Cons |
|---|---|---|---|
| **A — Green/brown** *(recommended)* | Harvest only **living green** tissue; the core starts at the top of the brown | Visually unambiguous in the field. Matches the peat guide's **Frame A** note | The green/brown line moves seasonally and with moisture |
| **B — Fixed depth** | Harvest the top **5 cm**; the core starts at 5 cm | Perfectly repeatable and auditable | Includes dead moss in "vegetation"; excludes deep-growing living capitula |
| **C — Skip moss entirely** | No moss harvest. The core takes everything | **Zero double-counting risk.** Simplest | Loses a (small) pool. Be explicit that you did this |

**Option C is a perfectly good answer** when peat is deep, and is what most stock-focused
campaigns should do.

### Record it on the sheet

Whatever you choose, three things go in the notes:

1. **The boundary rule** you used (A, B or C, described in words)
2. **The depth of the green/brown transition** at this plot — this is the Frame A observation from
   [3A, Stage 3](3A_Peat_Coring.md#the-transitions-to-look-for--frames-a-b-and-c)
3. **Where your core's zero datum sits** relative to that transition

> [!IMPORTANT]
> **Living moss is not the only thing that shifts your zero.** Where the surface is loose
> *Sphagnum*, the "peat surface" is a judgement call of several centimetres — and that is exactly
> what Bansal's **surface compaction** measurement
> ([3A](3A_Peat_Coring.md#the-four-numbers-bansal-says-to-record)) is for. Record it, and be
> consistent about the datum across a campaign. An inconsistent zero adds noise to every depth
> comparison and to any age–depth model you build in
> [Part 5](../05_Chronology_Supplement/).

---

## Where the numbers go

The Wetland calculator has **no vegetation tabs** — deliberately, so there is one place each
measurement lives rather than two competing versions.

```
Trees, shrubs, ground layer
        │
        ▼
Forests calculator  ──►  3. Tree Data · 4. Understory Data
        │
        ▼
        kg C/m² per plot
        │
        ▼
Wetland calculator  ──►  1. Plot & Site Log, "Vegetation carbon (kg C/m²)"
        │
        ▼
        added to the peat stock in 5. Plot Summary
```

**Match the `Plot ID` exactly across both workbooks.** That string is the join, and a mismatch
silently drops the vegetation from the total.

> [!NOTE]
> **Mind the plot areas when you transfer.** Tree carbon comes out of a **400 m²** plot; peat
> carbon out of **100 m²**. Both are already **per square metre** by the time they reach the
> `Vegetation carbon` column, so they add directly — but only if you carried the per-m² figure
> across and not a per-plot total. The Forests calculator reports per-m²; check the units on the
> cell you copy.

---

## ✅ Before you leave the plot

| | |
|---|---|
| ☐ | Decision recorded: **is vegetation in scope at this plot?** |
| ☐ | If trees: 400 m² plot laid out, species / DBH / height recorded, small stems flagged |
| ☐ | Standing dead trees **counted and noted** as an uncovered pool |
| ☐ | If shrubs: medium plot measured, species checked against the coefficient table |
| ☐ | If ground layer: small plots clipped, bagged, labelled, **date recorded** |
| ☐ | ***Sphagnum* boundary rule** written in the notes, and the green/brown depth recorded |
| ☐ | Visible live roots picked out of peat sections, and the fact noted |
| ☐ | All of the above done **before** any coring at this plot |

---

[← 3A — Peat Coring](3A_Peat_Coring.md) · [← 3 — Field Methods](README.md) · [Back to main guide](../README.md) · Next: [4 — Data Interpretation →](../04_Data_Interpretation/)
