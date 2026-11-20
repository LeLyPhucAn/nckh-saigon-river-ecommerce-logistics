"""
Pipeline Coordinator Module.
Coordinates the end-to-end execution of:
1. Data Ingestion & Validation
2. GIS Feature Extraction & Cartography (Day 1)
3. Fuzzy AHP Global Weight Synthesis
4. Corridor Segment Evaluation
5. TOPSIS Micro-Hub Site Selection
6. Sensitivity Analysis
7. Ward-Level Spatial Econometrics & SPSS Generation
8. RIS Multimodal Simulation Demo
"""

from pathlib import Path
import pandas as pd
from src.config import TABLES_DIR, CHARTS_DIR, SPSS_DIR
from src.gis.spatial_features import export_day1_datasets, plot_day1_corridor_map
from src.models.fuzzy_ahp import FuzzyAHPModel
from src.models.segment_evaluator import SegmentEvaluator
from src.models.topsis import TOPSISModel
from src.models.sensitivity_engine import SensitivityEngine
from src.models.ward_econometrics import WardEconometricModel
from src.models.ris_simulation import RISSimulationModel
from src.visualization.chart_renderer import (
    plot_fuzzy_ahp_weights,
    plot_segment_scores,
    plot_topsis_rankings,
    plot_radar_chart,
    plot_sensitivity,
    plot_ward_regression_fit,
    plot_ris_comparison,
)


def run_full_pipeline_workflow() -> dict:
    """Executes the entire research pipeline and returns paths to all generated artifacts."""
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    SPSS_DIR.mkdir(parents=True, exist_ok=True)

    artifacts = {}

    # Stage 1: GIS Extraction
    print("[1/7] Ingesting raw GIS features & building spatial buffers...")
    hubs_path, segs_path = export_day1_datasets()
    map_path = plot_day1_corridor_map()
    artifacts["gis_hubs"] = hubs_path
    artifacts["gis_segments"] = segs_path
    artifacts["gis_map"] = map_path

    # Stage 2: Fuzzy AHP
    print("[2/7] Running Fuzzy AHP priority weight synthesis...")
    ahp_model = FuzzyAHPModel()
    ahp_res = ahp_model.fit()
    weights_csv = TABLES_DIR / "fuzzy_ahp_weights.csv"
    ahp_res.global_weights_df.to_csv(weights_csv, index=False, encoding="utf-8-sig")
    weights_chart = CHARTS_DIR / "fuzzy_ahp_weights.png"
    plot_fuzzy_ahp_weights(ahp_res.global_weights_df, weights_chart)
    artifacts["weights_csv"] = weights_csv
    artifacts["weights_chart"] = weights_chart

    # Stage 3: Segment Evaluation
    print("[3/7] Scoring 3 corridor segments via Min-Max WLC...")
    seg_eval = SegmentEvaluator(ahp_model=ahp_model)
    seg_res = seg_eval.evaluate()
    seg_csv = TABLES_DIR / "corridor_segment_scores.csv"
    seg_res.summary_scores_df.to_csv(seg_csv, index=False, encoding="utf-8-sig")
    seg_chart = CHARTS_DIR / "segment_potential_scores.png"
    plot_segment_scores(seg_res.summary_scores_df, seg_chart)
    artifacts["segment_csv"] = seg_csv
    artifacts["segment_chart"] = seg_chart

    # Stage 4: TOPSIS Hub Selection
    print("[4/7] Executing TOPSIS algorithm on 8 candidate Micro-Hubs...")
    topsis_model = TOPSISModel()
    topsis_res = topsis_model.fit()
    topsis_csv = TABLES_DIR / "topsis_hub_rankings.csv"
    topsis_res.rankings_df.to_csv(topsis_csv, index=False, encoding="utf-8-sig")
    topsis_chart = CHARTS_DIR / "topsis_rankings.png"
    plot_topsis_rankings(topsis_res.rankings_df, topsis_chart)
    radar_chart = CHARTS_DIR / "micro_hub_radar_chart.png"
    plot_radar_chart(radar_chart)
    artifacts["topsis_csv"] = topsis_csv
    artifacts["topsis_chart"] = topsis_chart
    artifacts["radar_chart"] = radar_chart

    # Stage 5: Sensitivity Analysis
    print("[5/7] Running Sensitivity Analysis across ±20% weight scenarios...")
    sens_engine = SensitivityEngine(topsis_model=topsis_model)
    sens_res = sens_engine.run_scenarios()
    sens_csv = TABLES_DIR / "sensitivity_analysis_results.csv"
    sens_res.rankings_by_scenario_df.to_csv(sens_csv, index=False, encoding="utf-8-sig")
    sens_chart = CHARTS_DIR / "sensitivity_analysis.png"
    plot_sensitivity(sens_res.rankings_by_scenario_df, sens_chart)
    artifacts["sensitivity_csv"] = sens_csv
    artifacts["sensitivity_chart"] = sens_chart

    # Stage 6: Ward Econometrics & SPSS
    print("[6/7] Estimating OLS Regression across 28 riverine wards & generating SPSS syntax...")
    reg_model = WardEconometricModel()
    reg_res = reg_model.fit()
    ward_csv = SPSS_DIR / "spss_ward_data.csv"
    reg_res.processed_ward_df.to_csv(ward_csv, index=False, encoding="utf-8-sig")
    reg_csv = TABLES_DIR / "econometric_regression_results.csv"
    reg_res.coefficients_df.to_csv(reg_csv, index=False, encoding="utf-8-sig")
    reg_chart = CHARTS_DIR / "ward_regression_fit.png"
    plot_ward_regression_fit(reg_res.processed_ward_df, reg_res.coefficients_df, reg_res.model_metrics, reg_chart)
    artifacts["ward_csv"] = ward_csv
    artifacts["spss_syntax"] = reg_res.spss_syntax_path
    artifacts["regression_csv"] = reg_csv
    artifacts["regression_chart"] = reg_chart

    # Stage 7: RIS Simulation
    print("[7/7] Simulating 3,000 parcels dispatch under RIS vs Conventional Road...")
    ris_model = RISSimulationModel()
    ris_res = ris_model.simulate()
    ris_csv = TABLES_DIR / "ris_operational_simulation_comparison.csv"
    ris_res.comparison_df.to_csv(ris_csv, index=False, encoding="utf-8-sig")
    ris_chart = CHARTS_DIR / "ris_vs_road_comparison.png"
    plot_ris_comparison(ris_res.metrics_raw, ris_chart)
    artifacts["ris_csv"] = ris_csv
    artifacts["ris_chart"] = ris_chart

    return artifacts
