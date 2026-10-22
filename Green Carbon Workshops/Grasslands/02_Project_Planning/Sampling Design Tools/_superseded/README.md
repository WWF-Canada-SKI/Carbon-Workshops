# Superseded

`ForestSamplingTool_GEE.js` was copied in from the Forests workshop as a stand-in while no
grassland tool existed. It is kept for reference only.

**Do not use it to size a grassland campaign.** Three things in it do not match this workshop:

| | |
|---|---|
| **Priors** | Forest carbon values, not grassland |
| **Plot footprint** | 400 m², the tree plot — not the soil/root sampling unit |
| **Pools** | One pool. It has no concept of sizing soil and roots separately, which is the central design decision in [Part 2 Step 4](../../#step-4--decide-how-many-plots-and-samples) |

The grassland replacement is [`GrasslandSamplingTool_GEE.js`](../GrasslandSamplingTool_GEE.js). The [Sample Allocation Calculator](../grassland-sample-allocation.xlsx) and the
[Sample Size Explorer](../index.html) instead.
