"""
Bộ công cụ phân tích độ nhạy (Sensitivity Analysis).
Kiểm tra độ ổn định thứ hạng TOPSIS khi biến động trọng số (±10%, ±20%).
Dựa trên phương pháp của Mazarakis et al. (2025).
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


class SensitivityEngine:
    """Thực thi các kịch bản biến thiên trọng số đa tiêu chí."""

    def __init__(self, topsis_model: Optional[TOPSISModel] = None) -> None:
        self.topsis_model = topsis_model if topsis_model is not None else TOPSISModel()

    def run_scenarios(self) -> SensitivityResult:
        """Chạy 5 kịch bản phân tích độ nhạy trên trọng số chi phí và nhu cầu."""
        scenarios: List[Dict[str, float | str]] = [
            {"name": "Cost -20%", "rent_factor": 0.80, "condo_factor": 1.20},
            {"name": "Cost -10%", "rent_factor": 0.90, "condo_factor": 1.10},
            {"name": "Baseline (0%)", "rent_factor": 1.00, "condo_factor": 1.00},
            {"name": "Cost +10%", "rent_factor": 1.10, "condo_factor": 0.90},
            {"name": "Cost +20%", "rent_factor": 1.20, "condo_factor": 0.80},
        ]

        base_rent_w = 0.165
        base_condo_w = 0.125

        cc_records: List[Dict[str, str | float]] = []
        rank_records: List[Dict[str, str | int]] = []

        for sc in scenarios:
            rent_fac = float(sc["rent_factor"])
            condo_fac = float(sc["condo_factor"])
            adj = {
                "est_land_rent_vnd_m2": base_rent_w * rent_fac,
                "condos_1500m": base_condo_w * condo_fac,
            }
            res = self.topsis_model.fit(custom_weights=adj)
            res_df = res.rankings_df

            cc_row: Dict[str, str | float] = {"scenario": str(sc["name"])}
            rank_row: Dict[str, str | int] = {"scenario": str(sc["name"])}
            for _, row in res_df.iterrows():
                hid = row["hub_id"]
                cc_row[hid] = row["closeness_coefficient"]
                rank_row[hid] = int(row["rank"])

            cc_records.append(cc_row)
            rank_records.append(rank_row)

        return SensitivityResult(
            scenarios_df=pd.DataFrame(cc_records),
            rankings_by_scenario_df=pd.DataFrame(rank_records),
        )
