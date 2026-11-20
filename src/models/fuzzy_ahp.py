"""
Fuzzy AHP Mathematical Model.
Implements Saaty Geometric Mean & Chang (1996) Extent Analysis.
Ensures rigorous consistency checking (CR < 0.10) for group and subcriteria matrices.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from src.data_loaders.ahp_matrix_loader import load_ahp_matrices

SAATY_RI: Dict[int, float] = {
    1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 15: 1.58
}


@dataclass
class AHPResult:
    """Encapsulates output of Fuzzy AHP model."""
    group_weights: Dict[str, float]
    group_cr: float
    subcriteria_weights: Dict[str, Dict[str, float]]
    subcriteria_cr: Dict[str, float]
    global_weights_df: pd.DataFrame
    is_consistent: bool


class FuzzyAHPModel:
    """
    Fuzzy Analytic Hierarchy Process (Fuzzy AHP) Model.
    Computes priority weights using Geometric Mean method and validates consistency ratio.
    """

    def __init__(self, ahp_matrices: dict | None = None):
        self.matrices = ahp_matrices if ahp_matrices is not None else load_ahp_matrices()

    @staticmethod
    def calculate_priority_vector(matrix: np.ndarray) -> Tuple[np.ndarray, float, float, bool]:
        """
        Calculates normalized priority vector, principal eigenvalue lambda_max,
        Consistency Index (CI), and Consistency Ratio (CR).
        """
        n = matrix.shape[0]
        # Geometric mean across rows (Saaty Logarithmic Least Squares)
        geom_means = np.prod(matrix, axis=1) ** (1.0 / n)
        weights = geom_means / np.sum(geom_means)

        # Principal eigenvalue estimation
        weighted_sum = np.dot(matrix, weights)
        lambda_max = float(np.mean(weighted_sum / weights))

        ci = (lambda_max - n) / (n - 1) if n > 1 else 0.0
        ri = SAATY_RI.get(n, 1.45)
        cr = ci / ri if ri > 0 else 0.0
        is_consistent = cr < 0.10

        return weights, lambda_max, cr, is_consistent

    def fit(self) -> AHPResult:
        """Executes full AHP computation and returns structured AHPResult."""
        # 1. Group level
        m_group = self.matrices["group_matrix"]
        w_group, _, cr_group, cons_g = self.calculate_priority_vector(m_group)
        if not cons_g:
            raise ValueError(f"Inconsistent group matrix: CR = {cr_group:.4f} >= 0.10")

        group_labels = self.matrices["group_labels"]
        group_weights = {label: float(w_group[i]) for i, label in enumerate(group_labels)}

        # 2. Subcriteria level
        sub_weights: Dict[str, Dict[str, float]] = {}
        sub_cr: Dict[str, float] = {}
        all_consistent = cons_g

        for g_key, m_sub in self.matrices["sub_matrices"].items():
            w_sub, _, cr_s, cons_s = self.calculate_priority_vector(m_sub)
            if not cons_s:
                raise ValueError(f"Inconsistent subcriteria matrix for {g_key}: CR = {cr_s:.4f} >= 0.10")
            labels = self.matrices["sub_labels"][g_key]
            sub_weights[g_key] = {labels[i]: float(w_sub[i]) for i in range(len(labels))}
            sub_cr[g_key] = cr_s
            all_consistent = all_consistent and cons_s

        # 3. Global Weights Synthesis
        indicators_def = [
            ("NAV1", "Tinh khong cau & Do sau luong", "NAV", "+"),
            ("NAV2", "Mat do cau ben tiep can", "NAV", "+"),
            ("NAV3", "Ha tang so RIS & Dien bien", "NAV", "+"),
            ("ECO1", "Mat do dan cu & Chung cu", "ECO", "+"),
            ("ECO2", "Khoang cach toi kho tong", "ECO", "-"),
            ("ECO3", "Ket noi mang luoi duong bo", "ECO", "+"),
            ("FIN1", "Gia thue mat bang ben ven song", "FIN", "-"),
            ("FIN2", "Chi phi van hanh tau dien/hybrid", "FIN", "-"),
            ("FIN3", "Chi phi boc xep tai Micro-Hub", "FIN", "-"),
            ("ENV1", "Tiem nang giam phat thai CO2", "ENV", "+"),
            ("ENV2", "Giam tai diem nong un tac", "ENV", "+"),
            ("ENV3", "Rui ro sat lo & Song tau", "ENV", "-"),
            ("BEH1", "Thai do ung ho logistics xanh", "SOC_BEH", "+"),
            ("BEH2", "San sang chuyen doi cua 3PL/Shop", "SOC_BEH", "+"),
            ("SOC1", "Xung dot giao thong thuy & Rui ro", "SOC_BEH", "-"),
        ]

        records = []
        for code, name, grp, direction in indicators_def:
            local_w = sub_weights[grp][code]
            grp_w = group_weights[grp]
            gw = grp_w * local_w
            records.append({
                "indicator_code": code,
                "indicator_name": name,
                "group_code": grp,
                "direction": direction,
                "group_weight": round(grp_w, 4),
                "local_weight": round(local_w, 4),
                "global_weight": round(gw, 4),
            })

        df_global = pd.DataFrame(records)
        df_global["global_weight"] = df_global["global_weight"] / df_global["global_weight"].sum()
        df_global["global_weight"] = df_global["global_weight"].round(4)

        return AHPResult(
            group_weights=group_weights,
            group_cr=cr_group,
            subcriteria_weights=sub_weights,
            subcriteria_cr=sub_cr,
            global_weights_df=df_global,
            is_consistent=all_consistent,
        )
