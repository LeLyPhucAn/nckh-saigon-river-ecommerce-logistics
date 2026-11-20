"""
Day 1 Execution Script: GIS Corridor Analysis & Micro-Hub Candidate Extraction.
Run this script to generate Day 1 datasets and publication map:
    python run_day1.py
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.gis.spatial_features import export_day1_datasets, plot_day1_corridor_map
import pandas as pd


def main():
    print("=" * 75)
    print("🚀 RUNNING DAY 1: SAIGON RIVER GIS SPATIAL BUFFER & POI EXTRACTION")
    print("=" * 75)

    print("\n[Step 1/2] Processing GIS spatial geometries & exporting datasets...")
    hubs_path, segments_path = export_day1_datasets()
    print(f"  -> Candidate Hubs dataset saved: {hubs_path}")
    print(f"  -> Corridor Segments dataset saved: {segments_path}")

    print("\n[Step 2/2] Rendering high-resolution Day 1 cartographic map (300 DPI)...")
    map_path = plot_day1_corridor_map()
    print(f"  -> Publication map saved: {map_path}")

    # Display summary tables in terminal
    df_hubs = pd.read_csv(hubs_path)
    df_segments = pd.read_csv(segments_path)

    print("\n" + "=" * 75)
    print("📊 BẢNG 1: THỐNG KÊ 8 BẾN ỨNG VIÊN (CANDIDATE MICRO-HUBS)")
    print("=" * 75)
    display_cols = [
        "hub_id",
        "hub_name",
        "segment_id",
        "dist_to_cbd_km",
        "bridge_clearance_m",
        "condos_1500m",
        "malls_1500m",
        "road_density_1500m_km_per_km2",
        "est_land_rent_vnd_m2",
    ]
    print(df_hubs[display_cols].to_string(index=False))

    print("\n" + "=" * 75)
    print("📊 BẢNG 2: THỐNG KÊ 3 TIỂU ĐOẠN HÀNH LANG SÔNG SÀI GÒN")
    print("=" * 75)
    seg_cols = [
        "segment_id",
        "length_km",
        "avg_depth_m",
        "num_bridges",
        "total_condos_buffer",
        "avg_road_density",
        "avg_land_rent_vnd_m2",
    ]
    print(df_segments[seg_cols].to_string(index=False))
    print("\n✅ HOÀN THÀNH CÔNG VIỆC NGÀY 1!")


if __name__ == "__main__":
    main()
