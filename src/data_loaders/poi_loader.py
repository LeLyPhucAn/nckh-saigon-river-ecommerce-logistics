"""
Mô đun nạp dữ liệu POI đô thị.
Đọc danh mục chung cư cao tầng, TTTM, văn phòng từ CSV.
"""

from pathlib import Path
from typing import Optional
import pandas as pd

from src.config import RAW_DATA_DIR


def load_notable_pois(file_path: Optional[Path] = None) -> pd.DataFrame:
    """Nạp và xác thực danh mục các điểm POI đô thị phụ tải."""
    if file_path is None:
        file_path = RAW_DATA_DIR / "notable_pois_raw.csv"

    if not file_path.exists():
        raise FileNotFoundError(f"Không tìm thấy tệp POI: {file_path}")

    df = pd.read_csv(file_path, encoding="utf-8")
    required_cols = ["name", "type", "lat", "lon", "segment_id"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Thiếu cột bắt buộc trong tệp POI: {col}")

    return df
