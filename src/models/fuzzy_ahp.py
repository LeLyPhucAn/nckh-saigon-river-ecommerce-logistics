"""
Mô hình toán học Fuzzy AHP.
Áp dụng trung bình hình học Saaty & phân tích mở rộng Chang (1996).
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
    """Đóng gói kết quả đầu ra của mô hình Fuzzy AHP."""
    group_weights: Dict[str, float]
    group_cr: float
    subcriteria_weights: Dict[str, Dict[str, float]]
    subcriteria_cr: Dict[str, float]
    global_weights_df: pd.DataFrame
    is_consistent: bool


class FuzzyAHPModel:
    """Mô hình tính toán trọng số đa tiêu chí Fuzzy AHP."""

    def __init__(self, ahp_matrices: Optional[dict] = None) -> None:
        self.matrices = (
            ahp_matrices if ahp_matrices is not None else load_ahp_matrices()
        )

    @staticmethod
    def calculate_priority_vector(
        matrix: np.ndarray
    ) -> Tuple[np.ndarray, float, float, bool]:
        """
        Tính vector trọng số chuẩn hóa, trị riêng lớn nhất lambda_max,
        chỉ số nhất quán (CI) và tỷ số nhất quán (CR).
        """
        n = matrix.shape[0]
        # Trung bình hình học theo từng hàng
        geom_means = np.prod(matrix, axis=1) ** (1.0 / n)
        weights = geom_means / np.sum(geom_means)

        # Ước lượng trị riêng lớn nhất
        weighted_sum = np.dot(matrix, weights)
        lambda_max = float(np.mean(weighted_sum / weights))

        ci = (lambda_max - n) / (n - 1) if n > 1 else 0.0
        ri = SAATY_RI.get(n, 1.45)
        cr = ci / ri if ri > 0 else 0.0
        is_consistent = cr < 0.10

        return weights, lambda_max, cr, is_consistent

    def fit(self) -> AHPResult:
        """Thực thi tính toán trọng số toàn cục và kiểm định CR."""
        # 1. Trọng số cấp nhóm tiêu chí
        m_group = self.matrices["group_matrix"]
        w_group, _, cr_group, cons_g = self.calculate_priority_vector(m_group)
        if not cons_g:
            raise ValueError(f"Ma trận nhóm không nhất quán: CR = {cr_group:.4f} >= 0.10")

        group_labels = self.matrices["group_labels"]
        group_weights = {
            label: float(w_group[i]) for i, label in enumerate(group_labels)
        }

        # 2. Trọng số cấp tiêu chí con
        sub_weights: Dict[str, Dict[str, float]] = {}
        sub_cr: Dict[str, float] = {}
        all_consistent = cons_g

        for g_key, m_sub in self.matrices["sub_matrices"].items():
            w_sub, _, cr_s, cons_s = self.calculate_priority_vector(m_sub)
            if not cons_s:
                raise ValueError(
                    f"Ma trận nhóm {g_key} không nhất quán: CR = {cr_s:.4f} >= 0.10"
                )
            labels = self.matrices["sub_labels"][g_key]
            sub_weights[g_key] = {
                labels[i]: float(w_sub[i]) for i in range(len(labels))
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
        df_global["global_weight"] = (
            df_global["global_weight"] / df_global["global_weight"].sum()
        ).round(4)

        return AHPResult(
            group_weights=group_weights,
            group_cr=cr_group,
            subcriteria_weights=sub_weights,
            subcriteria_cr=sub_cr,
            global_weights_df=df_global,
            is_consistent=all_consistent,
        )
