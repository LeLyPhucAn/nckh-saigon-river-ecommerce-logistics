"""
Data Loaders Package.
Provides clean, validated data ingestion from CSV/JSON sources into typed DataFrames.
"""

from .hub_loader import load_candidate_hubs, load_river_segments
from .poi_loader import load_notable_pois
from .ahp_matrix_loader import load_ahp_matrices
from .ward_loader import load_ward_socioeconomic_data

__all__ = [
    "load_candidate_hubs",
    "load_river_segments",
    "load_notable_pois",
    "load_ahp_matrices",
    "load_ward_socioeconomic_data",
]
