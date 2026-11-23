"""
Mô hình mô phỏng luồng vận hành RIS (Giai đoạn 4).
Mô phỏng đa kịch bản phụ tải bưu kiện (1.000 - 5.000 bưu kiện) trên trục kết nối
từ Bến Hiệp Bình Chánh (HUB01) về bến tối ưu từ TOPSIS (Bến Tân Cảng - HUB06).
So sánh chi tiết chi phí, thời gian và phát thải CO2 theo tiêu chuẩn IPCC và EVN.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import pandas as pd


@dataclass
class SimulationResult:
    """Đóng gói kết quả so sánh kịch bản mô phỏng vận hành."""
    comparison_df: pd.DataFrame
    metrics_raw: Dict[str, float]
    multi_scenario_df: pd.DataFrame


class RISSimulationModel:
    """Mô hình mô phỏng logistics đa phương thức đường thủy đô thị."""

    def __init__(
        self,
        total_parcels: int = 3000,
        cargo_ton: float = 3.0,
        destination_hub_name: str = "Bến Tân Cảng (HUB06)",
        water_distance_km: float = 8.2,
        road_distance_km: float = 11.5,
    ) -> None:
        self.total_parcels = total_parcels
        self.cargo_ton = cargo_ton
        self.destination_hub_name = destination_hub_name
        self.water_distance_km = water_distance_km
        self.road_distance_km = road_distance_km

    def calculate_single_scenario(
        self, parcels: int, tons: float
    ) -> Dict[str, float]:
        """Tính toán các chỉ số cho một kịch bản tải trọng cụ thể."""
        # 1. Đường bộ: Xe tải nhẹ diesel (1.5 - 2.5T)
        num_trucks = max(1, int(np.ceil(tons / 1.5))) if "np" in globals() else max(1, (parcels + 1499) // 1500)
        num_trucks = max(2, num_trucks) # Giờ cao điểm tối thiểu 2 xe gom
        road_speed_kmh = 13.5
        road_time_min = (self.road_distance_km / road_speed_kmh) * 60 + 15 + (12 * num_trucks)

        # Định mức 14L/100km cho xe tải nhẹ nội đô
        diesel_liters = (self.road_distance_km * num_trucks) * 0.14
        road_fuel_cost = diesel_liters * 21500
        road_labor_cost = 350000 * num_trucks
        road_handling_cost = parcels * 1800 # Bốc xếp kho lẻ
        road_total_cost = road_fuel_cost + road_labor_cost + road_handling_cost
        road_cost_parcel = road_total_cost / parcels
        road_co2_kg = diesel_liters * 2.68 # IPCC 2.68 kg CO2/L

        # 2. Đường thủy: Tàu điện giám sát RIS + Xe máy điện chặng cuối
        water_speed_kmh = 18.0
        water_time_min = (self.water_distance_km / water_speed_kmh) * 60 + 18 + 15

        # Suất tiêu thụ điện sà lan điện: 6.16 kWh/tấn.hành trình
        elec_kwh = max(10.0, tons * 6.16)
        water_energy_cost = elec_kwh * 3200
        water_crew_cost = 420000 # Lương kíp thuyền viên
        water_handling_cost = parcels * (800 + 400) # 800đ roll-on bến + 400đ xe điện
        water_total_cost = water_energy_cost + water_crew_cost + water_handling_cost
        water_cost_parcel = water_total_cost / parcels
        water_co2_kg = elec_kwh * 0.7221 # Hệ số phát thải lưới điện VN

        return {
            "parcels": parcels,
            "tons": tons,
            "road_time_min": road_time_min,
            "water_time_min": water_time_min,
            "time_saving_pct": ((road_time_min - water_time_min) / road_time_min) * 100,
            "road_cost_total": road_total_cost,
            "water_cost_total": water_total_cost,
            "road_cost_parcel": road_cost_parcel,
            "water_cost_parcel": water_cost_parcel,
            "cost_saving_pct": ((road_cost_parcel - water_cost_parcel) / road_cost_parcel) * 100,
            "road_co2": road_co2_kg,
            "water_co2": water_co2_kg,
            "co2_saving_pct": ((road_co2_kg - water_co2_kg) / road_co2_kg) * 100,
        }

    def simulate(self) -> SimulationResult:
        """Chạy mô phỏng đối chứng và tính toán các chỉ số kinh tế - môi trường."""
        # 1. Kịch bản cơ sở (3.000 bưu kiện)
        base_res = self.calculate_single_scenario(self.total_parcels, self.cargo_ton)

        records: List[Dict[str, str]] = [
            {
                "Chỉ số so sánh": "Tuyến kết nối mô phỏng",
                "Đơn vị": "Hành lang",
                "Đường bộ truyền thống (Xe tải nhẹ)": "Kho Hiệp Bình Chánh -> QL13 -> Tân Cảng",
                "Đường thủy tích hợp RIS (Tàu điện)": f"Bến Hiệp Bình Chánh -> {self.destination_hub_name}",
                "Hiệu quả chênh lệch": "Đúng tuyến tối ưu TOPSIS",
            },
            {
                "Chỉ số so sánh": "Tổng khối lượng bưu kiện",
                "Đơn vị": "kiện / tấn",
                "Đường bộ truyền thống (Xe tải nhẹ)": f"{self.total_parcels:,} kiện ({self.cargo_ton:.1f} tấn)",
                "Đường thủy tích hợp RIS (Tàu điện)": f"{self.total_parcels:,} kiện ({self.cargo_ton:.1f} tấn)",
                "Hiệu quả chênh lệch": "Tương đương quy mô",
            },
            {
                "Chỉ số so sánh": "Khoảng cách hành trình",
                "Đơn vị": "km",
                "Đường bộ truyền thống (Xe tải nhẹ)": f"{self.road_distance_km:.1f} km",
                "Đường thủy tích hợp RIS (Tàu điện)": f"{self.water_distance_km:.1f} km",
                "Hiệu quả chênh lệch": f"-{self.road_distance_km - self.water_distance_km:.1f} km (-{((self.road_distance_km - self.water_distance_km)/self.road_distance_km)*100:.1f}%)",
            },
            {
                "Chỉ số so sánh": "Thời gian giao hàng giờ cao điểm",
                "Đơn vị": "phút",
                "Đường bộ truyền thống (Xe tải nhẹ)": f"{base_res['road_time_min']:.1f} phút",
                "Đường thủy tích hợp RIS (Tàu điện)": f"{base_res['water_time_min']:.1f} phút",
                "Hiệu quả chênh lệch": f"-{base_res['road_time_min'] - base_res['water_time_min']:.1f} phút (-{base_res['time_saving_pct']:.1f}%)",
            },
            {
                "Chỉ số so sánh": "Tổng chi phí vận hành (OPEX)",
                "Đơn vị": "VNĐ",
                "Đường bộ truyền thống (Xe tải nhẹ)": f"{int(base_res['road_cost_total']):,} VNĐ",
                "Đường thủy tích hợp RIS (Tàu điện)": f"{int(base_res['water_cost_total']):,} VNĐ",
                "Hiệu quả chênh lệch": f"-{int(base_res['road_cost_total'] - base_res['water_cost_total']):,} VNĐ (-{base_res['cost_saving_pct']:.1f}%)",
            },
            {
                "Chỉ số so sánh": "Chi phí trên mỗi bưu kiện",
                "Đơn vị": "VNĐ/kiện",
                "Đường bộ truyền thống (Xe tải nhẹ)": f"{int(base_res['road_cost_parcel']):,} VNĐ",
                "Đường thủy tích hợp RIS (Tàu điện)": f"{int(base_res['water_cost_parcel']):,} VNĐ",
                "Hiệu quả chênh lệch": f"-{int(base_res['road_cost_parcel'] - base_res['water_cost_parcel']):,} VNĐ/kiện (-{base_res['cost_saving_pct']:.1f}%)",
            },
            {
                "Chỉ số so sánh": "Phát thải khí nhà kính (CO2)",
                "Đơn vị": "kg CO2",
                "Đường bộ truyền thống (Xe tải nhẹ)": f"{base_res['road_co2']:.2f} kg",
                "Đường thủy tích hợp RIS (Tàu điện)": f"{base_res['water_co2']:.2f} kg",
                "Hiệu quả chênh lệch": f"-{base_res['road_co2'] - base_res['water_co2']:.2f} kg CO2 (-{base_res['co2_saving_pct']:.1f}%)",
            },
        ]

        metrics = {
            "road_time_min": base_res["road_time_min"],
            "water_time_min": base_res["water_time_min"],
            "road_cost_parcel": base_res["road_cost_parcel"],
            "water_cost_parcel": base_res["water_cost_parcel"],
            "road_co2": base_res["road_co2"],
            "water_co2": base_res["water_co2"],
        }

        # 2. Đa kịch bản phụ tải (1.000, 2.000, 3.000, 5.000 bưu kiện)
        volume_scenarios = [
            (1000, 1.0, "Kịch bản 1: Thử nghiệm / Ngoài giờ cao điểm"),
            (2000, 2.0, "Kịch bản 2: Vận hành tiêu chuẩn thường nhật"),
            (3000, 3.0, "Kịch bản 3: Giờ cao điểm / Chiến dịch khuyến mãi"),
            (5000, 5.0, "Kịch bản 4: Mở rộng toàn diện (Mega Campaign)"),
        ]

        multi_records = []
        for p_count, t_count, sc_name in volume_scenarios:
            s_res = self.calculate_single_scenario(p_count, t_count)
            multi_records.append({
                "scenario_name": sc_name,
                "parcels": p_count,
                "cargo_tons": t_count,
                "road_time_min": round(s_res["road_time_min"], 1),
                "water_time_min": round(s_res["water_time_min"], 1),
                "time_saving_pct": round(s_res["time_saving_pct"], 1),
                "road_cost_parcel_vnd": int(s_res["road_cost_parcel"]),
                "water_cost_parcel_vnd": int(s_res["water_cost_parcel"]),
                "cost_saving_pct": round(s_res["cost_saving_pct"], 1),
                "road_co2_kg": round(s_res["road_co2"], 2),
                "water_co2_kg": round(s_res["water_co2"], 2),
                "co2_saving_pct": round(s_res["co2_saving_pct"], 1),
            })

        return SimulationResult(
            comparison_df=pd.DataFrame(records),
            metrics_raw=metrics,
            multi_scenario_df=pd.DataFrame(multi_records),
        )
