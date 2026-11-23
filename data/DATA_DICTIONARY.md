# Từ Điển Dữ Liệu & Nguồn Gốc Số Liệu (Data Dictionary & Provenance)
## Dự án: Đưa Dòng Sông Vào Chuỗi Cung Ứng Thương Mại Điện Tử TP.HCM

Tài liệu này đặc tả toàn bộ các biến số, cấu trúc dữ liệu, đơn vị đo lường, nguồn gốc trích xuất và phân loại mức độ tin cậy của dữ liệu nạp vào hệ thống mô hình hóa đa phương thức.

---

## 1. Phân Loại Dữ Liệu Theo Mức Độ Tin Cậy (Data Classification)

Tất cả các biến trong hệ thống được phân loại minh bạch thành 3 nhóm:
* **[Thực địa - Thực tế] (Empirical/Official):** Dữ liệu thu thập từ các văn bản quy hoạch chính thức, số liệu thủy văn trạm quan trắc, thông số kỹ thuật công trình cầu cảng, hoặc tọa độ không gian GIS đo đạc thực tế.
* **[Thứ cấp - Thống kê] (Secondary/Statistical):** Dữ liệu kế thừa từ Niên giám Thống kê TP.HCM, Báo cáo Chỉ số Thương mại điện tử Việt Nam (VECOM), hoặc các báo cáo thị trường bất động sản chính thức (Savills, CBRE).
* **[Mô phỏng - Tham số chuẩn] (Simulated/Calibrated):** Dữ liệu tham số định mức vận tải, hệ số phát thải IPCC/EVN, hoặc ma trận so sánh cặp chuyên gia kế thừa từ các công trình khoa học quốc tế uy tín (Fathoni et al., 2017; Peña et al., 2019; Janjevic & Ndiaye, 2014).

---

## 2. Bảng Đặc Tả Biến Số Cho 8 Bến Thủy Ứng Viên (`candidate_hubs_raw.csv` & `gis_candidate_hubs.csv`)

| Tên biến | Kiểu dữ liệu | Đơn vị | Phân loại | Nguồn trích xuất / Phương pháp đo đạc | Ý nghĩa trong mô hình |
| :--- | :---: | :---: | :---: | :--- | :--- |
| `hub_id` | Chuỗi | Mã ID | **[Thực địa]** | Mã định danh chuẩn hóa: `HUB01` đến `HUB08`. | Khóa chính liên kết các bảng. |
| `hub_name` | Chuỗi | Tên bến | **[Thực địa]** | Quyết định quy hoạch mạng lưới đường thủy nội địa TP.HCM đến năm 2030 (Sở GTVT TP.HCM). | Tên bến thủy hiện hữu / quy hoạch. |
| `segment_id` | Chuỗi | Mã đoạn | **[Thực địa]** | Phân định theo 3 tiểu đoạn hành lang sông Sài Gòn (`SEG1`, `SEG2`, `SEG3`). | Liên kết với mô hình đánh giá đoạn sông. |
| `district` | Chuỗi | Hành chính | **[Thực địa]** | Đơn vị hành chính cấp Quận/TP: TP. Thủ Đức, Bình Thạnh, Quận 1, Quận 4. | Phân nhóm địa lý. |
| `lat`, `lon` | Số thực | Độ (WGS84) | **[Thực địa]** | Tọa độ địa lý WGS84 (EPSG:4326) trích xuất từ OpenStreetMap và định vị vệ tinh GPS. | Điểm đặt trạm Micro-Hub, tạo vùng đệm GIS. |
| `nearest_bridge` | Chuỗi | Tên cầu | **[Thực địa]** | Danh bạ luồng hàng hải & đường thủy nội địa Nam Bộ. | Cầu khống chế tĩnh không gần nhất. |
| `bridge_clearance_m` | Số thực | Mét ($m$) | **[Thực địa]** | Hồ sơ kỹ thuật công trình cầu vượt sông Sài Gòn (Sở GTVT TP.HCM). Cầu Bình Lợi mới ($7.0\text{ m}$), Cầu Sài Gòn ($10.0\text{ m}$), Ba Son ($10.5\text{ m}$). | Tiêu chí kỹ thuật thông thuyền (`NAV1`). Hạn chế chiều cao sà lan/tàu hàng. |
| `river_depth_m` | Số thực | Mét ($m$) | **[Thực địa]** | Thủy đồ điện tử trạm Phú An & Chi cục ĐTNĐ phía Nam (biên độ triều $+1.5\text{ m}$ đến $-2.0\text{ m}$, luồng sâu $8.0 - 11.5\text{ m}$). | Độ sâu mớn nước cho tàu cập bến an toàn (`NAV1`). |
| `dist_to_cbd_km` | Số thực | km | **[Thực địa]** | Đo cự ly theo trục đường thủy về Bến Bạch Đằng / Bến Nhà Rồng (Lõi CBD). | Chi phí cự ly vận chuyển (`ECO2`). |
| `est_land_rent_vnd_m2` | Số nguyên | VNĐ/$m^2$/tháng | **[Thứ cấp]** | Bảng giá đất TP.HCM & Báo cáo thị trường mặt bằng thương mại/kho bãi ven sông (Savills/CBRE 2023-2024). | Chi phí thuê mặt bằng trạm Micro-Hub (`FIN1`). |
| `ris_readiness_score` | Số thực | Thang 1 - 5 | **[Thứ cấp]** | Tiêu chuẩn PIANC (2019) về Hệ thống thông tin đường thủy: Mức độ phủ sóng AIS, radar, camera luồng, trạm thông báo NtS. | Khả năng tự động hóa và an toàn giám sát (`NAV3`). |
| `erosion_safety_score` | Số thực | Thang 1 - 5 | **[Thực tế]** | Báo cáo hiện trạng sạt lở bờ sông kênh rạch TP.HCM (Sở NN&PTNT & Sở GTVT). Thanh Đa ($2.2$ - rủi ro cao), Tân Cảng/Ba Son ($4.8 - 5.0$ - kè bê tông kiên cố). | Mức độ an toàn kết cấu bến bãi (`ENV3`). |
| `condos_500m`, `condos_1500m` | Số nguyên | Điểm POI | **[Thực địa]** | Đếm không gian (Spatial Overlay) trong vùng đệm 500m và 1500m từ tập dữ liệu POI trích xuất từ OpenStreetMap (OSM). | Phụ tải phát sinh đơn hàng TMĐT (`ECO1`). |
| `malls_500m`, `malls_1500m` | Số nguyên | Điểm POI | **[Thực địa]** | Đếm các TTTM, cao ốc văn phòng thương mại trong vùng đệm 500m và 1500m từ OSM. | Mật độ hoạt động kinh tế & khách hàng B2C (`ECO1`). |
| `population_1500m` | Số nguyên | Người | **[Thứ cấp]** | Tổng hợp từ Niên giám Thống kê TP.HCM và lưới dân số WorldPop cắt theo vùng đệm $1.5\text{ km}$. | Quy mô thị trường tiêu thụ bưu kiện chặng cuối. |
| `road_density_1500m_km_per_km2` | Số thực | $\text{km/km}^2$ | **[Thực địa]** | Tính tổng chiều dài mạng lưới đường bộ trong bán kính $1.5\text{ km}$ chia cho diện tích vùng đệm ($7.07\text{ km}^2$). | Khả năng kết nối giao hàng chặng cuối xe điện (`ECO3`). |

---

## 3. Bảng Đặc Tả Biến Số Cho 3 Tiểu Đoạn Hành Lang Sông (`river_corridor_raw.csv`)

| Tên biến | Đơn vị | Phân loại | Nguồn trích xuất | Ý nghĩa |
| :--- | :---: | :---: | :--- | :--- |
| `segment_id` | Mã ID | **[Thực địa]** | `SEG1`, `SEG2`, `SEG3`. | Phân đoạn địa lý nghiên cứu. |
| `segment_name` | Tên | **[Thực địa]** | Tên gọi đặc trưng của tiểu đoạn sông. | Định danh báo cáo. |
| `start_point`, `end_point` | Tên mốc | **[Thực địa]** | Cột mốc địa lý thực tế (Cầu Bình Lợi, Bán đảo Thanh Đa, Cầu Sài Gòn, Bến Bạch Đằng). | Ranh giới phân đoạn. |
| `length_km` | km | **[Thực địa]** | Số hóa trục tim sông trên hệ tọa độ UTM Zone 48N (EPSG:32648). | Chiều dài hành trình vận tải thủy. |
| `avg_depth_m` | Mét ($m$) | **[Thực địa]** | Đo sâu bình quân từ tài liệu thủy văn đoạn luồng. | Khả năng chạy tàu tải trọng lớn. |
| `num_bridges` | Cầu | **[Thực địa]** | Số cầu vượt sông trên đoạn. | Điểm nghẽn tiềm tàng trên luồng. |
| `min_bridge_clearance_m` | Mét ($m$) | **[Thực địa]** | Tĩnh không của cây cầu thấp nhất trên đoạn. | Giới hạn tĩnh không tàu container/bưu kiện. |
| `role` | Chuỗi | **[Thứ cấp]** | Quy hoạch logistics đô thị TP.HCM đến năm 2030. | Vai trò chức năng của phân đoạn. |

---

## 4. Bảng Đặc Tả Biến Số Kinh Tế Lượng 28 Phường Ven Sông (`ward_socioeconomic_raw.csv`)

| Tên biến | Đơn vị | Phân loại | Nguồn trích xuất | Ý nghĩa kinh tế lượng |
| :--- | :---: | :---: | :--- | :--- |
| `ward_name` | Tên | **[Thực tế]** | 28 phường ven sông Sài Gòn (Thủ Đức, Bình Thạnh, Q1, Q4, Q7). | Đơn vị quan sát ($N = 28$). |
| `district` | Tên | **[Thực tế]** | Thuộc 5 quận/thành phố ven hành lang nghiên cứu. | Phân nhóm địa bàn. |
| `pop_density_k_per_km2` | Nghìn người/$\text{km}^2$ | **[Thứ cấp]** | Niên giám Thống kê Cục Thống kê TP.HCM (2022-2023). | Biến độc lập $X_1$: Mật độ tập trung nhu cầu. |
| `dist_to_hub_km` | km | **[Thực địa]** | Khoảng cách đường bộ ngắn nhất từ UBND phường/trung tâm dân cư đến bến thủy gần nhất (tính từ mạng lưới đường OSM). | Biến độc lập $X_2$: Rào cản tiếp cận trạm trung chuyển thủy (kỳ vọng hệ số âm). |
| `land_rent_mil_vnd_m2` | Triệu VNĐ/$m^2$/tháng | **[Thứ cấp]** | Khảo sát đơn giá thuê mặt bằng kho bãi/thương mại bình quân của phường. | Biến độc lập $X_3$: Áp lực chi phí mặt bằng giao hàng đường bộ. |
| `road_ris_score` | Thang 1 - 5 | **[Thực tế]** | Mức độ ùn tắc giao thông giờ cao điểm trên các trục đường hướng tâm của phường (Sở GTVT TP.HCM). | Biến độc lập $X_4$: Động lực chuyển đổi sang đường thủy để né kẹt xe. |
| `est_saving_pct` | Phần trăm ($\%$) | **[Mô phỏng]** | Tỷ lệ tiết kiệm chi phí ước tính khi giao qua Micro-Hub ven sông thay vì kho tổng ngoại thành. | Biến độc lập $X_5$: Lợi ích kinh tế trực tiếp. |
| `ecommerce_demand_index` | Điểm 0 - 100 | **[Thứ cấp/Tổng hợp]** | Chỉ số phụ tải nhu cầu TMĐT tổng hợp từ: Dân số $\times$ Tỷ lệ mua sắm trực tuyến (VECOM EBI) $\times$ Tần suất đơn hàng đô thị, chuẩn hóa về thang điểm 100. | **Biến phụ thuộc $Y$**: Nhu cầu chuyển dịch logistics sang hành lang sông. |

---

## 5. Tham Số Mô Phỏng Vận Hành RIS & Đối Chứng Đường Bộ (`ris_simulation.py`)

| Tham số | Giá trị | Đơn vị | Phân loại | Tài liệu tham chiếu |
| :--- | :---: | :---: | :---: | :--- |
| **Quy mô lô hàng mô phỏng** | 1.000, 2.000, 3.000, 5.000 | bưu kiện/chuyến | **[Mô phỏng]** | Janjevic & Ndiaye (2014) - Mô hình sà lan bưu kiện đô thị Châu Âu (*Mokum Mariteam*). |
| **Khối lượng hàng** | 1.0, 2.0, 3.0, 5.0 | tấn | **[Mô phỏng]** | Định mức bưu kiện TMĐT trung bình $1.0\text{ kg/kiện}$. |
| **Cự ly đường bộ (QL13)** | 11.5 | km | **[Thực địa]** | Trục kho Hiệp Bình Chánh $\rightarrow$ QL13 $\rightarrow$ Cầu Bình Triệu $\rightarrow$ Xô Viết Nghệ Tĩnh $\rightarrow$ Tân Cảng. |
| **Vận tốc xe tải giờ cao điểm** | 13.5 | km/h | **[Thực tế]** | Báo cáo tốc độ lưu thông trung bình giờ cao điểm TP.HCM (Sở GTVT TP.HCM). |
| **Định mức tiêu hao diesel** | 14.0 | Lít / 100 km | **[Thực tế]** | Định mức kỹ thuật xe tải nhẹ $1.5 - 2.5\text{ tấn}$ trong đô thị đông đúc. |
| **Đơn giá dầu diesel** | 21.500 | VNĐ/Lít | **[Thực tế]** | Giá bán lẻ xăng dầu Petrolimex vùng 1 (cập nhật 2024). |
| **Hệ số phát thải Diesel** | 2.68 | $\text{kg CO}_2\text{/Lít}$ | **[Tham số chuẩn]** | Hướng dẫn kiểm kê phát thải khí nhà kính quốc gia IPCC (IPCC Guidelines). |
| **Cự ly đường thủy (Hiệp Bình Chánh - Tân Cảng)** | 8.2 | km | **[Thực địa]** | Đo theo trục luồng sông Sài Gòn trên GIS. |
| **Vận tốc tàu điện thủy** | 18.0 | km/h (~9.7 knots) | **[Thực tế]** | Vận tốc an toàn quy định trên luồng sông Sài Gòn đoạn nội đô. |
| **Suất tiêu thụ điện sà lan** | 6.16 | $\text{kWh/tấn.hành trình}$ | **[Tham số chuẩn]** | Báo cáo kỹ thuật tàu điện đô thị (Janjevic & Ndiaye, 2014; World Bank, 2019). |
| **Đơn giá điện sản xuất/sạc** | 3.200 | VNĐ/kWh | **[Thực tế]** | Biểu giá bán lẻ điện sản xuất giờ bình thường EVN. |
| **Hệ số phát thải lưới điện VN** | 0.7221 | $\text{kg CO}_2\text{/kWh}$ | **[Tham số chuẩn]** | Hệ số phát thải lưới điện Việt Nam (Cục Biến đổi Khí hậu - Bộ TN&MT công bố). |
| **Chi phí bốc dỡ roll-on/roll-off** | 800 | VNĐ/kiện | **[Mô phỏng]** | Định mức bốc xếp bằng khay/pallet cơ giới hóa tại bến Micro-Hub. |
| **Chi phí xe máy điện chặng cuối** | 400 | VNĐ/kiện | **[Mô phỏng]** | Định mức giao hàng chặng cuối bán kính $1.5\text{ km}$ bằng xe máy điện (Selex/DatBike). |

---

Tài liệu này là căn cứ đảm bảo tính minh bạch, kiểm chứng và bảo vệ thành công trước mọi hội đồng phản biện khoa học.
