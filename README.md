# Đưa Dòng Sông Vào Chuỗi Cung Ứng Thương Mại Điện Tử
## Tiềm Năng Vận Tải Thủy Tại Hành Lang Hiệp Bình Chánh – Trung Tâm TP.HCM

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Architecture: Clean Code](https://img.shields.io/badge/architecture-Clean%20Code%20%7C%20Modular-blueviolet.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Pipeline: Complete](https://img.shields.io/badge/Pipeline-Complete%20100%25-brightgreen.svg)]()
[![Econometrics: SPSS](https://img.shields.io/badge/Econometrics-SPSS%20%7C%20OLS%20R2%3D0.884-orange.svg)]()

Dự án nghiên cứu khoa học đánh giá tiềm năng khai thác tuyến sông Sài Gòn (đoạn từ cầu Bình Lợi / Hiệp Bình Chánh về bến Bạch Đằng / Khánh Hội) cho logistics thương mại điện tử (TMĐT) đô thị, kết hợp Hệ thống thông tin đường thủy (RIS) và phương tiện xanh chặng cuối.

Mã nguồn được tái cấu trúc toàn diện theo triết lý **Clean Code**, phân tách mạch lạc giữa tầng dữ liệu đầu vào (**Data Loaders**), tầng mô hình toán học (**Mathematical Models**), tầng trực quan hóa (**Visualizers**) và tầng điều phối (**Pipeline Coordinator**).

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

Mã nguồn được tổ chức theo chuẩn kiến trúc phân lớp (Layered Architecture):

```text
saigon-river-ecommerce-logistics/
│
├── .gitignore                          # Loại trừ file rác, tài liệu PDF, docx, virtualenv
├── requirements.txt                    # Danh mục thư viện Python phụ thuộc
├── README.md                           # Tài liệu tổng quan (file này)
├── run_day1.py                         # Script thực thi Ngày 1 (GIS & Spatial Extraction)
├── run_full_pipeline.py                # Script điều phối chạy toàn bộ mô hình (1 chạm)
├── generate_docx_report.py             # Script xuất Báo cáo Khoa học đặc tả (.docx)
│
├── data/
│   ├── raw/                            # DỮ LIỆU ĐẦU VÀO NẠP VÀO MÔ HÌNH (100% minh bạch)
│   │   ├── candidate_hubs_raw.csv      # Thông số kỹ thuật & giá đất 8 bến ứng viên
│   │   ├── river_corridor_raw.csv      # Thông số 3 tiểu đoạn hành lang sông Sài Gòn
│   │   ├── notable_pois_raw.csv        # Tọa độ các cụm chung cư cao tầng, TTTM, văn phòng
│   │   ├── ward_socioeconomic_raw.csv  # Dữ liệu kinh tế - không gian 28 phường ven sông
│   │   └── ahp_pairwise_matrices.json  # Toàn bộ ma trận so sánh cặp AHP (Group & Sub)
│   └── processed/                      # Dữ liệu sạch xuất từ Ngày 1
│       ├── gis_candidate_hubs.csv      # 8 bến kèm phụ tải không gian tính từ GIS
│       └── gis_corridor_segments.csv   # 3 đoạn kèm phụ tải và mật độ đường
│
├── src/                                # GÓI MÃ NGUỒN CHÍNH (CLEAN CODE)
│   ├── __init__.py
│   ├── config.py                       # Đường dẫn hệ thống, hằng số GIS & CRS
│   │
│   ├── data_loaders/                   # TẦNG NẠP VÀ XÁC THỰC DỮ LIỆU (Data Loaders)
│   │   ├── __init__.py
│   │   ├── hub_loader.py               # Nạp bến ứng viên & đoạn sông
│   │   ├── poi_loader.py               # Nạp các điểm POI đô thị
│   │   ├── ward_loader.py              # Nạp dữ liệu 28 phường
│   │   └── ahp_matrix_loader.py        # Nạp & kiểm tra tính tương hỗ AHP (A[j,i] = 1/A[i,j])
│   │
│   ├── models/                         # TẦNG MÔ HÌNH TOÁN HỌC & KINH TẾ LƯỢNG (Models)
│   │   ├── __init__.py
│   │   ├── fuzzy_ahp.py                # Class FuzzyAHPModel (Saaty Geometric Mean & CR < 0.10)
│   │   ├── segment_evaluator.py        # Class SegmentEvaluator (Min-Max WLC đoạn sông)
│   │   ├── topsis.py                   # Class TOPSISModel (Vector Norm, A+, A-, CC_k)
│   │   ├── sensitivity_engine.py       # Class SensitivityEngine (Phân tích độ nhạy ±20%)
│   │   ├── ward_econometrics.py        # Class WardEconometricModel (OLS Regression, VIF, SPSS)
│   │   └── ris_simulation.py           # Class RISSimulationModel (Mô phỏng 3.000 bưu kiện)
│   │
│   ├── visualization/                  # TẦNG TRỰC QUAN HÓA & CARTOGRAPHY (Visualizers)
│   │   ├── __init__.py
│   │   └── chart_renderer.py           # Xuất 7 biểu đồ 300 DPI (Trọng số, Radar, Độ nhạy, OLS, RIS)
│   │
│   ├── gis/                            # Mô đun không gian Ngày 1 (GIS)
│   │   ├── __init__.py
│   │   ├── network_extractor.py        # Dựng Polyline & buffers 500m/1500m (UTM Zone 48N)
│   │   └── spatial_features.py         # Trích xuất POIs & xuất bản đồ Ngày 1
│   │
│   └── pipeline/                       # TẦNG ĐIỀU PHỐI QUY TRÌNH (Pipeline)
│       ├── __init__.py
│       └── coordinator.py              # Điều phối liên kết toàn bộ Data Loaders -> Models -> Visualizers
│
├── spss_models/                        # Dữ liệu cấp phường & Cú pháp SPSS (.sps)
│   ├── spss_ward_data.csv              # Dữ liệu 28 phường ven sông Sài Gòn
│   └── regression_syntax.sps           # File cú pháp chạy hồi quy trên IBM SPSS Statistics
│
├── outputs/                            # Kết quả xuất tự động
│   ├── tables/                         # 6 bảng số liệu CSV
│   ├── charts/                         # 7 biểu đồ khoa học 300 DPI
│   ├── maps/                           # Bản đồ không gian GIS (saigon_river_corridor_day1.png)
│   └── Bao_Cao_Chi_Tiet_Mo_Hinh_NCKH_Song_Sai_Gon.docx # Báo cáo Word học thuật toàn diện
```

---

## 3. Cài Đặt & Hướng Dẫn Thực Thi

### 3.1. Cài đặt môi trường
Khuyến nghị sử dụng Python 3.10 trở lên. Cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

### 3.2. Thực thi toàn bộ quy trình (One-Click Pipeline)
Để chạy tự động toàn bộ mô hình, xuất ra toàn bộ bảng biểu, biểu đồ 300 DPI và tệp Word báo cáo:

```bash
python run_full_pipeline.py
```

---

## 4. Tóm Tắt Kết Quả Định Lượng Toàn Diện

1. **Trọng số Toàn cục Fuzzy AHP ($W_i$):** $CR = 0.048 < 0.10$. Nhóm Chi phí mặt bằng & OPEX (`FIN`: $31.25\%$) và Nhu cầu TMĐT (`ECO`: $29.49\%$) giữ vai trò chi phối.
2. **Xếp hạng 3 Tiểu đoạn Sông:** Tiểu đoạn 2 (Thảo Điền – Tân Cảng) đạt điểm tiềm năng cao nhất ($0.7842$, Hạng 1), kế tiếp là Tiểu đoạn 1 ($0.6425$, Hạng 2), và Tiểu đoạn 3 ($0.5180$, Hạng 3).
3. **Xếp hạng TOPSIS 8 Micro-Hubs:**
   * 🥇 **Top 1 – `HUB06` Bến Tân Cảng ($CC = 0.7351$):** Trạm trung chuyển chính (Primary Micro-Hub).
   * 🥈 **Top 2 – `HUB05` Bến Bình An ($CC = 0.6978$):** Trạm hỗ trợ bán đảo Thủ Thiêm (Secondary Hub).
   * 🥉 **Top 3 – `HUB01` Bến Hiệp Bình Chánh ($CC = 0.6724$):** Trạm gom hàng đầu mối phía Bắc (Inbound Gateway).
4. **Kiểm định Hồi quy Kinh tế lượng 28 Phường:** $R^2 = 0.8840$, $R^2_{\text{adj}} = 0.8576$, $F = 33.56$ ($p < 0.001$), toàn bộ $VIF < 1.62$.
5. **Mô phỏng Kịch bản RIS Demo (3.000 bưu kiện):** Tiết kiệm $32.2\%$ thời gian giao hàng giờ cao điểm, $38.8\%$ chi phí vận hành đơn hàng, và $37.8\%$ phát thải $\text{CO}_2$.
