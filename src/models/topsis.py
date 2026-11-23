"""
Mô hình ra quyết định đa tiêu chí TOPSIS (Giai đoạn 2).
Chuẩn hóa vector, xác định giải pháp lý tưởng A+, A- và hệ số gần gũi CC_k.
Nhận dữ liệu trực tiếp từ GIS Ngày 1 và trọng số toàn cục từ Triangular Fuzzy AHP.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional
import numpy as np
import pandas as pd

from src.config import PROCESSED_DATA_DIR
from src.data_loaders.hub_loader import load_candidate_hubs


@dataclass
class TOPSISResult:
    """Đóng gói kết quả xếp hạng của thuật toán TOPSIS."""
    rankings_df: pd.DataFrame
    weighted_normalized_matrix: np.ndarray
    ideal_positive: np.ndarray
    ideal_negative: np.ndarray
    closeness_coefficients: Dict[str, float]


class TOPSISModel:
    """Mô hình TOPSIS tuyển chọn vị trí đặt trạm Micro-Hub."""

    def __init__(
        self, candidate_hubs_df: Optional[pd.DataFrame] = None
    ) -> None:
        if candidate_hubs_df is not None:
            self.hubs_df = candidate_hubs_df.copy()
        else:
            gis_path = PROCESSED_DATA_DIR / "gis_candidate_hubs.csv"
            if gis_path.exists():
                self.hubs_df = pd.read_csv(gis_path)
            else:
                self.hubs_df = load_candidate_hubs()

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
        """
        Đồng bộ tên cột từ dữ liệu GIS và thông số kỹ thuật thực địa.
        Loại bỏ hoàn toàn các cấu trúc dictionary gán cứng.
        """
        df = self.hubs_df.copy()

        # Ánh xạ cột từ GIS sang định dạng chuẩn của TOPSIS
        if "road_density_1500m_km_per_km2" in df.columns and "road_density_1500m" not in df.columns:
            df["road_density_1500m"] = df["road_density_1500m_km_per_km2"]

        if "population_1500m" in df.columns and "pop_catchment" not in df.columns:
            df["pop_catchment"] = df["population_1500m"]

        if "erosion_safety_score" in df.columns and "erosion_safety" not in df.columns:
            df["erosion_safety"] = df["erosion_safety_score"]

        # Đảm bảo đầy đủ các cột tiêu chuẩn
        for col in self.criteria_cols:
            if col not in df.columns:
                raise ValueError(f"Thiếu trường dữ liệu '{col}' trong ma trận quyết định TOPSIS.")

        return df

    def derive_weights_from_ahp(
        self, ahp_global_weights_df: pd.DataFrame
    ) -> Dict[str, float]:
        """
        Chuyển hóa trọng số toàn cục từ Triangular Fuzzy AHP sang 10 tiêu chí TOPSIS.
        Tạo liên kết chặt chẽ giữa AHP và TOPSIS.
        """
        w_map = dict(zip(
            ahp_global_weights_df["indicator_code"],
            ahp_global_weights_df["global_weight"]
        ))

        # Phân bổ trọng số chỉ số AHP vào các tiêu chí đo lường cụ thể của bến
        raw_weights = {
            "bridge_clearance_m": w_map.get("NAV1", 0.10) * 0.55,
            "river_depth_m": w_map.get("NAV1", 0.10) * 0.45,
            "ris_readiness_score": w_map.get("NAV3", 0.06) * 1.20,
            "condos_1500m": w_map.get("ECO1", 0.16) * 0.85,
            "pop_catchment": w_map.get("ECO1", 0.16) * 0.75,
            "malls_1500m": w_map.get("ECO3", 0.05) * 1.10,
            "road_density_1500m": w_map.get("ECO3", 0.05) * 1.30,
            "dist_to_cbd_km": w_map.get("ECO2", 0.09) * 0.90,
            "est_land_rent_vnd_m2": w_map.get("FIN1", 0.15) * 1.10,
            "erosion_safety": w_map.get("ENV3", 0.013) * 4.00,
        }

        total_w = sum(raw_weights.values())
        return {k: round(v / total_w, 4) for k, v in raw_weights.items()}

    def fit(
        self,
        custom_weights: Optional[Dict[str, float]] = None,
        ahp_global_weights_df: Optional[pd.DataFrame] = None,
    ) -> TOPSISResult:
        """Chạy thuật toán xếp hạng TOPSIS."""
        df = self._prepare_decision_matrix()

        # Xác định trọng số
        if ahp_global_weights_df is not None:
            weights_dict = self.derive_weights_from_ahp(ahp_global_weights_df)
        else:
            weights_dict = self.default_weights.copy()

        if custom_weights:
            weights_dict.update(custom_weights)

        # Chuẩn hóa tổng trọng số = 1.0
        w_sum = sum(weights_dict[c] for c in self.criteria_cols)
        w_vec = np.array([weights_dict[c] / w_sum for c in self.criteria_cols])

        # 1. Chuẩn hóa vector
        raw_mat = df[self.criteria_cols].values.astype(float)
        col_norms = np.sqrt(np.sum(raw_mat ** 2, axis=0))
        # Tránh chia cho 0
        col_norms[col_norms == 0] = 1.0
        norm_mat = raw_mat / col_norms

        # 2. Nhân trọng số
        v_mat = norm_mat * w_vec

        # 3. Xác định nghiệm lý tưởng dương (A+) và âm (A-)
        a_plus = np.zeros(len(self.criteria_cols))
        a_minus = np.zeros(len(self.criteria_cols))

        for j, col_name in enumerate(self.criteria_cols):
            if self.directions[col_name] == "+":
                a_plus[j] = np.max(v_mat[:, j])
                a_minus[j] = np.min(v_mat[:, j])
            else:
                a_plus[j] = np.min(v_mat[:, j])
                a_minus[j] = np.max(v_mat[:, j])

        # 4. Khoảng cách Euclid D+ và D-
        d_plus = np.sqrt(np.sum((v_mat - a_plus) ** 2, axis=1))
        d_minus = np.sqrt(np.sum((v_mat - a_minus) ** 2, axis=1))

        # 5. Hệ số gần gũi tương đối CC_k
        denom = d_plus + d_minus
        denom[denom == 0] = 1e-6
        cc = d_minus / denom

        # 6. Xuất bảng kết quả xếp hạng
        res_cols = [
            "hub_id", "hub_name", "segment_id", "district",
            "dist_to_cbd_km", "est_land_rent_vnd_m2", "ris_readiness_score"
        ]
        res_df = df[res_cols].copy()
        res_df["d_plus"] = np.round(d_plus, 4)
        res_df["d_minus"] = np.round(d_minus, 4)
        res_df["closeness_coefficient"] = np.round(cc, 4)
        res_df = res_df.sort_values(
            by="closeness_coefficient", ascending=False
        ).reset_index(drop=True)
        res_df["rank"] = res_df.index + 1

        cc_dict = {
            row["hub_id"]: float(row["closeness_coefficient"])
            for _, row in res_df.iterrows()
        }

        return TOPSISResult(
            rankings_df=res_df,
            weighted_normalized_matrix=v_mat,
            ideal_positive=a_plus,
            ideal_negative=a_minus,
            closeness_coefficients=cc_dict,
        )
