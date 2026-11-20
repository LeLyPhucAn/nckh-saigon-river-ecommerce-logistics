"""
Mô hình đánh giá tiềm năng tiểu đoạn sông (Giai đoạn 1).
Chuẩn hóa Min-Max theo hướng tiêu chí (J+, J-) và tính điểm WLC.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import pandas as pd

from src.data_loaders.hub_loader import load_river_segments
from .fuzzy_ahp import FuzzyAHPModel


@dataclass
class SegmentResult:
    """Đóng gói kết quả chấm điểm tiềm năng đoạn sông."""
    normalized_matrix: pd.DataFrame
    summary_scores_df: pd.DataFrame
    scores_dict: Dict[str, float]


class SegmentEvaluator:
    """Đánh giá và xếp hạng tiềm năng 3 tiểu đoạn sông Sài Gòn."""

    def __init__(self, ahp_model: Optional[FuzzyAHPModel] = None) -> None:
        self.ahp_model = ahp_model if ahp_model is not None else FuzzyAHPModel()

    def evaluate(self) -> SegmentResult:
        """Chuẩn hóa chỉ số và tính điểm tiềm năng tổng hợp."""
        ahp_res = self.ahp_model.fit()
        df_weights = ahp_res.global_weights_df

        # Ma trận giá trị thực địa theo 15 chỉ số
        raw_matrix_dict = {
            "indicator_code": [
                "NAV1", "NAV2", "NAV3",
                "ECO1", "ECO2", "ECO3",
                "FIN1", "FIN2", "FIN3",
                "ENV1", "ENV2", "ENV3",
                "BEH1", "BEH2", "SOC1"
            ],
            "SEG1": [7.0, 1.2, 4.2, 5.0, 4.5, 14.5, 196666, 420000, 2200, 85.0, 3.2, 3.8, 3.8, 3.6, 1.8],
            "SEG2": [10.0, 1.8, 4.8, 10.0, 9.8, 21.6, 350000, 510000, 2800, 145.0, 4.4, 2.2, 4.2, 4.1, 2.5],
            "SEG3": [10.0, 2.4, 5.0, 6.0, 14.2, 29.4, 600000, 590000, 3500, 190.0, 4.8, 1.5, 4.5, 4.3, 3.2],
        }
        df_raw = pd.DataFrame(raw_matrix_dict)
        weight_cols = ["indicator_code", "direction", "global_weight"]
        df_merged = pd.merge(df_raw, df_weights[weight_cols], on="indicator_code")

        segments: List[str] = ["SEG1", "SEG2", "SEG3"]
        norm_matrix = df_merged.copy()

        # Chuẩn hóa Min-Max: Lợi ích (+) và Chi phí (-)
        for idx, row in df_merged.iterrows():
            vals = [row[s] for s in segments]
            min_v, max_v = min(vals), max(vals)
            direction = row["direction"]

            for s in segments:
                val = row[s]
                if max_v == min_v:
                    norm_v = 1.0
                elif direction == "+":
                    norm_v = (val - min_v) / (max_v - min_v)
                else:
                    norm_v = (max_v - val) / (max_v - min_v)
                norm_matrix.at[idx, s] = round(norm_v, 4)

        # Tính điểm tổng hợp có trọng số
        scores: Dict[str, float] = {}
        for s in segments:
            weighted_val = norm_matrix[s] * norm_matrix["global_weight"]
            scores[s] = round(float(weighted_val.sum()), 4)

        # Lập bảng kết quả xếp hạng
        df_seg_meta = load_river_segments()
        summary_records = []
        for _, s_row in df_seg_meta.iterrows():
            sid = s_row["segment_id"]
            summary_records.append({
                "segment_id": sid,
                "segment_name": s_row["segment_name"],
                "length_km": s_row["length_km"],
                "composite_score": scores[sid],
                "role": s_row["role"],
            })

        df_summary = pd.DataFrame(summary_records)
        df_summary = df_summary.sort_values(
            by="composite_score", ascending=False
        ).reset_index(drop=True)
        df_summary["rank"] = df_summary.index + 1

        return SegmentResult(
            normalized_matrix=norm_matrix,
            summary_scores_df=df_summary,
            scores_dict=scores,
        )
