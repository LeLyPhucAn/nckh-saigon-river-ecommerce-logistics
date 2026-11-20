# Dự án Nghiên cứu: Đưa Dòng Sông Vào Chuỗi Cung Ứng Thương Mại Điện Tử (Hành lang Hiệp Bình Chánh – Trung tâm TP.HCM)

> **Hướng dẫn dành cho AI Agent:** Tệp `README.md` này là tài liệu đặc tả kiến trúc cốt lõi (System Context & Specification) của dự án. Mọi mã nguồn (Python/R/GIS), công thức toán học, cấu trúc dữ liệu và nội dung phân tích học thuật do bạn tạo ra **bắt buộc phải tuân thủ nghiêm ngặt** khung phương pháp luận, bộ tiêu chí và các ràng buộc được định nghĩa dưới đây.

---

## 1. Tổng quan & Mục tiêu Nghiên cứu

* **Tên đề tài:** Đưa dòng sông vào chuỗi cung ứng thương mại điện tử: Tiềm năng vận tải thủy tại hành lang Hiệp Bình Chánh – Trung tâm TP.HCM.
* **Bối cảnh & Phạm vi không gian:** Tuyến sông Sài Gòn đoạn từ khu vực cầu Bình Lợi / Hiệp Bình Chánh (TP. Thủ Đức) về đến khu vực Bến Bạch Đằng / Khánh Hội (Quận 1 – Quận 4), TP.HCM.
* **Mục tiêu cốt lõi:**
  1. Đánh giá và xếp hạng mức độ tiềm năng phát triển vận tải hàng hóa thương mại điện tử (TMĐT) của các tiểu đoạn sông trên hành lang nghiên cứu.
  2. Tối ưu hóa lựa chọn vị trí đặt các **Trạm trung chuyển vi mô thủy – bộ (Urban Waterway Micro-Hubs)** dọc tuyến sông dựa trên bài toán đa tiêu chí (kỹ thuật, kinh tế, chi phí mặt bằng ven sông, môi trường và hành vi khách hàng).
  3. Kiểm chứng thực nghiệm các nhân tố hành vi, cảm xúc tiêu dùng xanh và chi phí ảnh hưởng đến ý định chấp nhận vận tải thủy TMĐT thông qua mô hình kinh tế lượng (SPSS).
  4. Xây dựng kịch bản mô phỏng (Demo) luồng vận hành vận tải thủy đô thị tích hợp **Hệ thống thông tin đường thủy (River Information Services – RIS)**.

---

## 2. Bước tiến Khoa học so với Nghiên cứu Nền tảng (Fathoni et al., 2017)

Mô hình này kế thừa ý tưởng kết hợp GIS và ra quyết định đa tiêu chí từ nghiên cứu của *Fathoni et al. (2017) - "Analysis to assess potential rivers for cargo transport in Indonesia"* (sông Musi), nhưng **nâng cấp toàn diện** để khắc phục 4 khoảng trống nghiên cứu khi áp dụng vào siêu đô thị TP.HCM:

| Khía cạnh | Mô hình gốc (Fathoni et al., 2017) | Mô hình nâng cấp của Dự án (TP.HCM) |
| :--- | :--- | :--- |
| **Đối tượng hàng hóa** | Hàng rời khối lượng lớn (than, dầu cọ, phân bón) ở vùng nông thôn. | Bưu kiện TMĐT đô thị (B2C/B2B2C), yêu cầu tốc độ nhanh, khung giờ giao hàng chặt chẽ và logistics ngược. |
| **Phạm vi đầu ra** | Chỉ dừng lại ở xếp hạng vĩ mô 3 đoạn sông. | **2 tầng kết quả:** (1) Chấm điểm tiềm năng tiểu đoạn sông; (2) Xếp hạng tọa độ tối ưu đặt **Trạm trung chuyển (Micro-Hubs)**. |
| **Biến số kinh tế** | Bỏ qua giá đất và chi phí vận hành bến bãi. | Tích hợp trực tiếp **giá thuê mặt bằng ven sông (CAPEX)**, **chi phí vận hành tàu điện/hybrid & bốc xếp (OPEX)**. |
| **Công nghệ & Hành vi** | Chỉ đếm báo hiệu vật lý; trọng số dựa hoàn toàn vào cảm tính 50 chuyên gia. | Tích hợp hạ tầng số **RIS**; sử dụng **Fuzzy AHP** giảm tính mờ chủ quan và dùng **Hồi quy SPSS** để kiểm chứng hành vi, cảm xúc khách hàng. |

> **Cảnh báo Ràng buộc cho AI Agent:** Tuyệt đối **KHÔNG** sử dụng các chỉ số đặc thù của nông thôn như "tỷ lệ hộ nghèo" hay "vận chuyển nông sản/khoáng sản thô" vào mô hình TP.HCM. Mọi hàm mục tiêu và biến số phải phản ánh đặc thù logistics đô thị mật độ cao.

---

## 3. Kiến trúc Mô hình Lai 3 Giai đoạn (Hybrid 3-Stage Pipeline)

AI Agent cần triển khai hệ thống phân tích theo đúng trình tự 3 giai đoạn sau:

### Giai đoạn 1: Đánh giá Tiềm năng Hành lang (Corridor Potential Assessment)
* **Phân đoạn không gian (GIS):** Chia tuyến sông Sài Gòn từ Hiệp Bình Chánh đến Bạch Đằng/Khánh Hội thành 3 tiểu đoạn đặc trưng:
  * *Tiểu đoạn 1 (Cửa ngõ gom hàng Đông Bắc):* Hiệp Bình Chánh – Thanh Đa.
  * *Tiểu đoạn 2 (Đô thị chuyển tiếp mật độ cao):* Thảo Điền – Tân Cảng.
  * *Tiểu đoạn 3 (Lõi trung tâm tiêu thụ):* Ba Son – Bạch Đằng – Khánh Hội.
* **Vùng đệm & Đẳng thời:** Tạo vùng đệm không gian (Buffer Zone) bán kính $500\text{ m}$ và $1.5\text{ km}$ dọc hai bờ sông, kết hợp vùng đẳng thời (Network Isochrone) $5 - 10\text{ phút}$ di chuyển chặng cuối từ các bến thủy.
* **Thuật toán trọng số:** Sử dụng **Fuzzy AHP (AHP mờ tam giác)** để tính trọng số toàn cục $W_i$ cho 15 chỉ số thuộc 5 nhóm tiêu chí, sau đó tổng hợp điểm tiềm năng cho từng tiểu đoạn.

### Giai đoạn 2: Lựa chọn Vị trí Trạm Trung chuyển Tối ưu (Micro-Hub Site Selection)
* **Tập ứng viên ($A_k$):** Sàng lọc $6 - 8$ bến thủy hiện hữu hoặc vị trí quy hoạch dọc các tiểu đoạn tiềm năng (ví dụ: Bến Hiệp Bình Chánh, Bến Thanh Đa, Bến Thảo Điền, Bến Tân Cảng, Bến Bạch Đằng, Bến Khánh Hội).
* **Thuật toán xếp hạng:** Áp dụng **TOPSIS** (hoặc **VIKOR**) kết hợp bộ trọng số từ Fuzzy AHP và dữ liệu thực địa TP.HCM (đặc biệt là giá thuê mặt bằng ven sông và chi phí vận hành) để tính hệ số gần gũi lý tưởng $CC_k$, từ đó chọn ra Top 2–3 vị trí tối ưu nhất.

### Giai đoạn 3: Kiểm định Thực nghiệm (SPSS) & Mô phỏng Vận hành (RIS Demo)
* **Kinh tế lượng (SPSS):** Phân tích dữ liệu khảo sát sơ cấp ($n \ge 200$ người tiêu dùng TMĐT và $n \ge 100$ chủ shop/3PL) qua các bước: Thống kê mô tả $\rightarrow$ Kiểm định độ tin cậy Cronbach's Alpha $\rightarrow$ Phân tích nhân tố khám phá (EFA) $\rightarrow$ Phân tích hồi quy tuyến tính bội / Hồi quy Logistic nhị phân để đo lường tác động của chi phí, thời gian, RIS và cảm xúc xanh đến ý định sử dụng.
* **Mô phỏng RIS (Demo):** Xây dựng luồng dữ liệu mô phỏng hành trình một lô hàng TMĐT từ kho tổng (Thủ Đức/Bình Dương) $\rightarrow$ Bến Hiệp Bình Chánh $\rightarrow$ Tàu thủy tích hợp RIS $\rightarrow$ Trạm trung chuyển trung tâm $\rightarrow$ Xe máy điện giao chặng cuối.

---

## 4. Cơ sở Toán học & Công thức Chuẩn

Khi viết mã Python/R hoặc trình bày phương pháp luận, AI Agent sử dụng bộ công thức chuẩn sau:

### 4.1. Thuật toán Fuzzy AHP (Thang mờ tam giác Chang, 1996)
Chuyển đổi thang đánh giá Saaty ($1 - 9$) sang số mờ tam giác $\tilde{a}_{ij} = (l_{ij}, m_{ij}, u_{ij})$ với nghịch đảo $\tilde{a}_{ij}^{-1} = \left(\frac{1}{u_{ij}}, \frac{1}{m_{ij}}, \frac{1}{l_{ij}}\right)$.

Kiểm định tính nhất quán trên ma trận giải mờ (Crisp Matrix $A$) thông qua trị riêng lớn nhất $\lambda_{\max}$:

$$CI = \frac{\lambda_{\max} - n}{n - 1}, \quad CR = \frac{CI}{RI}$$

Điều kiện chấp nhận ma trận so sánh cặp là $CR < 0.1$ (với $n$ là số tiêu chí và $RI$ là chỉ số ngẫu nhiên theo bảng Saaty).

### 4.2. Chuẩn hóa Dữ liệu Không gian & Kinh tế (Min-Max Normalization)
Tách biệt rõ nhóm tiêu chí **Lợi ích ($J^+$ - càng lớn càng tốt)** và nhóm tiêu chí **Chi phí/Rủi ro ($J^-$ - càng nhỏ càng tốt)**:

* Đối với tiêu chí thuộc nhóm $J^+$:

$$r_{ik} = \frac{x_{ik} - \min_{k}(x_{ik})}{\max_{k}(x_{ik}) - \min_{k}(x_{ik})}$$

* Đối với tiêu chí thuộc nhóm $J^-$ (ví dụ: chi phí thuê mặt bằng, chi phí vận hành, rủi ro sạt lở):

$$r_{ik} = \frac{\max_{k}(x_{ik}) - x_{ik}}{\max_{k}(x_{ik}) - \min_{k}(x_{ik})}$$

### 4.3. Thuật toán TOPSIS Xếp hạng Trạm Trung chuyển
1. Tính ma trận chuẩn hóa có trọng số: $v_{ik} = W_i \times r_{ik}$ (với $\sum_{i=1}^{m} W_i = 1$).
2. Xác định giải pháp lý tưởng tốt nhất ($A^+$) và tệ nhất ($A^-$):

$$A^+ = \left\{ \max_k v_{ik} \mid i \in J^+; \, \min_k v_{ik} \mid i \in J^- \right\}, \quad A^- = \left\{ \min_k v_{ik} \mid i \in J^+; \, \max_k v_{ik} \mid i \in J^- \right\}$$

3. Tính khoảng cách Euclid của phương án trạm $k$ tới $A^+$ và $A^-$:

$$D_k^+ = \sqrt{\sum_{i=1}^{m} (v_{ik} - v_i^+)^2}, \quad D_k^- = \sqrt{\sum_{i=1}^{m} (v_{ik} - v_i^-)^2}$$

4. Tính hệ số gần gũi tương đối $CC_k \in [0, 1]$ (trạm có $CC_k$ lớn nhất được xếp hạng 1):

$$CC_k = \frac{D_k^-}{D_k^+ + D_k^-}$$

### 4.4. Mô hình Hồi quy Kiểm chứng Hành vi (SPSS)
Mô hình hồi quy tuyến tính bội đánh giá mức độ tác động đến Ý định sử dụng dịch vụ giao hàng TMĐT đường sông ($Y$):

$$Y = \beta_0 + \beta_1 X_{\text{Cost}} + \beta_2 X_{\text{Time\_RIS}} + \beta_3 X_{\text{Green\_Emotion}} + \beta_4 X_{\text{Convenience}} - \beta_5 X_{\text{Risk}} + \epsilon$$

Trong đó $\beta_i$ là hệ số hồi quy chuẩn hóa, kiểm định mức ý nghĩa thống kê với $p\text{-value} < 0.05$ và hệ số phóng đại phương sai $VIF < 2.0$.

---

## 5. Bộ 15 Chỉ số Đánh giá & Nguồn Dữ liệu Thực nghiệm TP.HCM

| Nhóm tiêu chí | Mã | Tên chỉ số thành phần | Hướng | Đơn vị đo | Nguồn dữ liệu thu thập tại TP.HCM |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **1. Luồng lạch & RIS** | `NAV1` | Tĩnh không cầu & Độ sâu luồng thông thuyền | $J^+$ | $\text{m}$ | Cục ĐTNĐ VN, số liệu bán nhật triều trạm Phú An. |
| | `NAV2` | Mật độ cầu bến tiếp cận trong vùng đệm | $J^+$ | $\text{bến/km}^2$ | Quy hoạch kết cấu hạ tầng ĐTNĐ TP.HCM đến 2030. |
| | `NAV3` | Mức độ sẵn sàng hạ tầng số RIS (AIS, 4G/5G, ENC) | $J^+$ | Điểm ($1-5$) | Cảng vụ ĐTNĐ TP.HCM & khảo sát thực địa tuyến. |
| **2. Nhu cầu TMĐT** | `ECO1` | Mật độ dân cư, chung cư & văn phòng vùng đệm | $J^+$ | $\text{người/km}^2$ | Niên giám thống kê TP.HCM, WorldPop, Google POI. |
| | `ECO2` | Khoảng cách từ bến gom tới kho tổng (Thủ Đức/BD) | $J^-$ | $\text{km}$ | Phân tích mạng lưới (QGIS / Distance Matrix API). |
| | `ECO3` | Khả năng kết nối mạng lưới đường bộ chặng cuối | $J^+$ | $\text{km/km}^2$ | Bản đồ giao thông Sở GTVT TP.HCM & OpenStreetMap. |
| **3. Chi phí & Tài chính** | `FIN1` | Đơn giá thuê mặt bằng trạm ven sông (CAPEX) | $J^-$ | $\text{VNĐ/m}^2\text{/tháng}$ | Bảng giá đất TP.HCM, báo cáo CBRE/Savills & thực tế. |
| | `FIN2` | Chi phí vận hành tàu điện/hybrid trên tuyến (OPEX) | $J^-$ | $\text{VNĐ/chuyến}$ | Định mức vận tải thủy Bộ GTVT & báo giá đóng tàu. |
| | `FIN3` | Chi phí bốc xếp & lưu kho trung chuyển tại Micro-Hub | $J^-$ | $\text{VNĐ/kiện}$ | Khảo sát định mức chi phí các doanh nghiệp 3PL. |
| **4. Môi trường Đô thị** | `ENV1` | Tiềm năng cắt giảm phát thải khí nhà kính | $J^+$ | $\text{kg CO}_2\text{/ngày}$ | Hệ số phát thải chuẩn IPCC / Bộ TN&MT. |
| | `ENV2` | Mức độ giảm tải cho các điểm nóng ùn tắc đường bộ | $J^+$ | Điểm ($1-5$) | Báo cáo điểm đen ùn tắc giao thông Sở GTVT TP.HCM. |
| | `ENV3` | Mức độ rủi ro sạt lở bờ sông & tác động sóng tàu | $J^-$ | Điểm ($1-5$) | Bản đồ cảnh báo sạt lở bờ sông, kênh, rạch TP.HCM. |
| **5. Hành vi & An toàn** | `BEH1` | Cảm xúc & thái độ ủng hộ logistics xanh của người mua | $J^+$ | Điểm Likert | Khảo sát định lượng người tiêu dùng ($n \ge 200$, SPSS). |
| | `BEH2` | Mức độ sẵn sàng chuyển đổi của chủ shop & 3PL | $J^+$ | Điểm Likert | Khảo sát nhà bán hàng/đơn vị vận chuyển ($n \ge 100$). |
| | `SOC1` | Mật độ xung đột giao thông thủy & rủi ro tai nạn | $J^-$ | $\text{vụ/năm}$ | Ban An toàn Giao thông TP.HCM & Cảng vụ ĐTNĐ. |

---

## 6. Cấu trúc Thư mục Dự án Đề xuất

AI Agent nên tổ chức mã nguồn và dữ liệu theo cấu trúc chuẩn hóa sau để dễ dàng bảo trì và tái lập kết quả:

```text
saigon-river-ecommerce-logistics/
|-- README.md                         # Tài liệu đặc tả hệ thống (file này)
|-- data/
|   |-- raw/                          # Dữ liệu thô: khảo sát chuyên gia, khảo sát SPSS, GIS shapefiles
|   |-- processed/                    # Dữ liệu đã làm sạch và chuẩn hóa Min-Max
|-- src/
|   |-- 01_fuzzy_ahp.py               # Tính ma trận mờ tam giác, kiểm định CR < 0.1 và xuất trọng số W_i
|   |-- 02_gis_buffer_analysis.py     # Trích xuất chỉ số không gian vùng đệm 500m - 1.5km & Isochrone
|   |-- 03_segment_scoring.py         # Chấm điểm tiềm năng 3 tiểu đoạn sông (Giai đoạn 1)
|   |-- 04_topsis_hub_selection.py    # Chạy thuật toán TOPSIS xếp hạng trạm Micro-Hub (Giai đoạn 2)
|   |-- 05_sensitivity_analysis.py    # Phân tích độ nhạy khi thay đổi trọng số chi phí/hành vi
|   |-- 06_ris_simulation_demo.py     # Mô phỏng vận hành tích hợp RIS & so sánh chi phí/CO2 với đường bộ
|-- spss_models/
|   |-- survey_data.sav               # Dữ liệu khảo sát hành vi & cảm xúc khách hàng
|   |-- regression_syntax.sps         # Lệnh chạy Cronbach's Alpha, EFA và Hồi quy trên SPSS
|-- outputs/
|   |-- tables/                       # Bảng trọng số, bảng xếp hạng đoạn sông, bảng xếp hạng trạm
|   |-- charts/                       # Biểu đồ cột trọng số, biểu đồ Radar, biểu đồ độ nhạy, bản đồ GIS
```

---

## 7. Danh mục Đầu ra & Biểu đồ Bắt buộc

Mọi script mô hình hóa do AI Agent viết cần tự động xuất ra đầy đủ các kết quả phục vụ trực tiếp cho bài báo khoa học và slide bảo vệ:

1. **Bảng trọng số Fuzzy AHP ($W_i$) & Kiểm định nhất quán ($CR$):** Chứng minh sự vượt trội về tầm quan trọng của yếu tố Chi phí mặt bằng/vận hành, Kết nối TMĐT và Hạ tầng RIS.
2. **Bảng điểm & Xếp hạng 3 tiểu đoạn sông Sài Gòn:** Kết quả Giai đoạn 1 kèm bản đồ nhiệt không gian GIS.
3. **Bảng xếp hạng Top vị trí đặt Trạm trung chuyển ($CC_k$):** Kết quả Giai đoạn 2 (so sánh trực tiếp giữa Hiệp Bình Chánh, Thanh Đa, Tân Cảng, Bạch Đằng...).
4. **Biểu đồ Radar (Spider Chart):** So sánh đa chiều điểm mạnh/yếu của từng ứng viên trạm trung chuyển trên 5 trục tiêu chí.
5. **Biểu đồ Phân tích Độ nhạy (Sensitivity Analysis):** Kiểm tra tính ổn định của thứ hạng trạm khi biến động trọng số nhóm Chi phí (`FIN`) hoặc Hành vi (`BEH`) trong biên độ $\pm 20\%$.
6. **Bảng kết quả Hồi quy SPSS & Biểu đồ đối chiếu Kịch bản RIS Demo:** So sánh thời gian vận chuyển, chi phí trên mỗi đơn hàng và lượng phát thải $\text{CO}_2$ giữa phương án đường bộ thuần túy và phương án kết hợp vận tải thủy sông Sài Gòn.

---

## 8. Quy tắc Thực thi dành cho AI Agent

1. **Tính minh bạch và tái lập (Reproducibility):** Mọi hàm tính toán trong Python (`numpy`, `pandas`, `geopandas`, `matplotlib`) phải có chú thích rõ ràng, cố định `random_seed` (nếu có mô phỏng) và xuất kết quả ra định dạng `.csv` / `.xlsx` kèm biểu đồ độ phân giải cao ($300\text{ DPI}$).
2. **Kiểm tra ràng buộc toán học tự động:** Trong `01_fuzzy_ahp.py`, luôn cài đặt câu lệnh kiểm tra `assert CR < 0.1` trước khi chuyển trọng số sang bước tính TOPSIS.
3. **Chuẩn mực học thuật:** Khi hỗ trợ viết nội dung báo cáo hoặc giải thích kết quả, sử dụng văn phong khoa học khách quan, trích dẫn đúng nguồn (Fathoni et al., 2017; Chang, 1996; Hwang & Yoon, 1981; PIANC, 2019) và luôn đối chiếu kết quả định lượng với thực tiễn giao thông, thủy văn và thị trường bất động sản tại TP.HCM.