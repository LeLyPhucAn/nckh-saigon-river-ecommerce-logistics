"""
Mô đun nạp ma trận so sánh cặp AHP.
Đọc từ JSON và kiểm tra tính tương hỗ: A[j, i] == 1 / A[i, j].
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional
import numpy as np

from src.config import RAW_DATA_DIR


def load_ahp_matrices(file_path: Optional[Path] = None) -> Dict[str, Any]:
    """Nạp và kiểm tra tính hợp lệ của ma trận so sánh cặp AHP."""
    if file_path is None:
        file_path = RAW_DATA_DIR / "ahp_pairwise_matrices.json"

    if not file_path.exists():
        raise FileNotFoundError(f"Không tìm thấy tệp ma trận AHP: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    group_matrix = np.array(data["groups"]["matrix"], dtype=float)
    sub_matrices = {
        k: np.array(v["matrix"], dtype=float)
        for k, v in data["subcriteria"].items()
    }

    # Kiểm tra tính tương hỗ: đường chéo = 1 và A[j, i] = 1 / A[i, j]
    def check_reciprocal(mat: np.ndarray, name: str) -> None:
        n = mat.shape[0]
        for i in range(n):
            if not np.isclose(mat[i, i], 1.0, atol=1e-3):
                raise ValueError(f"Đường chéo {name}[{i},{i}] phải bằng 1.0")
            for j in range(i + 1, n):
                expected = 1.0 / mat[i, j]
                if not np.isclose(mat[j, i], expected, atol=1e-2):
                    raise ValueError(
                        f"Vi phạm tính tương hỗ {name}[{j},{i}]: "
                        f"kỳ vọng {expected:.3f}, nhận được {mat[j, i]:.3f}"
                    )

    check_reciprocal(group_matrix, "Ma trận nhóm")
    for g_key, s_mat in sub_matrices.items():
        check_reciprocal(s_mat, f"Ma trận tiêu chí con {g_key}")

    return {
        "group_matrix": group_matrix,
        "group_labels": data["groups"]["labels"],
        "sub_matrices": sub_matrices,
        "sub_labels": {k: v["labels"] for k, v in data["subcriteria"].items()},
    }
