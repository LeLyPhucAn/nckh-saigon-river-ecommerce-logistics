"""
Mô hình mô phỏng luồng vận hành RIS (Giai đoạn 4).
Mô phỏng 3.000 bưu kiện (3.0 tấn) trên trục Hiệp Bình Chánh – Trung tâm.
So sánh trực tiếp xe tải đường bộ qua QL13 với tàu điện thủy tích hợp RIS.
"""

from dataclasses import dataclass
from typing import Dict, List
import pandas as pd


@dataclass
class SimulationResult:
    """Đóng gói kết quả so sánh kịch bản mô phỏng vận hành."""
    comparison_df: pd.DataFrame
    metrics_raw: Dict[str, float]


class RISSimulationModel:
    """Mô hình mô phỏng logistics đa phương thức đường thủy đô thị."""

    def __init__(
        self, total_parcels: int = 3000, cargo_ton: float = 3.0
    ) -> None:
        self.total_parcels = total_parcels
        self.cargo_ton = cargo_ton

    def simulate(self) -> SimulationResult:
        """Chạy mô phỏng đối chứng và tính toán các chỉ số kinh tế - môi trường."""
        # 1. Kịch bản đường bộ: 2 xe tải nhẹ diesel chạy qua QL13 - XVNT
        road_distance_km = 11.5
        road_speed_kmh = 13.5
        # thời gian chạy + trễ đèn giao thông/kẹt xe + bốc dỡ
        road_time_min = (
            (road_distance_km / road_speed_kmh) * 60 + 15 + 25
        )

        diesel_liters = (road_distance_km * 2) * 0.14  # định mức 14L/100km
        road_total_cost = (
            (diesel_liters * 21500)
            + (350000 * 2)
            + (self.total_parcels * 1800)
        )
        road_cost_parcel = road_total_cost / self.total_parcels
        road_co2_kg = diesel_liters * 2.68  # hệ số phát thải diesel IPCC

        # 2. Kịch bản đường thủy: Tàu điện giám sát RIS + giao chặng cuối xe máy điện
        water_distance_km = 8.2
        water_speed_kmh = 18.0
        # thời gian chạy luồng + cập bến bốc dỡ roll-on + giao chặng cuối
        water_time_min = (
            ((water_distance_km / water_speed_kmh) * 60) + 18 + 15
        )

        elec_kwh = 18.5
        water_total_cost = (
            (elec_kwh * 3200)
            + 420000
            + (self.total_parcels * 1200)
        )
        water_cost_parcel = water_total_cost / self.total_parcels
        water_co2_kg = elec_kwh * 0.7221  # hệ số phát thải lưới điện Việt Nam

        records: List[Dict[str, str]] = [
            {
                "Chỉ số so sánh": "Tổng khối lượng bưu kiện",
                "Đơn vị": "kiện / tấn",
                "Đường bộ truyền thống (Xe tải nhẹ)": f"{self.total_parcels:,} kiện (3.0 tấn)",
                "Đường thủy tích hợp RIS (Tàu điện)": f"{self.total_parcels:,} kiện (3.0 tấn)",
                "Hiệu quả chênh lệch": "Tương đương",
            },
            {
                "Chỉ số so sánh": "Khoảng cách hành trình",
                "Đơn vị": "km",
                "Đường bộ truyền thống (Xe tải nhẹ)": f"{road_distance_km:.1f} km",
                "Đường thủy tích hợp RIS (Tàu điện)": f"{water_distance_km:.1f} km",
                "Hiệu quả chênh lệch": f"-{road_distance_km - water_distance_km:.1f} km (-28.7%)",
            },
            {
                "Chỉ số so sánh": "Thời gian giao hàng giờ cao điểm",
                "Đơn vị": "phút",
                "Đường bộ truyền thống (Xe tải nhẹ)": f"{road_time_min:.1f} phút",
                "Đường thủy tích hợp RIS (Tàu điện)": f"{water_time_min:.1f} phút",
                "Hiệu quả chênh lệch": f"-{road_time_min - water_time_min:.1f} phút (-{((road_time_min - water_time_min)/road_time_min)*100:.1f}%)",
            },
            {
                "Chỉ số so sánh": "Tổng chi phí vận hành (OPEX)",
                "Đơn vị": "VNĐ",
                "Đường bộ truyền thống (Xe tải nhẹ)": f"{int(road_total_cost):,} VNĐ",
                "Đường thủy tích hợp RIS (Tàu điện)": f"{int(water_total_cost):,} VNĐ",
                "Hiệu quả chênh lệch": f"-{int(road_total_cost - water_total_cost):,} VNĐ (-{((road_total_cost - water_total_cost)/road_total_cost)*100:.1f}%)",
            },
            {
                "Chỉ số so sánh": "Chi phí trên mỗi bưu kiện",
                "Đơn vị": "VNĐ/kiện",
                "Đường bộ truyền thống (Xe tải nhẹ)": f"{int(road_cost_parcel):,} VNĐ",
                "Đường thủy tích hợp RIS (Tàu điện)": f"{int(water_cost_parcel):,} VNĐ",
                "Hiệu quả chênh lệch": f"-{int(road_cost_parcel - water_cost_parcel):,} VNĐ/kiện (-{((road_cost_parcel - water_cost_parcel)/road_cost_parcel)*100:.1f}%)",
            },
            {
                "Chỉ số so sánh": "Phát thải khí nhà kính (CO2)",
                "Đơn vị": "kg CO2",
                "Đường bộ truyền thống (Xe tải nhẹ)": f"{road_co2_kg:.2f} kg",
                "Đường thủy tích hợp RIS (Tàu điện)": f"{water_co2_kg:.2f} kg",
                "Hiệu quả chênh lệch": f"-{road_co2_kg - water_co2_kg:.2f} kg CO2 (-{((road_co2_kg - water_co2_kg)/road_co2_kg)*100:.1f}%)",
            },
        ]

        metrics = {
            "road_time_min": road_time_min,
            "water_time_min": water_time_min,
            "road_cost_parcel": road_cost_parcel,
            "water_cost_parcel": water_cost_parcel,
            "road_co2": road_co2_kg,
            "water_co2": water_co2_kg,
        }

        return SimulationResult(
            comparison_df=pd.DataFrame(records),
            metrics_raw=metrics,
        )
