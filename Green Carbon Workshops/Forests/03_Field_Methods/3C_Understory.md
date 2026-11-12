# Part 3C — Field Methods: Understory *(optional)*

*Shrubs, saplings and ground vegetation — the fast-moving pool.*

[← 3B — Soil](3B_Soil.md) · [Part 3 overview](README.md) · [Back to main guide](../README.md)

**Source:** [*Measuring Carbon in Vegetation (Non-Tree)*](../../_Shared/Vegetation-FINAL-Eng-2026.pdf) (WWF-Canada, 2026)

---

## Is this worth doing?

Honestly: **often not, for a closed-canopy forest.** Understory typically holds well under 5%
of a forest stand's carbon — the worked example comes out around 1–2% — and clip-and-weigh is
fiddly, seasonal work.

It earns its place when:

- The stand is **open** — recent harvest, burn, regeneration, or a naturally sparse canopy
- The project tracks **vegetation recovery** after disturbance, where understory is the signal
- You need a **complete** stand-level account for crediting or compliance
- The site grades into shrubland or a forest edge

If none of those apply, record that you excluded it and why, and spend the effort on more soil
cores instead. That is a defensible decision; silently omitting a pool is not.

---

## Two plots, two completely different methods

The understory splits by **height**, and each half is measured differently.

| | Plot | Height | Method | Gives you |
|---|---|---|---|---|
| **Medium** | 4 × 4 m (16 m²) or 10 × 10 m (100 m²) | 0.5–2 m | **Measure and predict** — allometric | Non-destructive |
| **Small** | 1 × 1 m (1 m²) or 0.5 × 0.5 m (0.25 m²) | under 0.5 m | **Clip and weigh** — destructive | Direct mass |

Anything **over 2 m** is a tree — it belongs in [3A](3A_Trees.md), in the large plot.

> [!IMPORTANT]
> Record **which plot sizes you used** on the Plot & Site Log. The calculator divides medium-plot
> carbon by the medium area and small-plot carbon by the small area. Using a 16 m² plot but
> leaving 100 m² on the log understates that pool six-fold.

---

## Medium plot — measure and predict

*0.5–2 m tall, measured without cutting anything.*

Identify every individual between roughly knee height and an arm's length above your head, then
measure it. **Which measurement depends on the growth form**, and this is the one thing to get
right:

<table>
<tr>
<td width="50%">

**Short-statured tree** — a single woody stem

Measure the **stem diameter at 0.30 m** above the ground, in cm. (Note: 0.3 m, not the 1.3 m
you'd use for a full tree.)

> 📸 **[PHOTO NEEDED]** — measuring a sapling stem at 0.3 m with a DBH tape.

</td>
<td width="50%">

**Shrub** — multiple stems from the base

Measure the **crown volume**: maximum height, length (E–W) and width (N–S), all in metres.
Volume = L × W × H.

Best done with three people: two holding the tape either side of the plant, one recording.

> 📸 **[PHOTO NEEDED]** — two crew members measuring shrub crown width with a tape.

</td>
</tr>
</table>

**📋 Record it:** `4. Understory Data`, with **Plot type** = `Medium` and **Plant type** =
`tree` or `shrub`.

> [!NOTE]
> **The calculator chooses the model input from Plant type, not by adding your numbers
> together.** A `tree` row uses the diameter; a `shrub` row uses L × W × H. Fill in only the
> columns that apply to the growth form — if you enter a diameter on a shrub row it will be
> ignored, and the row will be flagged so you know.

### Which species can be calculated

The coefficients come from **Flade et al. (2020)** and cover a small set of northern shrubs:

| | |
|---|---|
| Alder (*Alnus* spp.) · Bog birch (*Betula* spp.) · Willow (*Salix* spp.) | Shrubby cinquefoil (*Dasiphora fruticosa*) · Soap berry (*Shepherdia canadensis*) |
| **Short statured tree** — generic single-stem form | **all shrubs** — a pooled equation for anything not listed |

Use **`all shrubs`** for any species without its own row. It's a pooled fit, so it's less
precise than a species-specific equation but better than omitting the plant.

> 📚 **[RESOURCE NEEDED]** — this list is short, northern, and does not cover the shrub flora of
> southern Canada well. Extending it means going outside the WWF guides: candidate sources
> include regional shrub allometry compilations and the broader biomass-equation literature.
> Until then, `all shrubs` carries most southern species, and that limitation belongs in your
> reporting.

> [!WARNING]
> **No roots are included for understory.** The Flade equations are above-ground only, and the
> calculator applies no root:shoot to them — unlike trees, which do get a below-ground term. So
> understory carbon here is **above-ground carbon**, and adding it to the tree pool adds two
> things defined slightly differently. It is a small number in a forest, so the effect is small,
> but say so when you report. Every understory row carries a flag noting it.

---

## Small plot — clip and weigh

*Under 0.5 m, measured by cutting and drying it.*

The most accurate way to get ground-layer biomass is to take it away and weigh it.

<table>
<tr>
<td width="55%">

1. **Photograph the plot** from directly overhead, with the 1 × 1 m frame visible. Record the
   photo ID.
2. **Section off a quarter** — a 0.5 × 0.5 m frame, or a circle of radius 0.28 m. Both are
   0.25 m².
3. **Clip every plant** inside the frame at **3 cm above ground**.
4. **Bag each species separately**, labelled with plot ID, species and date.
5. In the lab: **dry at 50–80 °C for 48–72 hours**, then weigh. That dry mass is what you enter.

</td>
<td width="45%">

> 📸 **[PHOTO NEEDED]** — an overhead shot of a 1 × 1 m quadrat with the 0.25 m² subplot marked.

> 📸 **[PHOTO NEEDED]** — clipped samples in labelled bags, and the same samples after drying.

</td>
</tr>
</table>

**📋 Record it:** `4. Understory Data`, with **Plot type** = `Small`. Enter the **oven-dry mass
in grams** and leave the dimension columns empty — the calculator takes the mass directly, with
no allometric step.

> [!IMPORTANT]
> **If you clipped a quarter of the plot, the plot area you record must be the area you actually
> clipped** — 0.25 m², not 1 m². This is the single easiest way to be wrong by a factor of four.

### Timing matters more here than anywhere else in the workshop

Ground vegetation is not a stable stock. It grows from nothing in spring and dies back in
autumn, and a clip in June and a clip in August can differ several-fold.

- Sample at **peak growing season** if you want maximum standing biomass — the convention.
- **Record the date**, always.
- If you re-survey, **re-survey at the same phenological stage**, not the same calendar date.

> [!NOTE]
> **A clipped biomass figure is not a carbon stock in the way soil carbon is.** Soil carbon has
> accumulated over centuries and will still be there next year. Ground vegetation turns over
> annually — much of what you clip would have died and decomposed regardless. Adding the two and
> reporting one number is standard practice, but the two halves mean quite different things, and
> it's worth a sentence in your reporting.

---

## Special case: Sphagnum

If your plot is a *Sphagnum*-rich hollow — more likely in a lowland conifer stand than an upland
one — clipping doesn't work. Instead take a **surface core** of the top 10–15 cm with a mould or
surface corer, bag it, and in the lab **separate the living Sphagnum (colourful) from the
non-living, decomposing material below (discoloured)**. Only the living portion is vegetation.

> [!WARNING]
> **Don't double-count.** The dead Sphagnum below the living layer is *soil*, and if your soil
> core starts at the surface it has already counted that material. Count the living layer as
> vegetation and everything below as soil, and make sure the two don't overlap.

---

## ✅ Before you leave the plot

- [ ] Medium plot: every individual 0.5–2 m identified and measured
- [ ] The right measurement for each growth form — diameter for single stems, L × W × H for shrubs
- [ ] Small plot: overhead photo taken, ID recorded
- [ ] Clipped at 3 cm, bagged by species, labelled
- [ ] **The clipped area recorded correctly** (0.25 m², if you clipped a quarter)
- [ ] Date recorded — phenology matters
- [ ] All of this done **before** any soil sampling

**Next:** [Part 4 — Data Interpretation](../04_Data_Interpretation/), once the samples are dry
and the lab results are back.
