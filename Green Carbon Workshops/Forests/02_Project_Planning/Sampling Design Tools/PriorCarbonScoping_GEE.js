// =================================================================
// Charlie's Place KBA — Forest Carbon Assessment v4.3
// =================================================================
// Changes from v4.2:
//
//   Config:
//     TL_SOC_ASSET / TL_UNC_ASSET removed.
//     SOTHE_FC_UNC_ASSET and SOTHE_SC_UNC_ASSET added (actual paths).
//     N_UNC_BINS, MIN_PTS_PER_STRATUM, NEYMAN_DIAG_N added.
//
//   Globals:
//     sothe_fc_unc — Sothe forest carbon uncertainty (kg/m²)
//     sothe_sc_unc — Sothe soil carbon uncertainty (kg/m²)
//     tl_soc / tl_unc removed entirely.
//
//   Step 2:
//     Loads both Sothe uncertainty layers. Band [0] selected
//     explicitly for robustness against multi-band assets.
//     Both layers visualised + stats printed.
//
//   Step 4:
//     HEGL_BANDS updated: 'sothe_sc_covariate' replaces
//     'tl_soc_covariate'.
//
//   Step 6:
//     TL SOC asset load removed.
//     sothe_sc used as the depth-RF spatial prior covariate
//     (band renamed sothe_sc_covariate). Prediction stack likewise.
//
//   Step 7:
//     Soil ensemble: Hegl 3D RF + Sothe SC + SoilGrids 0-100 cm.
//     Forest combined uncertainty = sqrt(ensemble_SD^2 + sothe_fc_unc^2)
//     Soil combined uncertainty   = sqrt(ensemble_SD^2 + sothe_sc_unc^2)
//     Both RSS images stored globally for Step 8.
//
//   Step 8 — full Neyman rewrite:
//     Land-cover strata from ESA WorldCover v200 (10 m, reprojected
//     to EXPORT_SCALE), reclassified to 5 types:
//       1 = Forest/tree cover   (class 10)
//       2 = Shrub/Grassland     (classes 20, 30, 100)
//       3 = Wetland             (classes 90, 95)
//       4 = Cropland            (class 40)
//       5 = Other/barren        (classes 50, 60, 70)
//       0 = Open water (80) — excluded from sampling.
//     Uncertainty bins 0-3 set from p25/p50/p75 quantile breaks.
//     Composite stratum key = lc_class x N_UNC_BINS + unc_bin.
//     Neyman weights N_h x sigma_h estimated from a dense pixel
//     sample (NEYMAN_DIAG_N pts at 2x EXPORT_SCALE) evaluated
//     client-side — avoids GEE grouped-reducer ambiguity.
//     Floor of MIN_PTS_PER_STRATUM applied per occupied stratum.
//     classValues/classPoints arrays passed to stratifiedSample
//     in a single call per pool.
//     Forest sampling masked to forest_nf_mask.
//     Soil sampling over full AOI (soil C everywhere).
//
//   Step 9:
//     TL SOC rows replaced by Sothe SC + uncertainty rows.
//     Sothe uncertainty rasters queued for export.
// =================================================================


// ─────────────────────────────────────────────────────────────────
// SECTION A — CONFIGURATION
// ─────────────────────────────────────────────────────────────────
var AOI_ASSET     = 'projects/blue-carbon-hub/assets/Charlies_Place_KBA_boundaryFile_2025';
var WOSIS_ASSET   = 'projects/north-star-project-470316/assets/wosis_layers_canada';
var CANPEAT_ASSET = 'projects/north-star-project-470316/assets/peat_profiles';

// v4.3: Sothe et al. uncertainty layers (McMaster/WWF-Canada, 250 m, kg/m2)
var SOTHE_FC_UNC_ASSET = 'projects/carbon-learning-library/assets/McMasterWWFCanadaforestcarbon250mkgm2uncertaintyversion1';
var SOTHE_SC_UNC_ASSET = 'projects/carbon-learning-library/assets/McMasterWWFCanadasoilcarbon1muncertainty250mkgm2version3';

// v4.2: combined harmonised soil profiles
var COMBINED_ASSET = 'projects/north-star-project-470316/assets/combined_profiles';

var EXPORT_CRS     = 'EPSG:32621';
var EXPORT_SCALE   = 25;
var EXPORT_FOLDER  = 'CharliesPlace_Carbon_2025';
var SNAPSHOT_SCALE = 30;

// v4.2: Google Satellite Embedding
var EMBEDDING_YEAR = null;   // null = median across all available years
var EMBED_SCALE    = 10;

var N_FOREST_SAMPLES = 100;
var N_SOIL_SAMPLES   = 100;
var FOREST_THRESHOLD = 0.5;

var GEDI_START = '2019-04-18';
var GEDI_END   = '2023-12-31';
var S2_START   = '2020-01-01';
var S2_END     = '2023-12-31';
var SAR_START  = '2020-01-01';
var SAR_END    = '2023-12-31';
var TC_START   = '2000-01-01';
var TC_END     = '2022-12-31';
var IPCC_RS    = 0.285;

var TOP_N_BANDS       = 6;
var PILOT_N_TREES     = 100;
var FINAL_N_TREES     = 100;
var MIN_GEDI_POINTS   = 50;
var GEDI_SAMPLE_SCALE = 100;
var GEDI_NUM_PIXELS   = 3000;

// v4.4: Neyman allocation config
// N_UNC_BINS           — number of quantile uncertainty bins per LC class
// MIN_PTS_PER_STRATUM  — minimum points allocated to any occupied stratum
var N_UNC_BINS          = 4;
var MIN_PTS_PER_STRATUM = 3;

var AGBD_VIS = {
  min: 0, max: 250,
  palette: ['white', 'yellow', 'orange', 'green', 'darkgreen']
};


// ─────────────────────────────────────────────────────────────────
// SECTION B — AOI + CANADA BOUNDARY
// ─────────────────────────────────────────────────────────────────
var aoiFC      = ee.FeatureCollection(AOI_ASSET);
var aoi        = aoiFC.union().geometry();
var aoi_buffer = aoi.buffer(50000);

var canada_boundary = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017')
  .filter(ee.Filter.eq('country_na', 'Canada'));

Map.centerObject(aoi, 11);
Map.addLayer(canada_boundary, { color: 'b0b0b0', fillColor: '00000000', width: 1 },
  'Canada Boundary', false);
Map.addLayer(aoiFC, { color: '000000', fillColor: '00000000', width: 2 },
  'Conservation Project Boundary', false);


// ─────────────────────────────────────────────────────────────────
// SECTION C — GLOBAL PIPELINE STATE
// ─────────────────────────────────────────────────────────────────
var WOSIS_2023_Raw      = null;
var CanPeatData_Raw     = null;
var sothe_fc            = null;
var sothe_fc_unc        = null;   // v4.3: Sothe FC uncertainty (kg/m2)
var sothe_sc            = null;
var sothe_sc_unc        = null;   // v4.3: Sothe SC uncertainty (kg/m2)
var sg_soc_1m           = null;
var soil_prior_mean     = null;
var scanfi_img          = null;
var gedi_l2a            = null;
var gedi_l4a_col        = null;
var gedi_agbd_se        = null;
var sothe_ch            = null;
var meta_ch             = null;
var scanfi_ch           = null;
var covariates          = null;
var covariates_filled   = null;
var COV_BANDS           = null;
var COV_BANDS_CLIENT    = null;
var HEGL_BANDS          = null;
var sbfi_agb_raster     = null;
var forest_rf_pred      = null;
var hegl_total_soc      = null;
var forest_ens_mean     = null;
var forest_ens_sd       = null;
var soil_ens_mean       = null;
var soil_ens_sd         = null;
var forest_uncertainty  = null;   // v4.3: RSS(ensemble_SD, sothe_fc_unc)
var soil_uncertainty    = null;   // v4.3: RSS(ensemble_SD, sothe_sc_unc)
var total_ecosystem_c   = null;
var forest_nf_mask      = null;
var dsm_forest          = null;
var dsm_soil            = null;
var forest_sampling_pts = null;
var soil_sampling_pts   = null;

// 2-stage RF globals
var TOP_BANDS_CLIENT = null;
var TOP_BANDS_EE     = null;
var gedi_training    = null;
var agbd_modeled     = null;

// snapshot / embedding globals
var snapshot_btn  = null;
var sg_ocs_layers = null;
var embed_img     = null;


// ─────────────────────────────────────────────────────────────────
// SECTION D — UTILITY FUNCTIONS
// ─────────────────────────────────────────────────────────────────
function printStats(img, band, geom, scale, label) {
  img.select(band).reduceRegion({
    reducer: ee.Reducer.mean()
      .combine(ee.Reducer.min(),    null, true)
      .combine(ee.Reducer.max(),    null, true)
      .combine(ee.Reducer.stdDev(), null, true),
    geometry:   geom  || aoi,
    scale:      scale || EXPORT_SCALE,
    crs:        EXPORT_CRS,
    maxPixels:  1e11,
    bestEffort: true
  }).evaluate(function(r) {
    var f = function(k) { return r[k] !== undefined ? r[k].toFixed(3) : 'null'; };
    print(label + ' — mean: ' + f(band + '_mean') +
          ' | min: '  + f(band + '_min') +
          ' | max: '  + f(band + '_max') +
          ' | sd: '   + f(band + '_stdDev'));
  });
}

function addLayerWithStats(img, band, vis, label, geom, scale) {
  Map.addLayer(img.select(band), vis, label, false);
  printStats(img, band, geom, scale, label);
}

function getStats(img, band, sc) {
  var s = img.select(band).reduceRegion({
    reducer: ee.Reducer.mean()
      .combine(ee.Reducer.stdDev(), null, true)
      .combine(ee.Reducer.min(),    null, true)
      .combine(ee.Reducer.max(),    null, true),
    geometry:   aoi,
    scale:      sc || EXPORT_SCALE,
    crs:        EXPORT_CRS,
    maxPixels:  1e11,
    bestEffort: true
  });
  return {
    mean: s.get(band + '_mean'),
    sd:   s.get(band + '_stdDev'),
    min:  s.get(band + '_min'),
    max:  s.get(band + '_max')
  };
}

function cvStat(sd, mean) {
  return ee.Number(sd).divide(ee.Number(mean).abs().add(0.001)).multiply(100);
}


// ─────────────────────────────────────────────────────────────────
// SECTION E — SAR UTILITY
// ─────────────────────────────────────────────────────────────────
function buildSARComposites() {
  var s1 = ee.ImageCollection('COPERNICUS/S1_GRD')
    .filterBounds(aoi_buffer).filterDate(SAR_START, SAR_END)
    .filter(ee.Filter.eq('instrumentMode', 'IW'))
    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
    .select(['VV', 'VH'])
    .map(function(img) { return img.updateMask(img.select('VV').gt(-30)); });

  var asc  = s1.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'));
  var desc = s1.filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'));
  var emptyOrbit = ee.Image.constant([-999,-999]).rename(['VV','VH']).updateMask(ee.Image(0));

  var seasonal = function(col, m0, m1) {
    var sub = col.filter(ee.Filter.calendarRange(m0, m1, 'month'));
    return ee.Image(ee.Algorithms.If(sub.size().gt(0), sub.median(), emptyOrbit));
  };

  var asc_spring  = seasonal(asc,  3, 4);
  var asc_summer  = seasonal(asc,  7, 8);
  var desc_spring = seasonal(desc, 3, 4);
  var desc_summer = seasonal(desc, 7, 8);

  return {
    asc_spring:  asc_spring,
    asc_summer:  asc_summer,
    desc_spring: desc_spring,
    desc_summer: desc_summer,
    asc_change:  asc_summer.select('VV').subtract(asc_spring.select('VV')).rename('asc_vv_change'),
    desc_change: desc_summer.select('VV').subtract(desc_spring.select('VV')).rename('desc_vv_change')
  };
}


// ─────────────────────────────────────────────────────────────────
// SECTION F — UI
// ─────────────────────────────────────────────────────────────────
var statusLabel    = null;
var progressLabels = [];
var progressSteps  = [
  '[ ] Step 1: Raw data imported',
  '[ ] Step 2: Raster priors loaded',
  '[ ] Step 3: GEDI + CHMs loaded',
  '[ ] Step 4: Covariates + variable selection',
  '[ ] Step 5: Forest model trained',
  '[ ] Step 6: Soil model trained',
  '[ ] Step 7: Ensemble built',
  '[ ] Step 8: Sampling complete',
  '[ ] Step 9: Exports queued'
];
var mainPanel = null;

function markDone(idx) {
  if (!progressLabels[idx]) return;
  progressLabels[idx].setValue(progressSteps[idx].replace('[ ]', '[checkmark]'));
  progressLabels[idx].style().set('color', '#2e7d32');
}

function setStatus(msg) {
  if (statusLabel) statusLabel.setValue(msg);
  print('STATUS: ' + msg);
}

function makeButton(label, onClick) {
  return ui.Button({
    label: label, onClick: onClick,
    style: { width: '260px', margin: '2px 0', fontSize: '11px' }
  });
}

function makeSectionLabel(text) {
  return ui.Label(text, {
    fontWeight: 'bold', fontSize: '11px', color: '#222222', margin: '8px 0 3px 0'
  });
}

var SNAPSHOT_BTN_INDEX = 7;

function insertSnapshotButton() {
  if (snapshot_btn) return;
  snapshot_btn = ui.Button({
    label: '[4b] Export Covariate Snapshot (30 m GeoTIFF)',
    onClick: step4b_exportCovariateSnapshot,
    style: { width: '260px', margin: '2px 0', fontSize: '11px',
             color: '#ffffff', backgroundColor: '#1565c0' }
  });
  if (mainPanel) {
    mainPanel.insert(SNAPSHOT_BTN_INDEX, snapshot_btn);
    setStatus('Step 4 complete. Use [4b] to export covariate snapshot.');
  }
}

function initUI() {
  mainPanel = ui.Panel({
    style: { width: '290px', padding: '14px', position: 'top-left', backgroundColor: '#ffffff' }
  });
  mainPanel.add(ui.Label("Charlie's Place KBA", {
    fontWeight: 'bold', fontSize: '16px', color: '#111111', margin: '0 0 2px 0'
  }));
  mainPanel.add(ui.Label('Forest Carbon Assessment v4.4', {
    fontSize: '12px', color: '#555555', margin: '0 0 12px 0'
  }));
  mainPanel.add(makeSectionLabel('PIPELINE'));
  mainPanel.add(makeButton('[1] Import Raw Field Data',           step1_importRawData));
  mainPanel.add(makeButton('[2] Import Raster Priors',            step2_importRasterPriors));
  mainPanel.add(makeButton('[3] GEDI + Canopy Height Models',     step3_importGEDI));
  mainPanel.add(makeButton('[4] Build Covariates + Var Selection', step4_buildCovariates));
  // [4b] snapshot button inserted dynamically after Step 4 completes
  mainPanel.add(makeButton('[5] Train Final AGBD Model (top 6)',  step5_trainFinalGEDI));
  mainPanel.add(makeButton('[6] Build Soil Carbon Model',         step6_buildSoilModel));
  mainPanel.add(makeButton('[7] Build Ensemble Models',           step7_buildEnsemble));
  mainPanel.add(makeButton('[8] Generate Sampling Points',        step8_generateSampling));
  mainPanel.add(makeButton('[9] Reports and Exports',             step9_reportsAndExports));

  mainPanel.add(makeSectionLabel('PROGRESS'));
  var progressPanel = ui.Panel({ style: { margin: '0 0 8px 0' } });
  progressLabels = progressSteps.map(function(txt) {
    var lbl = ui.Label(txt, { fontSize: '10px', color: '#999999', margin: '1px 0' });
    progressPanel.add(lbl);
    return lbl;
  });
  mainPanel.add(progressPanel);
  mainPanel.add(makeSectionLabel('STATUS'));
  statusLabel = ui.Label('Ready - click [1] to begin.', {
    fontSize: '11px', color: '#333333', margin: '0 0 10px 0'
  });
  mainPanel.add(statusLabel);
  mainPanel.add(ui.Label(
    'Scale: ' + EXPORT_SCALE + 'm | CRS: UTM Zone 21N\n' +
    'Forest: ' + N_FOREST_SAMPLES + ' pts | Soil: ' + N_SOIL_SAMPLES + ' pts\n' +
    'RF: pilot ' + PILOT_N_TREES + ' -> final ' + FINAL_N_TREES +
    ' trees (top ' + TOP_N_BANDS + ' bands)\n' +
    'Sampling: Neyman | LC: ESA WorldCover | unc bins: ' + N_UNC_BINS,
    { fontSize: '9px', color: '#aaaaaa', margin: '4px 0 0 0', whiteSpace: 'pre' }
  ));
  Map.add(mainPanel);
}


// ─────────────────────────────────────────────────────────────────
// STEP 4b — EXPORT COVARIATE SNAPSHOT + CORE POINT SAMPLES (v4.2)
// Unchanged from v4.2
// ─────────────────────────────────────────────────────────────────
function step4b_exportCovariateSnapshot() {
  if (!covariates)   { setStatus('Run Step 4 first - covariates not built.');        return; }
  if (!sg_ocs_layers){ setStatus('Run Step 2 first - SoilGrids OCS not available.'); return; }
  if (!sothe_sc)     { setStatus('Run Step 2 first - Sothe SC not loaded.');          return; }
  if (!sothe_fc)     { setStatus('Run Step 2 first - Sothe FC not loaded.');          return; }
  if (!sothe_ch)     { setStatus('Run Step 3 first - Sothe CHM not loaded.');         return; }
  if (!gedi_l4a_col) { setStatus('Run Step 3 first - GEDI L4A not loaded.');          return; }
  if (!embed_img)    { setStatus('Run Step 2 first - Google Embedding not loaded.');  return; }

  setStatus('Step 4b: Assembling covariate snapshot stack...');

  var gedi_l4a_median = gedi_l4a_col
    .map(function(img) {
      var q = img.select('l4_quality_flag').eq(1).and(img.select('degrade_flag').eq(0));
      return img.select(['agbd', 'agbd_se']).updateMask(q);
    })
    .median().rename(['gedi_agbd', 'agbd_se']);

  var sothe_ch_band    = sothe_ch.select([0]).rename('sothe_ch');
  var cov_stack_global = covariates
    .addBands(sg_ocs_layers)
    .addBands(sothe_sc.rename('sothe_sc'))
    .addBands(sothe_fc.rename('sothe_fc'))
    .addBands(sothe_ch_band)
    .addBands(gedi_l4a_median);

  var snapshot = cov_stack_global.clip(aoi);

  snapshot.bandNames().evaluate(function(names) {
    print('COVARIATE SNAPSHOT BAND INVENTORY (' + names.length + ' bands)');
    names.forEach(function(b, i) { print('  ' + (i+1) + '. ' + b); });
  });

  // Task 1 - AOI covariate raster
  Export.image.toDrive({
    image: snapshot.toFloat(), description: 'CharliesPlace_Covariate_Snapshot_30m',
    folder: EXPORT_FOLDER, region: aoi,
    scale: SNAPSHOT_SCALE, crs: EXPORT_CRS, maxPixels: 1e13, fileFormat: 'GeoTIFF'
  });
  print('Task 1 queued: CharliesPlace_Covariate_Snapshot_30m.tif');

  // Task 2 - AOI Google Embedding V1
  Export.image.toDrive({
    image: embed_img.clip(aoi).toFloat(), description: 'CharliesPlace_GoogleEmbedding_V1_10m',
    folder: EXPORT_FOLDER, region: aoi,
    scale: EMBED_SCALE, crs: EXPORT_CRS, maxPixels: 1e13, fileFormat: 'GeoTIFF'
  });
  print('Task 2 queued: CharliesPlace_GoogleEmbedding_V1_10m.tif');

  var combined     = ee.FeatureCollection(COMBINED_ASSET);
  var wosis_na     = combined.filter(ee.Filter.eq('dataset', 'WOSIS 2023'))
                             .filter(ee.Filter.inList('country_name',
                               ee.List(['Canada', 'United States of America'])));
  var canpeat_pts  = combined.filter(ee.Filter.eq('dataset', 'Peat Database'));
  var janousek_pts = combined.filter(ee.Filter.eq('dataset', 'Janousek'));
  var core_pts     = wosis_na.merge(canpeat_pts).merge(janousek_pts);

  core_pts.size().evaluate(function(n)    { print('Total core points: ' + n); });
  wosis_na.size().evaluate(function(n)    { print('  WOSIS (NA): '   + n); });
  canpeat_pts.size().evaluate(function(n) { print('  CanPeat:    '   + n); });
  janousek_pts.size().evaluate(function(n){ print('  Janousek:   '   + n); });

  // Task 3 - Covariate CSV at core points
  Export.table.toDrive({
    collection:  cov_stack_global.sampleRegions({
      collection: core_pts, scale: SNAPSHOT_SCALE, tileScale: 4, geometries: true
    }),
    description: 'CorePoints_Covariates_CSV', folder: EXPORT_FOLDER, fileFormat: 'CSV'
  });
  print('Task 3 queued: CorePoints_Covariates_CSV.csv');

  // Task 4 - Google Embedding CSV at core points
  Export.table.toDrive({
    collection: embed_img.sampleRegions({
      collection: core_pts, scale: EMBED_SCALE, tileScale: 4, geometries: true
    }),
    description: 'CorePoints_GoogleEmbedding_V1_CSV', folder: EXPORT_FOLDER, fileFormat: 'CSV'
  });
  print('Task 4 queued: CorePoints_GoogleEmbedding_V1_CSV.csv');
  print('Note: Janousek points outside 50 km buffer will have null embedding values.');
  setStatus('Step 4b: 4 tasks queued. Open Tasks panel to run each one.');
}


// ─────────────────────────────────────────────────────────────────
// STEP 1 — IMPORT RAW FIELD DATA (unchanged)
// ─────────────────────────────────────────────────────────────────
function step1_importRawData() {
  setStatus('Step 1: Loading WOSIS and CanPeat field data...');
  WOSIS_2023_Raw  = ee.FeatureCollection(WOSIS_ASSET);
  CanPeatData_Raw = ee.FeatureCollection(CANPEAT_ASSET);
  WOSIS_2023_Raw.size().evaluate(function(n)  { print('WOSIS_2023_Raw - count:', n); });
  CanPeatData_Raw.size().evaluate(function(n) { print('CanPeatData_Raw - count:', n); });
  Map.addLayer(WOSIS_2023_Raw,  { color: '1565c0' }, 'WOSIS_2023_Raw',  false);
  Map.addLayer(CanPeatData_Raw, { color: 'e65100' }, 'CanPeatData_Raw', false);
  markDone(0);
  setStatus('Step 1 complete.');
}


// ─────────────────────────────────────────────────────────────────
// STEP 2 — RASTER PRIORS  (v4.3: adds Sothe uncertainty)
// ─────────────────────────────────────────────────────────────────
function step2_importRasterPriors() {
  setStatus('Step 2: Loading raster priors...');

  // Sothe et al. carbon stocks
  sothe_fc = ee.ImageCollection('projects/sat-io/open-datasets/carbon_stocks_ca/fc')
    .first().clip(aoi).rename('sothe_fc');
  sothe_fc.bandNames().evaluate(function(n) { print('Sothe FC bands:', n); });

  sothe_sc = ee.ImageCollection('projects/sat-io/open-datasets/carbon_stocks_ca/sc')
    .first().clip(aoi).rename('sothe_sc');
  sothe_sc.bandNames().evaluate(function(n) { print('Sothe SC bands:', n); });

  // v4.3: Sothe uncertainty layers
  // select([0]) guards against multi-band assets; rename gives a predictable band name.
  sothe_fc_unc = ee.Image(SOTHE_FC_UNC_ASSET).select([0]).clip(aoi).rename('sothe_fc_unc');
  sothe_sc_unc = ee.Image(SOTHE_SC_UNC_ASSET).select([0]).clip(aoi).rename('sothe_sc_unc');
  sothe_fc_unc.bandNames().evaluate(function(n) { print('Sothe FC uncertainty band:', n); });
  sothe_sc_unc.bandNames().evaluate(function(n) { print('Sothe SC uncertainty band:', n); });

  // SoilGrids SOC + BDOD
  var sg_soc  = ee.Image('projects/soilgrids-isric/soc_mean').clip(aoi_buffer);
  var sg_bdod = ee.Image('projects/soilgrids-isric/bdod_mean').clip(aoi_buffer);
  sg_soc.bandNames().evaluate(function(n)  { print('SoilGrids SOC bands:',  n); });
  sg_bdod.bandNames().evaluate(function(n) { print('SoilGrids BDOD bands:', n); });

  // Per-depth OCS layers (kg/m2): SOC g/kg / 10 x BD kg/dm3 x thickness cm / 100
  var ocsLayer = function(socBand, bdBand, thickness) {
    return sg_soc.select(socBand).divide(10)
      .multiply(sg_bdod.select(bdBand).divide(100))
      .multiply(thickness).divide(100);
  };
  var ocs_0_5    = ocsLayer('soc_0-5cm_mean',    'bdod_0-5cm_mean',     5).rename('sg_ocs_0_5cm');
  var ocs_5_15   = ocsLayer('soc_5-15cm_mean',   'bdod_5-15cm_mean',   10).rename('sg_ocs_5_15cm');
  var ocs_15_30  = ocsLayer('soc_15-30cm_mean',  'bdod_15-30cm_mean',  15).rename('sg_ocs_15_30cm');
  var ocs_30_60  = ocsLayer('soc_30-60cm_mean',  'bdod_30-60cm_mean',  30).rename('sg_ocs_30_60cm');
  var ocs_60_100 = ocsLayer('soc_60-100cm_mean', 'bdod_60-100cm_mean', 40).rename('sg_ocs_60_100cm');

  sg_ocs_layers = ocs_0_5.addBands(ocs_5_15).addBands(ocs_15_30)
    .addBands(ocs_30_60).addBands(ocs_60_100).clip(aoi);

  sg_soc_1m = ocs_0_5.add(ocs_5_15).add(ocs_15_30).add(ocs_30_60).add(ocs_60_100)
    .rename('sg_soc_1m').clip(aoi);

  // Soil prior mean (retained for reference; not a direct ensemble member in v4.3)
  soil_prior_mean = sg_soc_1m.rename('sg')
    .addBands(sothe_sc.rename('sothe'))
    .reduce(ee.Reducer.mean()).rename('soil_prior_mean');

  var soil_diff = sothe_sc.subtract(sg_soc_1m).rename('sothe_minus_sg_soc');

  // SCANFI
  scanfi_img = ee.Image('projects/gcpm041u-lemur/assets/scanfi_v12/SCANFI_v1_2').clip(aoi);
  scanfi_img.bandNames().evaluate(function(n) {
    print('SCANFI v1.2 bands:', n);
    Map.addLayer(scanfi_img.select(n[0]),
      { min: 0, max: 200, palette: ['#f7f7f7', '#74c476', '#00441b'] },
      'SCANFI Biomass (' + n[0] + ')', false);
  });

  var soilVis   = { min: 0, max: 30, palette: ['#fff7bc', '#fe9929', '#993404'] };
  var forestVis = { min: 0, max: 20, palette: ['#f7fcf5', '#74c476', '#00441b'] };
  var diffVis   = { min: -10, max: 10, palette: ['#d73027', '#ffffbf', '#1a9850'] };
  var uncVis    = { min: 0,  max: 10, palette: ['#2166ac', '#f7f7f7', '#d6604d'] };

  addLayerWithStats(sg_soc_1m,      'sg_soc_1m',         soilVis,   'SoilGrids SOC 0-100 cm (kg/m2)',             aoi, 250);
  addLayerWithStats(sothe_sc,        'sothe_sc',           soilVis,   'Sothe et al. Soil Carbon (kg/m2)',            aoi, 250);
  addLayerWithStats(soil_prior_mean, 'soil_prior_mean',    soilVis,   'Soil Carbon Prior Mean (kg/m2)',              aoi, 250);
  addLayerWithStats(soil_diff,       'sothe_minus_sg_soc', diffVis,   'Soil Diff: Sothe - SoilGrids (kg/m2)',        aoi, 250);
  addLayerWithStats(sothe_fc,        'sothe_fc',           forestVis, 'Sothe et al. Forest Carbon (kg/m2)',          aoi, 250);

  // v4.3: visualise Sothe uncertainty
  addLayerWithStats(sothe_fc_unc, 'sothe_fc_unc', uncVis, 'Sothe Forest Carbon Uncertainty (kg/m2)', aoi, 250);
  addLayerWithStats(sothe_sc_unc, 'sothe_sc_unc', uncVis, 'Sothe Soil Carbon Uncertainty (kg/m2)',   aoi, 250);

  // Google Satellite Embedding V1 (v4.2, unchanged)
  var embedCol = ee.ImageCollection('GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL').filterBounds(aoi_buffer);
  if (EMBEDDING_YEAR !== null) {
    embedCol = embedCol.filter(ee.Filter.calendarRange(EMBEDDING_YEAR, EMBEDDING_YEAR, 'year'));
  }
  embed_img = embedCol.median().clip(aoi_buffer);
  embed_img.bandNames().size().evaluate(function(n) {
    print('Google Satellite Embedding V1 - bands: ' + n + ' | scale: ' + EMBED_SCALE + ' m');
  });

  markDone(1);
  setStatus('Step 2 complete - raster priors, Sothe uncertainty, and Google Embedding loaded.');
}


// ─────────────────────────────────────────────────────────────────
// STEP 3 — GEDI + CANOPY HEIGHT MODELS (unchanged)
// ─────────────────────────────────────────────────────────────────
function step3_importGEDI() {
  setStatus('Step 3: Loading GEDI L2A and L4A...');

  var l2a_col = ee.ImageCollection('LARSE/GEDI/GEDI02_A_002_MONTHLY')
    .filterDate(GEDI_START, GEDI_END).filterBounds(aoi_buffer)
    .map(function(img) {
      var q = img.select('quality_flag').eq(1).and(img.select('degrade_flag').eq(0));
      return img.select(['rh98']).updateMask(q);
    });

  gedi_l4a_col = ee.ImageCollection('LARSE/GEDI/GEDI04_A_002_MONTHLY')
    .filterDate(GEDI_START, GEDI_END).filterBounds(aoi_buffer)
    .select(['agbd', 'agbd_se', 'l4_quality_flag', 'degrade_flag']);

  l2a_col.size().evaluate(function(n)      { print('GEDI L2A images in buffer:', n); });
  gedi_l4a_col.size().evaluate(function(n) { print('GEDI L4A images in buffer:', n); });

  gedi_l2a     = l2a_col.median().clip(aoi);
  gedi_agbd_se = gedi_l4a_col.select('agbd_se').mean().multiply(0.1).rename('agbd_se_kgm2').clip(aoi);

  var shot_density = l2a_col
    .map(function(img) { return img.select('rh98').mask().rename('shot'); })
    .sum().rename('gedi_shot_density').clip(aoi);

  printStats(gedi_l2a, 'rh98', aoi, 25, 'GEDI L2A rh98 Canopy Height (m)');

  sothe_ch = ee.ImageCollection('projects/sat-io/open-datasets/carbon_stocks_ca/ch')
    .filterBounds(aoi_buffer).first().clip(aoi);
  var sothe_ch_b1 = sothe_ch.select([0]).rename('sothe_ch');

  meta_ch = ee.ImageCollection('projects/sat-io/open-datasets/facebook/meta-canopy-height')
    .filterBounds(aoi_buffer).mosaic()
    .reproject({ crs: EXPORT_CRS, scale: EXPORT_SCALE }).clip(aoi).rename('meta_ch');

  scanfi_ch = scanfi_img.select('height').rename('scanfi_ch');

  printStats(sothe_ch_b1, 'sothe_ch',  aoi, 25, 'Sothe Canopy Height Model (m)');
  printStats(meta_ch,     'meta_ch',   aoi, 25, 'Meta Canopy Height Model (m)');
  printStats(scanfi_ch,   'scanfi_ch', aoi, 25, 'SCANFI Canopy Height (m)');

  var gedi_rh98 = gedi_l2a.select('rh98');
  var printMeanDiff = function(chm, chmBand, label) {
    chm.select(chmBand).subtract(gedi_rh98).rename('diff')
      .reduceRegion({
        reducer: ee.Reducer.mean(), geometry: aoi,
        scale: EXPORT_SCALE, crs: EXPORT_CRS, maxPixels: 1e11, bestEffort: true
      }).evaluate(function(r) {
        print(label + ' vs GEDI rh98 - mean diff (m): ' +
          (r['diff'] !== undefined ? r['diff'].toFixed(3) : 'null'));
      });
  };
  printMeanDiff(sothe_ch_b1, 'sothe_ch',  'Sothe CHM');
  printMeanDiff(meta_ch,     'meta_ch',   'Meta CHM');
  printMeanDiff(scanfi_ch,   'scanfi_ch', 'SCANFI CHM');

  var htVis = { min: 0, max: 30, palette: ['#f7fcb9', '#addd8e', '#31a354', '#006837'] };
  Map.addLayer(gedi_l2a.select('rh98'), htVis, 'GEDI L2A Canopy Height rh98 (m)', false);
  Map.addLayer(sothe_ch_b1, htVis, 'Sothe Canopy Height Model (m)',  false);
  Map.addLayer(meta_ch,     htVis, 'Meta Canopy Height Model (m)',   false);
  Map.addLayer(scanfi_ch,   htVis, 'SCANFI Canopy Height (m)',       false);
  Map.addLayer(shot_density, { min: 0, max: 50, palette: ['#ffffcc', '#c7e9b4', '#0c2c84'] },
    'GEDI Shot Density', false);

  markDone(2);
  setStatus('Step 3 complete - GEDI and CHMs loaded.');
}


// ─────────────────────────────────────────────────────────────────
// STEP 4 — BUILD COVARIATE STACK + PILOT RF
// v4.3: HEGL_BANDS updated to sothe_sc_covariate
// ─────────────────────────────────────────────────────────────────
function step4_buildCovariates() {
  if (!gedi_l2a) { setStatus('Run Step 3 first - GEDI rh98 not available.'); return; }
  setStatus('Step 4: Building covariate stack...');

  var dem    = ee.Image('NASA/NASADEM_HGT/001').select('elevation');
  var slope  = ee.Terrain.slope(dem);
  var aspect = ee.Terrain.aspect(dem);
  var twi    = slope.multiply(Math.PI / 180).tan().max(ee.Image(0.001)).pow(-1).log().rename('twi');
  var dem_focal = dem.reduceNeighborhood({
    reducer: ee.Reducer.mean(), kernel: ee.Kernel.circle({ radius: 500, units: 'meters' })
  });
  var tpi = dem.subtract(dem_focal).rename('tpi');

  var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    .filterBounds(aoi_buffer).filterDate(S2_START, S2_END)
    .filter(ee.Filter.calendarRange(6, 9, 'month'))
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
    .map(function(img) {
      var qa   = img.select('QA60');
      var mask = qa.bitwiseAnd(1 << 10).eq(0).and(qa.bitwiseAnd(1 << 11).eq(0));
      return img.updateMask(mask).divide(10000).copyProperties(img, ['system:time_start']);
    }).median();

  var ndvi = s2.normalizedDifference(['B8', 'B4']).rename('ndvi');
  var ndwi = s2.normalizedDifference(['B3', 'B8']).rename('ndwi');
  var nbr  = s2.normalizedDifference(['B8', 'B12']).rename('nbr');
  var evi  = s2.expression('2.5*((NIR-RED)/(NIR+6*RED-7.5*BLUE+1))',
    { NIR: s2.select('B8'), RED: s2.select('B4'), BLUE: s2.select('B2') }).rename('evi');

  var climate = ee.ImageCollection('IDAHO_EPSCOR/TERRACLIMATE')
    .filterBounds(aoi_buffer).filterDate(TC_START, TC_END)
    .select(['tmmn', 'tmmx', 'pr', 'soil']).mean();

  setStatus('Step 4: Building SAR composites...');
  var sar = buildSARComposites();

  var grid_fe = ee.FeatureCollection(
    'projects/sat-io/open-datasets/CA_FOREST/CA_SBFI/GRID_forested_ecosystems');

  sbfi_agb_raster = grid_fe.filter(ee.Filter.notNull(['STRUCTURE_AGB_AVG']))
    .reduceToImage({ properties: ['STRUCTURE_AGB_AVG'], reducer: ee.Reducer.first() })
    .rename('sbfi_agb_avg')
    .addBands(
      grid_fe.filter(ee.Filter.notNull(['STRUCTURE_AGB_SD']))
        .reduceToImage({ properties: ['STRUCTURE_AGB_SD'], reducer: ee.Reducer.first() })
        .rename('sbfi_agb_sd')
    )
    .reproject({ crs: EXPORT_CRS, scale: EXPORT_SCALE }).clip(aoi);

  sbfi_agb_raster.bandNames().evaluate(function(n) { print('SBFI rasterised bands:', n); });
  Map.addLayer(grid_fe, { color: '888888' }, 'SBFI Grid Forested Ecosystems (vector)', false);

  var lead_species = ee.Image('projects/sat-io/open-datasets/CA_FOREST/LEAD_TREE_SPECIES')
    .rename('lead_tree_species').clip(aoi_buffer);

  var candidate = dem.rename('elevation')
    .addBands(slope.rename('slope')).addBands(aspect.rename('aspect'))
    .addBands(twi).addBands(tpi)
    .addBands(ndvi).addBands(ndwi).addBands(nbr).addBands(evi)
    .addBands(s2.select(['B2', 'B3', 'B4', 'B8', 'B11', 'B12']))
    .addBands(climate.select('tmmn').rename('tmmn'))
    .addBands(climate.select('tmmx').rename('tmmx'))
    .addBands(climate.select('pr').rename('map'))
    .addBands(climate.select('soil').rename('soil_moisture'))
    .addBands(sar.asc_spring.select('VV').rename('sar_asc_spr_vv'))
    .addBands(sar.asc_spring.select('VH').rename('sar_asc_spr_vh'))
    .addBands(sar.asc_summer.select('VV').rename('sar_asc_sum_vv'))
    .addBands(sar.asc_summer.select('VH').rename('sar_asc_sum_vh'))
    .addBands(sar.asc_change.rename('sar_asc_vv_change'))
    .addBands(sbfi_agb_raster.select('sbfi_agb_avg'))
    .addBands(sbfi_agb_raster.select('sbfi_agb_sd'))
    .addBands(lead_species)
    .reproject({ crs: EXPORT_CRS, scale: EXPORT_SCALE });

  setStatus('Step 4: Checking band coverage over AOI...');

  candidate.reduceRegion({
    reducer: ee.Reducer.count(), geometry: aoi,
    scale: EXPORT_SCALE, crs: EXPORT_CRS, maxPixels: 1e11, bestEffort: true
  }).evaluate(function(counts) {
    var allBands = candidate.bandNames().getInfo();
    var goodBands = [], deadBands = [];
    allBands.forEach(function(b) {
      if (counts[b] && counts[b] > 0) { goodBands.push(b); } else { deadBands.push(b); }
    });
    print('COVARIATE COVERAGE: ' + goodBands.length + '/' + allBands.length + ' bands with data');
    if (deadBands.length > 0) { print('DROPPED bands:', deadBands); }

    var coreBands   = ['elevation', 'ndvi', 'B8'];
    var missingCore = coreBands.filter(function(b) { return goodBands.indexOf(b) === -1; });
    if (missingCore.length > 0) {
      setStatus('Core bands missing: ' + missingCore.join(', ') + ' - cannot proceed.'); return;
    }

    covariates        = candidate.select(goodBands);
    covariates_filled = covariates.unmask(-9999);
    COV_BANDS         = ee.List(goodBands);
    COV_BANDS_CLIENT  = goodBands;

    // v4.3: sothe_sc_covariate replaces tl_soc_covariate
    HEGL_BANDS = COV_BANDS.cat(ee.List(['sothe_sc_covariate', 'depth_cm']));

    print('Final covariate stack (' + goodBands.length + ' bands):', goodBands);
    covariates.projection().evaluate(function(p) { print('Covariate projection:', p); });

    Map.addLayer(ndvi.clip(aoi),
      { min: -0.1, max: 0.9, palette: ['#d73027', '#ffffbf', '#1a9850'] },
      'NDVI (S2 Summer Median)', false);
    Map.addLayer(covariates.select('twi').clip(aoi),
      { min: 0, max: 10, palette: ['#ffffcc', '#41b6c4', '#0c2c84'] }, 'TWI', false);
    Map.addLayer(covariates.select('tpi').clip(aoi),
      { min: -30, max: 30, palette: ['#4575b4', '#ffffbf', '#d73027'] }, 'TPI', false);

    _step4_pilotRF(goodBands);
  });
}

function _step4_pilotRF(goodBands) {
  var gedi_raw = ee.ImageCollection('LARSE/GEDI/GEDI04_A_002_MONTHLY')
    .filterDate(GEDI_START, GEDI_END).filterBounds(aoi_buffer)
    .map(function(img) {
      var quality = img.select('l4_quality_flag').eq(1).and(img.select('degrade_flag').eq(0));
      return img.select(['agbd', 'agbd_se']).updateMask(quality);
    });

  var sampled = gedi_raw.median().select('agbd').addBands(covariates)
    .sample({
      region: aoi_buffer, scale: GEDI_SAMPLE_SCALE, numPixels: GEDI_NUM_PIXELS,
      seed: 42, tileScale: 4, geometries: true, dropNulls: true
    }).filter(ee.Filter.gt('agbd', 0)).filter(ee.Filter.lt('agbd', 600));

  sampled.size().evaluate(function(nPoints) {
    print('GEDI L4A training points (0 < agbd < 600):', nPoints);
    if (nPoints === 0) { setStatus('No GEDI L4A points found. Check date range or AOI buffer.'); return; }

    var trainingSamples;
    if (nPoints < MIN_GEDI_POINTS) {
      print('Low density (' + nPoints + ' pts) - buffering shots by 500 m.');
      var buffered = sampled.map(function(f) { return f.buffer(500); });
      trainingSamples = covariates.select(goodBands).sampleRegions({
        collection: buffered, properties: ['agbd'], scale: EXPORT_SCALE, tileScale: 4
      }).filter(ee.Filter.notNull(goodBands)).filter(ee.Filter.gt('agbd', 0));
    } else {
      trainingSamples = sampled.filter(ee.Filter.notNull(goodBands));
    }
    print('Training samples (complete cases):', trainingSamples.size());
    setStatus('Step 4: Training pilot RF (' + PILOT_N_TREES + ' trees, ' + goodBands.length + ' bands)...');

    var goodBandsEE = ee.List(goodBands);
    var pilotRF = ee.Classifier.smileRandomForest({
      numberOfTrees: PILOT_N_TREES, minLeafPopulation: 5, bagFraction: 0.632, seed: 42
    }).setOutputMode('REGRESSION')
      .train({ features: trainingSamples, classProperty: 'agbd', inputProperties: goodBandsEE });

    var importanceDict = ee.Dictionary(pilotRF.explain().get('importance'));
    var sorted = ee.FeatureCollection(
      importanceDict.keys().map(function(key) {
        return ee.Feature(null, { band: key, importance: importanceDict.getNumber(key) });
      })
    ).sort('importance', false);

    sorted.limit(TOP_N_BANDS).aggregate_array('band').evaluate(function(topBands) {
      if (!topBands || topBands.length === 0) { setStatus('Variable selection returned no bands.'); return; }

      importanceDict.evaluate(function(impObj) {
        var chartData = [];
        for (var b in impObj) { chartData.push({ band: b, importance: impObj[b] }); }
        chartData.sort(function(a, b) { return b.importance - a.importance; });
        var chartFC = ee.FeatureCollection(chartData.map(function(d) {
          return ee.Feature(null, { band: d.band, importance: d.importance });
        }));
        print(ui.Chart.feature.byFeature(chartFC, 'band', 'importance').setChartType('BarChart')
          .setOptions({
            title: 'Pilot RF - Variable Importance (all ' + goodBands.length + ' bands)',
            hAxis: { title: 'Importance (Gini)' }, vAxis: { title: 'Band' },
            legend: 'none', colors: ['#2E7D32'], bar: { groupWidth: '80%' }
          }));
      });

      print('Variable selection - top ' + topBands.length + ' bands:');
      topBands.forEach(function(b) { print('  ' + b); });

      TOP_BANDS_CLIENT = topBands;
      TOP_BANDS_EE     = ee.List(topBands);
      gedi_training    = trainingSamples;

      markDone(3);
      insertSnapshotButton();
    });
  });
}


// ─────────────────────────────────────────────────────────────────
// STEP 5 — TRAIN FINAL AGBD MODEL (unchanged)
// ─────────────────────────────────────────────────────────────────
function step5_trainFinalGEDI() {
  if (!covariates)    { setStatus('Run Step 4 first - covariates not built.'); return; }
  if (!TOP_BANDS_EE)  { setStatus('Run Step 4 first - variable selection not complete.'); return; }
  if (!gedi_training) { setStatus('Run Step 4 first - GEDI training data not loaded.'); return; }
  setStatus('Step 5: Training final RF (' + FINAL_N_TREES + ' trees, top ' + TOP_N_BANDS + ' bands)...');

  gedi_training.aggregate_stats('agbd').evaluate(function(s) {
    print('GEDI AGBD training distribution (Mg/ha): n=' + s.total_count +
          ' mean=' + s.mean.toFixed(2) + ' sd=' + s.total_sd.toFixed(2));
  });

  var finalRF = ee.Classifier.smileRandomForest({
    numberOfTrees: FINAL_N_TREES, minLeafPopulation: 5, bagFraction: 0.632, seed: 42
  }).setOutputMode('REGRESSION')
    .train({ features: gedi_training, classProperty: 'agbd', inputProperties: TOP_BANDS_EE });

  ee.Dictionary(finalRF.explain().get('importance')).evaluate(function(impObj) {
    var chartData = [];
    for (var b in impObj) { chartData.push({ band: b, importance: impObj[b] }); }
    chartData.sort(function(a, bv) { return bv.importance - a.importance; });
    var chartFC = ee.FeatureCollection(chartData.map(function(d) {
      return ee.Feature(null, { band: d.band, importance: d.importance });
    }));
    print(ui.Chart.feature.byFeature(chartFC, 'band', 'importance').setChartType('BarChart')
      .setOptions({
        title: 'Final RF (' + FINAL_N_TREES + ' trees) - Variable Importance',
        hAxis: { title: 'Importance (Gini)' }, vAxis: { title: 'Band' },
        legend: 'none', colors: ['#1565C0'], bar: { groupWidth: '80%' }
      }));
  });

  var agbd_mgha = covariates.select(TOP_BANDS_EE).classify(finalRF).clip(aoi).rename('agbd_mgha');
  agbd_mgha     = agbd_mgha.updateMask(agbd_mgha.gte(0).and(agbd_mgha.lte(600)));
  agbd_modeled  = agbd_mgha.rename('agbd_modeled');
  forest_rf_pred = agbd_mgha.multiply(0.1).rename('forest_carbon_kgm2');

  agbd_mgha.reduceRegion({
    reducer: ee.Reducer.mean().combine(ee.Reducer.min(), null, true)
              .combine(ee.Reducer.max(), null, true).combine(ee.Reducer.stdDev(), null, true),
    geometry: aoi, scale: EXPORT_SCALE, crs: EXPORT_CRS, maxPixels: 1e11, bestEffort: true
  }).evaluate(function(r) {
    var f = function(k) { return r[k] !== undefined ? r[k].toFixed(2) : 'null'; };
    print('Forest RF: mean=' + f('agbd_mgha_mean') + ' min=' + f('agbd_mgha_min') +
          ' max=' + f('agbd_mgha_max') + ' sd=' + f('agbd_mgha_stdDev') + ' Mg/ha');
  });

  Map.addLayer(agbd_mgha, AGBD_VIS, 'AGBD - Final RF (Mg/ha)');
  addLayerWithStats(forest_rf_pred, 'forest_carbon_kgm2',
    { min: 0, max: 20, palette: ['#f7fcf5', '#74c476', '#00441b'] },
    'Forest Carbon - GEDI RF (kg/m2)');
  Map.addLayer(gedi_agbd_se,
    { min: 0, max: 5, palette: ['#ffffcc', '#fd8d3c', '#800026'] },
    'GEDI AGBD SE (kg/m2)', false);

  Export.image.toDrive({
    image: agbd_mgha.toFloat(), description: 'AGBD_RF_Top6_Extrapolation_MgHa',
    folder: EXPORT_FOLDER, region: aoi, scale: EXPORT_SCALE, crs: EXPORT_CRS, maxPixels: 1e13
  });

  markDone(4);
  setStatus('Step 5 complete - final RF trained on top ' + TOP_BANDS_CLIENT.length + ' bands. Export queued.');
}


// ─────────────────────────────────────────────────────────────────
// STEP 6 — SOIL DATA CHECK  (v4.4: RF training removed)
//
//   No model is trained here. Step 6 now simply confirms that
//   sothe_sc and sg_soc_1m (loaded in Step 2) are ready for the
//   two-member ensemble in Step 7.
//
//   Rationale: adding a GEE-trained RF as a third ensemble member
//   introduces an opaque, data-limited error source at this AOI
//   scale. The Sothe et al. + SoilGrids pairing already represents
//   two independently-derived 1 m SOC products; the ensemble SD
//   between them is a more interpretable disagreement signal than
//   out-of-bag RF error, and the per-pixel Sothe uncertainty layer
//   captures remaining product uncertainty. Step 7 propagates both
//   via RSS to produce the combined soil uncertainty image used in
//   Neyman allocation.
// ─────────────────────────────────────────────────────────────────
function step6_buildSoilModel() {
  if (!sothe_sc)  { setStatus('Run Step 2 first - Sothe SC not loaded.'); return; }
  if (!sg_soc_1m) { setStatus('Run Step 2 first - SoilGrids 1 m not loaded.'); return; }

  print('Step 6: Soil ensemble will use Sothe et al. (2022) and SoilGrids v2.0 (0-100 cm).');
  print('  Sothe SC:   national soil carbon map, 250 m (kg/m2)');
  print('  SoilGrids:  depth-integrated OCS 0-100 cm, 250 m (kg/m2)');
  print('  Ensemble mean + SD computed in Step 7.');
  print('  Combined uncertainty: sqrt(sothe_sc_unc^2 + ensemble_SD^2)');

  // Visualise both source layers so you can sanity-check agreement
  var soilVis = { min: 0, max: 30, palette: ['#fff7bc', '#fe9929', '#993404'] };
  addLayerWithStats(sothe_sc,  'sothe_sc',  soilVis, 'Sothe SC - soil source 1 (kg/m2)', aoi, 250);
  addLayerWithStats(sg_soc_1m, 'sg_soc_1m', soilVis, 'SoilGrids 0-100 cm - soil source 2 (kg/m2)', aoi, 250);

  // Difference map: shows where the two products disagree spatially.
  // High |diff| pixels will drive the Neyman allocation once ensemble SD
  // is folded into combined uncertainty in Step 7.
  var diff = sothe_sc.subtract(sg_soc_1m).rename('sothe_minus_sg');
  Map.addLayer(diff, { min: -15, max: 15, palette: ['#d73027', '#ffffbf', '#1a9850'] },
    'Soil Source Diff: Sothe - SoilGrids (kg/m2)', false);
  printStats(diff, 'sothe_minus_sg', aoi, 250, 'Soil Source Diff: Sothe - SoilGrids (kg/m2)');

  markDone(5);
  setStatus('Step 6 complete - soil sources verified. Run Step 7 to build ensemble.');
}


// ─────────────────────────────────────────────────────────────────
// STEP 7 — BUILD ENSEMBLE MODELS  (v4.4: soil RF removed)
//
//   Forest ensemble: unchanged (GEDI RF + Sothe FC + SBFI, 3 members).
//   Forest uncertainty = sqrt(ensemble_SD^2 + sothe_fc_unc^2).
//
//   Soil ensemble: 2-member (Sothe SC + SoilGrids 0-100 cm).
//   Soil ensemble mean   = equal-weight mean of the two products.
//   Soil ensemble SD     = inter-product disagreement (σ_disagree).
//   Soil combined unc    = sqrt(sothe_sc_unc^2 + σ_disagree^2).
//
//   The RSS formulation treats the per-pixel Sothe product uncertainty
//   and the inter-product disagreement as independent error sources —
//   a conservative assumption appropriate for a KBA assessment.
//   Pixels where the two products disagree most will receive the
//   highest combined uncertainty, and therefore the most sampling
//   effort under Neyman allocation in Step 8.
// ─────────────────────────────────────────────────────────────────
function step7_buildEnsemble() {
  if (!forest_rf_pred)  { setStatus('Run Step 5 first - forest model missing.'); return; }
  if (!sothe_sc)        { setStatus('Run Step 2 first - Sothe SC not loaded.'); return; }
  if (!sg_soc_1m)       { setStatus('Run Step 2 first - SoilGrids 1 m not loaded.'); return; }
  if (!sothe_fc)        { setStatus('Run Step 2 first - Sothe FC not loaded.'); return; }
  if (!sothe_fc_unc)    { setStatus('Run Step 2 first - Sothe FC uncertainty missing.'); return; }
  if (!sothe_sc_unc)    { setStatus('Run Step 2 first - Sothe SC uncertainty missing.'); return; }
  if (!sbfi_agb_raster) { setStatus('Run Step 4 first - SBFI not rasterised.'); return; }
  setStatus('Step 7: Building forest ensemble...');

  // ── Forest ensemble: GEDI RF + Sothe FC + SBFI (unchanged) ─────
  var sbfi_kgm2 = sbfi_agb_raster.select('sbfi_agb_avg').multiply(0.1).rename('sbfi_fc').clip(aoi);

  var forest_ensemble = forest_rf_pred.rename('gedi_rf')
    .addBands(sothe_fc.rename('sothe_fc'))
    .addBands(sbfi_kgm2.rename('sbfi_fc'));

  var f_count = forest_ensemble.reduce(ee.Reducer.count()).rename('f_model_count');
  var f_mask  = f_count.gte(2);

  forest_ens_mean = forest_ensemble.reduce(ee.Reducer.mean()).updateMask(f_mask).rename('forest_ens_mean');
  forest_ens_sd   = forest_ensemble.reduce(ee.Reducer.stdDev()).updateMask(f_mask).rename('forest_ens_sd');

  dsm_forest     = ee.Image(1).where(forest_rf_pred.mask().not(), ee.Image(2)).clip(aoi).rename('forest_data_source');
  forest_nf_mask = forest_ens_mean.gt(FOREST_THRESHOLD);

  // Blend ensemble SD with GEDI footprint-level SE
  var gedi_se_pct = gedi_agbd_se.divide(forest_ens_mean.abs().add(0.001));
  var raw_f_sd    = forest_ens_sd.where(gedi_agbd_se.mask(), forest_ens_sd.add(gedi_se_pct).divide(2));

  // RSS of model-spread SD and Sothe FC product uncertainty
  forest_uncertainty = raw_f_sd.pow(2).add(sothe_fc_unc.pow(2))
    .sqrt().updateMask(f_mask).rename('forest_uncertainty_combined');

  setStatus('Step 7: Building soil ensemble (Sothe SC + SoilGrids)...');

  // ── Soil ensemble: Sothe SC + SoilGrids 0-100 cm (2 members) ───
  // Two independently-derived national products at matching 250 m
  // resolution. The ensemble SD is a direct measure of where the two
  // products disagree — the most interpretable disagreement signal
  // available without fitting a local model.
  var soil_stack = sothe_sc.rename('sothe')
    .addBands(sg_soc_1m.rename('soilgrids'));

  var s_count = soil_stack.reduce(ee.Reducer.count()).rename('s_model_count');
  var s_mask  = s_count.gte(2);

  soil_ens_mean = soil_stack.reduce(ee.Reducer.mean()).updateMask(s_mask).rename('soil_ens_mean');
  soil_ens_sd   = soil_stack.reduce(ee.Reducer.stdDev()).updateMask(s_mask).rename('soil_ens_sd');

  // Combined uncertainty: RSS of inter-product disagreement and
  // per-pixel Sothe product uncertainty.
  // sothe_sc_unc is asymmetric in principle, but treating it as
  // symmetric (1 SD) is standard for RSS propagation.
  soil_uncertainty = sothe_sc_unc.pow(2).add(soil_ens_sd.pow(2))
    .sqrt().updateMask(s_mask).rename('soil_uncertainty_combined');

  // Data-source map: 1=both available, 2=SoilGrids only, 3=Sothe only
  dsm_soil = ee.Image(1)
    .where(sothe_sc.mask().not(), ee.Image(2))
    .where(sg_soc_1m.mask().not(), ee.Image(3))
    .where(sothe_sc.mask().not().and(sg_soc_1m.mask().not()), ee.Image(4))
    .clip(aoi).rename('soil_data_source');

  total_ecosystem_c = forest_ens_mean.add(soil_ens_mean).rename('total_ecosystem_c_kgm2');

  // Validate pixel counts
  forest_uncertainty.reduceRegion({
    reducer: ee.Reducer.count(), geometry: aoi, scale: EXPORT_SCALE, crs: EXPORT_CRS,
    maxPixels: 1e11, bestEffort: true
  }).evaluate(function(r) { print('Valid forest uncertainty pixels:', r['forest_uncertainty_combined'] || 0); });
  soil_uncertainty.reduceRegion({
    reducer: ee.Reducer.count(), geometry: aoi, scale: EXPORT_SCALE, crs: EXPORT_CRS,
    maxPixels: 1e11, bestEffort: true
  }).evaluate(function(r) { print('Valid soil uncertainty pixels:', r['soil_uncertainty_combined'] || 0); });

  var carbonVis = { min: 0, max: 20, palette: ['#f7f7f7', '#2ca25f', '#006837'] };
  var sdVis     = { min: 0, max: 5,  palette: ['#2166ac', '#f7f7f7', '#d6604d'] };
  var uncVis    = { min: 0, max: 10, palette: ['#2166ac', '#f7f7f7', '#d6604d'] };
  var totalVis  = { min: 0, max: 50, palette: ['#f7f7f7', '#2ca25f', '#006837'] };

  Map.addLayer(forest_ens_mean,    carbonVis, 'Forest Ensemble Mean (kg/m2)',        false);
  Map.addLayer(forest_ens_sd,      sdVis,     'Forest Ensemble SD (kg/m2)',          false);
  Map.addLayer(forest_uncertainty, uncVis,    'Forest Uncertainty Combined (kg/m2)', false);
  Map.addLayer(sothe_fc_unc,       uncVis,    'Sothe FC Uncertainty (kg/m2)',        false);
  Map.addLayer(soil_ens_mean,      carbonVis, 'Soil Ensemble Mean - Sothe+SoilGrids (kg/m2)', true);
  Map.addLayer(soil_ens_sd,        sdVis,     'Soil Disagreement SD (kg/m2)',        false);
  Map.addLayer(soil_uncertainty,   uncVis,    'Soil Uncertainty Combined (kg/m2)',   true);
  Map.addLayer(sothe_sc_unc,       uncVis,    'Sothe SC Uncertainty (kg/m2)',        false);
  Map.addLayer(total_ecosystem_c,  totalVis,  'Total Ecosystem Carbon (kg/m2)',      false);
  Map.addLayer(dsm_forest, { min: 1, max: 2, palette: ['#2ca25f', '#feb24c'] },
    'Forest Data Source (1=GEDI RF, 2=Sothe FC)', false);
  Map.addLayer(dsm_soil, { min: 1, max: 4, palette: ['#2ca25f', '#feb24c', '#de2d26', '#969696'] },
    'Soil Data Source (1=Both, 2=SoilGrids only, 3=Sothe only, 4=Neither)', false);
  Map.addLayer(forest_nf_mask, { min: 0, max: 1, palette: ['#ffffff', '#006837'] },
    'Forest / Non-Forest Mask', false);

  printStats(forest_ens_mean,    'forest_ens_mean',             aoi, 25,  'Forest Ensemble Mean (kg/m2)');
  printStats(forest_uncertainty, 'forest_uncertainty_combined', aoi, 25,  'Forest Uncertainty Combined (kg/m2)');
  printStats(soil_ens_mean,      'soil_ens_mean',               aoi, 250, 'Soil Ensemble Mean (kg/m2)');
  printStats(soil_ens_sd,        'soil_ens_sd',                 aoi, 250, 'Soil Disagreement SD (kg/m2)');
  printStats(sothe_sc_unc,       'sothe_sc_unc',                aoi, 250, 'Sothe SC Uncertainty (kg/m2)');
  printStats(soil_uncertainty,   'soil_uncertainty_combined',   aoi, 250, 'Soil Uncertainty Combined (kg/m2)');
  printStats(total_ecosystem_c,  'total_ecosystem_c_kgm2',      aoi, 25,  'Total Ecosystem Carbon (kg/m2)');

  markDone(6);
  setStatus('Step 7 complete - forest + soil ensembles built. Soil: Sothe SC + SoilGrids, RSS uncertainty.');
}


// ─────────────────────────────────────────────────────────────────
// STEP 8 — NEYMAN-ALLOCATION STRATIFIED SAMPLING  (v4.4)
//
// Two stratification dimensions per pool:
//
//   1. ESA WorldCover v200 (10 m) reclassified and reprojected to
//      EXPORT_SCALE. Five broad LC types:
//        1 = Forest/tree cover  (class 10)
//        2 = Shrub/Grassland    (classes 20, 30, 100)
//        3 = Wetland            (classes 90, 95)
//        4 = Cropland           (class 40)
//        5 = Other/barren       (classes 50, 60, 70)
//        0 = Open water (class 80) -- excluded from sampling
//
//   2. Uncertainty quantile bin (0 = lowest, N_UNC_BINS-1 = highest).
//      Breaks computed from p25/p50/p75 of the combined uncertainty
//      image within the sampling domain.
//
//   Composite stratum key = lc_class x N_UNC_BINS + unc_bin.
//   For N_UNC_BINS=4: valid strata 4..23 (lc 1-5, bin 0-3).
//   Keys 0-3 (lc=0, water) are excluded in the allocation loop.
//
// Neyman optimal allocation:
//   n_h = n_total x (N_h x sigma_h) / sum(N_j x sigma_j)
//   N_h = exact pixel count from frequencyHistogram (reduceRegion).
//   sigma_h = bin-midpoint estimate from p25/p50/p75 breaks (Step 1).
//   Both computed via server-side reduceRegion; no FeatureCollection
//   evaluate() call, no timeout risk, deterministic across runs.
//   Floor: MIN_PTS_PER_STRATUM per occupied stratum.
//
// Forest sampling: uncertainty and LC masked to forest_nf_mask.
// Soil sampling:   uncertainty and LC over full AOI.
// Both called via _neymanSample() independently.
// ─────────────────────────────────────────────────────────────────
function step8_generateSampling() {
  if (!forest_uncertainty) { setStatus('Run Step 7 first - forest uncertainty missing.'); return; }
  if (!soil_uncertainty)   { setStatus('Run Step 7 first - soil uncertainty missing.');   return; }
  if (!forest_nf_mask)     { setStatus('Run Step 7 first - forest mask missing.');        return; }
  setStatus('Step 8: Loading ESA WorldCover land-cover strata...');

  // ESA WorldCover v200: reproject to EXPORT_SCALE before reclassification
  // so that pixel boundaries align with the covariate grid.
  var worldcover = ee.ImageCollection('ESA/WorldCover/v200')
    .first()
    .reproject({ crs: EXPORT_CRS, scale: EXPORT_SCALE })
    .clip(aoi);

  // Reclassify; open water maps to 0 (excluded).
  var lc_broad = worldcover.remap(
    [10,  20,  30,  40,  50,  60,  70,  80,  90,  95, 100],
    [ 1,   2,   2,   4,   5,   5,   5,   0,   3,   3,   2]
  ).rename('lc_class').toInt();

  // Mask out 0 (water/unclassified) so those pixels cannot be sampled.
  lc_broad = lc_broad.updateMask(lc_broad.gt(0));

  Map.addLayer(lc_broad, {
    min: 1, max: 5, palette: ['#006837', '#addd8e', '#41b6c4', '#fec44f', '#bdbdbd']
  }, 'ESA WorldCover - Broad LC (1=Forest 2=Shrub/Grass 3=Wetland 4=Crop 5=Other)', false);

  // Extra bands to carry through to sampled points
  var forestExtras = forest_ens_mean.unmask(0)
    .addBands(forest_ens_sd.unmask(0))
    .addBands(forest_uncertainty.unmask(0))
    .addBands(dsm_forest)
    .addBands(lc_broad);

  var soilExtras = soil_ens_mean.unmask(0)
    .addBands(soil_ens_sd.unmask(0))
    .addBands(soil_uncertainty.unmask(0))
    .addBands(dsm_soil)
    .addBands(lc_broad);

  // Forest: apply forest_nf_mask to both uncertainty and LC images
  var forest_unc_masked = forest_uncertainty.updateMask(forest_nf_mask);
  var lc_forest_masked  = lc_broad.updateMask(forest_nf_mask);

  _neymanSample(
    forest_unc_masked, 'forest_uncertainty_combined',
    lc_forest_masked,  'lc_class',
    forestExtras, N_FOREST_SAMPLES, 'Forest',
    function(pts) {
      forest_sampling_pts = pts;
      pts.size().evaluate(function(n) {
        Map.addLayer(pts, { color: '1565c0' }, 'Forest Sampling - Neyman (' + n + ')', false);
        print('Forest Neyman sampling complete: ' + n + ' points.');
      });
    }
  );

  // Soil: sample over full AOI
  _neymanSample(
    soil_uncertainty, 'soil_uncertainty_combined',
    lc_broad,         'lc_class',
    soilExtras, N_SOIL_SAMPLES, 'Soil',
    function(pts) {
      soil_sampling_pts = pts;
      pts.size().evaluate(function(n) {
        Map.addLayer(pts, { color: 'e65100' }, 'Soil Sampling - Neyman (' + n + ')', false);
        print('Soil Neyman sampling complete: ' + n + ' points.');
        markDone(7);
        setStatus('Step 8 complete - Neyman-allocated forest + soil sampling points generated.');
      });
    }
  );

  // Power analysis runs in parallel with sampling (independent of sample output)
  _powerAnalysis();
}

// ─────────────────────────────────────────────────────────────────
// _neymanSample — Neyman optimal allocation helper
//
// Algorithm:
//   1. Compute p25/p50/p75 quantile breaks from unc_img client-side.
//   2. Build composite stratum image = lc_class x N_UNC_BINS + unc_bin.
//   3. Draw NEYMAN_DIAG_N pixels at 2x EXPORT_SCALE to estimate
//      N_h (pixel count proxy) and sigma_h (mean uncertainty) per stratum.
//   4. Neyman weights: n_h = n_total x (N_h sigma_h) / sum(N_j sigma_j).
//      Apply MIN_PTS_PER_STRATUM floor. Skip strata with N_h = 0.
//   5. Pass classValues/classPoints to stratifiedSample.
//
// Arguments:
//   unc_img    - ee.Image, single masked uncertainty band
//   unc_band   - string, band name in unc_img
//   lc_img     - ee.Image, single masked LC class band (values 1-5)
//   lc_band    - string, band name in lc_img
//   extra_bands- ee.Image, additional bands to carry through to points
//   n_total    - integer, total sample budget
//   pool_label - string, 'Forest' or 'Soil' (for console output)
//   callback   - function(ee.FeatureCollection), called with final pts
// ─────────────────────────────────────────────────────────────────
// ─────────────────────────────────────────────────────────────────
// _neymanSample — Neyman optimal allocation helper  (v4.4 rewrite)
//
// Algorithm:
//   1. Compute p25/p50/p75 of the uncertainty image (reduceRegion).
//   2. Assign each pixel to an uncertainty bin 0–3 (quartile-based).
//   3. Build composite stratum image = lc_class × N_UNC_BINS + unc_bin.
//   4. Count pixels per stratum via frequencyHistogram (reduceRegion).
//      N_h is the exact pixel count at EXPORT_SCALE — no sampling.
//   5. Approximate σ_h from bin midpoints derived in Step 1:
//        bin 0: σ ≈ p25 / 2
//        bin 1: σ ≈ (p25 + p50) / 2
//        bin 2: σ ≈ (p50 + p75) / 2
//        bin 3: σ ≈ p75 × 1.5  (conservative upper-tail estimate)
//      Midpoints preserve the relative ordering of Neyman weights
//      across bins, which is all that matters for allocation.
//      This replaces the previous .sample() + client-side tally step,
//      which failed when GEE returned undefined for large FeatureCollection
//      evaluate() calls.
//   6. Neyman weights: w_h = N_h × σ_h.
//      n_h = n_total × w_h / Σ(w_j),  floor at MIN_PTS_PER_STRATUM.
//      Strata with N_h = 0 are skipped.
//   7. Pass classValues / classPoints to stratifiedSample.
//
// Arguments:
//   unc_img    — ee.Image, single masked uncertainty band
//   unc_band   — string, band name in unc_img
//   lc_img     — ee.Image, single masked LC class band (values 1–5)
//   lc_band    — string, band name in lc_img
//   extra_bands— ee.Image, additional bands to carry to sampled points
//   n_total    — integer, total sample budget
//   pool_label — string, 'Forest' or 'Soil' (for console output)
//   callback   — function(ee.FeatureCollection), called with final pts
// ─────────────────────────────────────────────────────────────────
function _neymanSample(unc_img, unc_band, lc_img, lc_band, extra_bands, n_total, pool_label, callback) {

  var unc = unc_img.select(unc_band);

  // Step 1 — quartile breaks for uncertainty binning
  unc.reduceRegion({
    reducer:    ee.Reducer.percentile([25, 50, 75]),
    geometry:   aoi,
    scale:      EXPORT_SCALE,
    crs:        EXPORT_CRS,
    maxPixels:  1e11,
    bestEffort: true
  }).evaluate(function(pct, pctErr) {

    if (pctErr) {
      print('ERROR computing percentiles (' + pool_label + '): ' + pctErr);
      setStatus(pool_label + ' percentile computation failed - see console.');
      return;
    }

    var p25 = (pct[unc_band + '_p25'] !== undefined) ? pct[unc_band + '_p25'] : 1;
    var p50 = (pct[unc_band + '_p50'] !== undefined) ? pct[unc_band + '_p50'] : 3;
    var p75 = (pct[unc_band + '_p75'] !== undefined) ? pct[unc_band + '_p75'] : 6;

    print(pool_label + ' uncertainty quartile breaks:');
    print('  p25=' + p25.toFixed(4) + ' | p50=' + p50.toFixed(4) + ' | p75=' + p75.toFixed(4));

    // Representative σ per bin (midpoint of each quartile interval).
    // Bin 3 uses p75 × 1.5 as a conservative estimate of the upper-tail mean.
    // Only relative magnitudes matter for Neyman weighting.
    var binSigmas = [
      p25 / 2,               // bin 0: [0,   p25)
      (p25 + p50) / 2,       // bin 1: [p25, p50)
      (p50 + p75) / 2,       // bin 2: [p50, p75)
      p75 * 1.5              // bin 3: [p75, ∞)
    ];

    print('  Bin σ_h midpoints: [' +
      binSigmas.map(function(v){ return v.toFixed(4); }).join(', ') + ']');

    // Step 2 — uncertainty bin image (0 = lowest, N_UNC_BINS-1 = highest)
    var unc_unm = unc.unmask(0);
    var unc_bin = ee.Image(N_UNC_BINS - 1)
      .where(unc_unm.lt(p75), N_UNC_BINS - 2)
      .where(unc_unm.lt(p50), N_UNC_BINS - 3)
      .where(unc_unm.lt(p25), 0)
      .toInt().rename('unc_bin');

    // Composite stratum key: lc_class × N_UNC_BINS + unc_bin
    // lc_class ∈ {1..5}, unc_bin ∈ {0..3} → stratum ∈ {4..23}
    var stratum = lc_img.select(lc_band).multiply(N_UNC_BINS).add(unc_bin)
      .toInt().rename('stratum');

    // ── Strata visualization (vis=false; toggle on manually) ──────
    // Uncertainty bins: blue (low) → red (high), masked to valid LC pixels.
    Map.addLayer(
      unc_bin.updateMask(lc_img.select(lc_band).mask()),
      { min: 0, max: N_UNC_BINS - 1,
        palette: ['#2c7bb6', '#abd9e9', '#fdae61', '#d7191c'] },
      pool_label + ' Uncertainty Bins (0=low 3=high)',
      false
    );
    // Composite strata: hue encodes LC class, lightness encodes uncertainty bin.
    // 20 colours mapped linearly over stratum range [4, 5×N_UNC_BINS + N_UNC_BINS-1].
    // Read as: darker within each hue-group = higher uncertainty bin.
    Map.addLayer(
      stratum,
      { min: N_UNC_BINS,
        max: 5 * N_UNC_BINS + (N_UNC_BINS - 1),
        palette: [
          '#d4e6f1','#85c1e9','#2e86c1','#1a5276',   // LC1 Forest  (blue,  low→high unc)
          '#d5f5e3','#76d7c4','#1abc9c','#0e6655',   // LC2 Shrub   (teal,  low→high unc)
          '#e8daef','#bb8fce','#8e44ad','#6c3483',   // LC3 Wetland (purple)
          '#fef9e7','#f8c471','#e67e22','#ca6f1e',   // LC4 Crop    (orange)
          '#f2f3f4','#aab7b8','#717d7e','#424949'    // LC5 Other   (grey)
        ] },
      pool_label + ' Composite Strata (LC x unc_bin)',
      false
    );
    // ─────────────────────────────────────────────────────────────
    // This operates on the full-resolution raster — no sampling, no timeout risk.
    stratum.reduceRegion({
      reducer:    ee.Reducer.frequencyHistogram(),
      geometry:   aoi,
      scale:      EXPORT_SCALE,
      crs:        EXPORT_CRS,
      maxPixels:  1e11,
      bestEffort: true
    }).get('stratum').evaluate(function(histObj, histErr) {

      if (histErr) {
        print('ERROR in stratum histogram (' + pool_label + '): ' + histErr);
        setStatus(pool_label + ' stratum histogram failed - see console.');
        return;
      }
      if (!histObj || Object.keys(histObj).length === 0) {
        print('WARNING: empty stratum histogram (' + pool_label + '). Check AOI data coverage.');
        setStatus(pool_label + ': empty histogram - no valid strata found.');
        return;
      }

      // Step 4 — client-side Neyman allocation using bin-midpoint σ_h
      var keys        = Object.keys(histObj);
      var totalWeight = 0;
      var strata      = {};

      keys.forEach(function(h) {
        var hInt    = parseInt(h);
        var lc_code = Math.floor(hInt / N_UNC_BINS);
        var unc_b   = hInt % N_UNC_BINS;
        if (lc_code < 1) return;              // skip water / masked (lc = 0)

        var N_h     = histObj[h] || 0;
        var sigma_h = binSigmas[unc_b] || 0;
        var w_h     = N_h * sigma_h;

        strata[h]    = { N: N_h, sigma: sigma_h, w: w_h, lc: lc_code, bin: unc_b };
        totalWeight += w_h;
      });

      var classValues = [];
      var classPoints = [];
      var lcNames     = ['?', 'Forest', 'Shrub/Grass', 'Wetland', 'Cropland', 'Other'];

      print('NEYMAN ALLOCATION - ' + pool_label);
      print('  Total Neyman weight Σ(N_h × σ_h) = ' + totalWeight.toFixed(2));
      print('  Strata:');

      keys.forEach(function(h) {
        var s = strata[h];
        if (!s) return;

        var n_h;
        if (totalWeight > 0 && s.w > 0) {
          n_h = Math.max(MIN_PTS_PER_STRATUM,
                  Math.round(n_total * s.w / totalWeight));
        } else if (s.N > 0) {
          n_h = MIN_PTS_PER_STRATUM;  // occupied stratum with zero uncertainty
        } else {
          return;
        }

        var lcName = lcNames[s.lc] || ('LC' + s.lc);
        print('    h=' + h + ' (' + lcName + ', bin=' + s.bin + ')' +
              '  N_h=' + s.N + '  σ_h=' + s.sigma.toFixed(4) + '  n_h=' + n_h);

        classValues.push(parseInt(h));
        classPoints.push(n_h);
      });

      var allocTotal = classPoints.reduce(function(a, b) { return a + b; }, 0);
      print('  Total allocated = ' + allocTotal + '  (target = ' + n_total + ')');

      if (classValues.length === 0) {
        setStatus(pool_label + ': no valid strata - check AOI data coverage.');
        return;
      }

      // Step 5 — single stratifiedSample call with Neyman-derived classPoints
      var pts = extra_bands.addBands(stratum)
        .stratifiedSample({
          numPoints:   0,
          classBand:   'stratum',
          region:      aoi,
          scale:       EXPORT_SCALE,
          classValues: classValues,
          classPoints: classPoints,
          geometries:  true,
          seed:        42,
          tileScale:   4,
          dropNulls:   true
        })
        .map(function(f) { return f.set('pool', pool_label); });

      callback(pts);
    });
  });
}


// ─────────────────────────────────────────────────────────────────
// _powerAnalysis — sampling power for stratified Neyman design
//
// Estimand:  Mean carbon density (kg/m²) per pool.
// Framework: Simple random sampling (SRS) bounds — conservative
//   because Neyman stratification always does as well or better.
//   The gap between the SRS curve and the true Neyman variance
//   represents the stratification gain.
//
// Formula (SRS):
//   SE(n) = σ / √n     (σ = SD of carbon map over AOI)
//   MOE(n) = t₉₀ × SE(n) = 1.645 × σ / √n
//   Relative MOE (%) = 100 × MOE(n) / μ = 100 × 1.645 × CV / √n
//
// Benchmark: ±20% relative MOE at 90% CI (VM0033-aligned).
//   n_min = ⌈(t₉₀ × CV / 0.20)²⌉
//
// σ and μ come from the ensemble mean images (forest: forest-masked;
// soil: full AOI) so the CV is data-driven.
// ─────────────────────────────────────────────────────────────────
function _powerAnalysis() {
  if (!forest_ens_mean || !soil_ens_mean || !forest_nf_mask) {
    print('Power analysis skipped — run Steps 5-7 first.');
    return;
  }

  // σ and μ from carbon maps at full pixel resolution
  var f_stats = forest_ens_mean.updateMask(forest_nf_mask).reduceRegion({
    reducer:    ee.Reducer.mean().combine(ee.Reducer.stdDev(), null, true),
    geometry:   aoi, scale: EXPORT_SCALE, crs: EXPORT_CRS,
    maxPixels:  1e11, bestEffort: true
  });

  var s_stats = soil_ens_mean.reduceRegion({
    reducer:    ee.Reducer.mean().combine(ee.Reducer.stdDev(), null, true),
    geometry:   aoi, scale: EXPORT_SCALE, crs: EXPORT_CRS,
    maxPixels:  1e11, bestEffort: true
  });

  ee.List([
    f_stats.get('forest_ens_mean_mean'),
    f_stats.get('forest_ens_mean_stdDev'),
    s_stats.get('soil_ens_mean_mean'),
    s_stats.get('soil_ens_mean_stdDev')
  ]).evaluate(function(vals, err) {

    if (err || !vals || vals.some(function(v){ return v === null; })) {
      print('Power analysis error: ' + (err || 'null values in carbon stats'));
      return;
    }

    var f_mean = vals[0], f_sd = vals[1];
    var s_mean = vals[2], s_sd = vals[3];
    var f_cv   = f_sd / Math.max(Math.abs(f_mean), 0.001);
    var s_cv   = s_sd / Math.max(Math.abs(s_mean), 0.001);

    var t90        = 1.645;
    var MOE_TARGET = 0.20;   // 20% relative MOE
    var N_CHART    = 100;    // x-axis range

    // n_min = ceil((t90 × CV / MOE_target)²)
    var f_nmin = Math.ceil(Math.pow(t90 * f_cv / MOE_TARGET, 2));
    var s_nmin = Math.ceil(Math.pow(t90 * s_cv / MOE_TARGET, 2));

    // Relative MOE at currently allocated n
    var f_moe_cur = 100 * t90 * f_cv / Math.sqrt(N_FOREST_SAMPLES);
    var s_moe_cur = 100 * t90 * s_cv / Math.sqrt(N_SOIL_SAMPLES);

    // ── Console summary ────────────────────────────────────────
    print('');
    print('════ STATISTICAL POWER ANALYSIS (Step 8) ═══════════════');
    print('Estimand:  Mean carbon density (kg/m²)');
    print('CI:        90%  |  MOE benchmark: ±20% of mean  |  t = 1.645');
    print('Basis:     SRS bounds (conservative). Neyman stratification');
    print('           achieves equal or lower variance at the same n.');
    print('');
    print('FOREST (forested pixels only):');
    print('  μ = ' + f_mean.toFixed(3) + ' kg/m²  |  σ = ' + f_sd.toFixed(3) +
          ' kg/m²  |  CV = ' + (f_cv * 100).toFixed(1) + '%');
    print('  n_min for ±20% MOE (SRS):  ' + f_nmin +
          (f_nmin > N_CHART ? '  ← exceeds chart range' : ''));
    print('  Allocated n = ' + N_FOREST_SAMPLES + '  →  expected MOE = ±' +
          f_moe_cur.toFixed(1) + '%' +
          (f_moe_cur <= 20 ? '  ✓ meets target' : '  ⚠ exceeds target'));
    print('');
    print('SOIL (full AOI):');
    print('  μ = ' + s_mean.toFixed(3) + ' kg/m²  |  σ = ' + s_sd.toFixed(3) +
          ' kg/m²  |  CV = ' + (s_cv * 100).toFixed(1) + '%');
    print('  n_min for ±20% MOE (SRS):  ' + s_nmin +
          (s_nmin > N_CHART ? '  ← exceeds chart range' : ''));
    print('  Allocated n = ' + N_SOIL_SAMPLES + '  →  expected MOE = ±' +
          s_moe_cur.toFixed(1) + '%' +
          (s_moe_cur <= 20 ? '  ✓ meets target' : '  ⚠ exceeds target'));
    print('════════════════════════════════════════════════════════');
    print('');

    // ── Build chart: 1-100 samples, three series ────────────────
    var features = [];
    for (var n = 1; n <= N_CHART; n++) {
      features.push(ee.Feature(null, {
        'n':              n,
        'Forest MOE (%)': 100 * t90 * f_cv / Math.sqrt(n),
        'Soil MOE (%)':   100 * t90 * s_cv / Math.sqrt(n),
        'Target ±20%':    20
      }));
    }

    // y-axis ceiling: next multiple of 20 above the larger single-sample MOE
    var y_max = Math.min(300,
      Math.ceil(Math.max(100 * t90 * f_cv, 100 * t90 * s_cv) / 20) * 20 + 20
    );

    var chart = ui.Chart.feature.byFeature(
      ee.FeatureCollection(features), 'n',
      ['Forest MOE (%)', 'Soil MOE (%)', 'Target ±20%']
    )
    .setChartType('LineChart')
    .setOptions({
      title:  'Sampling Power: Relative MOE vs. n  (90% CI, SRS bound)\n' +
              'Forest CV=' + (f_cv*100).toFixed(1) + '%   ' +
              'Soil CV=' + (s_cv*100).toFixed(1) + '%   ' +
              'n_min: Forest=' + f_nmin + ', Soil=' + s_nmin,
      hAxis: {
        title: 'Field samples collected (n)',
        viewWindow: { min: 1, max: N_CHART },
        gridlines: { count: 10 }
      },
      vAxis: {
        title: 'Relative margin of error (%)',
        viewWindow: { min: 0, max: y_max },
        gridlines: { count: 8 }
      },
      series: {
        0: { color: '#1565c0', lineWidth: 2.5, pointSize: 0 },           // Forest
        1: { color: '#e65100', lineWidth: 2.5, pointSize: 0 },           // Soil
        2: { color: '#2e7d32', lineWidth: 1.5,                           // Target line
             lineDashStyle: [8, 4], pointSize: 0 }
      },
      legend: { position: 'bottom' },
      interpolateNulls: true
    });

    print(chart);
  });
}



// ─────────────────────────────────────────────────────────────────
function step9_reportsAndExports() {
  if (!forest_ens_mean)   { setStatus('Run Step 7 first - forest ensemble missing.'); return; }
  if (!soil_ens_mean)     { setStatus('Run Step 7 first - soil ensemble missing.');   return; }
  if (!total_ecosystem_c) { setStatus('Run Step 7 first - total C missing.');         return; }
  setStatus('Step 9: Computing AOI-wide summary statistics...');

  print('FOREST CARBON');
  printStats(forest_rf_pred,    'forest_carbon_kgm2',            aoi, 25,  'GEDI RF Forest Carbon (kg/m2)');
  printStats(sothe_fc,          'sothe_fc',                      aoi, 250, 'Sothe et al. Forest Carbon (kg/m2)');
  printStats(sothe_fc_unc,      'sothe_fc_unc',                  aoi, 250, 'Sothe FC Uncertainty (kg/m2)');
  printStats(forest_ens_mean,   'forest_ens_mean',               aoi, 25,  'Forest Ensemble Mean (kg/m2)');
  printStats(forest_ens_sd,     'forest_ens_sd',                 aoi, 25,  'Forest Ensemble SD (kg/m2)');
  printStats(forest_uncertainty,'forest_uncertainty_combined',   aoi, 25,  'Forest Uncertainty Combined (kg/m2)');

  print('SOIL CARBON');
  printStats(sg_soc_1m,         'sg_soc_1m',                    aoi, 250, 'SoilGrids SOC 0-100 cm (kg/m2)');
  printStats(sothe_sc,          'sothe_sc',                      aoi, 250, 'Sothe et al. Soil Carbon (kg/m2)');
  printStats(sothe_sc_unc,      'sothe_sc_unc',                  aoi, 250, 'Sothe SC Uncertainty (kg/m2)');
  printStats(soil_prior_mean,   'soil_prior_mean',               aoi, 250, 'Soil Prior Mean (kg/m2)');
  printStats(soil_ens_mean,     'soil_ens_mean',                 aoi, 250, 'Soil Ensemble Mean - Sothe+SoilGrids (kg/m2)');
  printStats(soil_ens_sd,       'soil_ens_sd',                   aoi, 250, 'Soil Disagreement SD (kg/m2)');
  printStats(soil_uncertainty,  'soil_uncertainty_combined',     aoi, 250, 'Soil Uncertainty Combined (kg/m2)');

  print('TOTAL ECOSYSTEM');
  printStats(total_ecosystem_c, 'total_ecosystem_c_kgm2',       aoi, 25,  'Total Ecosystem Carbon (kg/m2)');

  var st_gedi_f  = getStats(forest_rf_pred,   'forest_carbon_kgm2',          25);
  var st_sothe_f = getStats(sothe_fc,          'sothe_fc',                    250);
  var st_sothe_fu= getStats(sothe_fc_unc,      'sothe_fc_unc',                250);
  var st_sbfi    = getStats(sbfi_agb_raster.select('sbfi_agb_avg').multiply(0.1).rename('sbfi_kgm2'), 'sbfi_kgm2', 25);
  var st_fens    = getStats(forest_ens_mean,   'forest_ens_mean',             25);
  var st_func    = getStats(forest_uncertainty,'forest_uncertainty_combined', 25);
  var st_sg      = getStats(sg_soc_1m,         'sg_soc_1m',                   250);
  var st_sothe_s = getStats(sothe_sc,          'sothe_sc',                    250);
  var st_sothe_su= getStats(sothe_sc_unc,      'sothe_sc_unc',                250);
  var st_sens    = getStats(soil_ens_mean,     'soil_ens_mean',               250);
  var st_ssd     = getStats(soil_ens_sd,       'soil_ens_sd',                 250);
  var st_sunc    = getStats(soil_uncertainty,  'soil_uncertainty_combined',   250);
  var st_total   = getStats(total_ecosystem_c, 'total_ecosystem_c_kgm2',     25);

  var makeRow = function(source, desc, st, pool, res) {
    return ee.Feature(null, {
      '1_source':      source,
      '2_description': desc,
      '3_mean_kgm2':   st.mean,
      '3_min_kgm2':    st.min,
      '3_max_kgm2':    st.max,
      '4_sd_kgm2':     st.sd,
      '4_cv_pct':      cvStat(st.sd, st.mean),
      'pool':          pool,
      'res_m':         res
    });
  };

  var summaryTable = ee.FeatureCollection([
    // ── Forest ──────────────────────────────────────────────────
    makeRow('GEDI L4A v2 + 2-Stage RF (This Study)',
      'Pilot RF (' + PILOT_N_TREES + ' trees, all bands) -> top ' + TOP_N_BANDS +
      ' by Gini -> final RF (' + FINAL_N_TREES + ' trees). AGBD Mg/ha x 0.1 -> kg/m2.',
      st_gedi_f, 'Forest Carbon', 25),
    makeRow('Sothe et al. Forest Carbon',
      'McMaster/WWF-Canada national forest carbon map. Direct ensemble member (kg/m2).',
      st_sothe_f, 'Forest Carbon', 250),
    makeRow('Sothe et al. Forest Carbon - Uncertainty',
      'Per-pixel uncertainty for Sothe FC (kg/m2). RSS-combined with ensemble SD in Step 7.',
      st_sothe_fu, 'Forest Carbon Uncertainty', 250),
    makeRow('CFI SBFI - STRUCTURE_AGB_AVG',
      'Canadian SBFI gridded AGB (t/ha x 0.1 -> kg/m2). Ensemble source.',
      st_sbfi, 'Forest Carbon', 25),
    makeRow('Forest Ensemble Mean (This Study)',
      'Equal-weight mean of GEDI RF + Sothe FC + CFI SBFI (3 members).',
      st_fens, 'Forest Carbon', 25),
    makeRow('Forest Uncertainty Combined (This Study)',
      'sqrt(ensemble_SD^2 + sothe_fc_unc^2). Drives Neyman forest sampling allocation.',
      st_func, 'Forest Carbon Uncertainty', 25),
    // ── Soil ────────────────────────────────────────────────────
    makeRow('SoilGrids OCS 0-100 cm (sg_soc_1m)',
      'Sum of 5 per-depth OCS layers (kg/m2). Direct soil ensemble member.',
      st_sg, 'Soil Carbon', 250),
    makeRow('Sothe et al. Soil Carbon',
      'McMaster/WWF-Canada national soil carbon map. Direct soil ensemble member (kg/m2).',
      st_sothe_s, 'Soil Carbon', 250),
    makeRow('Sothe et al. Soil Carbon - Uncertainty',
      'Per-pixel uncertainty for Sothe SC (kg/m2). Propagated into combined soil uncertainty.',
      st_sothe_su, 'Soil Carbon Uncertainty', 250),
    makeRow('Soil Ensemble Mean (This Study)',
      'Equal-weight mean of Sothe SC + SoilGrids 0-100 cm (2 members, 250 m). ' +
      'No local RF trained; avoids introducing data-limited model error at KBA scale.',
      st_sens, 'Soil Carbon', 250),
    makeRow('Soil Disagreement SD (This Study)',
      'Pixel-wise SD between Sothe SC and SoilGrids OCS. Measures inter-product ' +
      'disagreement; high values indicate contested areas and receive more sampling effort.',
      st_ssd, 'Soil Carbon Uncertainty', 250),
    makeRow('Soil Uncertainty Combined (This Study)',
      'sqrt(sothe_sc_unc^2 + soil_ens_SD^2). RSS of product uncertainty and inter-product ' +
      'disagreement. Drives Neyman soil sampling allocation.',
      st_sunc, 'Soil Carbon Uncertainty', 250),
    // ── Total ───────────────────────────────────────────────────
    makeRow('Total Ecosystem Carbon (This Study)',
      'Forest Ensemble Mean + Soil Ensemble Mean (kg/m2).',
      st_total, 'Total Ecosystem', 25)
  ]);

  print('Summary table ready - open Tasks panel to run exports.');

  var exportRaster = function(img, desc) {
    Export.image.toDrive({
      image: img.toFloat(), description: desc, folder: EXPORT_FOLDER,
      region: aoi, scale: EXPORT_SCALE, maxPixels: 1e13, crs: EXPORT_CRS
    });
  };

  // Forest
  exportRaster(forest_ens_mean,    'Forest_Ensemble_Mean_kgm2');
  exportRaster(forest_ens_sd,      'Forest_Ensemble_SD_kgm2');
  exportRaster(forest_uncertainty, 'Forest_Uncertainty_Combined_kgm2');
  exportRaster(sothe_fc_unc,       'Sothe_FC_Uncertainty_kgm2');
  exportRaster(forest_rf_pred,     'GEDI_RF_Forest_Carbon_kgm2');

  // Soil
  exportRaster(soil_ens_mean,      'Soil_Ensemble_Mean_kgm2');
  exportRaster(soil_ens_sd,        'Soil_Disagreement_SD_kgm2');
  exportRaster(soil_uncertainty,   'Soil_Uncertainty_Combined_kgm2');
  exportRaster(sothe_sc_unc,       'Sothe_SC_Uncertainty_kgm2');
  exportRaster(sothe_sc,           'Sothe_SC_kgm2');
  exportRaster(sg_soc_1m,          'SoilGrids_OCS_0_100cm_kgm2');

  // Derived
  exportRaster(total_ecosystem_c,  'Total_Ecosystem_Carbon_kgm2');
  exportRaster(dsm_forest,         'Forest_Data_Source_Map');
  exportRaster(dsm_soil,           'Soil_Data_Source_Map');

  // Tables
  Export.table.toDrive({
    collection: canada_boundary, description: 'Canada_Country_Boundary',
    folder: EXPORT_FOLDER, fileFormat: 'KML'
  });
  Export.table.toDrive({
    collection: summaryTable, description: 'Carbon_Summary_Report_Table',
    folder: EXPORT_FOLDER, fileFormat: 'CSV'
  });

  if (forest_sampling_pts) {
    Export.table.toDrive({
      collection: forest_sampling_pts, description: 'Forest_Sampling_Points_Neyman_KML',
      folder: EXPORT_FOLDER, fileFormat: 'KML'
    });
    Export.table.toDrive({
      collection: forest_sampling_pts, description: 'Forest_Sampling_Points_Neyman_CSV',
      folder: EXPORT_FOLDER, fileFormat: 'CSV'
    });
  } else { print('Forest sampling points not generated - run Step 8.'); }

  if (soil_sampling_pts) {
    Export.table.toDrive({
      collection: soil_sampling_pts, description: 'Soil_Sampling_Points_Neyman_KML',
      folder: EXPORT_FOLDER, fileFormat: 'KML'
    });
    Export.table.toDrive({
      collection: soil_sampling_pts, description: 'Soil_Sampling_Points_Neyman_CSV',
      folder: EXPORT_FOLDER, fileFormat: 'CSV'
    });
  } else { print('Soil sampling points not generated - run Step 8.'); }

  markDone(8);
  setStatus('Step 9 complete - check Tasks panel to run all exports.');
}


// ─────────────────────────────────────────────────────────────────
// BOOT
// ─────────────────────────────────────────────────────────────────
print("=== Charlie's Place KBA - Forest Carbon Assessment v4.4 ===");
print('CRS: ' + EXPORT_CRS + ' | Scale: ' + EXPORT_SCALE + ' m');
print('Forest: ' + N_FOREST_SAMPLES + ' pts | Soil: ' + N_SOIL_SAMPLES + ' pts');
print('RF: pilot ' + PILOT_N_TREES + ' -> final ' + FINAL_N_TREES + ' trees (top ' + TOP_N_BANDS + ' bands)');
print('Sampling: Neyman | LC: ESA WorldCover v200 (5 types) x ' + N_UNC_BINS +
      ' uncertainty bins = up to ' + (5 * N_UNC_BINS) + ' strata per pool');
print('Uncertainty: sqrt(ensemble_SD^2 + sothe_unc^2) for both pools');
print('Run steps [1] to [9] in sequence using the panel buttons.');

try { initUI(); } catch(e) {
  print('Panel already rendered - hard refresh (Ctrl+Shift+R) to fully reset.');
}
