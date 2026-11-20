"""
RIS Operational Simulation Model.
Simulates parcel transportation for 3,000 packages (3.0 tons)
comparing Conventional Road Trucks vs Electric Barge + RIS + E-Cargo Bikes.
Calculates transit times, OPEX, cost per parcel, and CO2 emissions.
"""

from dataclasses import dataclass
from typing import Dict
import pandas as pd


@dataclass
class SimulationResult:
    """Encapsulates operational simulation comparison."""
    comparison_df: pd.DataFrame
    metrics_raw: Dict[str, float]


class RISSimulationModel:
    """Simulates multimodal urban waterway e-commerce logistics."""

    def __init__(self, total_parcels: int = 3000, cargo_ton: float = 3.0):
        self.total_parcels = total_parcels
        self.cargo_ton = cargo_ton

    def simulate(self) -> SimulationResult:
        """Runs the simulation and returns comparison data."""
        # 1. Road Scenario (Light Diesel Trucks via QL13 - XVNT)
        road_distance_km = 11.5
        road_speed_kmh = 13.5
        road_time_min = (road_distance_km / road_speed_kmh) * 60 + 15 + 25  # transit + signal delay + unloading

        diesel_liters = (road_distance_km * 2) * 0.14  # 14L/100km for 2 trucks
        road_total_cost = (diesel_liters * 21500) + (350000 * 2) + (self.total_parcels * 1800)
        road_cost_parcel = road_total_cost / self.total_parcels
        road_co2_kg = diesel_liters * 2.68  # IPCC factor

        # 2. Waterway Scenario (Electric Barge + RIS + E-Bike Last-Mile)
        water_distance_km = 8.2
        water_speed_kmh = 18.0
        water_time_min = ((water_distance_km / water_speed_kmh) * 60) + 18 + 15  # transit + berthing/crossdock + e-bike delivery

        elec_kwh = 18.5
        water_total_cost = (elec_kwh * 3200) + 420000 + (self.total_parcels * 1200)
        water_cost_parcel = water_total_cost / self.total_parcels
        water_co2_kg = elec_kwh * 0.7221  # Vietnam national grid factor

        records = [
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
