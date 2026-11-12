# Worked Example

[← Back to the main guide](../README.md)

---

Here we will show hypothetical examples for 2 different project:

| Part | Example | Data |
|---|---|---|
| **Planning and field practice** ([Parts 2](../02_Project_Planning/) and [3](../03_Field_Methods/)) | A team planning a baseline survey of the eelgrass at **Tsawwassen, BC** | ⚠️ **Constructed for teaching.** The site, boundary and zones come from a real run of the sampling tool; the team, its cores and its field records do not exist |
| **Analysis** ([Part 4](../04_Results/)) | Three eelgrass cores from the **Cowichan Estuary, BC**, followed from lab results to both analysis options | **Published measurements** (Douglas et al. 2022, via Janousek et al. 2025, CC BY 4.0), with **reconstructed** dry weights and **illustrative** lab details. The Option B area is a **hypothetical** boundary drawn for teaching |

The idea is simple: **work alongside these examples, and apply the blank templates to your own
site.**

| You want… | Use this |
|---|---|
| A completed planning example | [`02_Project_Planning.md`](02_Project_Planning.md) |
| A completed digital data sheet | [`04_Data_Interpretation/files/Eelgrass_Carbon_DigitalData_Example.xlsx`](../resources.md#pending-materials) |
| What a lab results sheet looks like | [`04_Data_Interpretation/files/Example_Lab_Results.xlsx`](../resources.md#pending-materials) |
| A blank data sheet to fill in | [`04_Data_Interpretation/files/Eelgrass_Carbon_DigitalData_BlankSheet.xlsx`](../resources.md#pending-materials) |
| A blank sampling calculator | [`02_Project_Planning/`](../02_Project_Planning/) |
| The analysis workflow (reusable) | [`04_Data_Interpretation/DataAnalysisWorkflow/`](../resources.md#pending-materials) |

---

## The thread, end to end

1. **Plan** ([Part 2](../02_Project_Planning/), [walkthrough](02_Project_Planning.md)) — the
   Tsawwassen team turns its question into a reporting depth, strata, a sample size and a set of
   coordinates.
2. **Collect** ([Part 3](../03_Field_Methods/)) — the field data sheet; its filled-in example
   uses the Tsawwassen core `WWF-01-A`.
3. **Analyse** ([Part 4](../04_Results/)) — the Cowichan cores in the digital data
   sheet, checked, turned into core stocks, and taken through Option A and Option B:

   ```r
   source("run_option_A.R")   # from 04_Data_Interpretation/DataAnalysisWorkflow/
   source("run_option_B.R")
   ```

## Headline results (Cowichan)

| | Result |
|---|---|
| Organic carbon stock, 0–15 cm, per core (measured) | **17.1, 12.1 and 14.5 Mg C/ha** |
| Against 53 published eelgrass cores from 8 BC and Washington estuaries | 77th–87th percentile |
| Option B, **hypothetical** 6.6 ha boundary, exploratory design — measured headline | **14.6 Mg C/ha in the top 15 cm, about 96 Mg C — all measured**. No interval: the cores were not placed at random |
| Option B — deeper scenario, clearly labelled | 0–30 cm: about 34 Mg C/ha, of which 38 % is estimated below the 20 cm cores. 0–50 and 0–100 cm are not reported — the cores are too short |

The cores stop at 20 cm, so anything deeper is part estimate, and the report says how much. A
**synthetic** stratified survey in the workflow shows what a probability design adds: an
interval, and explicit handling of an unsampled stratum.

## What's here

- **[`02_Project_Planning.md`](02_Project_Planning.md)** — the planning walkthrough: how the
  Tsawwassen team went from a carbon question to a target sample size and a set of coordinates,
  step by step. Constructed teaching data.
- **[`archive/`](archive/)** — the earlier Tsawwassen analysis walkthrough and data sheet, built on
  constructed cores and the earlier pipeline. Kept for reference only.
