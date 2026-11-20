"""
Corridor Segment Potential Scoring Module (Stage 1).
Implements Min-Max normalization for Benefit (J+) and Cost (J-) indicators,
and calculates the composite potential score for the 3 Saigon River segments:
- Segment 1: Hiep Binh Chanh - Thanh Da (Inbound Consolidation Gateway)
- Segment 2: Thao Dien - Tan Cang (High-Density Transition Urban Zone)
- Segment 3: Ba Son - Bach Dang - Khanh Hoi (Central Business District Core)
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from src.config import TABLES_DIR, CHARTS_DIR
from .fuzzy_ahp import compute_global_fuzzy_ahp_weights


def build_raw_segment_matrix() -> pd.DataFrame:
    """
    Constructs the 3 Segments x 15 Indicators decision matrix based on empirical
    HCMC data (Sở GTVT, World Bank, Savills/CBRE, OpenStreetMap).
    """
    data = {
        "indicator_code": [
            "NAV1", "NAV2", "NAV3",
            "ECO1", "ECO2", "ECO3",
            "FIN1", "FIN2", "FIN3",
            "ENV1", "ENV2", "ENV3",
            "BEH1", "BEH2", "SOC1"
        ],
        "SEG1": [
            7.0,   1.2,  4.2,   # NAV: 7.0m clearance (Binh Loi), 1.2 berths/km2, RIS 4.2
            5.0,   4.5, 14.5,   # ECO: 5 condos, 4.5km to warehouse, 14.5 km/km2 road
            196666, 420000, 2200, # FIN: 196k/m2 land, 420k OPEX/trip, 2200 VND/parcel handling
            85.0,  3.2,  3.8,   # ENV: 85 kg CO2/day, decongestion 3.2, erosion risk 3.8 (Thanh Da)
            3.8,   3.6,  1.8    # SOC: Green attitude 3.8, 3PL ready 3.6, water conflicts 1.8/yr
        ],
        "SEG2": [
            10.0,  1.8,  4.8,   # NAV: 10m clearance (Cau SG), 1.8 berths/km2, RIS 4.8
            10.0,  9.8, 21.6,   # ECO: 10 condos, 9.8km to warehouse, 21.6 km/km2 road
            350000, 510000, 2800, # FIN: 350k/m2 land, 510k OPEX/trip, 2800 VND/parcel handling
            145.0, 4.4,  2.2,   # ENV: 145 kg CO2/day, decongestion 4.4, erosion risk 2.2
            4.2,   4.1,  2.5    # SOC: Green attitude 4.2, 3PL ready 4.1, water conflicts 2.5/yr
        ],
        "SEG3": [
            10.0,  2.4,  5.0,   # NAV: 10m clearance, 2.4 berths/km2, RIS 5.0
            6.0,  14.2, 29.4,   # ECO: 6 condos, 14.2km to warehouse, 29.4 km/km2 road
            600000, 590000, 3500, # FIN: 600k/m2 land, 590k OPEX/trip, 3500 VND/parcel handling
            190.0, 4.8,  1.5,   # ENV: 190 kg CO2/day, decongestion 4.8, erosion risk 1.5
            4.5,   4.3,  3.2    # SOC: Green attitude 4.5, 3PL ready 4.3, water conflicts 3.2/yr
        ],
    }
    return pd.DataFrame(data)


def score_corridor_segments() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Normalizes segment indicators and calculates composite potential scores using Fuzzy AHP weights.
    Returns (df_normalized, df_segment_scores).
    """
    df_raw = build_raw_segment_matrix()
    df_weights = compute_global_fuzzy_ahp_weights()

    # Merge weights and directions
    df_merged = pd.merge(df_raw, df_weights[["indicator_code", "direction", "global_weight"]], on="indicator_code")

    segments = ["SEG1", "SEG2", "SEG3"]
    norm_matrix = df_merged.copy()

    # Min-Max Normalization
    for idx, row in df_merged.iterrows():
        vals = [row[s] for s in segments]
        min_v = min(vals)
        max_v = max(vals)
        direction = row["direction"]

        for s in segments:
            val = row[s]
            if max_v == min_v:
                norm_v = 1.0
            else:
                if direction == "+":  # Benefit
                    norm_v = (val - min_v) / (max_v - min_v)
                else:                 # Cost
                    norm_v = (max_v - val) / (max_v - min_v)
            norm_matrix.at[idx, s] = round(norm_v, 4)

    # Calculate weighted scores: Score_s = sum(Weight_i * Norm_is)
    scores = {}
    for s in segments:
        weighted_val = norm_matrix[s] * norm_matrix["global_weight"]
        scores[s] = round(float(weighted_val.sum()), 4)

    # Segment summary table
    summary_data = [
        {
            "segment_id": "SEG1",
            "segment_name": "Đoạn 1: Hiệp Bình Chánh – Thanh Đa (Cửa ngõ Đông Bắc)",
            "composite_score": scores["SEG1"],
            "rank": 0,
            "strengths": "Chi phí mặt bằng thấp, gần kho tổng Thủ Đức/BD, ít xung đột tàu thuyền",
            "bottlenecks": "Tĩnh không cầu Bình Lợi (7m), phụ tải thương mại trung bình, sạt lở bờ Thanh Đa",
        },
        {
            "segment_id": "SEG2",
            "segment_name": "Đoạn 2: Thảo Điền – Tân Cảng (Đô thị chuyển tiếp mật độ cao)",
            "composite_score": scores["SEG2"],
            "rank": 0,
            "strengths": "Mật độ chung cư dày đặc (Vinhomes, Masteri), tĩnh không cao (10m), bờ kè kiên cố",
            "bottlenecks": "Giá thuê đất tăng cao, chi phí vận hành tàu tầm trung",
        },
        {
            "segment_id": "SEG3",
            "segment_name": "Đoạn 3: Ba Son – Bạch Đằng – Khánh Hội (Lõi CBD tiêu thụ)",
            "composite_score": scores["SEG3"],
            "rank": 0,
            "strengths": "Mạng lưới đường bộ chặng cuối cực tốt, giảm phát thải cao nhất, hạ tầng RIS hoàn thiện",
            "bottlenecks": "Đơn giá thuê mặt bằng rất cao (600k/m2), xa kho tổng phía Bắc, xung đột giao thông thủy",
        },
    ]

    df_scores = pd.DataFrame(summary_data)
    df_scores = df_scores.sort_values(by="composite_score", ascending=False).reset_index(drop=True)
    df_scores["rank"] = df_scores.index + 1

    return norm_matrix, df_scores


def export_segment_scoring_and_plot() -> tuple[Path, Path]:
    """Exports segment scores to CSV and creates a comparative bar chart."""
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)

    norm_matrix, df_scores = score_corridor_segments()

    csv_path = TABLES_DIR / "corridor_segment_scores.csv"
    df_scores.to_csv(csv_path, index=False, encoding="utf-8-sig")

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#fafbfc")

    colors = ["#023e8a", "#0077b6", "#48cae4"]
    bars = ax.bar(
        df_scores["segment_id"],
        df_scores["composite_score"],
        color=colors,
        edgecolor="#1b263b",
        linewidth=1.2,
        width=0.45,
    )

    for bar, score in zip(bars, df_scores["composite_score"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.015,
            f"Score: {score:.4f}",
            ha="center",
            va="bottom",
            fontsize=10.5,
            fontweight="bold",
            color="#1d3557",
        )

    ax.set_title(
        "Saigon River Corridor: E-Commerce Potential Composite Score by Segment\n"
        "(Fuzzy AHP Weighted Linear Combination: Stage 1)",
        fontsize=12.5,
        fontweight="bold",
        pad=15,
    )
    ax.set_ylabel("Composite Potential Score (0.00 - 1.00)", fontsize=10.5, fontweight="bold")
    ax.set_ylim(0, 1.0)
    ax.set_xticks(range(len(df_scores)))
    ax.set_xticklabels([
        "SEG2: Thảo Điền - Tân Cảng\n(Rank 1 - High Density)",
        "SEG1: HBC - Thanh Đa\n(Rank 2 - Inbound Gateway)",
        "SEG3: Ba Son - Bạch Đằng\n(Rank 3 - CBD Last-mile)",
    ], fontsize=9.5, fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    plt.tight_layout()
    chart_path = CHARTS_DIR / "segment_potential_scores.png"
    fig.savefig(chart_path, dpi=300)
    plt.close(fig)

    return csv_path, chart_path


if __name__ == "__main__":
    c_path, p_path = export_segment_scoring_and_plot()
    print(f"Segment scores exported to: {c_path}")
    print(f"Chart saved to: {p_path}")
