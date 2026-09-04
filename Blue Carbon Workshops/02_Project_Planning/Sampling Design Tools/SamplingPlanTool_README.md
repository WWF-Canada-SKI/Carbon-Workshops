# Blue Carbon Sampling Design Tool

**WWF-Canada · Coastal Blue Carbon Hub · v2026.1**

A Google Earth Engine app that turns a site boundary and a precision target into a list of core locations you can take into the field.

It is the companion to **Part 2 (Project Planning)** of the Blue Carbon Eelgrass Workshop. Every number it reports also appears in the workshop's Sample Allocation Calculator, and the built-in self-test checks that the two agree.

---

## What it does

You tell it where you are working, whether the site is all one thing, what you are measuring, and how precise you need to be. It tells you how many cores you need, how to split them between zones, exactly where to put them, and writes the methods paragraph for your report.

It replaces three earlier single-purpose tools, because zone definition and core layout are handled independently — any way of defining zones combines with any layout.

---

## Getting started

1. Open the [Earth Engine Code Editor](https://code.earthengine.google.com/) and sign in with an account that has a registered Cloud project.
2. Paste the whole script into a new file and press **Run**.
3. The app appears in the left panel; the map is on the right.

The script is a single file with no external assets, so nothing needs to be installed.

To check the maths before you trust it, set `RUN_SELF_TEST = true` (line 1) and press Run. About 100 checks print to the Console, including the full sensitivity grid from the workshop workbook. Set it to `false` for the released app.

To check the Earth Engine side (area, clustering, buffers against real geometry), set `RUN_EE_TEST = true`. Those need a live connection, so results arrive one at a time.

---

## The six steps

### Step 1 · Where are you working?

Draw a polygon on the map, or point at a boundary already saved as an Earth Engine asset (`users/you/your_site`).

Press **Measure this site**. You get the area in hectares and the number of possible core positions, which is simply the area divided by the plot size.

Area is measured from the geometry itself, not by counting pixels, so it is correct at any site size. The tool then picks an analysis scale from 10, 20, 30, 50, 100 or 250 m, aiming for roughly 5,000 pixels across the site, and warns you if the site is small enough that areas will be approximate.

### Step 2 · Is the site all one thing?

If part of the site is denser, deeper, or under different management, split it into zones now. Splitting by something that actually drives carbon gives a tighter answer for the same number of cores.

Options, in order of how much control you keep:

| Option | What it does |
|---|---|
| **No — treat it as one area** | Skip zoning entirely. |
| **Draw them by hand** | Name a zone, draw it, add it, repeat. Best when you already know the site. |
| **Upload my own boundaries** | An Earth Engine asset with one polygon per zone and a column naming each. Several polygons can share a zone name; their areas are added together. |
| **Land cover (Dynamic World, 10 m)** | Reads the cover types present inside your boundary; you tick the ones to keep and rename them. |
| **Land cover (Copernicus, 100 m)** | Same, at 100 m. Only offered on larger sites. |
| **Satellite imagery grouping (30 m)** | Unsupervised k-means on a Sentinel-2 composite plus NDVI, NDWI and elevation. |
| **Satellite Embeddings grouping (10 m)** | Unsupervised k-means on the 64-band annual embedding. The default for small sites — a 5 ha meadow still holds about 500 pixels. |

Options that cannot resolve a site of your size are hidden, with a note saying why. On a 5 ha meadow, for example, the 100 m and 30 m sources drop out and only the 10 m ones remain.

For the automatic methods, a slider sets how many groups to look for (2–6).

Once zones are built you get a checklist. **Untick anything you are not sampling** — deep water, bare flat, land. Cores are shared out only among the zones you keep, and the area of the rest drops out of the calculation. If the zones cover less than 95% of your boundary, the tool says so.

### Step 3 · What are you measuring?

Choose the ecosystem — **eelgrass, salt marsh, tidal swamp or tideflat** — and the depth, **top 30 cm** or **full metre**. Mangrove is not offered because it does not occur north of California.

Then choose where the expected variability comes from:

- **Use the published regional average.** Pacific Northwest values (Alaska, British Columbia, Washington, Oregon) computed from core-level data in Janousek et al. (2025), so the standard deviation is the real spread between cores rather than a spread of published means. California and south are excluded — stocks there behave differently. Priors backed by fewer than 20 cores are flagged as indicative; a CV above 0.80 gets a warning that the campaign will be unusually large. Tideflat at 100 cm refuses to return a number rather than guessing from 9 cores.
- **I have my own data from this site.** Enter a mean and a between-core standard deviation from a pilot, an earlier survey, or nearby cores. This beats any regional figure, because local variability is what actually sets the core count. If your CV comes in below 0.15 the tool asks you to check you have entered a standard deviation and not a standard error.

Variability drives the core count more than anything else you choose in this app.

### Step 4 · How precise do you need to be?

Decide this before you see the answer, not after.

- **Margin of error:** within 10% (demanding), 20% (usual for coastal MMRV), or 30% (a first look).
- **Confidence:** 80%, 90% (usual), or 95%.
- **Allocation, when the site has zones:** split cores by zone area (proportional), or send more cores to patchier zones (Neyman).

The allocation choice drives both the sample-size formula and the split between zones. They are not mixed — sizing with one and splitting with the other under-samples, which is the error in the earlier tools.

You get the total core count, the per-zone breakdown, and a comparison line showing what 10%, 20% and 30% would each cost. Every zone gets at least 5 cores, and the campaign as a whole never drops below 5: with fewer, there is no standard deviation to work with, so the precision you actually achieved can never be checked afterwards.

The design is then checked for feasibility before any points are generated. Problems stop you and name the fix — a zone too small to hold its minimum, more cores than can physically fit at 10 m spacing, a site smaller than a single plot. Warnings let you continue but tell you what to expect.

Tick **Show the working** for the formula, the z value, N, CV and E, and a link to Appendix A.

### Step 5 · Where do the cores go?

| Layout | What it does |
|---|---|
| **Random** | Cores scattered at random. The default when a zone looks uniform. |
| **Even grid** | A regular lattice at `sqrt(area / n)` spacing, centred in the zone with a small deterministic jitter. Guarantees even coverage. |
| **Shore-parallel transects** | Lines following the long axis of the zone. Recommended for eelgrass. Set the number of lines (2–10). If the zone is nearly as wide as it is long it has no meaningful long axis, and the tool says so instead of picking one — enter a shoreline bearing yourself, or use the grid. You can supply a bearing at any time to override the axis. |
| **Composite plots** | Clusters of 3–10 subsamples pooled into one lab analysis. Fewer analyses, at the cost of losing within-plot variability. |

Whatever the layout, no two cores end up closer than 10 m — one plot width. Two cores 3 m apart both claim the same 100 m² plot, which is one observation counted twice. Points are oversampled, then thinned in a fixed order so the same seed always reproduces the same design.

Each zone also gets an inward edge buffer, chosen from 50, 25, 10 or 0 m: the largest buffer that still keeps 60% of the zone and leaves room for the cores. On raster and uploaded zones the buffer is re-checked against the real polygon, because a long thin fringe loses far more to a buffer than a compact shape does.

If a zone is too full to place everything at spacing, you are told how many did fit and why.

### Step 6 · Take it to the field

Download the core locations as **CSV, GeoJSON, KML or SHP**. Each point carries `core_id`, zone, layout, plot size, coordinates, and composite/subsample numbers where relevant — enough for a reviewer to reconstruct the design from the file alone.

Below the download you get a **methods paragraph** to paste into your report, naming the sample size, the formula, the precision target, where the variability figure came from, and the minimum spacing.

---

## Defaults

Set in `CONFIG` at the top of the script.

| Setting | Default | Why |
|---|---|---|
| Plot size | 100 m² (10 × 10 m) | Each core represents a plot, not a point (Appendix A3) |
| Confidence | 90% | Workshop Step 4 |
| Margin of error | 20% | Usual for coastal MMRV |
| Minimum cores per zone | 5 | Appendix A7 |
| Allocation | Proportional | |
| Ecosystem / depth | Eelgrass / 30 cm | |
| Seed | 42 | Change it for a different but equally valid design |

Change the seed and you get a different random draw; keep it and the design is exactly reproducible.

---

## How it is put together

| Section | Contents |
|---|---|
| 0 | Configuration and links to the workshop materials |
| 1 | `BCStats` — every number the tool reports originates here |
| 2 | `BCGeom` — analysis scale, spacing, buffers, feasibility |
| 3 | `BCTest` — self-test, pure JavaScript, no Earth Engine calls |
| 5 | `BCEarth` — everything touching Earth Engine |
| 6 | `BCLayout` (pure geometry) and `BCPlace` (Earth Engine wrappers) |
| 7 | The interface |

Sections 1 and 2 hold all the statistics and all the thresholds. Sections 5, 6 and 7 ask them for those values and do no arithmetic of their own, so the app and the workbook cannot drift apart. Sections 1, 2 and 6A run as plain JavaScript outside Earth Engine, which is what makes the self-test instant.

Sample size follows Cochran's formula with a finite-population correction. The inverse normal is Acklam's algorithm (relative error below 1.15e-9), not a polynomial approximation.

---

## Known limits

- **Priors are Pacific Northwest only.** Using them on an Atlantic or Arctic site is not defensible. Enter your own pilot data instead.
- **A regional average understates how patchy any single site is.** If your cores come back more variable than the prior, that is expected — recompute your achieved precision from the collected cores before reporting the estimate.
- **The long axis is a proxy for the shoreline,** not a coastline. On a complex shore, supply the bearing.
- **Analysis scale never goes finer than 10 m** (Sentinel-2). On sites under about 1 ha, zone areas are approximate.
- **Achieved precision is not the design precision.** Steps 1–5 size the campaign; Appendix A8 checks whether you hit the target once the cores are in.

---

## Citation

Janousek, C.N., Krause, J.R., Drexler, J.Z., Buffington, K.J., Poppe, K.L., Peck, E., et al. (2025). Blue carbon stocks along the Pacific coast of North America are mainly driven by local rather than regional factors. *Global Biogeochemical Cycles*, 39, e2024GB008239.

## Workshop materials

- Planning guide (Part 2)
- Sample allocation calculator (`BlueCarbon_SampleAllocation_2026.xlsx`)
- Appendix A — the maths behind this
- Coastal Blue Carbon Field Guide
- Field datasheets
- Worked example

Links are set in `CONFIG.REPO` and `CONFIG.LINKS`.
