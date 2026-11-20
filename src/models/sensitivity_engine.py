"""
Sensitivity Analysis Engine.
Tests the stability of TOPSIS Micro-Hub rankings under weight variations (±10%, ±20%)
following the methodology of Mazarakis et al. (2025).
"""

from dataclasses import dataclass
from typing import List
import pandas as pd
from .topsis import TOPSISModel


@dataclass
class SensitivityResult:
    """Encapsulates sensitivity analysis scenarios."""
    scenarios_df: pd.DataFrame
    rankings_by_scenario_df: pd.DataFrame


class SensitivityEngine:
    """Runs perturbation scenarios on criteria weights."""

    def __init__(self, topsis_model: TOPSISModel | None = None):
        self.topsis_model = topsis_model if topsis_model is not None else TOPSISModel()

    def run_scenarios(self) -> SensitivityResult:
        """Executes 5 sensitivity scenarios on land rent and demand weights."""
        scenarios = [
            {"name": "Cost -20%", "rent_factor": 0.80, "condo_factor": 1.20},
            {"name": "Cost -10%", "rent_factor": 0.90, "condo_factor": 1.10},
            {"name": "Baseline (0%)", "rent_factor": 1.00, "condo_factor": 1.00},
            {"name": "Cost +10%", "rent_factor": 1.10, "condo_factor": 0.90},
            {"name": "Cost +20%", "rent_factor": 1.20, "condo_factor": 0.80},
        ]

        base_rent_w = 0.165
        base_condo_w = 0.125

        cc_records: List[dict] = []
        rank_records: List[dict] = []

        for sc in scenarios:
            adj = {
                "est_land_rent_vnd_m2": base_rent_w * sc["rent_factor"],
                "condos_1500m": base_condo_w * sc["condo_factor"],
            }
            res = self.topsis_model.fit(custom_weights=adj)
            res_df = res.rankings_df

            cc_row = {"scenario": sc["name"]}
            rank_row = {"scenario": sc["name"]}
            for _, row in res_df.iterrows():
                hid = row["hub_id"]
                cc_row[hid] = row["closeness_coefficient"]
                rank_row[hid] = row["rank"]

            cc_records.append(cc_row)
            rank_records.append(rank_row)

        return SensitivityResult(
            scenarios_df=pd.DataFrame(cc_records),
            rankings_by_scenario_df=pd.DataFrame(rank_records),
        )
