"""
Tệp thực thi Ngày 1: Phân tích không gian GIS & Trích xuất bến ứng viên.
Chạy tệp này để tạo dữ liệu sạch Ngày 1 và xuất bản đồ:
    python run_day1.py
"""

from pathlib import Path
import sys
import pandas as pd

# Thêm đường dẫn gốc của dự án vào sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.gis.spatial_features import export_day1_datasets, plot_day1_corridor_map


def main() -> None:
    """Thực thi toàn bộ phân tích không gian GIS Ngày 1."""
    print("=" * 75)
    print("🚀 BẮT ĐẦU NGÀY 1: PHÂN TÍCH KHÔNG GIAN GIS & TRÍCH XUẤT PHỤ TẢI SÔNG SÀI GÒN")
    print("=" * 75)

    print("\n[Bước 1/2] Xử lý hình học không gian & xuất 2 tệp dữ liệu sạch...")
    hubs_path, segments_path = export_day1_datasets()
    print(f"  -> Bảng 8 bến ứng viên: {hubs_path}")
    print(f"  -> Bảng 3 tiểu đoạn sông: {segments_path}")

    print("\n[Bước 2/2] Xuất bản đồ cartography GIS chất lượng cao (300 DPI)...")
    map_path = plot_day1_corridor_map()
    print(f"  -> Bản đồ lưu tại: {map_path}")

    # Hiển thị bảng tổng hợp trong terminal
    df_hubs = pd.read_csv(hubs_path)
    df_segments = pd.read_csv(segments_path)

    print("\n" + "=" * 75)
    print("📊 BẢNG 1: THỐNG KÊ 8 BẾN ỨNG VIÊN (CANDIDATE MICRO-HUBS)")
    print("=" * 75)
    display_cols = [
        "hub_id", "hub_name", "segment_id", "dist_to_cbd_km",
        "bridge_clearance_m", "condos_1500m", "malls_1500m",
        "road_density_1500m_km_per_km2", "est_land_rent_vnd_m2"
    ]
    print(df_hubs[display_cols].to_string(index=False))

    print("\n" + "=" * 75)
    print("📊 BẢNG 2: THỐNG KÊ 3 TIỂU ĐOẠN HÀNH LANG SÔNG SÀI GÒN")
    print("=" * 75)
    seg_cols = [
        "segment_id", "length_km", "avg_depth_m", "num_bridges",
        "total_condos_buffer", "avg_road_density", "avg_land_rent_vnd_m2"
    ]
    print(df_segments[seg_cols].to_string(index=False))
    print("\n✅ HOÀN THÀNH CÔNG VIỆC NGÀY 1!")


if __name__ == "__main__":
    main()
