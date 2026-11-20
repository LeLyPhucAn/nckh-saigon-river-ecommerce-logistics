"""
Mô đun nạp dữ liệu bến ứng viên và đoạn sông.
Đọc từ data/raw/candidate_hubs_raw.csv và data/raw/river_corridor_raw.csv.
"""

from pathlib import Path
from typing import Optional
import pandas as pd

from src.config import RAW_DATA_DIR


def load_candidate_hubs(file_path: Optional[Path] = None) -> pd.DataFrame:
    """Nạp và kiểm tra cấu trúc dữ liệu 8 bến Micro-Hub ứng viên."""
    if file_path is None:
        file_path = RAW_DATA_DIR / "candidate_hubs_raw.csv"

    if not file_path.exists():
        raise FileNotFoundError(f"Không tìm thấy tệp bến ứng viên: {file_path}")

    df = pd.read_csv(file_path, encoding="utf-8")
    required_cols = [
        "hub_id", "hub_name", "segment_id", "district",
        "lat", "lon", "nearest_bridge", "bridge_clearance_m",
        "river_depth_m", "dist_to_cbd_km", "est_land_rent_vnd_m2",
        "ris_readiness_score"
    ]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Thiếu cột bắt buộc trong dữ liệu bến: {col}")

    return df


def load_river_segments(file_path: Optional[Path] = None) -> pd.DataFrame:
    """Nạp và kiểm tra cấu trúc dữ liệu 3 tiểu đoạn hành lang sông."""
    if file_path is None:
        file_path = RAW_DATA_DIR / "river_corridor_raw.csv"

    if not file_path.exists():
        raise FileNotFoundError(f"Không tìm thấy tệp đoạn sông: {file_path}")

    df = pd.read_csv(file_path, encoding="utf-8")
    required_cols = [
        "segment_id", "segment_name", "start_point", "end_point",
        "length_km", "avg_depth_m", "num_bridges",
        "min_bridge_clearance_m", "role"
    ]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Thiếu cột bắt buộc trong dữ liệu đoạn sông: {col}")

    return df
