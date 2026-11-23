"""
Mô đun điều phối luồng quy trình (Pipeline Coordinator).
Thực thi tuần tự 7 giai đoạn nghiên cứu từ nạp dữ liệu đến xuất báo cáo.
Kết nối dữ liệu chặt chẽ và nhất quán giữa GIS -> AHP -> TOPSIS -> Sensitivity -> Econometrics -> RIS.
"""

from pathlib import Path
from typing import Dict
import pandas as pd

from src.config import CHARTS_DIR, SPSS_DIR, TABLES_DIR
from src.gis.spatial_features import export_day1_datasets, plot_day1_corridor_map
from src.models.fuzzy_ahp import FuzzyAHPModel
from src.models.ris_simulation import RISSimulationModel
from src.models.segment_evaluator import SegmentEvaluator
from src.models.sensitivity_engine import SensitivityEngine
from src.models.topsis import TOPSISModel
from src.models.ward_econometrics import WardEconometricModel
from src.visualization.chart_renderer import (
    plot_fuzzy_ahp_weights,
    plot_radar_chart,
    plot_ris_comparison,
    plot_segment_scores,
    plot_sensitivity,
    plot_topsis_rankings,
    plot_ward_regression_fit,
)


def run_full_pipeline_workflow() -> Dict[str, Path]:
    """Thực thi toàn bộ luồng mô hình và trả về danh mục đường dẫn các tệp kết quả."""
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    SPSS_DIR.mkdir(parents=True, exist_ok=True)

    artifacts: Dict[str, Path] = {}

    # Giai đoạn 1: Giải tích không gian GIS Ngày 1
    print("[1/7] Nạp dữ liệu GIS & dựng vùng đệm đa tầng (500m & 1500m)...")
    hubs_path, segs_path = export_day1_datasets()
    map_path = plot_day1_corridor_map()
    artifacts["gis_hubs"] = hubs_path
    artifacts["gis_segments"] = segs_path
    artifacts["gis_map"] = map_path

    # Giai đoạn 2: Tính toán trọng số toàn cục Triangular Fuzzy AHP
    print("[2/7] Tính toán trọng số toàn cục Triangular Fuzzy AHP (TFN Buckley & Chang)...")
    ahp_model = FuzzyAHPModel()
    ahp_res = ahp_model.fit()
    weights_csv = TABLES_DIR / "fuzzy_ahp_weights.csv"
    ahp_res.global_weights_df.to_csv(weights_csv, index=False, encoding="utf-8-sig")
    weights_chart = CHARTS_DIR / "fuzzy_ahp_weights.png"
    plot_fuzzy_ahp_weights(ahp_res.global_weights_df, weights_chart)
    artifacts["weights_csv"] = weights_csv
    artifacts["weights_chart"] = weights_chart

    # Giai đoạn 3: Chấm điểm tiềm năng 3 tiểu đoạn sông (Min-Max WLC)
    print("[3/7] Chấm điểm tiềm năng 3 đoạn sông bằng Min-Max WLC...")
    seg_eval = SegmentEvaluator(ahp_model=ahp_model)
    seg_res = seg_eval.evaluate()
    seg_csv = TABLES_DIR / "corridor_segment_scores.csv"
    seg_res.summary_scores_df.to_csv(seg_csv, index=False, encoding="utf-8-sig")
    seg_chart = CHARTS_DIR / "segment_potential_scores.png"
    plot_segment_scores(seg_res.summary_scores_df, seg_chart)
    artifacts["segment_csv"] = seg_csv
    artifacts["segment_chart"] = seg_chart

    # Giai đoạn 4: Tuyển chọn vị trí trạm Micro-Hub bằng TOPSIS (Liên kết GIS và AHP)
    print("[4/7] Xếp hạng đa tiêu chí TOPSIS cho 8 trạm Micro-Hubs (nhận trực tiếp phụ tải GIS và trọng số AHP)...")
    df_gis_hubs = pd.read_csv(hubs_path)
    topsis_model = TOPSISModel(candidate_hubs_df=df_gis_hubs)
    topsis_res = topsis_model.fit(ahp_global_weights_df=ahp_res.global_weights_df)
    topsis_csv = TABLES_DIR / "topsis_hub_rankings.csv"
    topsis_res.rankings_df.to_csv(topsis_csv, index=False, encoding="utf-8-sig")
    topsis_chart = CHARTS_DIR / "topsis_rankings.png"
    plot_topsis_rankings(topsis_res.rankings_df, topsis_chart)
    radar_chart = CHARTS_DIR / "micro_hub_radar_chart.png"
    plot_radar_chart(radar_chart)
    artifacts["topsis_csv"] = topsis_csv
    artifacts["topsis_chart"] = topsis_chart
    artifacts["radar_chart"] = radar_chart

    # Giai đoạn 5: Phân tích độ nhạy (Kiểm định tính ổn định của HUB06)
    print("[5/7] Phân tích độ nhạy đa kịch bản & OAT (kiểm tra độ ổn định bến tối ưu HUB06)...")
    sens_engine = SensitivityEngine(topsis_model=topsis_model)
    sens_res = sens_engine.run_scenarios(ahp_global_weights_df=ahp_res.global_weights_df)
    sens_csv = TABLES_DIR / "sensitivity_analysis_results.csv"
    sens_res.rankings_by_scenario_df.to_csv(sens_csv, index=False, encoding="utf-8-sig")
    sens_chart = CHARTS_DIR / "sensitivity_analysis.png"
    plot_sensitivity(sens_res.rankings_by_scenario_df, sens_chart)
    artifacts["sensitivity_csv"] = sens_csv
    artifacts["sensitivity_chart"] = sens_chart

    # Giai đoạn 6: Hồi quy kinh tế lượng 28 phường & SPSS (Dữ liệu thực nghiệm minh bạch)
    print("[6/7] Ước lượng hồi quy OLS 28 phường ven sông & kiểm định VIF, Breusch-Pagan, SPSS...")
    reg_model = WardEconometricModel()
    reg_res = reg_model.fit()
    ward_csv = SPSS_DIR / "spss_ward_data.csv"
    reg_res.processed_ward_df.to_csv(ward_csv, index=False, encoding="utf-8-sig")
    reg_csv = TABLES_DIR / "econometric_regression_results.csv"
    reg_res.coefficients_df.to_csv(reg_csv, index=False, encoding="utf-8-sig")
    reg_chart = CHARTS_DIR / "ward_regression_fit.png"
    plot_ward_regression_fit(
        reg_res.processed_ward_df,
        reg_res.coefficients_df,
        reg_res.model_metrics,
        reg_chart
    )
    artifacts["ward_csv"] = ward_csv
    artifacts["spss_syntax"] = reg_res.spss_syntax_path
    artifacts["regression_csv"] = reg_csv
    artifacts["regression_chart"] = reg_chart

    # Giai đoạn 7: Mô phỏng luồng vận hành RIS (Liên kết với bến số 1 từ TOPSIS)
    top_hub = topsis_res.rankings_df.iloc[0]
    print(f"[7/7] Mô phỏng luồng vận hành RIS kết nối bến tối ưu {top_hub['hub_name']} ({top_hub['hub_id']})...")
    ris_model = RISSimulationModel(
        destination_hub_name=f"{top_hub['hub_name']} ({top_hub['hub_id']})",
        water_distance_km=8.2,
        road_distance_km=11.5
    )
    ris_res = ris_model.simulate()
    ris_csv = TABLES_DIR / "ris_operational_simulation_comparison.csv"
    ris_res.comparison_df.to_csv(ris_csv, index=False, encoding="utf-8-sig")
    ris_multi_csv = TABLES_DIR / "ris_multiscenario_simulation.csv"
    ris_res.multi_scenario_df.to_csv(ris_multi_csv, index=False, encoding="utf-8-sig")
    ris_chart = CHARTS_DIR / "ris_vs_road_comparison.png"
    plot_ris_comparison(ris_res.metrics_raw, ris_chart)
    artifacts["ris_csv"] = ris_csv
    artifacts["ris_multi_csv"] = ris_multi_csv
    artifacts["ris_chart"] = ris_chart

    print(f"\n>>> HOÀN THÀNH TOÀN BỘ PIPELINE: 7/7 giai đoạn thành công!")
    print(f"    - Bến tối ưu số 1: {top_hub['hub_name']} (CC = {top_hub['closeness_coefficient']:.4f})")
    print(f"    - Độ ổn định bến HUB06: {sens_res.hub06_stability_rate * 100:.1f}%")
    print(f"    - Mô hình hồi quy OLS: R2 = {reg_res.model_metrics['R_squared']:.4f}, F = {reg_res.model_metrics['F_Statistic']}")
    return artifacts
