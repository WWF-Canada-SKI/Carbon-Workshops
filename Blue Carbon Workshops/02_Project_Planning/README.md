<p align="center">
  <img src="images/banner_planning.svg" alt="Project Planning — Blue Carbon Eelgrass Workshop banner" width="100%">
</p>

---

[← 1 — Background](../01_Background/) · [Back to main guide](../README.md) · Next: [3 — Field Methods →](../03_Field_Methods/)

---

# Part 2 — Project Planning
## From a carbon question to a sampling design

**Quick links:** [Sampling Design Guide](Sampling-Design-Eng-2026.pdf) · [Sample Allocation Calculator](BlueCarbon_SampleAllocation_Spreadsheet_V2.xlsx) · [Calculator — Google Sheets copy](https://docs.google.com/spreadsheets/d/1TGLz11ZmWO2EsAF86PMbEYZFO75_X_pKdJPS38a0O-M/edit?usp=sharing) · [Blue Carbon Hub tool](https://blue-carbon-hub.projects.earthengine.app/) · [Coastal Blue Carbon Field Guide](../Coastal-Blue-Carbon-Field-Guide-FINAL.pdf) · [Appendix A — sampling logic](#appendix-a--a-brief-lesson-in-sampling-logic)

---

**Before collecting sediment cores**, four questions are worth addressing:

1. **What do I want to know?** Am I interested in collecting baseline data? Making a comparison between different management types? Tracking restoration success? All of the above?
2. **Where does that question apply?** The whole ecosystem, just the eelgrass, high meadow vs low?
3. **How much data do I need?** How many samples is enough? What is our capacity to meet this?
4. **Where should the samples be collected from?**

Answering these is what a **sampling design** aims to achieve. It turns a carbon question into a field plan: a number of cores, and a set of sampling coordinates.

This section covers the five steps of a sampling design.

| # | Step | Answers |
|---|------|---------|
| 1 | **Define the study area** | *Where, roughly, am I working?* |
| 2 | **Stratify** (optional) | *Does the site split into distinct areas?* |
| 3 | **Choose the carbon pool** | *Water, plant, or sediment?* |
| 4 | **Determine how many samples** | *How many cores meet my goal?* |
| 5 | **Determine where they go** | *Exactly where do I core?* |

> The methods here follow WWF-Canada's [Sampling Design guide](Sampling-Design-Eng-2026.pdf) and the sampling guidance in the [Howard et al. Blue Carbon Manual](https://www.thebluecarboninitiative.org/manual) (see [Section 1](../01_Background/)).

**Two companion tools** appear throughout:

<table>
<tr>
<td width="50%">

**🗺 [Blue Carbon Hub sampling-design app](https://blue-carbon-hub.projects.earthengine.app/view/blue-carbon-sampling-plan-tool)**  A spatial tool; draw your boundary, stratify it, place your samples on a map.

*Used in Steps 1, 2 and 5.*

</td>
<td width="50%">

**📄 [Sample Allocation Calculator](BlueCarbon_SampleAllocation_Spreadsheet_V2.xlsx)** A simple spreadsheet for estimating sample size.

*Used in Step 4.*

</td>
</tr>
</table>

If you want to know how the calculator returns the number it does and dive deeper into the math behind the tools, look to [**Appendix A**](#appendix-a--a-brief-lesson-in-sampling-logic), at the bottom of this page, where we go through how sample size is estimated before sampling, and how to check whether the sampling met your goals afterwards.

---

## Background: What sampling is, and why it works

Measuring every square metre of an entire ecosystem isn't always feasible. So we measure a **small portion** of it and use that to estimate the whole. Because an estimate built from a portion will never be exactly right every single time, we also want to know the probability that the estimate reflects the actual value. This is called **probability-based sampling**.

<table>
<tr>
<td width="60%">

<img width="100%" alt="What is sampling? — probability-based sampling explainer" src="https://github.com/user-attachments/assets/0c8db857-b05b-4969-936c-711d563e1978">

</td>
<td width="40%">

**Sampling** = taking a small portion of a thing to make an informed estimate of the whole.

A **sampling design** is the framework for choosing *what* and *where* to sample by dividing the study area into sites and plots, measuring those, and combining them into an estimate for the full area.

</td>
</tr>
</table>

The more samples you take, the closer your estimate is likely to be to the true value. Because you don't measure everything, every estimate carries uncertainty, which is why you will usually see a result reported in **three parts**:

| Component | | What it tells you |
|---|---|---|
| **Estimate** | $\bar{x}$ | The average carbon value across your sampled plots. |
| **Confidence level** | $1-\alpha$ | How often this procedure would capture the true value if repeated. At 95% confidence, about 95 out of every 100 samples would fall within this range of values. |
| **Margin of error** | $E$ | How precise that estimate is, or in words, the distance from the estimate to the edge of the interval, usually given relative to the mean (e.g. ±10%). |

> Put together: *"mean carbon = 100 ±10, at 95% confidence."*

### Seeing it on a map

These clips come from the **[Sample Size Visualization Tool](https://blue-carbon-hub.projects.earthengine.app/)**.

<table>
<tr>
<td width="60%">

<img width="100%" alt="Sample Allocation Visualizer — revealing the true carbon map as samples accumulate" src="images/download%20(2).gif">

</td>
<td width="40%">

The bottom-left map is a hypothetical carbon map, where each square is the carbon value at that location. Switch between the **True value** and the **Revealed** view to watch the map uncover itself one sample at a time.

</td>
</tr>
</table>

<table>
<tr>
<td width="60%">

<img width="100%" alt="Sample Allocation Visualizer — estimate converging on the true value as sample size grows" src="images/download%20(3).gif">

</td>
<td width="40%">

On the right, we see how each sample on the map is combined together to estimate the **true value** (dashed blue line). With a few samples the estimate is off and the error range (purple) is wide. As samples accumulate, it narrows.

**That purple band is your margin of error** — watch it shrink as the number of samples grows.

</td>
</tr>
</table>

### The takeaway

- Sampling estimates what's impractical to measure directly.
- The same process that produces an estimate can also tell you whether differences *within* or *between* sites are statistically significant.
- And it runs **backwards**: fix the precision you want, and it returns the number of cores needed to get there. That's Step 4, see [Appendix A2](#a2--working-backwards-from-precision-to-sample-size).

---

# Implementing a sampling design

<details>
<summary><b>📊 Meet the team at Tsawwassen Beach</b> &nbsp;·&nbsp; <i>the worked example, in brief</i></summary>

<br>

These drop-down menus contain brief descriptions from a hypothetical worked example. If you want to see how each of these steps can be applied, find them here or in the **→ [Worked Example](../Worked_Example/) folder**.

A team of four in B.C. is gathering **baseline carbon data in the Tsawwassen Beach eelgrass meadows**, before protection and restoration measures go in.

They want to gather information on two specific things:

**A)** the **average carbon stock** across the meadow, and

**B)** the ability to **compare** areas of the meadow against each other, and against future surveys.

Both need the same thing first: a sampling design. They appear at every step below.

**→ [Full planning walkthrough](../Worked_Example/02_Project_Planning.md)** · **→ [The whole project](../Worked_Example/)**

</details>

## Step 1 — Define your study area

*Where, roughly, am I working?*

Every carbon value you produce from collecting cores is reported **per unit area**, so the boundary of the area in this step is what turns a carbon *density* into a carbon *total*. It also sets $N$, the number of possible plot locations, which will determine how many plots to set up to meet your desired goals.

<table>
<tr>
<td width="45%">

<img width="100%" alt="Study area boundary — example" src="https://github.com/user-attachments/assets/68df05eb-c707-4cab-ab86-ec5117165b06">

</td>
<td width="55%">

The boundary can be a simple polygon drawn on a map, or a pre-defined area if one already exists for your site.

If you run transects, or already know the general area you're interested in, a simple estimate of the area is enough.

</td>
</tr>
</table>

<details>
<summary><b>📊 Worked example</b> &nbsp;·&nbsp; <i>how the Tsawwassen team defined their area</i></summary>

<br>

They opened the sampling-design tool and traced what they could see on recent imagery — a **5 ha inlet (50,000 m²)** they knew was mostly eelgrass. They did not survey the edge.

<img width="60%" alt="Drawing a study area boundary in Google Earth Engine" src="images/download%20(5).gif">

</details>

### 🛠 Your turn

<table>
<tr>
<td width="45%">

<img width="100%" alt="Drawing a study area boundary in Google Earth Engine" src="images/download%20(4).gif">

</td>
<td width="55%">

**Tool: [Blue Carbon Hub sampling-design app](https://blue-carbon-hub.projects.earthengine.app/view/blue-carbon-sampling-plan-tool)**

Draw a simple polygon over your area of interest — in the tool, in Google Earth Engine, or in whatever GIS you already use. Or import a pre-defined boundary if one exists.

Read the **area in m²** off the tool and write it down.

</td>
</tr>
</table>

> [!TIP]
> **✅ Before moving on, you should have:**
> - A boundary polygon (or a sketched area on a map)
> - Its **total area in m²** (Step 4 — Sample Allocation needs this number)

---

## Step 2 — Stratify your site *(optional)*

*Does the site split into distinct areas?*

When we measure carbon stock, we measure at a point and extrapolate this across a larger area, so the more that area resembles where we sampled, the more accurate the estimate will be. You wouldn't use a core from an eelgrass meadow to estimate carbon in an upland marsh, or vice versa. Splitting the two gives better numbers from the same effort.

<table>
<tr>
<td width="45%">

<img width="100%" alt="Stratification example — slide" src="https://github.com/user-attachments/assets/0aec62d8-db94-4ca2-8962-96d74799d016">

</td>
<td width="55%">

**Stratification** divides the study area into distinct sub-areas, so data collected in one is only applied within that one.

Beyond separating ecosystems, strata let you compare things deliberately: management techniques, restoration years, dense vs sparse meadow, depth zones.

Strata can be drawn by hand or derived from remote sensing.

</td>
</tr>
</table>

<details>
<summary><b>📊 Worked example</b> &nbsp;·&nbsp; <i>how the Tsawwassen team split their inlet</i></summary>

<br>

They split the 5 ha inlet into **two strata** — a denser central meadow and a sparser fringe — because density was the most obvious driver of variation on the imagery, and because their second question (B: comparing areas of the meadow) required the split to exist before fieldwork, not after.

</details>

### 🛠 Your turn

<table>
<tr>
<td width="45%">

<img width="100%" alt="Blue Carbon Stratified Sampling Tool — drawing and stratifying a study area" src="images/Screenshot%202026-07-21%20at%2010.46.13.png">

</td>
<td width="55%">

**Tool: [Blue Carbon Hub sampling-design app](https://blue-carbon-hub.projects.earthengine.app/)**

Take the boundary from Step 1 and either run the **automatic stratification**, or draw your strata by hand.

Record the **area in m² of each stratum** — Step 4 uses these to divide the cores between them.

> 🎥

</td>
</tr>
</table>

> [!TIP]
> **✅ Before moving on, you should have** either:
> - **One** area containing a single ecosystem type, **or**
> - **Multiple** boundaries containing distinct ecosystems, management areas, or anything else you want to compare
>
> Plus the **area in m² of each**.

---

## Step 3 — Choose what to measure

*Water, plant, or sediment carbon?*

<table>
<tr>
<td width="45%">

<img width="100%" alt="Carbon pools — slide" src="https://github.com/user-attachments/assets/a7ea0100-6160-4498-a282-5d44db722a59">

</td>
<td width="55%">

Carbon in a coastal ecosystem sits in several **pools**, such as the water column, the living plants, and the sediments.

For an eelgrass carbon project, the pool that matters most is the **sediment**. It holds the overwhelming majority of the carbon, and it's the pool that persists for a long time.

</td>
</tr>
</table>

<details>
<summary><b>📊 Worked example</b> &nbsp;·&nbsp; <i>what the Tsawwassen team chose</i></summary>

<br>

**Sediment**, cored **to refusal** rather than to a fixed depth so each core captures the full accumulated profile at that location.

</details>

### 🛠 Your turn

<table>
<tr>
<td width="45%">

> 📸 **[SCREENSHOT NEEDED]** — the carbon-pool selection, or a sediment core with its depth interval labelled.

</td>
<td width="55%">

See [Section 3 — Field Methods](../03_Field_Methods/) for how to measure expected sediment depth with a metal rod

or watch this video

> 🎥 *[VIDEO — "Site Selection and Required Materials"]* · [workshop playlist](https://www.youtube.com/playlist?list=PLLsjpJMfNDP5w78ZJNDUvMj1VoRG_qSwd)

</td>
</tr>
</table>

> [!TIP]
> **✅ Before moving on, you should have:**
> - The **carbon pool** you're measuring, written down
> - A **target core depth**, or a decision to core to refusal

---

## Step 4 — Decide how many samples

*How many cores meet my project goal?*

This is the step that sets how many samples are required to meet your goals. Too few cores and your estimate carries too much uncertainty to make confident decisions. Too many and you spend resources collecting data you didn't need, which could have gone towards other efforts.

To get there, you define three things, and the calculator returns an estimate of the number of samples.

| You provide | Meaning | Typical |
|---|---|---|
| **Area** (m²) | How big the boundary is, in square metres | derived from Step 1 |
| **Margin of error** ($E$) | How precise you need the estimate to be | ±10% or ±20% |
| **Confidence level** | How reliable that interval has to be | 80% or 90% |
| **A variability prior** *(optional)* | Roughly how much carbon is there, and how patchy | a pilot study, or regional values — see below |

### Where the prior comes from

The calculator needs a rough idea of how much carbon is there and how variable it is *before* you've measured anything. That's a **prior**, a rough estimate to start from.

Two sources, in order of preference:

| | Source | Use when |
|---|---|---|
| **1** | **A pilot study** — mean and standard deviation from a handful of your own cores, an earlier survey, or nearby sites | You can get a few cores before from a pilot study or from nearby locations. This is the better option: local variability is what actually drives sample size. |
| **2** | **Regional values** — published stocks from comparable ecosystems. By default we use the regional averages for coastal blue carbon ecosystems reported in Janousek et al. (2025) | You have no prior site data to go off. |

> [!NOTE]
> The sample design tool uses open coastal blue carbon data for the Pacific Northwest from:
> Janousek, C. N., Krause, J. R., Drexler, J. Z., Buffington, K. J., Poppe, K. L., Peck, E., et al. (2025). Blue carbon stocks along the Pacific coast of North America are mainly driven by local rather than regional factors. *Global Biogeochemical Cycles*, 39, e2024GB008239. [doi:10.1029/2024GB008239](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024GB008239)

<details>
<summary><b>📊 Worked example</b> &nbsp;·&nbsp; <i>what the Tsawwassen team calculated</i></summary>

<br>

<table>
<tr>
<td width="45%">

> **[SCREENSHOT NEEDED]**

</td>
<td width="55%">

**Their inputs:**

- **Total area** (Step 1) — 50,000 m² → at 100 m² per plot, $N$ = **500** possible plots
- **Confidence level** — 90% ($z = 1.645$)
- **Margin of error** — ±20% ($E = 0.20$)
- **Prior mean and SD** — ≈ 120 Mg C ha⁻¹, SD ≈ 60, from Janousek et al. (2025) → $CV = 0.5$

**Result: 23 cores.**

</td>
</tr>
</table>

</details>

### 🛠 Your turn

You can use the **📄 [Sample Allocation Calculator](BlueCarbon_SampleAllocation_Spreadsheet_V2.xlsx)**, or stick with the spatial tool in the **🗺 [Blue Carbon Hub app library](https://blue-carbon-hub.projects.earthengine.app/view/blue-carbon-sampling-plan-tool)**.

<table>
<tr>
<td width="45%">

<img width="100%" alt="Sample allocation calculator — basic inputs" src="https://github.com/user-attachments/assets/080e16d2-3be6-4da8-a0d1-bb4154c82e96">

</td>
<td width="55%">

Enter an area, a margin of error, and a confidence level; the sheet returns the number of plots.

This is the **Sample Allocation Calculator** named in Step 3 of the [Sampling Design guide](Sampling-Design-Eng-2026.pdf) (p.16), which uses the central limit theorem to estimate the minimum number of plots needed to hit a target precision for a large area.

**Sheet 1** returns the total *n* for the whole study area. **Sheet 2** splits that *n* across the strata from Step 2, proportional to area — used in Step 5.

</td>
</tr>
</table>

**The two tools will not always agree.** For the Tsawwassen inlet the spreadsheet returned **17** samples, while the spatial tool suggested **23**. The difference comes from the spatial tool having more information about the site: here it accounted for the two stratified areas, so it could allocate cores between them rather than treating the meadow as uniform. More information about a site generally means a more efficient design.

The quickest way to build intuition is to open the calculator — or the [Blue Carbon Hub visualizer](https://blue-carbon-hub.projects.earthengine.app/) — and change **one knob at a time**, watching *n* respond. [Appendix A4](#a4--what-actually-drives-sample-size) has the full comparison if you'd rather read it than run it.


> [!TIP]
> **✅ Before moving on, you should have:**
> - A **target margin of error** and **confidence level** you can justify
> - A **prior** for mean carbon and its variability, and a note of where it came from
> - A **required number of cores** from the calculator or the spatial tool
>
> After the field season, you'll come back and check whether you actually hit that precision target — see [Appendix A8](#a8--after-the-campaign-did-you-hit-your-target).

---

## Step 5 — Decide where the samples go

*Exactly where do I core?*

<table>
<tr>
<td width="45%">

<img width="100%" alt="Sampling strategies — slide" src="https://github.com/user-attachments/assets/a2d13fda-6c63-417d-aad6-b506be50a59d">

</td>
<td width="55%">

There are four common strategies for distributing samples. Which one fits depends on how much you already know about the site.

</td>
</tr>
</table>

| Strategy | When to use it |
|---|---|
| **Random** | Plots placed randomly across the study area. Random is typically the default when the area is uniform or there's no prior data. |
| **Systematic** | Plots at regular intervals. This method guarantees even coverage, but is most appropriate when you know the variation across the site is quite even. |
| **Stratified-random** | Strata first, then plots randomly assigned within each. This is the most accurate and cost-effective strategy. |
| **Convenience/practical** | Plots wherever is accessible. While not statistically rigorous, it is useful for a low-cost initial assessment. |

> See WWF-Canada, *[Measuring Carbon in Coastal Sediments](../Coastal-Blue-Carbon-Field-Guide-FINAL.pdf)* (2026), p.6.

### How does the total split across a boundary that has been stratified?

Each stratum gets a share of *n* **proportional to its area**, so a stratum covering half the meadow gets roughly half the cores.

More details of the allocation formula can be found in [Appendix A7](#a7--proportional-allocation-across-strata).

### For eelgrass specifically

<table>
<tr>
<td width="45%">

<img width="100%" alt="Eelgrass-specific sampling considerations — slide" src="https://github.com/user-attachments/assets/d5d1f4f8-7040-434c-8a72-41f3a88cec09">

</td>
<td width="55%">

Eelgrass varies differently *parallel* to shore than *perpendicular* to it — depth, exposure and sediment all change as you move offshore.

The field guide therefore recommends transects that **run parallel to the shoreline**, aligned with sediment depth, with a random or probability-based grid within each site and at least two replicates per site.

</td>
</tr>
</table>

<details>
<summary><b>📊 Worked example</b> &nbsp;·&nbsp; <i>where the Tsawwassen cores went</i></summary>

<br>

Their **23** cores were allocated across the two strata **proportionally by area**, with the 5-core minimum applied. Locations were generated as shoreline-parallel transects within each stratum and exported as coordinates for the field team.

**→ [See how they got there](../Worked_Example/02_Project_Planning.md)**

</details>

### 🛠 Your turn

<table>
<tr>
<td width="45%">

<img width="100%" alt="Blue Carbon Hub sampling-design tool — stratified sample allocation results" src="images/Screenshot%202026-07-21%20at%2010.47.16.png">

</td>
<td width="55%">

**Tool: [Blue Carbon Hub sampling-design app](https://blue-carbon-hub.projects.earthengine.app/)**

Feed it your strata from Step 2 and your *n* from Step 4. It allocates the cores between strata and generates sampling locations you can export and load onto a GPS.

**Source code:** [WWF-Canada-SKI/Carbon-Measurement — Sampling Design Tools](https://github.com/WWF-Canada-SKI/Carbon-Measurement/tree/main/Blue%20Carbon/Sampling%20Design%20Tools)

</td>
</tr>
</table>

> [!TIP]
> **✅ Before moving on, you should have:**
> - A **sampling strategy** chosen and justified
> - A **per-stratum core allocation**
> - A **coordinate list** of sampling locations, exported and loadable onto a GPS

---

## ✅ Sampling design complete

Before heading into the field, check you can answer all six:

```
  ☑  Study area boundary defined            → Step 1
  ☑  Strata identified (or ruled out)       → Step 2
  ☑  Carbon pool selected                   → Step 3
  ☑  Sample size calculated                 → Step 4
  ☑  Sampling locations generated           → Step 5
  ☑  Data sheets printed and ready          → Section 3
```

<details>
<summary><b>📊 The Tsawwassen plan at a glance</b></summary>

<br>

| Step | Their decision |
|---|---|
| 1 — Study area | A **5 ha inlet** (50,000 m²), traced roughly from imagery |
| 2 — Stratify | **Two strata** — denser meadow, sparser fringe |
| 3 — Carbon pool | **Sediment**, cored to refusal |
| 4 — Sample size | **23** cores at ±20%, 90% confidence |
| 5 — Locations | Allocated proportionally by stratum area, minimum 5 per stratum |

**→ [Read the full planning walkthrough](../Worked_Example/02_Project_Planning.md)**

</details>

You now have everything a field team needs: a boundary, strata, a carbon pool and depth, a core count, and a list of coordinates. 

What remains is the fieldwork itself. **Section 3** covers what to bring, how to take a sediment core, how to record information on the data sheet, and the handling and labelling the samples.

**Next: [Section 3 — Field Methods →](../03_Field_Methods/)**

---
---

# Appendix A — A brief lesson in sampling logic

*and the derivations that drive this work*

Steps 1–5 don't require any of this. But if you want to know why the calculator behaves the way it does, or you need to defend a sample size to a reviewer, it's all here — in the order the ideas actually build on each other.

| | | Used in |
|---|---|---|
| [A1](#a1--what-an-estimate-actually-is) | What an estimate actually is | Background |
| [A2](#a2--working-backwards-from-precision-to-sample-size) | Working backwards: from precision to sample size | Step 4 |
| [A3](#a3--cochrans-correction-why-big-areas-stop-needing-more-cores) | Cochran's correction | Step 4 |
| [A4](#a4--what-actually-drives-sample-size) | What actually drives sample size | Step 4 |
| [A5](#a5--the-proportion-form) | The proportion form | Step 4 |
| [A6](#a6--symbol-crosswalk-to-the-unfccc-a64-tool) | Symbol crosswalk to the UNFCCC A6.4 tool | Step 4 |
| [A7](#a7--proportional-allocation-across-strata) | Proportional allocation across strata | Step 5 |
| [A8](#a8--after-the-campaign-did-you-hit-your-target) | After the campaign: did you hit your target? | Step 4 |

---

### A1 — What an estimate actually is

*The machinery behind the [Background](#background--what-sampling-is-and-why-it-works) section.*

You core a subset of plots and average them. That average, $\bar{x}$, is your estimate of the meadow's true mean carbon.

How far off might it be? That depends on two things: how much the plots differ from each other (the standard deviation, $s$) and how many you took ($n$). Combined, they give the **standard error of the mean**:

$$SE = \frac{s}{\sqrt{n}}$$

The $\sqrt{n}$ is the whole story of sampling economics. Four times the cores buys you *twice* the precision — never four times.

The **margin of error** scales that standard error by a multiplier set by your confidence level:

$$E \cdot \bar{x} = z\,\frac{s}{\sqrt{n}}$$

where $z = 1.282$ at 80% confidence, $1.645$ at 90%, and $1.96$ at 95%. Writing $E$ as a *relative* quantity (a fraction of the mean) is what lets you say "±20%" without knowing the answer in advance.

---

### A2 — Working backwards: from precision to sample size

*The machinery behind [Step 4](#step-4--decide-how-many-samples).*

Everything in A1 runs in reverse. If you know the precision you want, you can solve for the $n$ that delivers it.

Start from the margin-of-error definition and solve for $n$:

$$E \cdot \bar{x} = z\,\frac{s}{\sqrt{n}} \qquad \Longrightarrow \qquad n = \left(\frac{z \cdot s}{E \cdot \bar{x}}\right)^{2}$$

Then replace $s/\bar{x}$ with the **coefficient of variation**, $CV$:

$$n = \left(\frac{z \cdot CV}{E}\right)^{2}, \qquad CV = \frac{s}{\bar{x}}$$

Expressing variability as a $CV$ makes the result **scale-free** — it no longer depends on whether carbon is measured in Mg C ha⁻¹, g cm⁻³, or anything else. A meadow with $CV = 0.5$ needs the same number of cores whether it holds 40 or 400 Mg C ha⁻¹.

Notice what's squared: **$z$, $CV$ and $E$**. That single fact explains almost everything in A4.

This is the **infinite-population** form. It assumes your study area could hold unlimited plots — which no real site can.

---

### A3 — Cochran's correction: why big areas stop needing more cores

*The machinery behind [Step 4](#step-4--decide-how-many-samples).*

A 5 ha inlet at 100 m² per plot holds exactly 500 possible plot locations. Sampling theory gives you credit for how much of that you've covered — 17 cores is about 3% of every plot there is, and tightening to ±10% takes you to 60 cores, or 12%. Cochran's **finite-population correction** accounts for it:

$$n \geq \frac{z^2\, N\, CV^2}{(N-1)\,E^2 + z^2\, CV^2}$$

where $N$ = study area ÷ plot footprint.

**One modelling choice everything depends on:** each core is taken to represent a **plot, not a pinprick**. This workshop uses a **10 × 10 m plot (100 m²)** per core, which is what converts an area into $N$. Change the plot size and every number downstream shifts.

As $N$ grows, $(N-1)E^2$ dominates the denominator and the correction fades — the formula converges on the infinite-population form in A2. That's why the effect of area **plateaus**: it matters when plots are genuinely scarce, and stops mattering once they aren't.

---

### A4 — What actually drives sample size

*The machinery behind [Step 4](#step-4--decide-how-many-samples). If you read one appendix section, read this one.*

Four inputs dominate, and two of them sit **squared** in the formula.

All numbers below are anchored on the settings used throughout this workshop, and typical of coastal MMRV work: a **5 ha inlet** ($N$ = 500 plots), **±20% margin of error**, **90% confidence**, $CV$ = 0.5 → **17 cores**. One knob turned at a time:

```
                                              cores needed (from 17)
  Precision      ±20% → ±10%     ████████████████████████  60
  Variability    CV 0.5 → 1.0    ████████████████████████  60
  Confidence     90% → 95%       █████████                 23
  Study area     5 ha → 50 ha    ███████                   17
```

| Knob | Turn it… | Effect on *n* | Why |
|---|---|---|---|
| **Margin of error, $E$** | tighter: ±20% → ±10% | **~3.5× more** (17 → 60) | $E$ is squared |
| **Variability, $CV$** | patchier: 0.5 → 1.0 | **~3.5× more** (17 → 60) | also squared |
| **Confidence** | stricter: 90% → 95% | **~35% more** (17 → 23) | $z$ is squared too, but 1.645 → 1.96 is a small step |
| **Study area** | bigger: 5 ha → 50 ha | **no change** (17 → 17) | see below |

Three things here routinely surprise people.

**CV is the hidden driver.** It's squared, exactly like $E$ — so a meadow twice as patchy needs roughly **three and a half times** the cores. This is why a good variability prior matters more than almost any other input, and why you pad the SD when you're unsure. It is also the one input you don't control: the meadow is as variable as it is.

**Precision is expensive; confidence is cheap.** Tightening $E$ from ±20% to ±10% more than triples the fieldwork. Raising confidence from 90% to 95% costs about a third more. **If the budget is fixed, loosening $E$ buys back far more cores than dropping confidence** — and a wider interval at 95% is usually easier to defend than a tight one at 90%.

**Area barely matters, and at ±20% it doesn't matter at all.** Running 1 ha → 5 ha → 50 ha → 500 ha gives **15 → 17 → 17 → 17** cores. A meadow a hundred times larger needs the same number of cores. You're estimating a *mean*, and pinning down a mean depends on variability, not on the size of the field. This is the single most counter-intuitive result in sampling design, and the one most worth being able to explain to a funder: **a bigger site is not a more expensive survey.**

> **Why "~3.5×" and not "4×"?** In a large area the squared terms give a clean fourfold: at 500 ha, halving $E$ takes *n* from 17 to 68. In a 5 ha inlet there are only 500 possible plots, so the finite-population correction from [A3](#a3--cochrans-correction-why-big-areas-stop-needing-more-cores) pulls it back to about 3.5×. **The smaller your study area, the more it dampens all four effects.**

---

### A5 — The proportion form

*The machinery behind [Step 4](#step-4--decide-how-many-samples), when the thing you're estimating isn't a mean.*

Everything above estimates a **continuous** variable — carbon stock. Some questions are instead about a **proportion**: what fraction of cores contain a peat horizon, what percentage of the meadow is still vegetated. Those use a parallel formula:

$$n \geq \frac{z^2\, N\, p\,q}{(N-1)\,E^2 p^2 + z^2\, p\, q}, \qquad q = 1-p$$

where $p$ is the expected proportion. **Use $p = 0.5$ when you have no prior** — it maximises $p\,q$ and therefore returns the largest, most conservative $n$.

---

### A6 — Symbol crosswalk to the UNFCCC A6.4 tool

*Useful if you're cross-referencing the [UNFCCC A6.4 Sampling & Surveys tool](Sampling-Design-Eng-2026.pdf) or its calculator.*

| This guide | UNFCCC tool | Meaning |
|---|---|---|
| $z$ | $Z_{\alpha/2}$ | z-multiplier set by confidence level |
| $E$ | $e_{abs}$ | target **relative** precision (0.20 = ±20% of the mean) |
| $s$ | $SD$ | expected standard deviation (your prior) |
| $\bar{x}$ | mean | expected mean (your prior) |
| $CV$ | $CV$ | coefficient of variation, $s/\bar{x}$ |
| $N$ | $N$ | population size — see note |
| $n$ | $n$ | number of plots/cores to collect |

> **Where the two calculators differ — and it's only one thing.** The formula is identical. They differ in how $N$ is obtained: the WWF-Canada area-based calculator derives it from **total area ÷ plot size**, while the UNFCCC tool takes a **population count** directly. Because $(N-1)$ barely moves the result once $N$ is large, both converge on the same answer — which is exactly the plateau described in [A4](#a4--what-actually-drives-sample-size).

---

### A7 — Proportional allocation across strata

*The machinery behind [Step 5](#step-5--decide-where-the-samples-go).*

Each stratum receives a share of the total $n$ proportional to its area:

$$n_h = \frac{g_h}{N}\times n$$

where $g_h$ is the size of stratum $h$ and $N$ is the total study area.

Then two practical rules are applied on top: round each $n_h$ **up** to a whole core, and raise any stratum below **5 cores** to 5. Both push the total above $n$ — deliberately. Rounding down or allowing a 2-core stratum would leave you unable to estimate variance within that stratum at all.

---

### A8 — After the campaign: did you hit your target?

*The machinery behind the check you run once [Step 4](#step-4--decide-how-many-samples)'s cores come back.*

Sample-size planning uses *expected* variability. Real cores may be more or less variable than your prior assumed, so before trusting the estimate, check the **achieved** precision against the target you set.

Recompute precision from what you actually measured:

$$\text{RME} = \frac{z \cdot SE}{\bar{x}}, \qquad SE = \sqrt{\left(1-\tfrac{n}{N}\right)\frac{s^2}{n}}$$

Here $s$ and $\bar{x}$ are the **sample** standard deviation and mean — measured, not assumed. The $\left(1-\tfrac{n}{N}\right)$ term is the finite-population correction from [A3](#a3--cochrans-correction-why-big-areas-stop-needing-more-cores), reappearing in its standard-error form.

Compare the **relative margin of error (RME)** to the target $E$ you set in Step 4:

- **RME ≤ E** → the estimate meets its reliability criterion. Report it.
- **RME > E** → the meadow was patchier than your prior assumed.

The calculator's post-survey cells do this for you.

**If you miss the target,** work down the ladder in order:

1. **Scrutinize the raw data** — outliers, skew, a mis-recorded core
2. **Post-stratify** — is there structure you didn't account for?
3. **Add cores**
4. **As a last resort**, report the conservative confidence bound — the interval end that *understates* carbon — so the estimate stays defensible

> 📸 **[SCREENSHOT NEEDED]** — the calculator's post-survey precision cells (SRS-Mean rows: SE, t-value, relative precision).

This comparison — not the planned sample size — is what you report and what a reviewer will check.

---

## In this section

- [`BlueCarbon_SampleAllocation_Spreadsheet_V2.xlsx`](BlueCarbon_SampleAllocation_Spreadsheet_V2.xlsx) — the sample-size and allocation calculator
- [`Sampling-Design-Eng-2026.pdf`](Sampling-Design-Eng-2026.pdf) — the WWF-Canada sampling-design guide
- `images/` — screenshots of the calculator and planning materials

<details>
<summary><b>📋 Slide/screenshot layout template — copy/paste this to add an image</b></summary>

Each image is a two-column block: the image on the left and a description on the right.
To add one, copy the block below and:

1. In GitHub's editor, click inside the left cell (between the blank lines) and **paste or drag your image** — or paste the image URL into `src="…"`.
2. Type your description in the right cell (plain text, **markdown**, links, and lists all work).

Keep the blank lines inside the cells — they're what let GitHub render the pasted image and formatted text.

```html
<table>
<tr>
<td width="45%">

<img width="100%" alt="Image description" src="PASTE_IMAGE_URL_HERE">

</td>
<td width="55%">

Paste your description here.

</td>
</tr>
</table>
```

</details>

---

[← 1 — Background](../01_Background/) · [Back to main guide](../README.md) · Next: [3 — Field Methods →](../03_Field_Methods/)
