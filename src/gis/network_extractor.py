"""
Network Extractor Module.
Generates geometric GeoDataFrames and multi-ring buffer zones (500m, 1500m).
"""

from typing import Dict, List, Tuple
import geopandas as gpd
from shapely.geometry import LineString, Point

from src.config import (
    BUFFER_LAST_MILE_M,
    BUFFER_MICRO_HUB_M,
    CRS_UTM48N,
    CRS_WGS84,
)
from src.data_loaders.hub_loader import load_candidate_hubs, load_river_segments

# Trajectory waypoints along the Saigon River study corridor (Lon, Lat)
RIVER_WAYPOINTS: Dict[str, List[Tuple[float, float]]] = {
    "SEG1": [
        (106.7085, 10.8231),  # Binh Loi Bridge
        (106.7140, 10.8270),
        (106.7212, 10.8285),  # Hiep Binh Chanh Wharf
        (106.7265, 10.8250),
        (106.7310, 10.8160),
        (106.7241, 10.8038),  # Thanh Da Peninsula
    ],
    "SEG2": [
        (106.7241, 10.8038),  # Thanh Da
        (106.7300, 10.8050),
        (106.7335, 10.8052),  # Thao Dien
        (106.7360, 10.7990),
        (106.7268, 10.7924),  # Binh An
        (106.7203, 10.7937),  # Tan Cang / Landmark 81
    ],
    "SEG3": [
        (106.7203, 10.7937),  # Tan Cang
        (106.7160, 10.7880),  # Saigon Pearl
        (106.7088, 10.7816),  # Ba Son
        (106.7065, 10.7715),  # Bach Dang
        (106.7045, 10.7670),  # Khanh Hoi / Ben Nghe Canal
    ],
}


def build_river_geodataframe() -> gpd.GeoDataFrame:
    """Constructs a GeoDataFrame of the 3 river segments."""
    segments_df = load_river_segments()
    geometries = []

    for _, row in segments_df.iterrows():
        sid = row["segment_id"]
        coords = RIVER_WAYPOINTS.get(sid, [])
        geometries.append(LineString(coords))

    gdf = gpd.GeoDataFrame(segments_df, geometry=geometries, crs=CRS_WGS84)
    return gdf


def build_hubs_geodataframe() -> gpd.GeoDataFrame:
    """Constructs a GeoDataFrame of the 8 candidate Micro-Hubs."""
    hubs_df = load_candidate_hubs()
    geometries = [Point(xy) for xy in zip(hubs_df["lon"], hubs_df["lat"])]
    gdf = gpd.GeoDataFrame(hubs_df, geometry=geometries, crs=CRS_WGS84)
    return gdf


def create_multiring_buffers(
    gdf_points: gpd.GeoDataFrame
) -> Dict[str, gpd.GeoDataFrame]:
    """
    Creates 500m and 1500m buffers around candidate hubs.
    Projects to UTM Zone 48N for precise metric calculations.
    """
    gdf_utm = gdf_points.to_crs(CRS_UTM48N)

    # 500m micro-hub pedestrian catchment
    buf_500 = gdf_utm.copy()
    buf_500["geometry"] = gdf_utm.geometry.buffer(BUFFER_MICRO_HUB_M)
    buf_500["buffer_radius_m"] = BUFFER_MICRO_HUB_M
    buf_500 = buf_500.to_crs(CRS_WGS84)

    # 1500m electric bike delivery catchment
    buf_1500 = gdf_utm.copy()
    buf_1500["geometry"] = gdf_utm.geometry.buffer(BUFFER_LAST_MILE_M)
    buf_1500["buffer_radius_m"] = BUFFER_LAST_MILE_M
    buf_1500 = buf_1500.to_crs(CRS_WGS84)

    return {
        "buffer_500m": buf_500,
        "buffer_1500m": buf_1500,
    }
