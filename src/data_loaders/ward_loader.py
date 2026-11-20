"""
Mô đun nạp dữ liệu kinh tế - xã hội cấp phường.
Đọc và xác thực dữ liệu 28 phường ven sông từ CSV.
"""

from pathlib import Path
from typing import Optional
import pandas as pd

from src.config import RAW_DATA_DIR


def load_ward_socioeconomic_data(
    file_path: Optional[Path] = None
) -> pd.DataFrame:
    """Nạp và xác thực tập dữ liệu 28 phường ven sông Sài Gòn."""
    if file_path is None:
        file_path = RAW_DATA_DIR / "ward_socioeconomic_raw.csv"

    if not file_path.exists():
        raise FileNotFoundError(f"Không tìm thấy tệp dữ liệu phường: {file_path}")

    df = pd.read_csv(file_path, encoding="utf-8")
    required_cols = [
        "ward_name", "district", "pop_density_k_per_km2",
        "dist_to_hub_km", "land_rent_mil_vnd_m2",
        "road_ris_score", "est_saving_pct"
    ]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Thiếu cột bắt buộc trong dữ liệu phường: {col}")

    if len(df) < 25:
        raise ValueError(f"Số lượng phường quá ít ({len(df)}), yêu cầu tối thiểu 25")

    return df
