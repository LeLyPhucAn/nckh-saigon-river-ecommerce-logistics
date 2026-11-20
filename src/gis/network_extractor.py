"""
Network Extractor Module.
Generates geometric GeoDataFrames for the Saigon River corridor, 
candidate Micro-Hubs, and multi-ring buffer zones (500m and 1500m) in UTM 48N.
"""

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, LineString
from src.config import (
    CANDIDATE_HUBS,
    RIVER_SEGMENTS,
    CRS_WGS84,
    CRS_UTM48N,
    BUFFER_MICRO_HUB_M,
    BUFFER_LAST_MILE_M,
)

# Detailed river trajectory waypoints along the Saigon River corridor
# From Hiep Binh Chanh / Binh Loi bridge down to Bach Dang / Khanh Hoi
RIVER_WAYPOINTS = {
    "SEG1": [
        (106.7085, 10.8231), # Near Cau Binh Loi
        (106.7140, 10.8270),
        (106.7212, 10.8285), # Ben Hiep Binh Chanh
        (106.7265, 10.8250),
        (106.7310, 10.8160),
        (106.7241, 10.8038), # Thanh Da peninsula apex
    ],
    "SEG2": [
        (106.7241, 10.8038), # Thanh Da
        (106.7300, 10.8050),
        (106.7335, 10.8052), # Thao Dien
        (106.7360, 10.7990),
        (106.7268, 10.7924), # Binh An
        (106.7203, 10.7937), # Tan Cang / Landmark 81
    ],
    "SEG3": [
        (106.7203, 10.7937), # Tan Cang
        (106.7160, 10.7880), # Saigon Pearl / Sunwah
        (106.7088, 10.7816), # Ba Son
        (106.7065, 10.7715), # Bach Dang
        (106.7045, 10.7670), # Khanh Hoi / Ben Nghe canal confluence
    ],
}


def build_river_geodataframe() -> gpd.GeoDataFrame:
    """Builds a GeoDataFrame representing the 3 river segments."""
    records = []
    for seg in RIVER_SEGMENTS:
        seg_id = seg["segment_id"]
        coords = RIVER_WAYPOINTS[seg_id]
        line = LineString(coords)
        record = {**seg, "geometry": line}
        records.append(record)

    gdf = gpd.GeoDataFrame(records, crs=CRS_WGS84)
    return gdf


def build_hubs_geodataframe() -> gpd.GeoDataFrame:
    """Builds a GeoDataFrame representing the 8 candidate Micro-Hub locations."""
    df = pd.DataFrame(CANDIDATE_HUBS)
    geometry = [Point(xy) for xy in zip(df["lon"], df["lat"])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs=CRS_WGS84)
    return gdf


def create_multiring_buffers(gdf_points: gpd.GeoDataFrame) -> dict[str, gpd.GeoDataFrame]:
    """
    Creates 500m (micro-hub pedestrian catchment) and 1500m (last-mile electric bike catchment)
    buffer zones around candidate hubs using UTM Zone 48N projected coordinate system.
    """
    # Project to metric coordinate system
    gdf_utm = gdf_points.to_crs(CRS_UTM48N)

    # 500m buffer
    gdf_buf_500 = gdf_utm.copy()
    gdf_buf_500["geometry"] = gdf_utm.geometry.buffer(BUFFER_MICRO_HUB_M)
    gdf_buf_500["buffer_radius_m"] = BUFFER_MICRO_HUB_M
    gdf_buf_500 = gdf_buf_500.to_crs(CRS_WGS84)

    # 1500m buffer
    gdf_buf_1500 = gdf_utm.copy()
    gdf_buf_1500["geometry"] = gdf_utm.geometry.buffer(BUFFER_LAST_MILE_M)
    gdf_buf_1500["buffer_radius_m"] = BUFFER_LAST_MILE_M
    gdf_buf_1500 = gdf_buf_1500.to_crs(CRS_WGS84)

    return {
        "buffer_500m": gdf_buf_500,
        "buffer_1500m": gdf_buf_1500,
    }
