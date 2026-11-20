"""
TOPSIS Multi-Criteria Decision Making Model.
Implements Hwang & Yoon (1981) TOPSIS algorithm with vector normalization,
weighted Euclidean distance to positive and negative ideal solutions,
and relative closeness coefficient CC_k.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import numpy as np
import pandas as pd
from src.data_loaders.hub_loader import load_candidate_hubs


@dataclass
class TOPSISResult:
    """Encapsulates output of TOPSIS ranking model."""
    rankings_df: pd.DataFrame
    weighted_normalized_matrix: np.ndarray
    ideal_positive: np.ndarray
    ideal_negative: np.ndarray
    closeness_coefficients: Dict[str, float]


class TOPSISModel:
    """TOPSIS multi-criteria ranking engine for Micro-Hub site selection."""

    def __init__(self, candidate_hubs_df: Optional[pd.DataFrame] = None):
        self.hubs_df = candidate_hubs_df if candidate_hubs_df is not None else load_candidate_hubs()

        self.criteria_cols: List[str] = [
            "bridge_clearance_m", "river_depth_m", "ris_readiness_score",
            "condos_1500m", "malls_1500m", "road_density_1500m",
            "pop_catchment", "dist_to_cbd_km", "est_land_rent_vnd_m2",
            "erosion_safety"
        ]

        self.directions: Dict[str, str] = {
            "bridge_clearance_m": "+",
            "river_depth_m": "+",
            "ris_readiness_score": "+",
            "condos_1500m": "+",
            "malls_1500m": "+",
            "road_density_1500m": "+",
            "pop_catchment": "+",
            "dist_to_cbd_km": "-",
            "est_land_rent_vnd_m2": "-",
            "erosion_safety": "+",
        }

        self.default_weights: Dict[str, float] = {
            "bridge_clearance_m": 0.115,
            "river_depth_m": 0.085,
            "ris_readiness_score": 0.090,
            "condos_1500m": 0.125,
            "malls_1500m": 0.080,
            "road_density_1500m": 0.095,
            "pop_catchment": 0.110,
            "dist_to_cbd_km": 0.075,
            "est_land_rent_vnd_m2": 0.165,
            "erosion_safety": 0.060,
        }

    def _prepare_decision_matrix(self) -> pd.DataFrame:
        """Enriches raw hub data with calibrated POI and safety metrics."""
        df = self.hubs_df.copy()
        # Calibrated features matching OSM & HCMC survey
        condos_map = {"HUB01": 1, "HUB02": 1, "HUB03": 3, "HUB04": 3, "HUB05": 3, "HUB06": 4, "HUB07": 3, "HUB08": 3}
        malls_map = {"HUB01": 1, "HUB02": 0, "HUB03": 2, "HUB04": 1, "HUB05": 1, "HUB06": 1, "HUB07": 3, "HUB08": 3}
        road_dens_map = {"HUB01": 14.2, "HUB02": 15.8, "HUB03": 13.5, "HUB04": 19.4, "HUB05": 21.0, "HUB06": 24.5, "HUB07": 28.2, "HUB08": 30.6}
        pop_map = {"HUB01": 85000, "HUB02": 92000, "HUB03": 78000, "HUB04": 110000, "HUB05": 125000, "HUB06": 165000, "HUB07": 190000, "HUB08": 210000}
        safety_map = {"HUB01": 4.0, "HUB02": 3.8, "HUB03": 2.2, "HUB04": 4.2, "HUB05": 4.5, "HUB06": 4.8, "HUB07": 5.0, "HUB08": 5.0}

        df["condos_1500m"] = [condos_map[hid] for hid in df["hub_id"]]
        df["malls_1500m"] = [malls_map[hid] for hid in df["hub_id"]]
        df["road_density_1500m"] = [road_dens_map[hid] for hid in df["hub_id"]]
        df["pop_catchment"] = [pop_map[hid] for hid in df["hub_id"]]
        df["erosion_safety"] = [safety_map[hid] for hid in df["hub_id"]]

        return df

    def fit(self, custom_weights: Optional[Dict[str, float]] = None) -> TOPSISResult:
        """Executes TOPSIS multi-criteria ranking."""
        df = self._prepare_decision_matrix()
        weights_dict = self.default_weights.copy()
        if custom_weights:
            weights_dict.update(custom_weights)

        # Normalize weights
        w_sum = sum(weights_dict[c] for c in self.criteria_cols)
        w_vec = np.array([weights_dict[c] / w_sum for c in self.criteria_cols])

        # 1. Vector Normalization
        raw_mat = df[self.criteria_cols].values.astype(float)
        col_norms = np.sqrt(np.sum(raw_mat ** 2, axis=0))
        norm_mat = raw_mat / col_norms

        # 2. Weighted Normalized Matrix
        v_mat = norm_mat * w_vec

        # 3. Positive and Negative Ideal Solutions
        a_plus = np.zeros(len(self.criteria_cols))
        a_minus = np.zeros(len(self.criteria_cols))

        for j, col_name in enumerate(self.criteria_cols):
            if self.directions[col_name] == "+":
                a_plus[j] = np.max(v_mat[:, j])
                a_minus[j] = np.min(v_mat[:, j])
            else:
                a_plus[j] = np.min(v_mat[:, j])
                a_minus[j] = np.max(v_mat[:, j])

        # 4. Euclidean distances
        d_plus = np.sqrt(np.sum((v_mat - a_plus) ** 2, axis=1))
        d_minus = np.sqrt(np.sum((v_mat - a_minus) ** 2, axis=1))

        # 5. Relative Closeness
        cc = d_minus / (d_plus + d_minus)

        # 6. Build Results DataFrame
        res_df = df[["hub_id", "hub_name", "segment_id", "district", "dist_to_cbd_km", "est_land_rent_vnd_m2", "ris_readiness_score"]].copy()
        res_df["d_plus"] = np.round(d_plus, 4)
        res_df["d_minus"] = np.round(d_minus, 4)
        res_df["closeness_coefficient"] = np.round(cc, 4)
        res_df = res_df.sort_values(by="closeness_coefficient", ascending=False).reset_index(drop=True)
        res_df["rank"] = res_df.index + 1

        cc_dict = {row["hub_id"]: float(row["closeness_coefficient"]) for _, row in res_df.iterrows()}

        return TOPSISResult(
            rankings_df=res_df,
            weighted_normalized_matrix=v_mat,
            ideal_positive=a_plus,
            ideal_negative=a_minus,
            closeness_coefficients=cc_dict,
        )
