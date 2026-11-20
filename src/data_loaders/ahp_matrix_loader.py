"""
AHP Matrix Data Loader.
Reads and validates pairwise comparison matrices from data/raw/ahp_pairwise_matrices.json.
Validates reciprocity: A[j, i] == 1 / A[i, j].
"""

import json
from pathlib import Path
import numpy as np
from src.config import RAW_DATA_DIR


def load_ahp_matrices(file_path: Path | None = None) -> dict:
    """Loads AHP pairwise comparison matrices from JSON configuration."""
    if file_path is None:
        file_path = RAW_DATA_DIR / "ahp_pairwise_matrices.json"

    if not file_path.exists():
        raise FileNotFoundError(f"AHP matrices file not found at: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Convert lists to numpy arrays
    group_matrix = np.array(data["groups"]["matrix"], dtype=float)
    sub_matrices = {}
    for grp_key, grp_data in data["subcriteria"].items():
        sub_matrices[grp_key] = np.array(grp_data["matrix"], dtype=float)

    # Validation: Reciprocity check
    def validate_reciprocity(mat: np.ndarray, name: str):
        n = mat.shape[0]
        for i in range(n):
            if not np.isclose(mat[i, i], 1.0, atol=1e-3):
                raise ValueError(f"Diagonal element in {name}[{i},{i}] must be 1.0, got {mat[i, i]}")
            for j in range(i + 1, n):
                expected = 1.0 / mat[i, j]
                if not np.isclose(mat[j, i], expected, atol=1e-2):
                    raise ValueError(f"Reciprocity violated in {name}[{j},{i}]: expected {expected:.4f}, got {mat[j, i]}")

    validate_reciprocity(group_matrix, "Group Matrix")
    for g_key, s_mat in sub_matrices.items():
        validate_reciprocity(s_mat, f"Subcriteria Matrix {g_key}")

    return {
        "group_matrix": group_matrix,
        "group_labels": data["groups"]["labels"],
        "sub_matrices": sub_matrices,
        "sub_labels": {k: v["labels"] for k, v in data["subcriteria"].items()},
    }
