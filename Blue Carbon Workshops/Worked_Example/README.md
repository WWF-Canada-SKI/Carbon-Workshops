# Worked Example

[← Back to the main guide](../README.md)

---

Here we will show hypothetical examples for 2 different project:

| Part | Example | Data |
|---|---|---|
| **Planning and field practice** ([Parts 2](../02_Project_Planning/) and [3](../03_Field_Methods/)) | A team planning a baseline survey of the eelgrass at **Tsawwassen, BC** | ⚠️ **Constructed for teaching.** The site, boundary and zones come from a real run of the sampling tool; the team, its cores and its field records do not exist |
| **Analysis** ([Part 4](../04_Results/#community-analysis-mapping-and-reporting)) | The **Boundary Bay** community analysis example, from the completed sediment data sheet to stock estimates, maps and a Quarto report | **Simulated measurements** for 12 cores and 120 sediment sections across two zones |

The idea is simple: **work alongside these examples, and apply the blank templates to your own
site.**

| You want… | Use this |
|---|---|
| A completed planning example | [`02_Project_Planning.md`](02_Project_Planning.md) |
| A completed digital data sheet | [Community analysis example workbook](https://github.com/CathalD/BlueCarbon_Community_Carbon_Analysis_Mapping/blob/main/data/field/blue_carbon_field_cores.xlsm) |
| What a lab results sheet looks like | [`04_Data_Interpretation/files/Example_Lab_Results.xlsx`](../resources.md#pending-materials) |
| A blank data sheet to fill in | [`04_Data_Interpretation/files/Eelgrass_Carbon_DigitalData_BlankSheet.xlsx`](../resources.md#pending-materials) |
| A blank sampling calculator | [`02_Project_Planning/`](../02_Project_Planning/) |
| The analysis workflow (reusable) | [Download and run the workshop in R](../04_Results/#run-the-analysis-and-explore-the-maps-in-r) |

---

## The thread, end to end

1. **Plan** ([Part 2](../02_Project_Planning/), [walkthrough](02_Project_Planning.md)) — the
   Tsawwassen team turns its question into a reporting depth, strata, a sample size and a set of
   coordinates.
2. **Collect** ([Part 3](../03_Field_Methods/)) — the field data sheet; its filled-in example
   uses the Tsawwassen core `WWF-01-A`.
3. **Analyse** ([Part 4](../04_Results/#community-analysis-mapping-and-reporting)) — use the
   Boundary Bay workbook for this separate exercise. Download the materials in R with
   `usethis::use_course()`, then run `source("Run_and_Visualize.R")` from the downloaded
   folder. The runner produces core stock tables, maps and `Blue_Carbon_Report.html`.

## Headline results for Boundary Bay

These stock estimates use simulated sediment measurements.

| Depth | Mean stock across the 12 cores |
|---|---:|
| 0–30 cm | 2.96 kg C/m² |
| 0–50 cm | 4.81 kg C/m² |
| 0–100 cm | 8.84 kg C/m² |

Open the 0–30 cm transfer map with `view_map(30, "transfer")` and compare the
Janousek prior, local Matérn correction and updated estimate. These layers show
how the reference data provide a starting point and how the workshop cores
change it across the study area. The optional [Gaussian process walkthrough](../04_Results/#how-the-gaussian-process-maps-work)
explains the calculation.

## What's here

- **[`02_Project_Planning.md`](02_Project_Planning.md)** — the planning walkthrough: how the
  Tsawwassen team went from a carbon question to a target sample size and a set of coordinates,
  step by step. Constructed teaching data.
- **[`archive/`](archive/)** — the earlier Tsawwassen analysis walkthrough and data sheet, built on
  constructed cores and the earlier pipeline. Kept for reference only.
