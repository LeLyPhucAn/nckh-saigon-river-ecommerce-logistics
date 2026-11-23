"""
Bộ công cụ phân tích độ nhạy (Sensitivity Analysis).
Kiểm tra độ ổn định thứ hạng TOPSIS khi biến động trọng số (±10%, ±20%).
Hỗ trợ cả phân tích đơn biến One-At-a-Time (OAT) trên toàn bộ tiêu chí
và các kịch bản tương tác đa tiêu chí chi phí - nhu cầu (Mazarakis et al., 2025).
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import pandas as pd

from .topsis import TOPSISModel


@dataclass
class SensitivityResult:
    """Đóng gói kết quả các kịch bản phân tích độ nhạy."""
    scenarios_df: pd.DataFrame
    rankings_by_scenario_df: pd.DataFrame
    oat_results_df: Optional[pd.DataFrame] = None
    hub06_stability_rate: float = 1.0


class SensitivityEngine:
    """Thực thi các kịch bản biến thiên trọng số đa tiêu chí."""

    def __init__(self, topsis_model: Optional[TOPSISModel] = None) -> None:
        self.topsis_model = topsis_model if topsis_model is not None else TOPSISModel()

    def run_scenarios(
        self, ahp_global_weights_df: Optional[pd.DataFrame] = None
    ) -> SensitivityResult:
        """
        Chạy 5 kịch bản phân tích độ nhạy chi phí và nhu cầu (±10%, ±20%),
        kết hợp kiểm tra độ nhạy OAT (One-At-a-Time) trên toàn bộ 10 tiêu chí.
        """
        # Xác định trọng số cơ sở (Baseline weights) từ AHP hoặc default
        if ahp_global_weights_df is not None:
            base_weights = self.topsis_model.derive_weights_from_ahp(ahp_global_weights_df)
        else:
            base_weights = self.topsis_model.default_weights.copy()

        base_rent_w = base_weights.get("est_land_rent_vnd_m2", 0.165)
        base_condo_w = base_weights.get("condos_1500m", 0.125)

        # 1. Kịch bản tương tác Chi phí đất vs Nhu cầu chung cư (Cost-Demand Scenarios)
        scenarios: List[Dict[str, float | str]] = [
            {"name": "Cost -20%", "rent_factor": 0.80, "condo_factor": 1.20},
            {"name": "Cost -10%", "rent_factor": 0.90, "condo_factor": 1.10},
            {"name": "Baseline (0%)", "rent_factor": 1.00, "condo_factor": 1.00},
            {"name": "Cost +10%", "rent_factor": 1.10, "condo_factor": 0.90},
            {"name": "Cost +20%", "rent_factor": 1.20, "condo_factor": 0.80},
        ]

        cc_records: List[Dict[str, str | float]] = []
        rank_records: List[Dict[str, str | int]] = []
        hub06_ranks: List[int] = []

        for sc in scenarios:
            rent_fac = float(sc["rent_factor"])
            condo_fac = float(sc["condo_factor"])
            adj = {
                "est_land_rent_vnd_m2": base_rent_w * rent_fac,
                "condos_1500m": base_condo_w * condo_fac,
            }
            res = self.topsis_model.fit(
                custom_weights=adj,
                ahp_global_weights_df=ahp_global_weights_df
            )
            res_df = res.rankings_df

            cc_row: Dict[str, str | float] = {"scenario": str(sc["name"])}
            rank_row: Dict[str, str | int] = {"scenario": str(sc["name"])}
            for _, row in res_df.iterrows():
                hid = row["hub_id"]
                cc_row[hid] = row["closeness_coefficient"]
                rank_row[hid] = int(row["rank"])
                if hid == "HUB06":
                    hub06_ranks.append(int(row["rank"]))

            cc_records.append(cc_row)
            rank_records.append(rank_row)

        # 2. Phân tích độ nhạy One-At-a-Time (OAT) trên toàn bộ tiêu chí
        oat_records = []
        factors = [0.8, 0.9, 1.0, 1.1, 1.2]
        factor_labels = ["-20%", "-10%", "0%", "+10%", "+20%"]

        for col in self.topsis_model.criteria_cols:
            orig_w = base_weights.get(col, 0.10)
            for fac, flab in zip(factors, factor_labels):
                adj_oat = {col: orig_w * fac}
                res_oat = self.topsis_model.fit(
                    custom_weights=adj_oat,
                    ahp_global_weights_df=ahp_global_weights_df
                )
                top_hub = res_oat.rankings_df.iloc[0]["hub_id"]
                hub06_rank = int(res_oat.rankings_df[res_oat.rankings_df["hub_id"] == "HUB06"]["rank"].values[0])
                hub06_ranks.append(hub06_rank)
                oat_records.append({
                    "criterion": col,
                    "variation": flab,
                    "factor": fac,
                    "top1_hub": top_hub,
                    "hub06_rank": hub06_rank,
                })

        stability_rate = float(sum(r == 1 for r in hub06_ranks) / len(hub06_ranks))

        return SensitivityResult(
            scenarios_df=pd.DataFrame(cc_records),
            rankings_by_scenario_df=pd.DataFrame(rank_records),
            oat_results_df=pd.DataFrame(oat_records),
            hub06_stability_rate=round(stability_rate, 4),
        )
