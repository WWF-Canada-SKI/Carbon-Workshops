# Sampling Design Tools — placeholders

> [!WARNING]
> **Nothing in this folder is wetland-specific yet.** A peatland sampling tool is in
> development. What is here is an interim stand-in, and you need to know what it does and
> doesn't give you before using it.

---

## What's here now

### `ForestSamplingTool_GEE.js` — usable, with one caveat

This is the **Forests** sampling tool, copied in unchanged. Paste it into the
[Google Earth Engine Code Editor](https://code.earthengine.google.com/) and run it.

**What transfers to a peatland without any change** — the statistics are ecosystem-free:

- Cochran's finite-population sample size (the *n* calculation behind
  [Part 2, Step 4](../README.md#step-4--decide-how-many-cores))
- Proportional allocation across strata, with the 5-per-stratum minimum
- The achieved-precision check you run after the field season
- Boundary geometry, buffering, plot layout and spacing
- Its self-test harness, which verifies every reported number against the workshop's own
  arithmetic

**What does NOT transfer, and will mislead you if you let it:**

| Setting | Forests value | Why it's wrong for a peatland |
|---|---|---|
| **Priors** | Forest biomass and mineral soil carbon | A bog holds several times the soil carbon of an upland forest, and is far more variable. Forest priors will **under-size** your campaign |
| **Plot size** | 400 m² (a tree plot) | The peat guide works in **10 × 10 m (100 m²)** plots, one coring site per plot |
| **Pool selection** | Trees / Soil / Understory | A peatland campaign is soil-first |

**How to use it anyway.** Ignore the built-in priors and **type in your own**: a mean and
standard deviation from a pilot survey, or from the peatland sources in
[Part 2, Step 4](../README.md#where-the-prior-comes-from). Set the plot size to 100 m². The
sample-size maths is then correct.

---

## What's coming

| Tool | Status |
|---|---|
| **Wetland sampling design tool** | To be built. Peatland priors, 100 m² plots, and stratification by wetland type and microform |
| **Prior carbon scoping tool** | A larger version is in development separately. The current Forests copy lives in [`../../../Forests/02_Project_Planning/Sampling Design Tools/`](../../../Forests/02_Project_Planning/Sampling%20Design%20Tools/) |

> 📌 **Note for whoever builds these.** The existing prior-scoping script already loads the two
> datasets a peatland prior needs — **CanPeat** peat profiles
> (`projects/north-star-project-470316/assets/peat_profiles`) and **WoSIS**
> (`projects/north-star-project-470316/assets/wosis_layers_canada`) — alongside the Sothe
> national soil carbon layer. The peatland prior source is already wired in; it just needs
> filtering to organic soils and summarising over an area of interest.

---

## In the meantime

You do not need Earth Engine to plan a campaign. Everything the tool computes is set out
longhand in [**Part 2, Appendix A**](../README.md#appendix-a--a-brief-lesson-in-sampling-logic),
and the depth survey — which matters more than the sample-size formula in a peatland — needs
nothing but a probe and a tape.
