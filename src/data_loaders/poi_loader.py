"""
Notable POIs Data Loader.
Reads urban POIs (High-density Condos, Shopping Malls, Office Centers) from data/raw/notable_pois_raw.csv.
"""

from pathlib import Path
import pandas as pd
from src.config import RAW_DATA_DIR


def load_notable_pois(file_path: Path | None = None) -> pd.DataFrame:
    """Loads and validates the POIs dataset."""
    if file_path is None:
        file_path = RAW_DATA_DIR / "notable_pois_raw.csv"

    if not file_path.exists():
        raise FileNotFoundError(f"POIs raw file not found at: {file_path}")

    df = pd.read_csv(file_path, encoding="utf-8")
    required_cols = ["name", "type", "lat", "lon", "segment_id"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column in POIs: {col}")

    return df
