# Đưa Dòng Sông Vào Chuỗi Cung Ứng Thương Mại Điện Tử
## Tiềm Năng Vận Tải Thủy Tại Hành Lang Hiệp Bình Chánh – Trung Tâm TP.HCM

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GIS-MCDM](https://img.shields.io/badge/GIS--MCDM-Fuzzy--AHP%20%7C%20TOPSIS-green.svg)]()

Dự án nghiên cứu khoa học đánh giá tiềm năng khai thác tuyến sông Sài Gòn (đoạn từ cầu Bình Lợi / Hiệp Bình Chánh về bến Bạch Đằng / Khánh Hội) cho logistics thương mại điện tử (TMĐT) đô thị, kết hợp Hệ thống thông tin đường thủy (RIS) và phương tiện xanh chặng cuối.

---

## 1. Cơ Sở Lý Thuyết & Kế Thừa Từ 3 Bài Báo Khoa Học Quốc Tế

Mô hình nghiên cứu được xây dựng trên sự kế thừa và giao thoa phương pháp luận từ 3 công trình khoa học quốc tế uy tín trong thư mục `data_bai_bao`:

| STT | Bài báo khoa học gốc | Đóng góp lý thuyết & Thuật toán | Ứng dụng cụ thể vào Đề tài TP.HCM |
| :---: | :--- | :--- | :--- |
| **1** | **Peña et al. (2019)**<br>*Hydrological Sciences Journal*<br>`Peña, Zapata & Barrios` | • Khung đánh giá đa tiêu chí (AHP) cho vị trí trên sông với 17 chỉ số vật lý/thủy văn.<br>• Phân tích độ bất định đánh giá chuyên gia bằng mô phỏng **Monte Carlo (Beta-PERT)**. | • Kế thừa các chỉ số kỹ thuật luồng lạch: Độ sâu thông thuyền ($X_9$), đoạn sông thẳng ($X_1$), an toàn bến bãi ($X_{16}$), hạ tầng viễn thông/RIS ($X_8$).<br>• Dùng phân phối Beta-PERT để kiểm chứng độ ổn định của ma trận trọng số AHP. |
| **2** | **Hagos et al. (2022)**<br>*Applied Water Science*<br>`Hagos, Andualem et al.` | • Tích hợp GIS và AHP với kỹ thuật phân lớp chuẩn hóa (Reclassification 1–5).<br>• Tổng hợp dữ liệu không gian theo các đơn vị hành chính cấp cơ sở (Woreda/Kebele). | • Phân cấp các chỉ số không gian thành 5 mức độ phụ tải TMĐT.<br>• Chuyển đổi mô hình hồi quy sang **dữ liệu kinh tế - không gian cấp Phường ($25 - 30$ phường ven sông)** phục vụ hồi quy SPSS không cần khảo sát tâm lý. |
| **3** | **Mazarakis et al. (2025)**<br>*Land (MDPI)*<br>`Mazarakis, Tsanakas et al.` | • Thiết lập hệ thống vùng đệm đa tầng (**Multi-ring Buffer Zones**) dọc hành lang sông.<br>• Quy trình kiểm định độ nhạy (**Sensitivity Analysis**) chuẩn mực với kịch bản biến động trọng số. | • Thiết lập vùng đệm $500\text{ m}$ (tiếp cận vi mô đi bộ/xe đẩy) và $1{,}5\text{ km}$ (chặng cuối xe máy điện $5 - 10\text{ phút}$).<br>• Chạy kịch bản phân tích độ nhạy $\pm 10\%, \pm 20\%$ cho nhóm tiêu chí Chi phí mặt bằng ven sông (`FIN1`) và OPEX (`FIN2`). |

---

## 2. Kiến Trúc Dự Án (Clean Modular Python Architecture)

Dự án được tổ chức theo kiến trúc chuẩn khoa học dữ liệu và phân tích không gian:

```text
saigon-river-ecommerce-logistics/
│
├── .gitignore                          # Cấu hình loại trừ file rác, dữ liệu tài liệu, PDF
├── requirements.txt                    # Danh mục thư viện Python phụ thuộc
├── README.md                           # Tài liệu tổng quan (file này)
├── run_day1.py                         # Script thực thi Ngày 1 (GIS & Spatial Extraction)
│
├── data/
│   ├── raw/                            # Dữ liệu gốc thu thập (toạ độ, niên giám, định mức)
│   └── processed/                      # Dữ liệu sạch đã qua xử lý Ngày 1
│       ├── gis_candidate_hubs.csv      # Bảng 8 bến ứng viên (phụ tải chung cư, TTTM, đường nhánh)
│       └── gis_corridor_segments.csv   # Bảng 3 tiểu đoạn sông (độ sâu, tĩnh không cầu, phụ tải)
│
├── src/                                # Toàn bộ mã nguồn Python mô đun hóa
│   ├── __init__.py
│   ├── config.py                       # Cấu hình tham số, tọa độ bến, hằng số GIS
│   ├── gis/                            # Mô đun xử lý không gian (Ngày 1)
│   │   ├── __init__.py
│   │   ├── network_extractor.py        # Dựng hình học Polyline 3 đoạn sông & buffer 500m/1500m
│   │   └── spatial_features.py         # Trích xuất POIs, mật độ đường, dân số, xuất bản đồ 300 DPI
│   ├── mcdm/                           # Mô đun Fuzzy AHP & TOPSIS (Ngày 2 & 3)
│   ├── econometrics/                   # Mô đun kinh tế lượng dữ liệu cấp Phường (Ngày 3)
│   └── simulation/                     # Mô đun mô phỏng luồng vận hành RIS (Ngày 4)
│
├── spss_models/                        # Dữ liệu cấp phường & Cú pháp SPSS (.sps)
├── outputs/                            # Kết quả xuất tự động
│   ├── tables/                         # Các bảng kết quả (.csv, .xlsx)
│   ├── charts/                         # Biểu đồ radar, độ nhạy, phân bổ trọng số
│   └── maps/                           # Bản đồ không gian GIS chất lượng cao
│       └── saigon_river_corridor_day1.png # Bản đồ phân tích không gian Ngày 1
```

---

## 3. Cài Đặt & Hướng Dẫn Thực Thi

### 3.1. Cài đặt môi trường
Khuyến nghị sử dụng Python 3.10 trở lên. Cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

### 3.2. Chạy Phân tích Không gian Ngày 1
Chạy script tự động hóa Ngày 1 để tạo 2 tệp dữ liệu sạch và xuất bản đồ cartography:

```bash
python run_day1.py
```

Kết quả đầu ra sẽ được tự động lưu vào:
* `data/processed/gis_candidate_hubs.csv`
* `data/processed/gis_corridor_segments.csv`
* `outputs/maps/saigon_river_corridor_day1.png`

---

## 4. Tóm Tắt Kết Quả Ngày 1

### 4.1. Bảng 8 Bến Thủy Ứng Viên (`gis_candidate_hubs.csv`)

| Mã bến | Tên bến ứng viên | Tiểu đoạn | Cự ly tới CBD (km) | Tĩnh không cầu (m) | Chung cư (1.5km) | TTTM (1.5km) | Mật độ đường ($\text{km/km}^2$) | Giá thuê đất ($\text{VNĐ/m}^2/\text{tháng}$) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `HUB01` | Bến Hiệp Bình Chánh | Đoạn 1 | 8.2 | 7.0 | 1 | 1 | 14.2 | 180,000 |
| `HUB02` | Bến Bình Lợi | Đoạn 1 | 7.1 | 7.0 | 1 | 0 | 15.8 | 220,000 |
| `HUB03` | Bến Thanh Đa | Đoạn 1 | 6.4 | 6.5 | 3 | 2 | 13.5 | 190,000 |
| `HUB04` | Bến Thảo Điền | Đoạn 2 | 5.2 | 10.0 | 3 | 1 | 19.4 | 350,000 |
| `HUB05` | Bến Bình An | Đoạn 2 | 3.8 | 10.0 | 3 | 1 | 21.0 | 320,000 |
| `HUB06` | Bến Tân Cảng | Đoạn 2 | 3.5 | 10.0 | 4 | 1 | 24.5 | 380,000 |
| `HUB07` | Bến Ba Son | Đoạn 3 | 1.5 | 10.5 | 3 | 3 | 28.2 | 550,000 |
| `HUB08` | Bến Bạch Đằng - Khánh Hội | Đoạn 3 | 0.8 | 10.0 | 3 | 3 | 30.6 | 650,000 |

### 4.2. Bảng 3 Tiểu Đoạn Hành Lang Sông (`gis_corridor_segments.csv`)

| Tiểu đoạn | Chiều dài (km) | Độ sâu TB (m) | Số cầu vượt | Phụ tải chung cư | Mật độ đường TB | Giá thuê đất TB ($\text{VNĐ/m}^2$) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Đoạn 1 (Cửa ngõ Đông Bắc)** | 5.8 | 8.0 | 2 | 5 | 14.50 | 196,666 |
| **Đoạn 2 (Đô thị chuyển tiếp)** | 4.6 | 9.5 | 1 | 10 | 21.63 | 350,000 |
| **Đoạn 3 (Lõi CBD tiêu thụ)** | 3.8 | 11.0 | 2 | 6 | 29.40 | 600,000 |

---

## 5. Bản Quyền & Trích Dẫn Học Thuật

Nếu sử dụng mã nguồn và dữ liệu từ repository này, vui lòng trích dẫn theo định dạng:
* Peña, L. E., Zapata, M. A., & Barrios, M. (2019). Analytic hierarchy process approach for the selection of stream-gauging sites. *Hydrological Sciences Journal*, 64(14), 1783–1792.
* Hagos, Y. G., Andualem, T. G., Yibeltal, M., & Mengie, M. A. (2022). Flood hazard assessment and mapping using GIS integrated with multi-criteria decision analysis in upper Awash River basin, Ethiopia. *Applied Water Science*, 12(7), 148.
* Mazarakis, V., Tsanakas, K., Greenbaum, N., Batzakis, D. V., Sorrentino, A., Tsodoulos, I., Valkanou, K., & Karymbalis, E. (2025). Flood-Hazard Assessment in the Messapios River Catchment by Integrating GIS-Based Multi-Criteria Decision Analysis and Analytic Hierarchy Process. *Land*, 14(3), 658.
