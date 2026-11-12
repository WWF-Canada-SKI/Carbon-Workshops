"""Build the two Grasslands .docx field assets.

    03_Field_Methods/datasheets/Grassland-Field-Data-Sheet.docx
    03_Field_Methods/checklists/Grassland_Carbon_Skill_Checklist.docx

Style is lifted from Wetlands/_source/build_docx.py so the series looks like
one thing. The field labels are READ OUT OF THE CALCULATOR rather than retyped,
which is what guarantees the datasheet and the workbook cannot drift apart.
"""
import os, sys, openpyxl
sys.path.insert(0, "/home/user/Terrestrial_Carbon_Workshops_V1/Grasslands/_source")
from grass_style import OUT as XLSX

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ROW_HEIGHT_RULE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

GRASS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ORANGE_BAND = "C2703A"   # section bands -- grassland earth
PALE   = "F2DFCE"
TINT   = "FDF6EF"
WHITE  = "ffffff"
GREY   = "d9d9d9"
FONT   = "Calibri"
TEAM   = "▶ TEAM"


def shade(cell, hexfill):
    tcPr = cell._tc.get_or_add_tcPr()
    for old in tcPr.findall(qn('w:shd')):
        tcPr.remove(old)
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hexfill)
    tcPr.append(shd)


def borders(table, sz=4):
    tblPr = table._tbl.tblPr
    for old in tblPr.findall(qn('w:tblBorders')):
        tblPr.remove(old)
    el = OxmlElement('w:tblBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        e = OxmlElement('w:' + edge)
        e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), str(sz))
        e.set(qn('w:space'), '0'); e.set(qn('w:color'), '000000')
        el.append(e)
    tblPr.append(el)


def set_widths(table, widths):
    """Fix column widths. LibreOffice sizes fixed-layout tables from w:tblGrid,
    which python-docx never writes -- without this the columns come out equal."""
    tblPr = table._tbl.tblPr
    for old in tblPr.findall(qn('w:tblLayout')):
        tblPr.remove(old)
    layout = OxmlElement('w:tblLayout'); layout.set(qn('w:type'), 'fixed')
    tblPr.append(layout)
    table.autofit = False
    tbl = table._tbl
    for old in tbl.findall(qn('w:tblGrid')):
        tbl.remove(old)
    grid = OxmlElement('w:tblGrid')
    for w in widths:
        gc = OxmlElement('w:gridCol'); gc.set(qn('w:w'), str(int(w.twips)))
        grid.append(gc)
    tbl.insert(list(tbl).index(tbl.tblPr) + 1, grid)
    for row in table.rows:
        for i, w in enumerate(widths):
            if i < len(row.cells):
                row.cells[i].width = w


def row_height(table, inches, first=0):
    for row in table.rows[first:]:
        row.height = Inches(inches)
        row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST


def write(cell, text, bold=False, size=9, align=None, italic=False, color=None):
    cell.text = ''
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(1); p.paragraph_format.space_after = Pt(1)
    if align is not None:
        p.alignment = align
    r = p.add_run(text)
    r.bold, r.italic = bold, italic
    r.font.size = Pt(size); r.font.name = FONT
    if color:
        r.font.color.rgb = RGBColor.from_string(color)


def para(doc, text, bold=False, size=10, italic=False, space_after=4, color=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(space_after)
    r = p.add_run(text)
    r.bold, r.italic = bold, italic
    r.font.size = Pt(size); r.font.name = FONT
    if color:
        r.font.color.rgb = RGBColor.from_string(color)
    return p


def band(table, row_idx, text, fill, color=None, size=9):
    row = table.rows[row_idx]
    merged = row.cells[0]
    for c in row.cells[1:]:
        merged = merged.merge(c)
    write(merged, text, bold=True, size=size, color=color)
    shade(merged, fill)
    return merged


def base_doc(margin=0.62, landscape=False):
    doc = Document()
    st = doc.styles['Normal']; st.font.name = FONT; st.font.size = Pt(10)
    s = doc.sections[0]
    if landscape:
        from docx.enum.section import WD_ORIENT
        w, h = s.page_width, s.page_height
        s.orientation = WD_ORIENT.LANDSCAPE
        s.page_width, s.page_height = max(w, h), min(w, h)
    for a in ('left_margin', 'right_margin', 'top_margin', 'bottom_margin'):
        setattr(s, a, Inches(margin))
    return doc


def grid(doc, heads, widths, nrows, size=8, height=0.24):
    t = doc.add_table(rows=1 + nrows, cols=len(heads))
    borders(t); set_widths(t, widths)
    for j, h in enumerate(heads):
        write(t.rows[0].cells[j], h, bold=True, size=size, align=WD_ALIGN_PARAGRAPH.CENTER)
        shade(t.rows[0].cells[j], GREY)
    for i in range(1, nrows + 1):
        fill = TINT if i % 2 else WHITE
        for j in range(len(heads)):
            write(t.rows[i].cells[j], "", size=9)
            shade(t.rows[i].cells[j], fill)
    row_height(t, height, first=1)
    return t


# ── read the field names out of the calculator ───────────────────────────────
wb = openpyxl.load_workbook(XLSX)


def cols(tab, row=4):
    ws = wb[tab]
    out = []
    for c in range(1, 40):
        v = ws.cell(row, c).value
        if v and not str(v).startswith("_"):
            out.append(str(v))
    return out


PLOT_COLS = cols("1. Plot & Site Log")
SOIL_COLS = cols("2. Soil Data")
ROOT_COLS = cols("3. Root Biomass")
VEG_COLS = cols("4. Vegetation Data")

CALC = {"calculated", "lab"}
# which soil/root/veg columns the crew fills in the field
SOIL_FIELD = ["Plot ID", "Core ID", "Increment #", "Top depth (cm)", "Bottom depth (cm)",
              "Corer diameter (cm)", "Depth driven (cm)", "Length recovered (cm)",
              "Coarse fragments (% vol)", "Bulk density basis", "Notes"]
ROOT_FIELD = ["Plot ID", "Core ID", "Top depth (cm)", "Bottom depth (cm)",
              "Diameter class", "Live or dead", "Sieve mesh (mm)", "Notes"]


def build_datasheet(path):
    doc = base_doc()
    para(doc, "WWF-Canada Carbon Training", size=9, color="7F7F7F", space_after=0)
    para(doc, "Grassland Field Data Sheet", bold=True, size=16, space_after=2)
    para(doc, "Field sheet for grassland carbon — soil, ROOTS and vegetation. Field names match "
              "the Grassland Carbon Calculator tabs, so transcription is a straight copy. "
              "Lab columns (bulk density, organic carbon, root mass, ash fraction) are filled "
              "when results come back and are not on this sheet.",
         size=8, italic=True, space_after=8)
    para(doc, "Project:  ____________________________________     Recorder:  _________________"
              "_______     Page ____ of ____", size=10, space_after=8)

    # ---- plot & site log -------------------------------------------------- #
    t = doc.add_table(rows=1 + 6, cols=3)
    borders(t); set_widths(t, [Inches(2.45), Inches(2.45), Inches(2.4)])
    band(t, 0, "1.  PLOT & SITE LOG      — one block per plot; fill this FIRST",
         ORANGE_BAND, color="FFFFFF", size=10)
    triples = [("Plot ID:", "Site ID:", "Study area:"),
               ("Location:", "Date:", "Elevation (m):"),
               ("Latitude:", "Longitude:", "GNSS accuracy (m):"),
               ("Datum:", "Canopy cover (%):", "Slope position:")]
    for i, tri in enumerate(triples, start=1):
        for j, lab in enumerate(tri):
            write(t.rows[i].cells[j], lab + "\n", size=9)
            shade(t.rows[i].cells[j], WHITE)
    band(t, 5, "Management history — from the landholder, not from the site. "
               "These are the stratification variables.", PALE, size=9)
    m = t.rows[6].cells[0].merge(t.rows[6].cells[1]).merge(t.rows[6].cells[2])
    m.text = ''
    for lab in ["Grassland type  (prairie / aspen parkland / Black Oak savannah / interior BC "
                "bunchgrass / other):  ______________________",
                "Management  (never cultivated / cultivated and reseeded / long-term tame "
                "pasture / hayed / unknown):  ______________",
                "Grazing regime  (none / season-long / rotational / heavy / unknown):  "
                "________________________________________",
                "Years since fire:  ____________        Native or seeded:  "
                "________________________________________________"]:
        p = m.add_paragraph() if m.paragraphs[0].text else m.paragraphs[0]
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(lab); r.font.size = Pt(9); r.font.name = FONT
    shade(m, WHITE)

    doc.add_paragraph()

    # ---- soil increments -------------------------------------------------- #
    para(doc, "2.  SOIL DATA — one row per depth increment", bold=True, size=12, space_after=2)
    para(doc, "Core ID:  ____________     Corer internal diameter:  ______ cm", size=9,
         space_after=2)
    para(doc, "Bulk-density basis the lab reports   (tick one):   fine earth / TOTAL volume ☐   "
              "fine earth / FINE-EARTH volume ☐   not confirmed ☐", size=9, space_after=2)
    para(doc, "Lab and method reference:  _____________________________________     "
              "Confirmed on:  ____________", size=9, space_after=2)
    para(doc, "This decides whether the coarse-fragment correction is applied once, twice or not "
              "at all. It is a pre-field configuration item, not something to settle afterwards.",
         size=8, italic=True, space_after=4)
    para(doc, "Record ACTUAL top and bottom depths, not the ones you planned — a truncated "
              "increment scaled as a full one is a silent error. If you hit refusal, record the "
              "depth and what stopped you: that is data, not a failure.",
         size=8, italic=True, space_after=5)
    grid(doc, ["Inc. #", "Top depth (cm)", "Bottom depth (cm)", "Depth driven (cm)",
               "Length recovered (cm)", "Coarse fragments (% vol)",
               "Notes — horizon change, refusal, moisture"],
         [Inches(0.5), Inches(0.85), Inches(0.95), Inches(0.9), Inches(1.0),
          Inches(1.05), Inches(2.05)], 12, height=0.26)

    # ---- roots ------------------------------------------------------------ #
    doc.add_page_break()
    para(doc, "3.  ROOT BIOMASS — one row per increment per diameter class",
         bold=True, size=13, space_after=2)
    para(doc, "Core ID:  ____________     Finest sieve mesh used:  ______ mm", size=9,
         space_after=2)
    para(doc, "Root/soil reporting boundary agreed with the lab   (tick one):   "
              "root-separated soil ☐   operational soil fraction ☐   NOT AGREED ☐",
         size=9, space_after=2)
    para(doc, "Agreed with / method ref. / date:  ______________________________________________"
              "____________________", size=9, space_after=2)
    para(doc, "Root-separated: roots are removed by the project's own procedure, so soil and "
              "root pools may be added. Operational: the lab removes only what its standard "
              "preparation picks out, so the pools OVERLAP and must be reported separately. "
              "Not agreed: the overlap is unknown, not zero — settle it before the samples go.",
         size=8, italic=True, space_after=4)
    para(doc, "Roots are MEASURED here, not estimated from a root:shoot ratio. Oven-dry mass is "
              "taken at 60–70 °C — NOT the 105 °C used for soil bulk density. Mass and ash "
              "fraction come back from the lab; this sheet records what you sampled.",
         size=8, italic=True, space_after=5)
    grid(doc, ["Top depth (cm)", "Bottom depth (cm)", "Diameter class (≤2 mm / >2 mm)",
               "Live or dead", "Notes"],
         [Inches(1.0), Inches(1.1), Inches(1.9), Inches(1.0), Inches(2.35)], 16, height=0.26)

    doc.add_paragraph()
    para(doc, "Roots still present in the deepest increment?   YES ☐    NO ☐", size=10,
         space_after=2)
    para(doc, "If YES, the root total is a MINIMUM — the profile did not end, your coring did. "
              "Native grassland roots reach metres.", size=8, italic=True, space_after=8)

    # ---- vegetation ------------------------------------------------------- #
    doc.add_page_break()
    para(doc, "4.  VEGETATION DATA — one block per plot", bold=True, size=13, space_after=2)
    para(doc, "Sampling date:  ____________", size=10, space_after=2)
    para(doc, "Phenological stage   (tick one):   early vegetative ☐   vegetative ☐   "
              "PEAK standing biomass ☐   flowering ☐   seed set / senescing ☐   "
              "dormant / cured ☐   unknown ☐", size=9, space_after=2)
    para(doc, "Recent grazing or removal:   none observed ☐   light ☐   moderate ☐   heavy ☐   "
              "hayed / mown ☐   burned ☐   unknown ☐", size=9, space_after=2)
    para(doc, "Comparable-season criterion met?   YES ☐    NO ☐    not assessed ☐        "
              "(the project rule, from the calculator: ______________________________)",
         size=9, space_after=2)
    para(doc, "Stage is what you FOUND, not what you wanted. Whether the plot is comparable is a "
              "separate judgement against the project's written rule, and recent removal is a "
              "third, independent fact — a heavily grazed plot measures what SURVIVED, not what "
              "grew.", size=8, italic=True, space_after=4)
    para(doc, "A standing crop is NOT a stock — it grows from nothing each spring and is gone by "
              "autumn. Clip at GROUND LEVEL, not grazing height. Photograph the quadrat before "
              "and after.", size=8, italic=True, space_after=6)

    t = doc.add_table(rows=8, cols=2)
    borders(t); set_widths(t, [Inches(3.65), Inches(3.65)])
    band(t, 0, "Small plot — clip and weigh", PALE, size=9)
    pairs = [("Small plot area (m²):   0.25  ☐   other: ______", "Quadrat photographed before and after?   Y ☐   N ☐"),
             ("Clip fresh mass — LIVE (g):", "Clip fresh mass — DEAD (g):"),
             ("Bags labelled:   ☐", "Number of bags:")]
    for i, (a, b) in enumerate(pairs, start=1):
        for j, lab in enumerate((a, b)):
            write(t.rows[i].cells[j], lab + "\n", size=9)
            shade(t.rows[i].cells[j], WHITE)
    band(t, 4, "Medium plot — shrubs (measure and predict)", PALE, size=9)
    pairs2 = [("Medium plot area (m²):", "Number of shrubs measured:"),
              ("Species recorded:   ☐", "Crown L × W × H or stem diam. at 0.3 m recorded:   ☐")]
    for i, (a, b) in enumerate(pairs2, start=5):
        for j, lab in enumerate((a, b)):
            write(t.rows[i].cells[j], lab + "\n", size=9)
            shade(t.rows[i].cells[j], WHITE)
    band(t, 7, "Large plot — trees.  Only if canopy cover ≥ the threshold set in the "
               "calculator (default 25%). Use the FORESTS tree datasheet.", PALE, size=9)

    doc.add_paragraph()
    para(doc, "Canopy cover (%):  ________        Trees measured?   YES ☐    NO ☐    "
              "N/A ☐        Trees open-grown?   YES ☐    NO ☐", size=10, space_after=2)
    para(doc, "Open-grown savannah trees have short boles and wide crowns. Allometric equations "
              "fitted on forest-grown stems extrapolate poorly to them — record the form so the "
              "biomass figure can be reported as more uncertain.", size=8, italic=True)

    # ---- sample inventory ------------------------------------------------- #
    doc.add_page_break()
    para(doc, "5.  SAMPLE / COOLER INVENTORY — reconcile BEFORE leaving the site",
         bold=True, size=13, space_after=2)
    para(doc, "Count what is in the cooler against what this sheet says you took. A discrepancy "
              "found here is a five-minute problem; found at the lab it is an unusable plot. "
              "The full chain-of-custody form travels with the cooler.",
         size=8, italic=True, space_after=5)
    t = doc.add_table(rows=1 + 4, cols=4)
    borders(t); set_widths(t, [Inches(2.6), Inches(1.5), Inches(1.5), Inches(1.7)])
    for j, h in enumerate(("Count", "Expected", "Present", "Discrepancy — and what you did")):
        write(t.rows[0].cells[j], h, bold=True, size=9)
        shade(t.rows[0].cells[j], GREY)
    for i, lab in enumerate(["Plots visited", "Cores attempted / accepted / rejected",
                             "Depth intervals", "Containers by analysis "
                             "(soil C / BD / roots / archive)"], start=1):
        write(t.rows[i].cells[0], lab, size=9)
        for j in range(4):
            shade(t.rows[i].cells[j], WHITE)
    doc.add_paragraph()
    para(doc, "Cooler ID:  __________   Seal no.:  __________   Temperature on closing:  "
              "______ °C   Time:  __________", size=9, space_after=2)
    para(doc, "Reconciled by:  ______________________     Signature:  ______________________"
              "     Date / time:  ______________", size=9, space_after=2)
    para(doc, "Unresolved discrepancies (write them down even if you cannot fix them — an "
              "undocumented gap is worse than a documented one):", size=9, space_after=2)
    para(doc, "_______________________________________________________________________________"
              "_______________________", size=9, space_after=2)

    doc.add_paragraph()
    para(doc, "Sources: Measuring Carbon in Vegetation (Non-Tree) and Measuring Carbon in "
              "Non-Peat Soils (WWF-Canada). Root separation is not covered by either guide; the "
              "method in Part 3 is a development draft pending specialist review.",
         size=7, italic=True, color="7F7F7F")

    os.makedirs(os.path.dirname(path), exist_ok=True)
    doc.save(path)
    return path


# ── the skill checklist ──────────────────────────────────────────────────────
CHECKLIST = [
    ("SECTION", "SECTION 1 — Sampling Design"),
    ("SUB", "Study area and strata"),
    ("Define the study area",
     "Draw the boundary and write down the RULE used. Exclude wetland inclusions, rock outcrop, roads and shelterbelts — in parkland and interior BC these can be a substantial fraction of a quarter section.",
     False,
     "Can state the inclusion rule out loud and point to two places on the map where it excluded land, and why."),
    ("Stratify on MANAGEMENT first",
     "Grazing regime, cultivation history, years since fire, native vs seeded. Not vegetation cover — management is the dominant variable in a grassland and it is mappable from a fence line.",
     False,
     "Names the management variable each stratum is built on, and can say which fence line or record it came from."),
    ("Get the management history",
     "From the landholder. Grazing and stocking, burn years, when cultivation stopped, seeding. This conversation is part of the method, not a courtesy.",
     False,
     "Has a named source for grazing, burn and cultivation history, or has written 'unknown' rather than a guess."),
    ("SUB", "How many cores"),
    ("Size SOIL and ROOTS separately",
     "Roots are 4–5x more variable than soil carbon, so at the same target they need 4–5x the cores. Set a looser target for roots (±40% rather than ±20%) or wash a random subset.",
     False,
     "Produces two different sample sizes from the tool and can say which CV and which target produced each."),
    ("Apply the t-floor",
     "Cochran's n uses z, which assumes a known SD. You estimate it, so add the two extra cores the t-multiplier needs.",
     False,
     "Shows the n from the tool with the t-adjustment on, and can say why z alone gives too few cores."),
    ("Decide if these are permanent plots",
     "A campaign designed for a one-off stock is often unusable as a monitoring baseline.",
     False,
     "States the decision and one consequence of it for where the core and quadrat go today."),
    ("SECTION", "SECTION 2 — Plot Setup"),
    ("SUB", "Laying out"),
    ("Lay out the plots",
     "Small 0.25 m² · medium 16–100 m² · large 400 m² if trees are in scope. Soil core offset from the quadrat.",
     False,
     "Plot sizes measured, not paced; the core position is offset from the quadrat and the offset is written down."),
    ("Record coordinates and GNSS accuracy",
     "At the plot centre.",
     False,
     "Coordinates, datum and the accuracy figure are all on the sheet. An accuracy field left blank fails this."),
    ("Mark a permanent plot so it can be refound",
     "Grassland has nothing to tag. Driven rod with recorded depth, buried magnet, AND a bearing and distance from something durable.",
     False,
     "Records at least two independent ways back to the marker, one of which does not depend on the GNSS."),
    ("Complete the plot log BEFORE touching anything",
     "Grassland type, management, grazing regime, years since fire, native or seeded, canopy cover.",
     False,
     "Log is finished and photographs taken while the plot is still undisturbed. Any later entry fails this."),
    ("SUB", "Photographs"),
    ("16-frame photo series",
     "Frames 1–2 straight down and straight up, 3–14 three per cardinal direction, 15–16 the quadrat overhead before and after clipping.",
     False,
     "All 16 frames present and identifiable by the board or first frame; filenames written on the plot log."),
    ("Quadrat before AND after clipping",
     "From the same position. The only record of what the standing crop looked like.",
     False,
     "Two frames from the same position, both legible, both filed against the plot."),
    ("SECTION", "SECTION 3 — Vegetation (before any coring)"),
    ("SUB", "Order of work"),
    ("Finish ALL vegetation work before coring",
     "Coring is destructive. A corer hole in a quadrat you have not yet clipped is a lost plot.",
     False,
     "Order of work on the sheet matches the order on the ground; no corer mark inside an unmeasured quadrat."),
    ("SUB", "Clip and weigh"),
    ("Clip at GROUND LEVEL",
     "Not grazing height — that is not a defined datum and will not repeat between crews or visits.",
     False,
     "Cut height is consistent across three quadrats and matches the written protocol, checked by the trainer against the stubble."),
    ("Separate live from dead",
     "Standing dead and litter hold carbon but are not production. Merging them later is easy; splitting them is not.",
     False,
     "Two labelled bags per quadrat, and the participant can justify three borderline pieces either way."),
    ("Confirm peak growing season, and record the date",
     "Peak is the only phenological point that repeats between sites and years. A clip-and-weigh without a date cannot be interpreted.",
     False,
     "Records the stage observed, the removal seen, and whether the project's season rule was met — three separate entries."),
    ("SUB", "Shrubs and trees"),
    ("Measure shrubs non-destructively",
     "Crown L × W × H, or stem diameter at 0.3 m. Check the species is in the coefficient table before relying on an allometric.",
     False,
     "Measures the predictor the chosen equation actually takes, at the height the equation defines, and says which equation."),
    ("Apply the tree-cover threshold consistently",
     "Default ≥25% canopy. Savannah sits right on this boundary, so the rule matters more here than anywhere else.",
     False,
     "Estimates cover the same way twice within a few per cent, and applies the project rule without renegotiating it on site."),
    ("Note whether trees are open-grown",
     "Savannah oaks have short boles and wide crowns; forest-fitted equations extrapolate poorly to them.",
     False,
     "Records crown and bole form, and can say why it matters for the biomass figure."),
    ("SECTION", "SECTION 4 — Soil Coring"),
    ("SUB", "Taking the core"),
    ("Measure and record the corer diameter",
     "It sets sample volume and therefore every bulk density. Out by 10% puts every carbon stock out by 21%. Write it on the corer.",
     False,
     "Reads the INSIDE diameter with calipers at two positions, records the value with units and the corer ID."),
    ("Core offset from the quadrat",
     "And record the offset, so the next visit can avoid this visit's holes.",
     False,
     "Bearing and distance from the marker written on the sheet before the corer goes in."),
    ("Do not core wet or frozen ground",
     "Both wreck bulk density.",
     False,
     "Records the moisture condition, and can say what a saturated or frozen core would do to bulk density."),
    ("Record depth driven AND length recovered",
     "If they differ, the increments are not where you think. Do NOT stretch them back out.",
     False,
     "Both numbers on the sheet for every core, including the ones where they agree."),
    ("SUB", "Sectioning"),
    ("Section at planned increments, record ACTUAL depths",
     "A truncated increment scaled as a full one is a silent error.",
     False,
     "Depths run continuously down the sheet, and any short interval is recorded short rather than rounded up."),
    ("Record depth to refusal and what stopped you",
     "Bedrock, cemented layer, stone. This is data, not a failure.",
     False,
     "Actual refusal depth and a stated cause. A planned depth entered for a refused core fails this."),
    ("Estimate coarse fragments per increment",
     "Rocks hold no carbon, and neither WWF guide's equations correct for them. Mandatory in interior BC.",
     False,
     "Gives a figure and the method used to get it, consistently across increments."),
    ("Ask the lab which bulk-density basis they report",
     "Fine earth over total volume, or over fine-earth volume. Getting it wrong understates a stony site by up to a third — or double-corrects it.",
     False,
     "Names the lab, the method reference and the date it was confirmed — before the field day, not after."),
    ("Label bags with plot, core and DEPTH INTERVAL",
     "Not just an increment number.",
     False,
     "A label picked at random off the bench identifies its sample with no datasheet in the room."),
    ("SECTION", "SECTION 5 — Root Separation"),
    ("SUB", "The decision that comes first"),
    ("Decide the root/soil boundary BEFORE the lab",
     "Sieve roots out and analyse root-free soil, OR leave fine roots in the soil pool and report only coarse roots separately. Both are defensible. Silence is not, and silence is the default if nobody decides.",
     False,
     "States which of the two boundaries applies, who agreed it and under what method, and what it means for adding the pools."),
    ("Record the sieve mesh",
     "Roots finer than the mesh are lost, so fine-root biomass is a known underestimate. Without the mesh size the figure cannot be interpreted.",
     False,
     "Every mesh used is written down, and the participant can say what the finest one implies about the fine-root figure."),
    ("SUB", "Processing"),
    ("Weigh the field-moist increment first",
     "Before anything is removed.",
     False,
     "Mass and subsample ID recorded before anything is washed or removed."),
    ("Soak and disperse, then wash over nested sieves",
     "2 mm for the fine/coarse split, plus a finer mesh to catch fine roots.",
     True,
     "Follows the written sequence, and reports losses rather than absorbing them."),
    ("Separate live from dead",
     "Flotation, then by eye — live roots are paler, turgid, elastic, with intact cortex.",
     False,
     "Two labelled bags per quadrat, and the participant can justify three borderline pieces either way."),
    ("Sort by diameter class",
     "≤2 mm fine, >2 mm coarse. A convention a crew can apply consistently, not a biological boundary.",
     False,
     "Applies the boundary the same way to twenty roots as to the first five, and says how diameter was measured."),
    ("Dry at 60–70 °C — NOT 105 °C",
     "105 °C is the soil bulk-density convention and can volatilise organics in root tissue. Two samples, two ovens, two conventions.",
     False,
     "Sets and records the temperature and the constant-mass criterion, and does not move a sample between the two conventions."),
    ("Ash-correct the root mass",
     "Washed roots retain adhering mineral soil. Combust a subsample and subtract the residue, or root biomass is systematically too high.",
     False,
     "Records the ash subsample and the ash mass, and can say which direction an uncorrected figure is wrong in."),
    ("Retain the root-free soil for carbon analysis",
     "Under the sieve-first option, this is what goes to the lab.",
     False,
     "Residue kept, labelled and linked to the interval it came from."),
    ("SECTION", "SECTION 6 — Calculations and Reporting"),
    ("SUB", "Calculations"),
    ("Soil carbon per increment",
     "Bulk density × (carbon % ÷ 100) × thickness, to kg C/m². Apply the coarse-fragment correction ONCE.",
     False,
     "Reproduces one increment by hand and gets the workbook's figure, with the coarse-fragment correction applied once."),
    ("Root carbon per increment",
     "Ash-corrected dry mass ÷ core area, scaled to m², × carbon fraction.",
     False,
     "Reproduces one row by hand, using the core area from the recorded diameter."),
    ("Report soil to 30 cm AND to the full depth cored",
     "30 cm is the comparability depth. It is a floor, not the total.",
     False,
     "Both figures reported, and the participant can say which one is comparable to other projects and why."),
    ("Check achieved precision, per pool",
     "Soil and roots against their separate targets. Use t, not z, at small n.",
     False,
     "Reads the achieved margin against the target for soil and roots separately, and says what to do if one misses."),
    ("SUB", "Reporting"),
    ("Report the standing crop separately",
     "Never merged into the soil figure.",
     False,
     "Vegetation kept in its own column through to the report, with the date and stage attached."),
    ("Flag a root total that stops at the bottom of the core",
     "It is a MINIMUM. Native grassland roots reach metres.",
     False,
     "Marks the total as a minimum whenever roots were still present in the deepest interval."),
    ("State what is excluded",
     "Shrub roots, litter, and below-ground tree biomass are in no pool this workshop measures. Name the gaps.",
     False,
     "Names shrub roots, litter and below-ground tree biomass as gaps, without being prompted."),
]


def build_checklist(path):
    doc = base_doc(margin=0.62)
    para(doc, "WWF-Canada Carbon Training", size=9, color="7F7F7F", space_after=0)
    para(doc, "Grassland Carbon Measurement — In-Field Skill Checklist",
         bold=True, size=15, space_after=4)
    para(doc, "Participant:  ________________________________     Date:  _____________     "
              "Site:  _____________", size=10, space_after=4)
    para(doc, "Work through each skill with your trainer. Check the left ☐ when you have "
              "practised it; the trainer checks the right ☐ only when the criterion in italics "
              "has been met — a named, observable thing, so two trainers sign off the same "
              "skill the same way. Section 5 — root separation — is the one most people arrive "
              "without.", size=8, italic=True, space_after=8)

    t = doc.add_table(rows=1 + len(CHECKLIST), cols=4)
    borders(t)
    widths = [Inches(0.35), Inches(1.65), Inches(4.35), Inches(0.85)]
    set_widths(t, widths)
    for j, h in enumerate(("", "Skill", "Description / Key Actions", "Complete ✔")):
        write(t.rows[0].cells[j], h, bold=True, size=9,
              align=WD_ALIGN_PARAGRAPH.CENTER if j in (0, 3) else None)
        shade(t.rows[0].cells[j], GREY)

    alt = 0
    for i, item in enumerate(CHECKLIST, start=1):
        if item[0] == "SECTION":
            band(t, i, item[1], ORANGE_BAND, color="FFFFFF", size=10); alt = 0; continue
        if item[0] == "SUB":
            band(t, i, item[1], PALE, size=9); alt = 0; continue
        skill, desc, team, criterion = item
        fill = TINT if alt % 2 else WHITE
        alt += 1
        row = t.rows[i]
        write(row.cells[0], "☐", size=11, align=WD_ALIGN_PARAGRAPH.CENTER)
        write(row.cells[1], (TEAM + "  " if team else "") + skill, bold=True, size=8)
        write(row.cells[2], desc, size=8)
        # the criterion the trainer signs against, in the same cell so the sheet
        # stays one page wider than it is long
        cp = row.cells[2].add_paragraph()
        cp.paragraph_format.space_before = Pt(2)
        cp.paragraph_format.space_after = Pt(0)
        cr = cp.add_run("Signed off when:  " + criterion)
        cr.italic = True
        cr.font.size = Pt(7.5)
        cr.font.name = FONT
        cr.font.color.rgb = RGBColor(0x7F, 0x4A, 0x28)
        write(row.cells[3], "☐", size=11, align=WD_ALIGN_PARAGRAPH.CENTER)
        for j in range(4):
            shade(row.cells[j], fill)

    doc.add_paragraph()
    para(doc, "Trainer:  ________________________________     Signature:  "
              "________________________________     Date:  _____________", size=10, space_after=8)
    para(doc, "Sources: Measuring Carbon in Vegetation (Non-Tree) and Measuring Carbon in "
              "Non-Peat Soils (WWF-Canada). Sampling-design items follow Part 2 of the Grassland "
              "Carbon Workshop; root separation follows Part 3A.",
         size=7, italic=True, color="7F7F7F")

    os.makedirs(os.path.dirname(path), exist_ok=True)
    doc.save(path)
    return path


# ── the sample inventory and chain of custody ────────────────────────────────
def build_custody(path):
    """The form that travels with the cooler.

    It is deliberately separate from the field data sheet: the data sheet stays
    with the crew and the custody form goes with the samples, and the whole
    point of a custody record is that the two are reconciled by different people
    at different times.
    """
    doc = base_doc(margin=0.62)
    para(doc, "WWF-Canada Carbon Training", size=9, color="7F7F7F", space_after=0)
    para(doc, "Grassland Sample Inventory and Chain of Custody",
         bold=True, size=15, space_after=3)
    para(doc, "One form per cooler. Complete the inventory BEFORE leaving the site, and again "
              "at every handoff. A sample whose custody cannot be traced is not evidence of "
              "anything, however carefully it was collected.",
         size=8, italic=True, space_after=8)

    para(doc, "Project:  ___________________________     Site / stratum:  "
              "___________________________     Cooler ID:  ____________", size=10,
         space_after=3)
    para(doc, "Field date(s):  ____________________     Crew:  "
              "_______________________________________________________", size=10, space_after=8)

    # ---- reconciliation --------------------------------------------------- #
    para(doc, "1.  SITE RECONCILIATION — before leaving", bold=True, size=12, space_after=2)
    t = doc.add_table(rows=1 + 6, cols=4)
    borders(t); set_widths(t, [Inches(2.7), Inches(1.3), Inches(1.3), Inches(2.0)])
    for j, h in enumerate(("Count", "Expected", "Present", "If they differ — what happened")):
        write(t.rows[0].cells[j], h, bold=True, size=9)
        shade(t.rows[0].cells[j], GREY)
    for i, lab in enumerate(["Plots visited",
                             "Cores attempted",
                             "Cores accepted / rejected",
                             "Depth intervals expected",
                             "Depth intervals present",
                             "Containers, all analyses"], start=1):
        write(t.rows[i].cells[0], lab, size=9)
        for j in range(4):
            shade(t.rows[i].cells[j], WHITE)

    doc.add_paragraph()

    # ---- containers by analysis ------------------------------------------- #
    para(doc, "2.  CONTAINERS BY ANALYSIS", bold=True, size=12, space_after=2)
    para(doc, "List ID ranges, not individual containers, where the IDs are consecutive.",
         size=8, italic=True, space_after=4)
    t = doc.add_table(rows=1 + 5, cols=4)
    borders(t); set_widths(t, [Inches(1.9), Inches(0.9), Inches(2.5), Inches(2.0)])
    for j, h in enumerate(("Analysis", "Count", "Container ID range",
                           "Preservation required")):
        write(t.rows[0].cells[j], h, bold=True, size=9)
        shade(t.rows[0].cells[j], GREY)
    for i, lab in enumerate(["Soil carbon", "Bulk density", "Roots", "Vegetation",
                             "Archive"], start=1):
        write(t.rows[i].cells[0], lab, size=9)
        for j in range(4):
            shade(t.rows[i].cells[j], WHITE)

    doc.add_paragraph()

    # ---- cold chain -------------------------------------------------------- #
    para(doc, "3.  COLD CHAIN AND SEAL", bold=True, size=12, space_after=2)
    para(doc, "Seal number:  ____________     Seal intact on arrival?   YES ☐    NO ☐    "
              "n/a ☐", size=10, space_after=3)
    t = doc.add_table(rows=1 + 3, cols=4)
    borders(t); set_widths(t, [Inches(2.0), Inches(1.8), Inches(1.7), Inches(1.8)])
    for j, h in enumerate(("Point", "Date / time", "Temperature (°C)", "Recorded by")):
        write(t.rows[0].cells[j], h, bold=True, size=9)
        shade(t.rows[0].cells[j], GREY)
    for i, lab in enumerate(["Cooler closed on site", "Transferred", "Received at lab"],
                            start=1):
        write(t.rows[i].cells[0], lab, size=9)
        for j in range(4):
            shade(t.rows[i].cells[j], WHITE)
    doc.add_paragraph()
    para(doc, "Holding time from collection to lab receipt:  ________ hours        "
              "Within the method's limit?   YES ☐    NO ☐", size=9, space_after=2)
    para(doc, "If NO, say so here rather than leaving the lab to discover it — an exceeded "
              "holding time is a qualifier on the result, not a reason to hide it.",
         size=8, italic=True, space_after=8)

    # ---- method record ----------------------------------------------------- #
    para(doc, "4.  METHOD RECORD THESE SAMPLES ASSUME", bold=True, size=12, space_after=2)
    para(doc, "These two are configuration decided before the field day. They travel with the "
              "samples because the lab's preparation has to match what the calculator assumes.",
         size=8, italic=True, space_after=4)
    para(doc, "Bulk-density basis the lab reports:   fine earth / TOTAL volume ☐   "
              "fine earth / FINE-EARTH volume ☐   not confirmed ☐", size=9, space_after=3)
    para(doc, "Root/soil reporting boundary:   root-separated soil ☐   "
              "operational soil fraction ☐   NOT AGREED ☐", size=9, space_after=3)
    para(doc, "Laboratory / method reference / date confirmed:  _______________________________"
              "_________________________________", size=9, space_after=8)

    # ---- custody ----------------------------------------------------------- #
    para(doc, "5.  CHAIN OF CUSTODY", bold=True, size=12, space_after=2)
    para(doc, "Every transfer gets a line. Both parties sign at the moment of transfer, not "
              "afterwards.", size=8, italic=True, space_after=4)
    t = doc.add_table(rows=1 + 5, cols=5)
    borders(t)
    set_widths(t, [Inches(1.7), Inches(1.7), Inches(1.3), Inches(1.3), Inches(1.3)])
    for j, h in enumerate(("Released by (print + sign)", "Received by (print + sign)",
                           "Date / time", "Containers", "Condition on receipt")):
        write(t.rows[0].cells[j], h, bold=True, size=8)
        shade(t.rows[0].cells[j], GREY)
    for i in range(1, 6):
        for j in range(5):
            write(t.rows[i].cells[j], "\n\n", size=9)
            shade(t.rows[i].cells[j], WHITE)

    doc.add_paragraph()
    para(doc, "Discrepancies, damage, or samples not delivered — record them even when they "
              "cannot be resolved:", size=9, space_after=3)
    for _ in range(3):
        para(doc, "______________________________________________________________________________"
                  "_______________________________", size=9, space_after=4)

    doc.add_paragraph()
    para(doc, "Sources: Measuring Carbon in Non-Peat Soils and Supplemental Guide: Laboratory "
              "Analysis (WWF-Canada). Confirm the laboratory's own submission form does not "
              "replace this one — where it does, use theirs and keep this as the field copy.",
         size=7, italic=True, color="7F7F7F")

    os.makedirs(os.path.dirname(path), exist_ok=True)
    doc.save(path)
    return path


if __name__ == "__main__":
    a = build_datasheet(os.path.join(GRASS, "03_Field_Methods", "datasheets",
                                     "Grassland-Field-Data-Sheet.docx"))
    b = build_checklist(os.path.join(GRASS, "03_Field_Methods", "checklists",
                                     "Grassland_Carbon_Skill_Checklist.docx"))
    c = build_custody(os.path.join(GRASS, "03_Field_Methods", "datasheets",
                                   "Grassland-Sample-Inventory-and-Chain-of-Custody.docx"))
    for p in (a, b, c):
        print(f"wrote {os.path.relpath(p, os.path.dirname(GRASS))}  "
              f"({os.path.getsize(p):,} bytes)")
