"""
Cấu hình dự án và các tham số không gian toàn cục.
Tuân thủ chuẩn PEP 8 và nguyên tắc Clean Code.
"""

from pathlib import Path

# Đường dẫn thư mục dữ liệu
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SPSS_DIR = BASE_DIR / "spss_models"

# Đường dẫn thư mục kết quả đầu ra
OUTPUTS_DIR = BASE_DIR / "outputs"
TABLES_DIR = OUTPUTS_DIR / "tables"
CHARTS_DIR = OUTPUTS_DIR / "charts"
MAPS_DIR = OUTPUTS_DIR / "maps"

# Hệ tọa độ không gian (CRS)
CRS_WGS84 = "EPSG:4326"    # Tọa độ GPS quốc tế (Kinh độ/Vĩ độ)
CRS_UTM48N = "EPSG:32648"  # Tọa độ phẳng mét chuẩn miền Nam Việt Nam

# Bán kính vùng đệm logistics (mét)
BUFFER_MICRO_HUB_M = 500   # Vùng tiếp cận vi mô (đi bộ / xe kéo tay)
BUFFER_LAST_MILE_M = 1500  # Vùng giao nhận chặng cuối (xe máy điện 5-10 phút)
