"""
Candidate Hubs & River Corridor Data Loader.
Reads raw data from data/raw/candidate_hubs_raw.csv and data/raw/river_corridor_raw.csv.
"""

from pathlib import Path
import pandas as pd
from src.config import RAW_DATA_DIR


def load_candidate_hubs(file_path: Path | None = None) -> pd.DataFrame:
    """Loads and validates the 8 candidate Micro-Hubs raw dataset."""
    if file_path is None:
        file_path = RAW_DATA_DIR / "candidate_hubs_raw.csv"

    if not file_path.exists():
        raise FileNotFoundError(f"Candidate hubs raw file not found at: {file_path}")

    df = pd.read_csv(file_path, encoding="utf-8")
    required_cols = [
        "hub_id", "hub_name", "segment_id", "district",
        "lat", "lon", "nearest_bridge", "bridge_clearance_m",
        "river_depth_m", "dist_to_cbd_km", "est_land_rent_vnd_m2",
        "ris_readiness_score"
    ]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column in candidate hubs: {col}")

    return df


def load_river_segments(file_path: Path | None = None) -> pd.DataFrame:
    """Loads and validates the 3 corridor segments raw dataset."""
    if file_path is None:
        file_path = RAW_DATA_DIR / "river_corridor_raw.csv"

    if not file_path.exists():
        raise FileNotFoundError(f"River corridor raw file not found at: {file_path}")

    df = pd.read_csv(file_path, encoding="utf-8")
    required_cols = [
        "segment_id", "segment_name", "start_point", "end_point",
        "length_km", "avg_depth_m", "num_bridges", "min_bridge_clearance_m", "role"
    ]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column in river corridor: {col}")

    return df
