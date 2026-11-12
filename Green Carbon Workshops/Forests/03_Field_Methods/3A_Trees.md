# Part 3A — Field Methods: Trees

*Measuring the trees that fill the `3. Tree Data` sheet.*

[← Part 3 overview](README.md) · [3B — Soil →](3B_Soil.md) · [Back to main guide](../README.md)

**Source:** [*Measuring Carbon in Trees*](Trees-FINAL-Eng-2026.pdf) (WWF-Canada, 2026) ·
**Checklist:** [`Forest_Carbon_Skill_Checklist.docx`](checklists/Forest_Carbon_Skill_Checklist.docx)

---

## What you're collecting, and why

For every tree over 2 m tall in the large plot, three things:

| Measurement | Unit | Why it's needed |
|---|---|---|
| **Species** | — | Chooses the allometric equation. Different species build wood at different densities |
| **DBH** | cm | The main predictor of biomass. Everything scales off it |
| **Height** | m | Optional, but it switches on a more precise equation |

That's it. **No lab, no samples, no cost beyond your crew's time** — which makes trees the
cheapest real carbon number in the workshop.

The reason three field measurements are enough is **allometry**: a published statistical
relationship between a tree's easily-measured dimensions and its hard-to-measure mass, fitted
on thousands of trees that *were* cut down and weighed. This workshop uses the Canadian
national equations of Lambert et al. (2005) and Ung et al. (2008), which cover 39 species plus
generic deciduous and conifer forms. They are built into the calculator's
`R1. Tree Coefficients` tab.

---

## Step-by-step

Five steps, once the plot is laid out per the [overview](README.md).

| # | Step | Answers |
|---|------|---------|
| 1 | **Lay out the large plot** | *Where is its edge, and which trees are in?* |
| 2 | **Flag every tree** | *How do I avoid counting one twice — or missing one?* |
| 3 | **Identify the species** | *Which equation applies?* |
| 4 | **Measure DBH** | *How big is it?* |
| 5 | **Measure height** | *How tall — on a subset, at least?* |

---

### 1. Lay out the large plot

*Where is its edge, and which trees are in?*

<table>
<tr>
<td width="45%">

> 📸 **[PHOTO NEEDED]** — running the tape out from the plot centre to 11.28 m and flagging
> the boundary trees.

</td>
<td width="55%">

The large plot is **400 m²**, in whichever shape suits the ground:

- **Circular**, radius **11.28 m** from the centre. One person holds the tape at the centre,
  another walks the circle flagging boundary trees.
- **Square**, 20 × 20 m — one person per side.
- **Rectangular**, 10 × 40 m — useful in narrow stands or along a gradient.

If you have a compass, align the width E–W and the length N–S. Record the slope in both
directions.

</td>
</tr>
</table>

> [!IMPORTANT]
> **The borderline-tree rule.** A tree on the boundary is **in** the plot if the **centre of its
> trunk** is inside the line. For a forked or split tree, find the centre **below** the fork.
> Decide this consistently — on a dense plot boundary it can shift the plot total by several
> per cent.

**On a slope**, 400 m² means 400 m² in horizontal projection. Either lengthen the tape —
`adjusted distance = horizontal ÷ cos(angle)`, so 23.1 m per side on a 30° slope — or record the
slope angles and answer **No** to *"Slope allowance applied in field?"* on the Plot & Site Log,
and the calculator corrects the area. The [Trees guide](Trees-FINAL-Eng-2026.pdf) appendix has a
lookup table.

---

### 2. Flag every tree before you measure any

*How do I avoid counting one twice — or missing one?*

<table>
<tr>
<td width="55%">

Walk the whole plot — perimeter *and* interior — and put a strip of flagging tape on **every
tree over 2 m tall**. Then start measuring, **removing the tape from each tree as you finish
it**.

At the end, no tape left means no tree missed and none counted twice. On a dense plot with 40
stems this is the difference between a clean dataset and an unresolvable one.

</td>
<td width="45%">

> 📸 **[PHOTO NEEDED]** — a flagged plot before measurement, tape visible on every stem.

</td>
</tr>
</table>

---

### 3. Identify the species

*Which equation applies?*

<table>
<tr>
<td width="45%">

> 📸 **[FIGURE NEEDED]** — the dichotomous key from the Trees guide (p.13), with a worked path
> circled.

</td>
<td width="55%">

Use a **dichotomous key** — a series of either/or questions about leaf shape, bark, branching
pattern, buds and cones that narrows to a species. Apps help (Google Lens, LeafSnap, vTree,
Seek by iNaturalist) but confirm with a key where you can.

**If you're unsure in the field**, don't guess. Photograph the leaf, bark, branching and any
buds, flowers or cones, and record a **photo ID next to that tree's measurements**. Identify it
properly later.

</td>
</tr>
</table>

> [!WARNING]
> **Species identification is a bigger source of error than your tape is.** The calculator will
> happily apply a birch equation to a misidentified poplar, and the number it returns will look
> entirely reasonable. Where you genuinely can't identify a stem, use the generic **`Deciduous`**
> or **`Conifers`** entry rather than guessing at a species.
>
> Avoid the generic **`All`** entry unless you truly cannot tell hardwood from softwood: there is
> no published root:shoot relationship for a mixed unknown, so the calculator averages the
> deciduous and conifer relationships and raises a flag on that row.

---

### 4. Measure DBH

*How big is it?*

<table>
<tr>
<td width="55%">

**Diameter at breast height** is measured at **1.3 m above ground**.

- With a **DBH tape**: wrap it round the trunk at 1.3 m and read the diameter directly. The tape
  is scaled so circumference reads out as diameter.
- Without one: measure the **circumference** with an ordinary tape, record it as circumference,
  and divide by π (3.1416) later. **Write down which one you measured** — a circumference
  recorded as a diameter overestimates biomass enormously.

On sloping ground, measure 1.3 m from the ground on the **uphill** side.

</td>
<td width="45%">

> 📸 **[PHOTO NEEDED]** — a DBH tape correctly positioned at 1.3 m, tape level and snug.

</td>
</tr>
</table>

**📋 Record it:** Plot ID, Tree ID, species and DBH on the
[Tree Survey Datasheet](datasheets/Tree-Survey-Datasheet.docx), then into `3. Tree Data`.

---

### 5. Measure height

*How tall — on a subset, at least?*

<table>
<tr>
<td width="45%">

> 📸 **[PHOTO NEEDED]** — taking a height with a laser rangefinder, standing back far enough to
> see base and top.

</td>
<td width="55%">

Stand far enough back to see both the base and the top of the tree. Sight the top, sight the
base, and the rangefinder computes the height.

**Height is optional per tree, and that's deliberate.** The calculator switches equations
automatically:

| If you record | The calculator uses | Column G says |
|---|---|---|
| DBH only | `a × DBH^b` | `DBH only` |
| DBH **and** height | `a × DBH^b × height^c` | `DBH + height` |

Measuring height on every tree is slow. Measuring it on **none** loses precision. A common
compromise, and what the worked example does, is to measure height on roughly **one tree in
three**, spread across the size range.

</td>
</tr>
</table>

> [!NOTE]
> **Leave the height cell blank if you didn't measure it — don't put 0.** A zero is a measurement
> claim; a blank is an honest absence. The calculator treats blank as "use the DBH-only equation"
> and would treat a 0 the same way here, but the habit matters on every other sheet.

---

## Permanent sample plots

If the plot will be re-measured in future years — which is the only way to measure
*sequestration* rather than *storage* — a few extra steps now save the whole exercise later:

- **Tag every tree** with a DBH of 9 cm or more. Nail a numbered metal tag at **1.3 m**, leaving
  room for the trunk to grow around the nail.
- **Mark the plot centre permanently** — a metal stake and a sign with the plot ID and
  coordinates.
- **Document the access route** in notes and waypoints. In ten years, nobody will remember it.
- Keep destructive sampling (soil) **outside** the plot.

> For fuller guidance see Canada's
> [National Forest Inventory Ground Sampling Guidelines](https://nfi.nfis.org/resources/groundplot/Gp_guidelines_v5.0.pdf),
> which the Trees guide points to.

---

## What happens to these numbers

For each tree, the calculator predicts four components separately — **wood, bark, branches and
foliage** — sums them to above-ground biomass, adds roots, and halves the total:

```
AGB (kg)    = Σ over {wood, bark, branches, foliage} of  a × DBH^b [× height^c]
BGB (kg)    = 1.576 × AGB^0.615   (deciduous)   or   0.222 × AGB   (conifer)
Carbon (kg) = (AGB + BGB) × 0.5
```

Then per plot: `tree carbon ÷ large plot area = kg C/m²`.

> [!NOTE]
> **On the two root equations.** The deciduous relationship is a power law and the conifer one is
> a fixed ratio — they come from different derivations, and at small tree sizes they diverge
> sharply. The Trees guide states roots are **18–30% of total tree biomass**; the calculator
> flags any tree falling outside 10–40% so you can see when the relationship is being pushed
> beyond where it was fitted. Treat below-ground biomass as the least certain number on the
> sheet.

---

## ✅ Before you leave the plot

- [ ] Every flagged tree measured, and all flagging removed
- [ ] Species recorded for each — or a photo ID where unsure
- [ ] DBH recorded, and noted whether it is diameter or circumference
- [ ] Heights on your chosen subset
- [ ] Plot ID identical to the Plot & Site Log
- [ ] Slope recorded, and whether the allowance was applied

**Next:** [3B — Soil](3B_Soil.md). Remember: **all vegetation work first**.
