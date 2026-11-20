# Tài liệu Đặc tả Nguồn Dữ liệu & Chiến lược Tìm kiếm (Data Acquisition & Calibration Guide)

> **Chỉ thị dành cho AI Agent:** Tệp này cung cấp bản đồ nguồn dữ liệu thứ cấp, các bộ thông số chuẩn từ các bài báo khoa học uy tín (quốc tế và Việt Nam) cùng hệ thống từ khóa tìm kiếm. Nhiệm vụ của bạn là **tìm kiếm, trích xuất, kiểm chứng và chuẩn hóa** các số liệu thực tế tại hành lang sông Sài Gòn (đoạn Hiệp Bình Chánh – Trung tâm TP.HCM) để nạp trực tiếp vào các mô hình **Fuzzy AHP**, **GIS – TOPSIS**, **Hồi quy đa biến SPSS** và **Mô phỏng RIS Demo** mà không cần chờ khảo sát sơ cấp.

---

## 1. Dữ liệu Kế thừa Trực tiếp từ Bài báo Nền tảng (Fathoni et al., 2017)

AI Agent sử dụng bộ trọng số và công thức từ nghiên cứu gốc trên hành lang sông Musi (*Muhammad Fathoni et al., 2017, Transportation Research Procedia, 25, 4544–4559*) làm **trọng số tham chiếu ban đầu (Baseline Weights)** trước khi hiệu chỉnh theo bối cảnh thương mại điện tử (TMĐT) đô thị TP.HCM:

* **Quy mô mẫu chuyên gia gốc:** $N = 50$ chuyên gia (41% quan chức giao thông, 12% tư vấn giao thông, 6% giảng viên đại học và các nhà khai thác vận tải thủy; 83% có trình độ Cử nhân/Thạc sĩ).
* **Độ nhất quán ma trận gốc:** Chỉ số nhất quán $CI = 0.0521 < 0.1$ (đạt chuẩn).
* **Công thức chuẩn hóa theo vùng đệm (Buffer Zone $500\text{ m} - 1\text{ km}$):**

$$
I_{ik} = \frac{X_{ik}}{\text{Area}_{\text{buffer}, k}}
$$

* **Bảng trọng số gốc cần kế thừa và tái cấu trúc:**

| Nhóm khía cạnh gốc (Trọng số) | Mã gốc | Chỉ số thành phần trong bài báo mẫu | Trọng số gốc ($w_i$) | Hướng chuyển đổi sang mô hình TP.HCM |
| :--- | :--- | :--- | :---: | :--- |
| **1. Kinh tế – ECO (42%)** | `ECO1B` | Chiều dài mạng lưới đường bộ/đường sắt song song | $13\%$ | Chuyển thành khả năng kết nối chặng cuối (`ECO3`) & khoảng cách kho tổng (`ECO2`). |
| | `ECO1A` | Số trung tâm hành chính quanh hành lang sông | $11\%$ | Chuyển thành mật độ chung cư, cao ốc văn phòng & TTTM (`ECO1`). |
| | `ECO2B` | Số trung tâm hoạt động kinh tế / $\text{Area}_{\text{buffer}}$ | $10\%$ | Tích hợp vào mật độ phát sinh/tiêu thụ đơn hàng TMĐT (`ECO1`). |
| | `ECO2A` | Thu nhập bình quân đầu người / $\text{Area}_{\text{buffer}}$ | $8\%$ | Mở rộng thêm nhóm **Chi phí mặt bằng & Vận hành (`FIN1`, `FIN2`, `FIN3`)**. |
| **2. Luồng lạch – NAV (26%)** | `NAV1` | Chiều dài luồng thông thuyền / $\text{Area}_{\text{buffer}}$ | $10\%$ | Chuyển thành tĩnh không cầu & độ sâu luồng bán nhật triều (`NAV1`). |
| | `NAV2` | Số lượng cầu cảng hiện hữu / $\text{Area}_{\text{buffer}}$ | $9\%$ | Giữ nguyên bản chất: mật độ cầu bến tiếp cận trong vùng đệm (`NAV2`). |
| | `NAV3` | Số lượng báo hiệu đường thủy / $\text{Area}_{\text{buffer}}$ | $7\%$ | Nâng cấp thành mức độ sẵn sàng hạ tầng số **RIS (`NAV3`)**. |
| **3. Xã hội – SOC (20%)** | `SOC1` | Số vụ tai nạn tàu thuyền / $\text{Area}_{\text{buffer}}$ | $12\%$ | Chuyển thành mật độ xung đột giao thông thủy đô thị (`SOC1`). |
| | `SOC2A` | Số hộ nghèo / $\text{Area}_{\text{buffer}}$ | $5\%$ | **Loại bỏ** (không phù hợp siêu đô thị), thay bằng **Hành vi & Cảm xúc xanh (`BEH1`, `BEH2`)**. |
| | `SOC2B` | Mật độ dân số / $\text{Area}_{\text{buffer}}$ | $3\%$ | Chuyển sang nhóm nhu cầu TMĐT đô thị (`ECO1`). |
| **4. Môi trường – ENV (12%)** | `ENV1` | Số sinh cảnh thủy sinh nhạy cảm / $\text{Area}_{\text{buffer}}$ | $7\%$ | Chuyển thành tiềm năng giảm phát thải $\text{CO}_2$ & giảm ùn tắc (`ENV1`, `ENV2`). |
| | `ENV2` | Diện tích khu bảo tồn / $\text{Area}_{\text{buffer}}$ | $5\%$ | Chuyển thành rủi ro sạt lở bờ sông & sóng tàu (`ENV3`). |

---

## 2. Danh mục Bài báo Khoa học Quốc tế & Thông số Cần Trích xuất

AI Agent cần truy xuất các công trình dưới đây để lấy bộ định mức kỹ thuật, trọng số MCDM và tham số mô phỏng vận tải thủy đô thị:

| Tác giả & Năm | Tên công trình & Tạp chí | Lĩnh vực | Dữ liệu & Thông số cụ thể cần trích xuất | Từ khóa tìm kiếm cho AI Agent |
| :--- | :--- | :--- | :--- | :--- |
| **Janjevic & Ndiaye (2014)** | *Inland waterway transport for urban freight distribution: A review of European initiatives*, WIT Transactions on The Built Environment, Vol. 138 | Vận tải hàng hóa & bưu kiện TMĐT bằng đường thủy đô thị | • Định mức tải trọng tàu nhỏ đô thị ($20 - 60\text{ tấn}$).<br>• Số lượng bưu kiện trung bình/chuyến ($1{,}500 - 4{,}000\text{ kiện}$).<br>• Thời gian bốc xếp tại bến ($30 - 45\text{ phút}$).<br>• Bán kính giao hàng chặng cuối bằng xe đạp/xe điện ($1.5 - 3.0\text{ km}$). | `"Janjevic" "Ndiaye" "Inland waterway transport for urban freight"` OR `"Mokum Mariteam"` `"Vert Chez Vous"` urban parcel barge |
| **Rao et al. (2015)** | *Location selection of city logistics centers under sustainability*, Transportation Research Part D, 36, 29–44 | Lựa chọn vị trí trạm trung chuyển logistics đô thị (Fuzzy TOPSIS) | • Cấu trúc ma trận đánh giá trạm trung chuyển đô thị.<br>• Trọng số tương đối giữa tiêu chí **Chi phí đất đai (Land Price)**, **Kết nối đa phương thức**, **Phát thải môi trường** và **Chấp nhận xã hội**. | `"Rao" "Location selection of city logistics centers under sustainability"` fuzzy TOPSIS weights |
| **Mihica et al. (2011)** & **PIANC (2019)** | *Policy and promotion of sustainable riverway transport in Europe - Danube River* (RSER, 15) & *PIANC Guidelines for River Information Services* | Hệ thống thông tin định vị đường thủy (RIS) | • Bộ 4 cấp độ đánh giá hạ tầng số RIS: (1) Thủy đồ điện tử Inland ECDIS, (2) Hệ thống nhận dạng tự động AIS, (3) Thông báo đường thủy NtS (mực nước, tĩnh không), (4) Kết nối trao đổi dữ liệu điện tử ERI với hệ thống quản lý kho/vận tải (WMS/TMS). | `"PIANC" "Guidelines for River Information Services"` OR `"Mihica" "sustainable riverway transport" RIS` |
| **Arencibia et al. (2015)** | *Modelling mode choice for freight transport using advanced choice experiments*, Transportation Research Part A, 75, 252–267 | Kinh tế lượng lựa chọn phương thức vận tải hàng hóa | • Hệ số co giãn của quyết định chuyển đổi phương thức vận tải theo **Chi phí vận chuyển**, **Thời gian hành trình** và **Độ tin cậy giao hàng** để đối chiếu với kết quả hồi quy SPSS. | `"Arencibia" "Modelling mode choice for freight transport"` cost reliability elasticity |
| **Hanh, V. T. (2006)** | *Canal-side highway in Ho Chi Minh City (HCMC), Vietnam: Issues of urban cultural conservation and tourism development*, GeoJournal, 66, 165–186 | Địa lý thủy văn & Kênh rạch đô thị TP.HCM | • Đặc điểm hình thái dòng chảy, lịch sử khai thác giao thông thủy và cấu trúc đô thị ven sông Sài Gòn – kênh rạch TP.HCM. | `"Hanh" "Canal-side highway in Ho Chi Minh City"` GeoJournal 2006 |

---

## 3. Nguồn Dữ liệu Thực nghiệm tại Việt Nam (Hành lang Sông Sài Gòn – TP.HCM)

AI Agent tìm kiếm và trích xuất dữ liệu từ các báo cáo chính thức và cơ sở dữ liệu mở tại Việt Nam theo bảng ánh xạ 15 chỉ số dưới đây:

### 3.1. Nhóm Kỹ thuật Luồng lạch, Hạ tầng số RIS & Bến thủy (`NAV1`, `NAV2`, `NAV3`)
* **Tài liệu mục tiêu:**
  1. *Quyết định phê duyệt Quy hoạch kết cấu hạ tầng đường thủy nội địa TP.HCM giai đoạn đến năm 2030* (Sở GTVT TP.HCM / TEDI South).
  2. *Thông báo hàng hải & Danh bạ luồng đường thủy nội địa quốc gia* (Cục Đường thủy nội địa Việt Nam – Chi cục ĐTNĐ phía Nam).
  3. *Số liệu thủy văn trạm Phú An (sông Sài Gòn)* – Đài Khí tượng Thủy văn khu vực Nam Bộ.
* **Thông số cần trích xuất:**
  * Chiều sâu luồng chạy tàu và biên độ dao động bán nhật triều không đều tại trạm Phú An (mực nước đỉnh triều khoảng $+1.5\text{ m}$ đến $+1.7\text{ m}$, chân triều $-1.8\text{ m}$ đến $-2.2\text{ m}$).
  * **Tĩnh không thông thuyền ($H_{\text{tk}}$)** thực tế của 6 cây cầu bắc qua hành lang nghiên cứu: Cầu Bình Lợi mới ($7.0\text{ m}$), Cầu Bình Triệu 1 & 2, Cầu Sài Gòn, Cầu Thủ Thiêm, Cầu Ba Son (Thủ Thiêm 2).
  * Tọa độ địa lý (`Lat, Lon`) của các bến thủy hiện hữu/quy hoạch: Bến Hiệp Bình Chánh, Bến Bình Lợi, Bến Thanh Đa, Bến Thảo Điền, Bến Tân Cảng, Bến Ba Son, Bến Bạch Đằng, Bến Khánh Hội.
* **Từ khóa tìm kiếm:**
  * `"tĩnh không thông thuyền" "cầu Bình Lợi" OR "cầu Bình Triệu" OR "cầu Sài Gòn" OR "cầu Ba Son"`
  * `"quy hoạch" "bến thủy nội địa" "sông Sài Gòn" TP.HCM`
  * `"biên độ triều" "trạm Phú An" sông Sài Gòn`

### 3.2. Nhóm Nhu cầu TMĐT & Dữ liệu Không gian GIS (`ECO1`, `ECO2`, `ECO3`)
* **Tài liệu & Nền tảng mục tiêu:**
  1. *Niên giám Thống kê TP.HCM* (Cục Thống kê TP.HCM – số liệu các năm gần nhất).
  2. *OpenStreetMap (Geofabrik Vietnam)* & *WorldPop Spatial Demographic Data*.
  3. *Báo cáo Chỉ số Thương mại điện tử Việt Nam (EBI)* – Hiệp hội Thương mại điện tử Việt Nam (VECOM).
* **Thông số cần trích xuất:**
  * Dân số, diện tích và mật độ dân số ($\text{người/km}^2$) của các phường ven sông thuộc TP. Thủ Đức (Hiệp Bình Chánh, Hiệp Bình Phước, Thảo Điền, An Khánh, Thủ Thiêm), Quận Bình Thạnh (Phường 25, 26, 27, 28, Phường 22), Quận 1 (Đa Kao, Bến Nghé, Nguyễn Thái Bình) và Quận 4 (Phường 12, 13, 18).
  * Số lượng và quy mô các đại đô thị, chung cư cao tầng, trung tâm thương mại nằm trong vùng đệm $500\text{ m} - 1.5\text{ km}$ (ví dụ: Gigamall Phạm Văn Đồng, Vạn Phúc City, Masteri Thảo Điền, Vinhomes Central Park, Saigon Pearl, Vinhomes Golden River).
  * Khoảng cách đường bộ từ các kho chia chọn (Sorting Hubs) tại TP. Thủ Đức & Dĩ An/Thuận An (KCN Sóng Thần, VSIP 1, Linh Trung) đến Bến Hiệp Bình Chánh.
* **Từ khóa tìm kiếm:**
  * `"Niên giám thống kê TP.HCM" diện tích dân số phường "Hiệp Bình Chánh" "Thảo Điền" "Bến Nghé"`
  * `"báo cáo chỉ số thương mại điện tử Việt Nam" VECOM TP.HCM`
  * `"trung tâm chia chọn" Shopee OR Lazada OR GHN "Thủ Đức" OR "Sóng Thần"`

### 3.3. Nhóm Chi phí Bất động sản & Định mức Vận tải Thủy (`FIN1`, `FIN2`, `FIN3`)
* **Tài liệu mục tiêu:**
  1. *Báo cáo của Ngân hàng Thế giới (World Bank, 2019): "Vietnam: Developing Inland Waterway Transport and Coastal Shipping"* & *Nghiên cứu VITRANSS 2 (JICA)*.
  2. *Bảng giá đất TP.HCM* (UBND TP.HCM) & *Báo cáo thị trường Bất động sản Công nghiệp/Thương mại TP.HCM* (Savills, CBRE, Cushman & Wakefield).
  3. *Định mức kinh tế – kỹ thuật vận tải đường thủy nội địa* (Bộ Giao thông Vận tải).
* **Thông số cần trích xuất:**
  * Đơn giá thuê mặt bằng thương mại/kho bãi ven sông ($\text{VNĐ/m}^2\text{/tháng}$ hoặc $\text{USD/m}^2\text{/tháng}$) phân theo 3 phân khu: Khu vực Hiệp Bình Chánh – Thủ Đức, Khu vực Thanh Đa – Tân Cảng (Bình Thạnh) và Khu vực Lõi trung tâm Quận 1 – Quận 4.
  * Định mức cước vận tải thủy nội địa tại khu vực phía Nam ($\text{VNĐ/tấn.km}$) so với cước vận tải xe tải nhẹ đường bộ ($1.5 - 2.5\text{ tấn}$).
  * Chi phí đầu tư/thuê tàu chở hàng cỡ nhỏ hoặc tàu điện/hybrid ($30 - 80\text{ tấn}$), chi phí nhiên liệu/điện năng và chi phí bốc xếp trung chuyển ($\text{VNĐ/kiện hàng}$).
* **Từ khóa tìm kiếm:**
  * `"Vietnam: Developing Inland Waterway Transport and Coastal Shipping" World Bank cost`
  * `"giá thuê kho bãi" OR "giá thuê mặt bằng" "Thủ Đức" "Bình Thạnh" "Quận 1" VNĐ/m2`
  * `"chi phí vận tải đường thủy nội địa" "tấn.km" miền Nam Việt Nam`

### 3.4. Nhóm Môi trường Đô thị & An toàn Giao thông Thủy (`ENV1`, `ENV2`, `ENV3`, `SOC1`)
* **Tài liệu mục tiêu:**
  1. *Cơ sở dữ liệu Quốc gia về Hệ số phát thải khí nhà kính* (Bộ Tài nguyên và Môi trường) & *Hướng dẫn kiểm kê khí nhà kính IPCC*.
  2. *Danh mục các vị trí sạt lở bờ sông, kênh, rạch nguy hiểm trên địa bàn TP.HCM* (Sở GTVT TP.HCM).
  3. *Báo cáo điểm đen ùn tắc giao thông và tình hình trật tự an toàn giao thông* (Sở GTVT & Ban An toàn Giao thông TP.HCM).
* **Thông số cần trích xuất:**
  * Hệ số phát thải $\text{CO}_2$ ($\text{g CO}_2\text{/tấn.km}$) của xe tải nhẹ chạy dầu diesel/xăng so với phương tiện thủy nội địa cỡ nhỏ / tàu điện.
  * Danh sách các điểm sạt lở bờ sông dọc hành lang nghiên cứu (đặc biệt khu vực bán đảo Thanh Đa – Bình Quới và phường Hiệp Bình Phước/Hiệp Bình Chánh).
  * Các điểm nóng ùn tắc song song với sông Sài Gòn (ngã tư Hàng Xanh, cầu Bình Triệu, đường Xô Viết Nghệ Tĩnh, Nguyễn Hữu Cảnh, Tôn Đức Thắng) và tần suất hoạt động của tuyến buýt sông Saigon Waterbus.
* **Từ khóa tìm kiếm:**
  * `"hệ số phát thải" "vận tải đường thủy" "đường bộ" Việt Nam CO2`
  * `"vị trí sạt lở bờ sông" "sông Sài Gòn" "Thanh Đa" OR "Hiệp Bình Chánh"`
  * `"điểm nguy cơ ùn tắc giao thông" "Hàng Xanh" OR "Bình Triệu" OR "Nguyễn Hữu Cảnh" TP.HCM`

---

## 4. Chiến lược Dữ liệu Thứ cấp Thay thế Khảo sát Sơ cấp (No-Survey Strategy)

Do hạn chế về thời gian không thể thu thập phiếu khảo sát người tiêu dùng, AI Agent thực hiện **2 kỹ thuật thay thế chuẩn khoa học** sau:

### 4.1. Thay thế Khảo sát Chuyên gia (Fuzzy AHP) bằng Trọng số Kế thừa + Phân tích Độ nhạy
1. Lấy ma trận trọng số nền từ **Fathoni et al. (2017)** và **Rao et al. (2015)**, điều chỉnh tỷ trọng nhóm Chi phí mặt bằng/vận hành (`FIN`) và Nhu cầu TMĐT (`ECO`) theo đặc thù đô thị TP.HCM.
2. Viết module **Phân tích độ nhạy (Sensitivity Analysis)** biến thiên trọng số của từng nhóm tiêu chí trong biên độ $\pm 10\%$ và $\pm 20\%$ (chia thành $10 - 15$ kịch bản giả định) để chứng minh thứ hạng trạm trung chuyển tối ưu giữ vững tính ổn định.

### 4.2. Thay thế Khảo sát Hành vi (SPSS) bằng Hồi quy Dữ liệu Không gian – Kinh tế Cấp Phường
AI Agent xây dựng bộ dữ liệu chéo (Cross-sectional Data) gồm **$N = 25$ đến $30$ phường/xã** nằm dọc hành lang sông Sài Gòn và các nhánh kênh kết nối trực tiếp (thuộc TP. Thủ Đức, Bình Thạnh, Quận 1, Quận 4, Quận 7) để chạy **Tương quan Pearson** và **Hồi quy tuyến tính bội trên SPSS**:

* **Biến phụ thuộc ($Y$ – `Ecom_Waterway_Potential`):** Chỉ số tiềm năng/nhu cầu chuyển dịch đơn hàng TMĐT sang đường thủy tại phường $j$ (tính tổng hợp từ quy mô dân số, mật độ chung cư/văn phòng và mức độ áp lực cấm tải/ùn tắc đường bộ).
* **Các biến độc lập ($X_1 \dots X_5$):**
  * $X_1$ (`Pop_Density`): Mật độ dân số của phường ($\text{người/km}^2$).
  * $X_2$ (`Dist_To_Jetty`): Khoảng cách mạng lưới đường bộ từ tâm phường tới bến thủy gần nhất ($\text{km}$).
  * $X_3$ (`Land_Rent_Cost`): Đơn giá thuê mặt bằng thương mại/kho bãi trung bình tại phường ($\text{triệu VNĐ/m}^2\text{/tháng}$).
  * $X_4$ (`LastMile_Connectivity`): Mật độ mạng lưới đường nhánh kết nối chặng cuối ($\text{km/km}^2$).
  * $X_5$ (`CO2_Cost_Saving`): Mức tiết kiệm chi phí và phát thải $\text{CO}_2$ ước tính khi chuyển từ đường bộ sang đường thủy ($\text{điểm chuẩn hóa}$).

---

## 5. Cấu trúc File Dữ liệu Chuẩn hóa AI Agent Cần Xuất Ra (`data/processed/`)

Sau khi tìm kiếm và trích xuất dữ liệu, AI Agent phải đóng gói kết quả thành 4 tệp `.csv` sạch với cấu trúc cột chính xác như sau:

### 5.1. `corridor_segments.csv` (Đầu vào Giai đoạn 1 – Đánh giá 3 tiểu đoạn sông)
```csv
segment_id,segment_name,length_km,buffer_area_km2,NAV1,NAV2,NAV3,ECO1,ECO2,ECO3,FIN1,FIN2,FIN3,ENV1,ENV2,ENV3,BEH1,BEH2,SOC1
SEG1,Hiep Binh Chanh - Thanh Da,6.5,13.0,,,,,,,,,,,,,
SEG2,Thao Dien - Tan Cang,5.8,11.6,,,,,,,,,,,,,
SEG3,Ba Son - Bach Dang - Khanh Hoi,4.2,8.4,,,,,,,,,,,,,
```

### 5.2. `hub_candidates.csv` (Đầu vào Giai đoạn 2 – Xếp hạng TOPSIS các trạm trung chuyển)
```csv
hub_id,hub_name,district,lat,lon,NAV1,NAV2,NAV3,ECO1,ECO2,ECO3,FIN1,FIN2,FIN3,ENV1,ENV2,ENV3,BEH1,BEH2,SOC1
HUB1,Ben Hiep Binh Chanh,Thu Duc,10.8315,106.7180,,,,,,,,,,,,,,,
HUB2,Ben Thanh Da,Binh Thanh,10.8162,106.7235,,,,,,,,,,,,,,,
HUB3,Ben Thao Dien,Thu Duc,10.8065,106.7320,,,,,,,,,,,,,,,
HUB4,Ben Tan Cang,Binh Thanh,10.7938,106.7230,,,,,,,,,,,,,,,
HUB5,Ben Bach Dang,District 1,10.7735,106.7065,,,,,,,,,,,,,,,
HUB6,Ben Khanh Hoi,District 4,10.7660,106.7080,,,,,,,,,,,,,,,
```

### 5.3. `spss_ward_data.csv` (Đầu vào Giai đoạn 3 – Hồi quy đa biến trên SPSS)
```csv
ward_id,ward_name,district,Ecom_Waterway_Potential,Pop_Density,Dist_To_Jetty,Land_Rent_Cost,LastMile_Connectivity,CO2_Cost_Saving
W01,Hiep Binh Chanh,Thu Duc,,,,,,
W02,Hiep Binh Phuoc,Thu Duc,,,,,,
W03,Thao Dien,Thu Duc,,,,,,
...
```

### 5.4. `ris_demo_parameters.csv` (Đầu vào Kịch bản Mô phỏng Vận hành RIS)
```csv
scenario,mode,distance_km,vessel_or_truck_capacity_parcels,transit_time_min,handling_time_min,cost_per_parcel_vnd,co2_emission_kg_per_trip
BASE_ROAD,Light Truck (2.5T) via QL13 - XVNT,16.5,2500,,,,
DEMO_WATER_RIS,Hybrid Barge + RIS + E-Bike Last-Mile,14.8,3000,,,,
```

---

## 6. Quy tắc Kiểm soát Chất lượng Dữ liệu (Data Governance Rules)

1. **Cấm bịa đặt số liệu (Zero Hallucination):** Mọi con số điền vào các tệp `.csv` đều phải có cột/tệp ghi chú nguồn trích dẫn rõ ràng (`source_citation`). Nếu một thông số chưa tìm thấy số liệu công bố chính thức cho đúng phường/bến đó, AI Agent phải lấy số liệu của cấp quận tương ứng hoặc nội suy từ tài liệu quy hoạch và gắn nhãn `[Estimated from District Average]`.
2. **Đồng nhất đơn vị đo lường:** Quy đổi toàn bộ đơn vị tiền tệ về `VNĐ`, diện tích về `km²` hoặc `m²`, khoảng cách về `km`, và phát thải về `kg CO2` trước khi chạy chuẩn hóa Min-Max.
3. **Tự động kiểm tra khuyết dữ liệu:** Đảm bảo không có giá trị `NaN` hoặc `0` bất hợp lý làm sai lệch mẫu số trong công thức chuẩn hóa Min-Max và khoảng cách Euclid của thuật toán TOPSIS.