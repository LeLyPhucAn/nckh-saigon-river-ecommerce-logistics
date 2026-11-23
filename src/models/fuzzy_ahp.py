"""
Mô hình toán học Triangular Fuzzy AHP (TFN-AHP).
Áp dụng số mờ tam giác TFN (l, m, u), phương pháp trung bình nhân mờ Buckley (1985)
kết hợp kiểm định độ mờ và khử mờ (Defuzzification) trọng tâm COA (Center of Area).
Đảm bảo tỷ số nhất quán CR < 0.10.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd

from src.data_loaders.ahp_matrix_loader import load_ahp_matrices

# Chỉ số ngẫu nhiên Saaty (RI)
SAATY_RI: Dict[int, float] = {
    1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12,
    6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 15: 1.58
}


@dataclass
class AHPResult:
    """Đóng gói kết quả đầu ra của mô hình Triangular Fuzzy AHP."""
    group_weights: Dict[str, float]
    group_fuzzy_weights: Dict[str, Tuple[float, float, float]]
    group_cr: float
    subcriteria_weights: Dict[str, Dict[str, float]]
    subcriteria_fuzzy_weights: Dict[str, Dict[str, Tuple[float, float, float]]]
    subcriteria_cr: Dict[str, float]
    global_weights_df: pd.DataFrame
    is_consistent: bool


class FuzzyAHPModel:
    """Mô hình tính toán trọng số đa tiêu chí Triangular Fuzzy AHP."""

    def __init__(self, ahp_matrices: Optional[dict] = None) -> None:
        self.matrices = (
            ahp_matrices if ahp_matrices is not None else load_ahp_matrices()
        )

    @staticmethod
    def crisp_to_tfn(val: float) -> np.ndarray:
        """
        Chuyển đổi thang đo Saaty sang Số mờ tam giác (TFN): (l, m, u).
        Nếu a_ij = 1 -> (1, 1, 1)
        Nếu a_ij > 1 -> (a_ij - 1, a_ij, a_ij + 1)
        Nếu a_ij < 1 -> (1 / (1/a_ij + 1), a_ij, 1 / max(1, 1/a_ij - 1))
        """
        if np.isclose(val, 1.0):
            return np.array([1.0, 1.0, 1.0])
        elif val > 1.0:
            return np.array([val - 1.0, val, val + 1.0])
        else:
            recip = 1.0 / val
            lower = 1.0 / (recip + 1.0)
            mid = val
            upper = 1.0 / max(1.0, recip - 1.0)
            return np.array([lower, mid, upper])

    @classmethod
    def calculate_fuzzy_priority_vector(
        cls, crisp_matrix: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray, float, bool]:
        """
        Tính toán vector trọng số mờ bằng phương pháp Buckley (1985),
        khử mờ bằng phương pháp trọng tâm (COA) và kiểm định tính nhất quán CR.
        """
        n = crisp_matrix.shape[0]

        # 1. Chuyển đổi ma trận thực sang ma trận mờ tam giác (n, n, 3)
        fuzzy_mat = np.zeros((n, n, 3))
        for i in range(n):
            for j in range(n):
                fuzzy_mat[i, j] = cls.crisp_to_tfn(crisp_matrix[i, j])

        # 2. Tính trung bình nhân mờ theo hàng: r_i = (prod l)^(1/n), (prod m)^(1/n), (prod u)^(1/n)
        geom_l = np.prod(fuzzy_mat[:, :, 0], axis=1) ** (1.0 / n)
        geom_m = np.prod(fuzzy_mat[:, :, 1], axis=1) ** (1.0 / n)
        geom_u = np.prod(fuzzy_mat[:, :, 2], axis=1) ** (1.0 / n)

        sum_l = float(np.sum(geom_l))
        sum_m = float(np.sum(geom_m))
        sum_u = float(np.sum(geom_u))

        # Vector trọng số mờ: w_tilde_i = r_i (*) (sum_r)^(-1)
        fuzzy_weights = np.column_stack([
            geom_l / sum_u,
            geom_m / sum_m,
            geom_u / sum_l
        ])

        # 3. Khử mờ (Defuzzification) bằng phương pháp trọng tâm COA: w_i = (l + m + u) / 3
        crisp_weights = np.mean(fuzzy_weights, axis=1)
        normalized_weights = crisp_weights / np.sum(crisp_weights)

        # 4. Kiểm định tỷ số nhất quán CR trên ma trận thức (modal values m_ij)
        weighted_sum = np.dot(crisp_matrix, normalized_weights)
        lambda_max = float(np.mean(weighted_sum / normalized_weights))

        ci = (lambda_max - n) / (n - 1) if n > 1 else 0.0
        ri = SAATY_RI.get(n, 1.45)
        cr = ci / ri if ri > 0 else 0.0
        is_consistent = cr < 0.10

        return normalized_weights, fuzzy_weights, cr, is_consistent

    def fit(self) -> AHPResult:
        """Thực thi tính toán trọng số toàn cục Fuzzy AHP và kiểm định CR."""
        # 1. Trọng số cấp nhóm tiêu chí
        m_group = self.matrices["group_matrix"]
        w_group, fw_group, cr_group, cons_g = self.calculate_fuzzy_priority_vector(m_group)
        if not cons_g:
            raise ValueError(f"Ma trận nhóm không nhất quán: CR = {cr_group:.4f} >= 0.10")

        group_labels = self.matrices["group_labels"]
        group_weights = {
            label: float(w_group[i]) for i, label in enumerate(group_labels)
        }
        group_fuzzy_weights = {
            label: (float(fw_group[i, 0]), float(fw_group[i, 1]), float(fw_group[i, 2]))
            for i, label in enumerate(group_labels)
        }

        # 2. Trọng số cấp tiêu chí con
        sub_weights: Dict[str, Dict[str, float]] = {}
        sub_fuzzy_weights: Dict[str, Dict[str, Tuple[float, float, float]]] = {}
        sub_cr: Dict[str, float] = {}
        all_consistent = cons_g

        for g_key, m_sub in self.matrices["sub_matrices"].items():
            w_sub, fw_sub, cr_s, cons_s = self.calculate_fuzzy_priority_vector(m_sub)
            if not cons_s:
                raise ValueError(
                    f"Ma trận nhóm {g_key} không nhất quán: CR = {cr_s:.4f} >= 0.10"
                )
            labels = self.matrices["sub_labels"][g_key]
            sub_weights[g_key] = {
                labels[i]: float(w_sub[i]) for i in range(len(labels))
            }
            sub_fuzzy_weights[g_key] = {
                labels[i]: (float(fw_sub[i, 0]), float(fw_sub[i, 1]), float(fw_sub[i, 2]))
                for i, range_idx in enumerate(range(len(labels)))
            }
            sub_cr[g_key] = cr_s
            all_consistent = all_consistent and cons_s

        # 3. Tổng hợp trọng số toàn cục: W_global = W_group * W_local
        indicators_def: List[Tuple[str, str, str, str]] = [
            ("NAV1", "Tĩnh không cầu & Độ sâu luồng", "NAV", "+"),
            ("NAV2", "Mật độ cầu bến tiếp cận", "NAV", "+"),
            ("NAV3", "Hạ tầng số RIS & Viễn thông", "NAV", "+"),
            ("ECO1", "Mật độ dân cư & Chung cư", "ECO", "+"),
            ("ECO2", "Khoảng cách tới kho tổng", "ECO", "-"),
            ("ECO3", "Kết nối mạng lưới đường bộ", "ECO", "+"),
            ("FIN1", "Giá thuê mặt bằng ven sông", "FIN", "-"),
            ("FIN2", "Chi phí vận hành tàu điện/hybrid", "FIN", "-"),
            ("FIN3", "Chi phí bốc xếp tại Micro-Hub", "FIN", "-"),
            ("ENV1", "Tiềm năng giảm phát thải CO2", "ENV", "+"),
            ("ENV2", "Giảm tải điểm nóng ùn tắc", "ENV", "+"),
            ("ENV3", "Rủi ro sạt lở & Sóng tàu", "ENV", "-"),
            ("BEH1", "Thái độ ủng hộ logistics xanh", "SOC_BEH", "+"),
            ("BEH2", "Sẵn sàng chuyển đổi của 3PL/Shop", "SOC_BEH", "+"),
            ("SOC1", "Xung đột giao thông thủy & Rủi ro", "SOC_BEH", "-"),
        ]

        records = []
        for code, name, grp, direction in indicators_def:
            local_w = sub_weights[grp][code]
            grp_w = group_weights[grp]
            gw = grp_w * local_w
            fw_local = sub_fuzzy_weights[grp][code]
            records.append({
                "indicator_code": code,
                "indicator_name": name,
                "group_code": grp,
                "direction": direction,
                "group_weight": round(grp_w, 4),
                "local_weight": round(local_w, 4),
                "global_weight": round(gw, 4),
                "fuzzy_l": round(fw_local[0] * group_fuzzy_weights[grp][0], 4),
                "fuzzy_m": round(fw_local[1] * group_fuzzy_weights[grp][1], 4),
                "fuzzy_u": round(fw_local[2] * group_fuzzy_weights[grp][2], 4),
            })

        df_global = pd.DataFrame(records)
        df_global["global_weight"] = (
            df_global["global_weight"] / df_global["global_weight"].sum()
        ).round(4)

        return AHPResult(
            group_weights=group_weights,
            group_fuzzy_weights=group_fuzzy_weights,
            group_cr=cr_group,
            subcriteria_weights=sub_weights,
            subcriteria_fuzzy_weights=sub_fuzzy_weights,
            subcriteria_cr=sub_cr,
            global_weights_df=df_global,
            is_consistent=all_consistent,
        )
