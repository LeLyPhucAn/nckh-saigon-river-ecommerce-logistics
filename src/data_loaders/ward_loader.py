"""
Ward Socio-Economic Data Loader.
Reads and validates the 28 wards dataset from data/raw/ward_socioeconomic_raw.csv.
"""

from pathlib import Path
import pandas as pd
from src.config import RAW_DATA_DIR


def load_ward_socioeconomic_data(file_path: Path | None = None) -> pd.DataFrame:
    """Loads and validates the 28-ward socio-economic dataset."""
    if file_path is None:
        file_path = RAW_DATA_DIR / "ward_socioeconomic_raw.csv"

    if not file_path.exists():
        raise FileNotFoundError(f"Ward socio-economic raw file not found at: {file_path}")

    df = pd.read_csv(file_path, encoding="utf-8")
    required_cols = [
        "ward_name", "district", "pop_density_k_per_km2",
        "dist_to_hub_km", "land_rent_mil_vnd_m2",
        "road_ris_score", "est_saving_pct"
    ]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column in ward data: {col}")

    if len(df) < 25:
        raise ValueError(f"Expected at least 25 wards along the corridor, got {len(df)}")

    return df
