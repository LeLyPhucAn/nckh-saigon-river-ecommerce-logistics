"""
Configuration and spatial parameters for the Saigon River E-commerce Logistics research.
Focus Corridor: Hiep Binh Chanh (Thu Duc City) -> Central Ho Chi Minh City (District 1 - District 4).
"""

from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUTS_DIR = BASE_DIR / "outputs"
TABLES_DIR = OUTPUTS_DIR / "tables"
CHARTS_DIR = OUTPUTS_DIR / "charts"
MAPS_DIR = OUTPUTS_DIR / "maps"
SPSS_DIR = BASE_DIR / "spss_models"

# Spatial Reference Systems
# WGS84 Geographic Coordinate System
CRS_WGS84 = "EPSG:4326"
# UTM Zone 48N - Projected Coordinate System for southern Vietnam (meters)
CRS_UTM48N = "EPSG:32648"

# Buffer radii in meters
BUFFER_MICRO_HUB_M = 500       # 500m pedestrian / micro-logistics walk zone
BUFFER_LAST_MILE_M = 1500      # 1500m e-bike / last-mile catchment zone

# Definition of the 8 candidate Micro-Hub locations along Saigon River
CANDIDATE_HUBS = [
    {
        "hub_id": "HUB01",
        "hub_name": "Ben Hiep Binh Chanh",
        "segment_id": "SEG1",
        "district": "Thu Duc City",
        "lat": 10.8285,
        "lon": 106.7212,
        "nearest_bridge": "Cau Binh Loi / Binh Trieu",
        "bridge_clearance_m": 7.0,
        "river_depth_m": 8.5,
        "dist_to_cbd_km": 8.2,
        "est_land_rent_vnd_m2": 180000,
        "ris_readiness_score": 4.5,
    },
    {
        "hub_id": "HUB02",
        "hub_name": "Ben Binh Loi",
        "segment_id": "SEG1",
        "district": "Binh Thanh",
        "lat": 10.8231,
        "lon": 106.7085,
        "nearest_bridge": "Cau Binh Loi",
        "bridge_clearance_m": 7.0,
        "river_depth_m": 8.0,
        "dist_to_cbd_km": 7.1,
        "est_land_rent_vnd_m2": 220000,
        "ris_readiness_score": 4.0,
    },
    {
        "hub_id": "HUB03",
        "hub_name": "Ben Thanh Da",
        "segment_id": "SEG1",
        "district": "Binh Thanh",
        "lat": 10.8038,
        "lon": 106.7241,
        "nearest_bridge": "Cau Kinh Thanh Da",
        "bridge_clearance_m": 6.5,
        "river_depth_m": 7.5,
        "dist_to_cbd_km": 6.4,
        "est_land_rent_vnd_m2": 190000,
        "ris_readiness_score": 4.0,
    },
    {
        "hub_id": "HUB04",
        "hub_name": "Ben Thao Dien",
        "segment_id": "SEG2",
        "district": "Thu Duc City",
        "lat": 10.8052,
        "lon": 106.7335,
        "nearest_bridge": "Cau Sai Gon",
        "bridge_clearance_m": 10.0,
        "river_depth_m": 9.0,
        "dist_to_cbd_km": 5.2,
        "est_land_rent_vnd_m2": 350000,
        "ris_readiness_score": 4.5,
    },
    {
        "hub_id": "HUB05",
        "hub_name": "Ben Binh An",
        "segment_id": "SEG2",
        "district": "Thu Duc City",
        "lat": 10.7924,
        "lon": 106.7268,
        "nearest_bridge": "Cau Sai Gon / Thu Thiem",
        "bridge_clearance_m": 10.0,
        "river_depth_m": 9.5,
        "dist_to_cbd_km": 3.8,
        "est_land_rent_vnd_m2": 320000,
        "ris_readiness_score": 4.8,
    },
    {
        "hub_id": "HUB06",
        "hub_name": "Ben Tan Cang",
        "segment_id": "SEG2",
        "district": "Binh Thanh",
        "lat": 10.7937,
        "lon": 106.7203,
        "nearest_bridge": "Cau Sai Gon",
        "bridge_clearance_m": 10.0,
        "river_depth_m": 10.0,
        "dist_to_cbd_km": 3.5,
        "est_land_rent_vnd_m2": 380000,
        "ris_readiness_score": 5.0,
    },
    {
        "hub_id": "HUB07",
        "hub_name": "Ben Ba Son",
        "segment_id": "SEG3",
        "district": "District 1",
        "lat": 10.7816,
        "lon": 106.7088,
        "nearest_bridge": "Cau Ba Son (Thu Thiem 2)",
        "bridge_clearance_m": 10.5,
        "river_depth_m": 11.0,
        "dist_to_cbd_km": 1.5,
        "est_land_rent_vnd_m2": 550000,
        "ris_readiness_score": 5.0,
    },
    {
        "hub_id": "HUB08",
        "hub_name": "Ben Bach Dang - Khanh Hoi",
        "segment_id": "SEG3",
        "district": "District 1 - District 4",
        "lat": 10.7715,
        "lon": 106.7065,
        "nearest_bridge": "Cau Khanh Hoi / Mong",
        "bridge_clearance_m": 10.0,
        "river_depth_m": 11.5,
        "dist_to_cbd_km": 0.8,
        "est_land_rent_vnd_m2": 650000,
        "ris_readiness_score": 5.0,
    },
]

# Definition of the 3 River Corridor Segments
RIVER_SEGMENTS = [
    {
        "segment_id": "SEG1",
        "segment_name": "Doan 1: Cua ngo gom hang Dong Bac (Hiep Binh Chanh - Thanh Da)",
        "start_point": "Cau Binh Loi (Hiep Binh Chanh)",
        "end_point": "Ban dao Thanh Da (Kenh Thanh Da)",
        "length_km": 5.8,
        "avg_depth_m": 8.0,
        "num_bridges": 2,  # Cau Binh Loi, Cau Binh Trieu
        "min_bridge_clearance_m": 7.0,
        "role": "Consolidation & Inbound Gateway from Binh Duong/Thu Duc Warehouses",
    },
    {
        "segment_id": "SEG2",
        "segment_name": "Doan 2: Do thi chuyen tiep mat do cao (Thao Dien - Tan Cang)",
        "start_point": "Ban dao Thanh Da",
        "end_point": "Cau Sai Gon / Tan Cang",
        "length_km": 4.6,
        "avg_depth_m": 9.5,
        "num_bridges": 1,  # Cau Sai Gon
        "min_bridge_clearance_m": 10.0,
        "role": "High-density Residential & Premium Demand Zone (B2C & C2C)",
    },
    {
        "segment_id": "SEG3",
        "segment_name": "Doan 3: Loi trung tam tieu thu (Ba Son - Bach Dang - Khanh Hoi)",
        "start_point": "Tan Cang",
        "end_point": "Ben Bach Dang / Cau Khanh Hoi",
        "length_km": 3.8,
        "avg_depth_m": 11.0,
        "num_bridges": 2,  # Cau Ba Son, Cau Khanh Hoi
        "min_bridge_clearance_m": 10.0,
        "role": "Central Business District & Last-Mile Electric Distribution Core",
    },
]

# Key Urban Commercial POIs and High-Density Condos in Study Area
NOTABLE_POIS = [
    {"name": "Gigamall Pham Van Dong", "type": "mall", "lat": 10.8280, "lon": 106.7235, "segment_id": "SEG1"},
    {"name": "Opal Riverside / Garden Condos", "type": "condo", "lat": 10.8260, "lon": 106.7205, "segment_id": "SEG1"},
    {"name": "Khu Do Thi Thanh Da", "type": "condo", "lat": 10.8060, "lon": 106.7220, "segment_id": "SEG1"},
    {"name": "Masteri Thao Dien Complex", "type": "condo", "lat": 10.8030, "lon": 106.7380, "segment_id": "SEG2"},
    {"name": "Gateway Thao Dien", "type": "condo", "lat": 10.8065, "lon": 106.7360, "segment_id": "SEG2"},
    {"name": "Vincom Mega Mall Thao Dien", "type": "mall", "lat": 10.8025, "lon": 106.7375, "segment_id": "SEG2"},
    {"name": "Vinhomes Central Park & Landmark 81", "type": "condo", "lat": 10.7950, "lon": 106.7220, "segment_id": "SEG2"},
    {"name": "Landmark 81 Commercial Center", "type": "mall", "lat": 10.7948, "lon": 106.7225, "segment_id": "SEG2"},
    {"name": "Saigon Pearl Complex", "type": "condo", "lat": 10.7895, "lon": 106.7180, "segment_id": "SEG2"},
    {"name": "Sunwah Pearl", "type": "condo", "lat": 10.7880, "lon": 106.7160, "segment_id": "SEG2"},
    {"name": "Vinhomes Golden River Ba Son", "type": "condo", "lat": 10.7830, "lon": 106.7095, "segment_id": "SEG3"},
    {"name": "Vincom Center Dong Khoi", "type": "mall", "lat": 10.7780, "lon": 106.7015, "segment_id": "SEG3"},
    {"name": "Takashimaya / Saigon Centre", "type": "mall", "lat": 10.7735, "lon": 106.7010, "segment_id": "SEG3"},
    {"name": "Bitexco Financial Tower", "type": "office_mall", "lat": 10.7716, "lon": 106.7044, "segment_id": "SEG3"},
    {"name": "Icon 56 & The Tresor Condos Q4", "type": "condo", "lat": 10.7680, "lon": 106.7040, "segment_id": "SEG3"},
    {"name": "Grand Riverside Ben Van Don", "type": "condo", "lat": 10.7620, "lon": 106.6980, "segment_id": "SEG3"},
]
