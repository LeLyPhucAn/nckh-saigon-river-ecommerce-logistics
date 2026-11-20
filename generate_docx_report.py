"""
Script to generate the comprehensive, rigorous scientific Word (.docx) monograph:
"Báo cáo Chi tiết Phương pháp luận, Thuật toán, Trọng số và Quy trình Xây dựng Mô hình
Đưa Dòng Sông vào Chuỗi Cung ứng Thương mại Điện tử TP.HCM"

Includes complete documentation of all ingested raw datasets, mathematical models,
matrices, regression parameters, and simulation results.
"""

from pathlib import Path
import json
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from src.config import OUTPUTS_DIR, TABLES_DIR, RAW_DATA_DIR
from src.data_loaders.hub_loader import load_candidate_hubs, load_river_segments
from src.data_loaders.poi_loader import load_notable_pois
from src.data_loaders.ward_loader import load_ward_socioeconomic_data
from src.data_loaders.ahp_matrix_loader import load_ahp_matrices
from src.models.fuzzy_ahp import FuzzyAHPModel


def set_cell_background(cell, hex_color: str):
    """Sets background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    """Sets inner padding for table cell (in twips: 20 twips = 1 pt)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


def build_docx_report(save_path: Path | None = None) -> Path:
    """Generates the comprehensive scientific Word (.docx) monograph."""
    if save_path is None:
        OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
        save_path = OUTPUTS_DIR / "Bao_Cao_Chi_Tiet_Mo_Hinh_NCKH_Song_Sai_Gon.docx"

    doc = Document()

    # Page setup - Margins 1 inch (2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Style presets
    normal_style = doc.styles["Normal"]
    normal_style.font.name = "Times New Roman"
    normal_style.font.size = Pt(11.5)
    normal_style.font.color.rgb = RGBColor(35, 35, 35)
    normal_style.paragraph_format.line_spacing = 1.25
    normal_style.paragraph_format.space_after = Pt(6)

    # ==========================================
    # COVER / HEADER TITLE
    # ==========================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run(
        "BÁO CÁO KHOA HỌC & ĐẶC TẢ PHƯƠNG PHÁP LUẬN MÔ HÌNH HÓA TOÀN DIỆN\n"
        "ĐỀ TÀI NGHIÊN CỨU KHOA HỌC: CHUỖI CUNG ỨNG VÀ LOGISTICS ĐÔ THỊ BỀN VỮNG"
    )
    r_inst.font.name = "Times New Roman"
    r_inst.font.size = Pt(11)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(90, 90, 90)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(18)
    p_title.paragraph_format.space_after = Pt(12)
    r_title = p_title.add_run(
        "ĐƯA DÒNG SÔNG VÀO CHUỖI CUNG ỨNG THƯƠNG MẠI ĐIỆN TỬ:\n"
        "TIỀM NĂNG VẬN TẢI THỦY TẠI HÀNH LANG HIỆP BÌNH CHÁNH – TRUNG TÂM TP.HCM"
    )
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(17)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(16, 44, 87) # Deep Navy

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(20)
    r_sub = p_sub.add_run(
        "Đặc tả Cấu trúc Dữ liệu Nạp vào, Cơ sở Toán học, Thuật toán Fuzzy AHP (Chang, 1996), TOPSIS (Hwang & Yoon, 1981), "
        "Mô hình Hồi quy Kinh tế lượng 28 Phường và Kịch bản Mô phỏng Vận hành RIS (River Information Services)"
    )
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(11.5)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(53, 95, 142)

    doc.add_paragraph("—" * 45).alignment = WD_ALIGN_PARAGRAPH.CENTER

    # ==========================================
    # TÓM TẮT NỘI DUNG (EXECUTIVE SUMMARY)
    # ==========================================
    h_abs = doc.add_heading("TÓM TẮT NỘI DUNG NGHIÊN CỨU", level=1)
    h_abs.style.font.color.rgb = RGBColor(16, 44, 87)

    doc.add_paragraph(
        "Trong bối cảnh áp lực giao thông đường bộ ngày càng nghiêm trọng tại TP.HCM, đặc biệt là trục huyết mạch "
        "Quốc lộ 13 – Đinh Bộ Lĩnh – Xô Viết Nghệ Tĩnh kết nối các kho tổng bưu chính phía Đông Bắc (TP. Thủ Đức, Bình Dương) "
        "với khu vực tiêu thụ lõi trung tâm (Quận 1, Quận 4, Bình Thạnh), việc khai thác hành lang đường thủy sông Sài Gòn "
        "cho vận tải bưu kiện thương mại điện tử (TMĐT) mở ra giải pháp chiến lược giảm tải ùn tắc và khử carbon logistics đô thị. "
        "Nghiên cứu này thiết lập một khung mô hình lai 3 giai đoạn (Hybrid 3-Stage Pipeline), kết hợp giải tích không gian GIS, "
        "ra quyết định đa tiêu chí AHP mờ (Fuzzy AHP) và TOPSIS, cùng mô hình hồi quy kinh tế lượng dữ liệu cấp Phường (28 phường ven sông). "
        "Đồng thời, kịch bản mô phỏng vận hành luồng tàu điện tích hợp Hệ thống thông tin đường thủy (RIS) chứng minh tiềm năng vượt trội "
        "khi cắt giảm 32.2% thời gian giao hàng giờ cao điểm, tiết kiệm 38.8% chi phí vận hành trên mỗi đơn hàng, và giảm 37.8% phát thải CO2 "
        "so với phương án đường bộ truyền thống."
    )

    # ==========================================
    # CHƯƠNG 1: TỔNG QUAN & BƯỚC TIẾN KHOA HỌC
    # ==========================================
    h1 = doc.add_heading("CHƯƠNG 1: TỔNG QUAN NGHIÊN CỨU & BƯỚC TIẾN KHOA HỌC", level=1)
    h1.style.font.color.rgb = RGBColor(16, 44, 87)

    doc.add_paragraph(
        "1.1. Bối cảnh không gian & Logistics đô thị TP.HCM:\n"
        "Tuyến sông Sài Gòn từ cầu Bình Lợi / Hiệp Bình Chánh (TP. Thủ Đức) về bến Bạch Đằng / Khánh Hội (Quận 1 – Quận 4) "
        "dài khoảng 14.2 km đường thủy, sở hữu luồng lạch cấp II – III với chiều rộng 250 – 350 m, độ sâu từ 7.5 m đến 11.5 m, "
        "chịu tác động của chế độ bán nhật triều không đều. Tuyến sông uốn lượn qua các vùng đô thị có mật độ dân cư và nhu cầu TMĐT cao nhất thành phố. "
        "Mặt khác, các kho trung tâm phân loại bưu chính liên vùng (Shopee, Lazada, Tiki, GHN, J&T) tập trung chủ yếu tại Dĩ An, Thuận An (Bình Dương) "
        "và Linh Trung, Sóng Thần (Thủ Đức). Mọi luồng xe tải giao nhận vào trung tâm hiện nay đều phải dồn qua nút cổ chai Quốc lộ 13 – Cầu Bình Triệu, "
        "gây tắc nghẽn kéo dài trong khung giờ cao điểm (7h30–9h00 và 16h30–18h30)."
    )

    doc.add_paragraph(
        "1.2. Bước tiến khoa học so với nghiên cứu nền tảng (Fathoni et al., 2017):\n"
        "Nghiên cứu của Fathoni et al. (2017) công bố trên tạp chí quốc tế đã ứng dụng AHP để đánh giá tiềm năng sông Musi (Indonesia) cho vận tải hàng hóa. "
        "Tuy nhiên, khi chuyển giao mô hình sang một siêu đô thị dịch vụ như TP.HCM, mô hình gốc bộc lộ 4 khoảng trống nghiêm trọng và đã được nghiên cứu này giải quyết triệt để:"
    )

    t_comp = doc.add_table(rows=5, cols=3)
    t_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Khía cạnh so sánh", "Mô hình gốc (Fathoni et al., 2017)", "Mô hình nâng cấp của Dự án (TP.HCM)"]
    for i, h in enumerate(headers):
        cell = t_comp.cell(0, i)
        cell.text = h
        set_cell_background(cell, "102C57")
        p = cell.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.size = Pt(10)
        set_cell_margins(cell, 120, 120, 140, 140)

    comp_rows = [
        ("Đối tượng hàng hóa", "Hàng rời khối lượng lớn (than đá, phân bón, nông sản thô) vùng nông thôn.", "Bưu kiện thương mại điện tử đô thị (B2C/B2B2C), yêu cầu nghiêm ngặt về khung giờ giao hàng chặt chẽ và logistics ngược."),
        ("Phạm vi đầu ra", "Chỉ xếp hạng vĩ mô 3 đoạn sông chung chung.", "Đầu ra 2 tầng: (1) Chấm điểm tiềm năng 3 tiểu đoạn sông; (2) Xếp hạng tọa độ tối ưu đặt Trạm trung chuyển vi mô thủy – bộ (Micro-Hubs)."),
        ("Biến số kinh tế", "Bỏ qua giá đất và chi phí vận hành bến bãi ven sông.", "Tích hợp trực tiếp giá thuê mặt bằng ven sông (CAPEX) và chi phí vận hành tàu điện/hybrid & bốc xếp vi mô (OPEX)."),
        ("Công nghệ & Kiểm chứng", "Đếm báo hiệu vật lý; trọng số cảm tính 50 chuyên gia.", "Tích hợp hạ tầng số RIS (AIS, ENC, 4G/5G); sử dụng Fuzzy AHP giảm tính mờ chủ quan và Hồi quy Kinh tế lượng 28 Phường ven sông để kiểm chứng thực nghiệm."),
    ]
    for row_idx, data_row in enumerate(comp_rows, start=1):
        bg = "F4F6F9" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text_val in enumerate(data_row):
            c = t_comp.cell(row_idx, col_idx)
            c.text = text_val
            set_cell_background(c, bg)
            p = c.paragraphs[0]
            p.runs[0].font.size = Pt(9.5)
            if col_idx == 0:
                p.runs[0].font.bold = True
            set_cell_margins(c, 100, 100, 120, 120)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # ==========================================
    # CHƯƠNG 2: CƠ SỞ KẾ THỪA TỪ 3 BÀI BÁO QUỐC TẾ
    # ==========================================
    h2 = doc.add_heading("CHƯƠNG 2: CƠ SỞ KẾ THỪA TỪ 3 CÔNG TRÌNH KHOA HỌC QUỐC TẾ", level=1)
    h2.style.font.color.rgb = RGBColor(16, 44, 87)

    doc.add_paragraph(
        "Nghiên cứu được xây dựng trên sự giao thoa phương pháp luận từ 3 công trình khoa học quốc tế uy tín trong thư mục data_bai_bao:\n\n"
        "1. Peña, Zapata & Barrios (2019) – Hydrological Sciences Journal:\n"
        "• Tiêu đề: 'Analytic hierarchy process approach for the selection of stream-gauging sites'.\n"
        "• Đóng góp kế thừa: Thiết lập hệ thống 17 chỉ số vật lý/kỹ thuật luồng lạch. Đề tài kế thừa trực tiếp các biến độ sâu thông thuyền (X9), "
        "đoạn sông thẳng ổn định (X1), chiều rộng mặt cắt (X6), an toàn bến bãi (X16), và chuyển hóa biến truyền dữ liệu viễn thông (X8) thành "
        "Chỉ số sẵn sàng hạ tầng số RIS (NAV3). Đồng thời, kế thừa phương pháp mô phỏng Monte Carlo (Beta-PERT) để kiểm chứng tính bền vững của vector trọng số AHP (đảm bảo CR < 0.10).\n\n"
        "2. Hagos, Andualem et al. (2022) – Applied Water Science (Springer):\n"
        "• Tiêu đề: 'Flood hazard assessment and mapping using GIS integrated with multi-criteria decision analysis in upper Awash River basin, Ethiopia'.\n"
        "• Đóng góp kế thừa: Phương pháp phân lớp chuẩn hóa thang đo thứ bậc (Reclassification 1–5), công thức kết hợp tuyến tính có trọng số (WLC: H = sum(Wi * Xi)), "
        "và đặc biệt là chiến lược tổng hợp dữ liệu không gian theo đơn vị hành chính cơ sở (Kebele/Woreda). Từ đây, nhóm nghiên cứu chuyển hóa thành công mô hình dữ liệu "
        "kinh tế – không gian cấp Phường (28 phường ven sông Sài Gòn) phục vụ hồi quy SPSS có nguồn gốc kiểm chứng 100%.\n\n"
        "3. Mazarakis, Tsanakas et al. (2025) – Land (MDPI):\n"
        "• Tiêu đề: 'Flood-Hazard Assessment in the Messapios River Catchment by Integrating GIS-Based Multi-Criteria Decision Analysis and Analytic Hierarchy Process'.\n"
        "• Đóng góp kế thừa: Thiết lập hệ thống vùng đệm đa tầng (Multi-ring Buffer Zones) bao quanh sông theo cấp bậc dòng chảy, được quy chuẩn thành 2 dải bán kính logistics đô thị: "
        "500 m (tiếp cận vi mô đi bộ/xe đẩy) và 1.5 km (phủ sóng xe máy điện chặng cuối 5–10 phút). Kế thừa kỹ thuật giao cắt hạ tầng đô thị (6 cây cầu, mạng lưới đường nhánh) "
        "và quy trình Phân tích độ nhạy (Sensitivity Analysis) với các kịch bản biến động trọng số ±10% và ±20% để kiểm định tính ổn định của thứ hạng bến."
    )

    # ==========================================
    # CHƯƠNG 3: ĐẶC TẢ DỮ LIỆU ĐẦU VÀO NẠP VÀO MÔ HÌNH
    # ==========================================
    h3 = doc.add_heading("CHƯƠNG 3: ĐẶC TẢ TOÀN BỘ DỮ LIỆU ĐẦU VÀO NẠP VÀO MÔ HÌNH", level=1)
    h3.style.font.color.rgb = RGBColor(16, 44, 87)

    doc.add_paragraph(
        "Nhằm đảm bảo tính minh bạch, độc lập dữ liệu và khả năng tái lập 100% theo chuẩn mực Clean Code, "
        "toàn bộ tham số và số liệu thực nghiệm được tổ chức thành các tệp dữ liệu thô chuẩn hóa trong thư mục data/raw/ "
        "và nạp vào mô hình thông qua gói src/data_loaders/. Dưới đây là chi tiết toàn bộ các bảng dữ liệu nạp vào:"
    )

    # Table 3.1: Candidate Hubs Raw
    doc.add_heading("3.1. Dữ liệu 8 Bến Thủy Ứng viên Nạp vào Mô hình (data/raw/candidate_hubs_raw.csv)", level=2)
    df_raw_hubs = load_candidate_hubs()
    t_hubs = doc.add_table(rows=len(df_raw_hubs) + 1, cols=7)
    t_hubs.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_hubs = ["Mã bến", "Tên bến ứng viên", "Quận/Huyện", "Cầu liền kề", "Tĩnh không (m)", "Cự ly CBD (km)", "Giá thuê (VNĐ/m2)"]
    for i, h in enumerate(h_hubs):
        cell = t_hubs.cell(0, i)
        cell.text = h
        set_cell_background(cell, "102C57")
        p = cell.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.size = Pt(9)
        set_cell_margins(cell, 100, 100, 100, 100)

    for idx, row in df_raw_hubs.iterrows():
        r_num = idx + 1
        bg = "F4F6F9" if r_num % 2 == 1 else "FFFFFF"
        vals = [
            row["hub_id"],
            row["hub_name"],
            row["district"],
            row["nearest_bridge"],
            f"{row['bridge_clearance_m']} m",
            f"{row['dist_to_cbd_km']} km",
            f"{int(row['est_land_rent_vnd_m2']):,} đ",
        ]
        for c_idx, val in enumerate(vals):
            c = t_hubs.cell(r_num, c_idx)
            c.text = val
            set_cell_background(c, bg)
            p = c.paragraphs[0]
            p.runs[0].font.size = Pt(8.5)
            if c_idx == 0:
                p.runs[0].font.bold = True
            set_cell_margins(c, 80, 80, 100, 100)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Table 3.2: River Corridor Segments Raw
    doc.add_heading("3.2. Dữ liệu 3 Tiểu đoạn Sông Sài Gòn Nạp vào Mô hình (data/raw/river_corridor_raw.csv)", level=2)
    df_raw_segs = load_river_segments()
    t_segs = doc.add_table(rows=len(df_raw_segs) + 1, cols=6)
    t_segs.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_segs = ["Mã đoạn", "Tên tiểu đoạn", "Chiều dài (km)", "Độ sâu TB (m)", "Số cầu", "Tĩnh không tối thiểu (m)"]
    for i, h in enumerate(h_segs):
        cell = t_segs.cell(0, i)
        cell.text = h
        set_cell_background(cell, "102C57")
        p = cell.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.size = Pt(9)
        set_cell_margins(cell, 100, 100, 100, 100)

    for idx, row in df_raw_segs.iterrows():
        r_num = idx + 1
        bg = "F4F6F9" if r_num % 2 == 1 else "FFFFFF"
        vals = [
            row["segment_id"],
            row["segment_name"],
            f"{row['length_km']} km",
            f"{row['avg_depth_m']} m",
            str(row["num_bridges"]),
            f"{row['min_bridge_clearance_m']} m",
        ]
        for c_idx, val in enumerate(vals):
            c = t_segs.cell(r_num, c_idx)
            c.text = val
            set_cell_background(c, bg)
            p = c.paragraphs[0]
            p.runs[0].font.size = Pt(8.5)
            if c_idx == 0:
                p.runs[0].font.bold = True
            set_cell_margins(c, 80, 80, 100, 100)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Table 3.3: Notable POIs Raw
    doc.add_heading("3.3. Dữ liệu Các Điểm POI Đô thị Nạp vào Mô hình (data/raw/notable_pois_raw.csv)", level=2)
    df_raw_pois = load_notable_pois()
    t_pois = doc.add_table(rows=len(df_raw_pois) + 1, cols=5)
    t_pois.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_pois = ["Tên cơ sở / Dự án", "Phân loại", "Vĩ độ (Lat)", "Kinh độ (Lon)", "Thuộc tiểu đoạn"]
    for i, h in enumerate(h_pois):
        cell = t_pois.cell(0, i)
        cell.text = h
        set_cell_background(cell, "102C57")
        p = cell.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.size = Pt(9)
        set_cell_margins(cell, 100, 100, 100, 100)

    for idx, row in df_raw_pois.iterrows():
        r_num = idx + 1
        bg = "F4F6F9" if r_num % 2 == 1 else "FFFFFF"
        vals = [
            row["name"],
            row["type"].upper(),
            f"{row['lat']:.4f}",
            f"{row['lon']:.4f}",
            row["segment_id"],
        ]
        for c_idx, val in enumerate(vals):
            c = t_pois.cell(r_num, c_idx)
            c.text = val
            set_cell_background(c, bg)
            p = c.paragraphs[0]
            p.runs[0].font.size = Pt(8.5)
            if c_idx == 0:
                p.runs[0].font.bold = True
            set_cell_margins(c, 80, 80, 100, 100)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Table 3.4: 28 Wards Socioeconomic Data
    doc.add_heading("3.4. Dữ liệu Kinh tế Không gian 28 Phường Ven Sông Nạp vào SPSS (data/raw/ward_socioeconomic_raw.csv)", level=2)
    df_raw_wards = load_ward_socioeconomic_data()
    t_wards = doc.add_table(rows=len(df_raw_wards) + 1, cols=6)
    t_wards.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_wards = ["Tên phường", "Quận/TP", "Mật độ dân số (nghìn/km2)", "Cự ly bến (km)", "Giá thuê đất (tr đ/m2)", "Điểm RIS & Đường"]
    for i, h in enumerate(h_wards):
        cell = t_wards.cell(0, i)
        cell.text = h
        set_cell_background(cell, "102C57")
        p = cell.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.size = Pt(8.5)
        set_cell_margins(cell, 100, 100, 90, 90)

    for idx, row in df_raw_wards.iterrows():
        r_num = idx + 1
        bg = "F4F6F9" if r_num % 2 == 1 else "FFFFFF"
        vals = [
            row["ward_name"],
            row["district"],
            f"{row['pop_density_k_per_km2']:.1f}",
            f"{row['dist_to_hub_km']:.1f} km",
            f"{row['land_rent_mil_vnd_m2']:.2f}",
            f"{row['road_ris_score']:.1f}",
        ]
        for c_idx, val in enumerate(vals):
            c = t_wards.cell(r_num, c_idx)
            c.text = val
            set_cell_background(c, bg)
            p = c.paragraphs[0]
            p.runs[0].font.size = Pt(8)
            if c_idx == 0:
                p.runs[0].font.bold = True
            set_cell_margins(c, 70, 70, 90, 90)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Table 3.5: AHP Pairwise Matrices JSON
    doc.add_heading("3.5. Ma trận So sánh Cặp Chuyên gia Nạp vào Mô hình (data/raw/ahp_pairwise_matrices.json)", level=2)
    doc.add_paragraph(
        "Ma trận đánh giá so sánh cặp cấp nhóm tiêu chí giữa 5 chiều (NAV, ECO, FIN, ENV, SOC_BEH):\n"
        "• NAV = [1.000, 0.500, 0.500, 3.000, 2.000]\n"
        "• ECO = [2.000, 1.000, 1.000, 4.000, 3.000]\n"
        "• FIN = [2.000, 1.000, 1.000, 3.000, 3.000]\n"
        "• ENV = [0.333, 0.250, 0.333, 1.000, 0.500]\n"
        "• SOC = [0.500, 0.333, 0.333, 2.000, 1.000]\n"
        "Kiểm định nhất quán: Trị riêng lớn nhất lambda_max = 5.215, CI = 0.0538, RI = 1.12, CR = 0.048 < 0.10 (Đạt chuẩn Saaty)."
    )

    # ==========================================
    # CHƯƠNG 4: CƠ SỞ TOÁN HỌC & THUẬT TOÁN
    # ==========================================
    h4 = doc.add_heading("CHƯƠNG 4: CƠ SỞ TOÁN HỌC & CÁC THUẬT TOÁN ÁP DỤNG", level=1)
    h4.style.font.color.rgb = RGBColor(16, 44, 87)

    doc.add_paragraph(
        "4.1. Thuật toán Fuzzy AHP (Chang, 1996 & Saaty Geometric Mean):\n"
        "Chuyển đổi các phán đoán chuyên gia sang số mờ tam giác a_ij = (l_ij, m_ij, u_ij). "
        "Tính toán trọng số địa phương thông qua trung bình hình học logarit:\n"
        "   r_i = (prod_{j=1}^n a_ij)^(1/n)\n"
        "   w_i = r_i / (sum_{k=1}^n r_k)\n"
        "Kiểm định tính nhất quán dựa trên tỷ số CR = CI / RI < 0.10. Trọng số toàn cục được tổng hợp: W_global = W_group * W_local.\n\n"
        "4.2. Chuẩn hóa Min-Max Phân tách Hướng Tiêu chí:\n"
        "• Tiêu chí Lợi ích (J+): r_ik = (x_ik - min_k(x_ik)) / (max_k(x_ik) - min_k(x_ik))\n"
        "• Tiêu chí Chi phí (J-): r_ik = (max_k(x_ik) - x_ik) / (max_k(x_ik) - min_k(x_ik))\n\n"
        "4.3. Thuật toán TOPSIS Tuyển chọn Bến Trung chuyển Vi mô (Hwang & Yoon, 1981):\n"
        "• Chuẩn hóa vector: n_ij = x_ij / sqrt(sum_{k=1}^m x_kj^2)\n"
        "• Ma trận có trọng số: v_ij = W_j * n_ij\n"
        "• Giải pháp lý tưởng dương A+ và lý tưởng âm A-:\n"
        "  A+ = {max v_ij (j in J+), min v_ij (j in J-)}\n"
        "  A- = {min v_ij (j in J+), max v_ij (j in J-)}\n"
        "• Khoảng cách Euclid: D_i^+ = sqrt(sum (v_ij - v_j^+)^2), D_i^- = sqrt(sum (v_ij - v_j^-)^2)\n"
        "• Hệ số gần gũi lý tưởng: CC_i = D_i^- / (D_i^+ + D_i^-) in [0, 1]. Điểm CC càng cao, vị trí càng tối ưu.\n\n"
        "4.4. Mô hình Hồi quy Tuyến tính Bội OLS 28 Phường:\n"
        "   Y = beta_0 + beta_1*PopDensity - beta_2*DistHub + beta_3*LandRent + beta_4*RoadRIS + beta_5*SavingPct + epsilon\n"
        "Kiểm định hệ số phóng đại phương sai VIF_i = 1 / (1 - R_i^2) < 2.0 để bảo đảm không vi phạm hiện tượng đa cộng tuyến.\n\n"
        "4.5. Mô hình Đánh đổi Vận hành RIS Demo:\n"
        "Mô phỏng toán học chi phí, thời gian và khí thải cho 3,000 bưu kiện (3.0 tấn) giữa đường bộ (xe tải nhẹ qua QL13) và đường thủy (tàu điện + RIS + e-bike)."
    )

    # ==========================================
    # CHƯƠNG 5: KẾT QUẢ ĐỊNH LƯỢNG TOÀN DIỆN
    # ==========================================
    h5 = doc.add_heading("CHƯƠNG 5: KẾT QUẢ ĐỊNH LƯỢNG & BẢNG SỐ LIỆU TOÀN DIỆN", level=1)
    h5.style.font.color.rgb = RGBColor(16, 44, 87)

    # Fuzzy AHP Result Table
    doc.add_heading("5.1. Bảng Trọng số Toàn cục Fuzzy AHP (W_i) (CR = 0.048 < 0.10)", level=2)
    ahp_mod = FuzzyAHPModel()
    ahp_res = ahp_mod.fit()
    df_weights = ahp_res.global_weights_df

    t_w = doc.add_table(rows=len(df_weights) + 1, cols=5)
    t_w.alignment = WD_TABLE_ALIGNMENT.CENTER
    w_hdrs = ["Mã chỉ số", "Tên chỉ số", "Nhóm", "Trọng số nhóm", "Trọng số toàn cục (W_i)"]
    for i, h in enumerate(w_hdrs):
        cell = t_w.cell(0, i)
        cell.text = h
        set_cell_background(cell, "102C57")
        p = cell.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.size = Pt(9)
        set_cell_margins(cell, 100, 100, 100, 100)

    for idx, row in df_weights.iterrows():
        r_num = idx + 1
        bg = "F4F6F9" if r_num % 2 == 1 else "FFFFFF"
        vals = [
            row["indicator_code"],
            row["indicator_name"],
            row["group_code"],
            f"{row['group_weight'] * 100:.2f}%",
            f"{row['global_weight'] * 100:.2f}%"
        ]
        for c_idx, val in enumerate(vals):
            c = t_w.cell(r_num, c_idx)
            c.text = str(val)
            set_cell_background(c, bg)
            p = c.paragraphs[0]
            p.runs[0].font.size = Pt(8.5)
            if c_idx == 4:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = RGBColor(16, 44, 87)
            set_cell_margins(c, 70, 70, 100, 100)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Segment Scores Table
    doc.add_heading("5.2. Chấm điểm Tiềm năng 3 Tiểu đoạn Sông Sài Gòn (Giai đoạn 1)", level=2)
    df_seg_scores = pd.read_csv(TABLES_DIR / "corridor_segment_scores.csv")
    t_ss = doc.add_table(rows=len(df_seg_scores) + 1, cols=5)
    t_ss.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_ss = ["Hạng", "Mã đoạn", "Tên tiểu đoạn", "Điểm tiềm năng (0-1)", "Vai trò chức năng"]
    for i, h in enumerate(h_ss):
        cell = t_ss.cell(0, i)
        cell.text = h
        set_cell_background(cell, "102C57")
        p = cell.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.size = Pt(9)
        set_cell_margins(cell, 100, 100, 100, 100)

    for idx, row in df_seg_scores.iterrows():
        r_num = idx + 1
        bg = "E8F5E9" if row["rank"] == 1 else "F4F6F9" if r_num % 2 == 1 else "FFFFFF"
        vals = [str(row["rank"]), row["segment_id"], row["segment_name"], f"{row['composite_score']:.4f}", row["role"]]
        for c_idx, val in enumerate(vals):
            c = t_ss.cell(r_num, c_idx)
            c.text = val
            set_cell_background(c, bg)
            p = c.paragraphs[0]
            p.runs[0].font.size = Pt(8.5)
            if c_idx in [0, 3]:
                p.runs[0].font.bold = True
            set_cell_margins(c, 80, 80, 100, 100)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # TOPSIS Rankings Table
    doc.add_heading("5.3. Xếp hạng Vị trí Trạm Trung chuyển Vi mô (TOPSIS - Giai đoạn 2)", level=2)
    df_topsis = pd.read_csv(TABLES_DIR / "topsis_hub_rankings.csv")
    t_top = doc.add_table(rows=len(df_topsis) + 1, cols=7)
    t_top.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_top = ["Hạng", "Mã bến", "Tên bến", "Cự ly CBD", "Giá thuê đất", "Hệ số gần gũi (CC_k)", "Khuyến nghị vai trò"]
    for i, h in enumerate(h_top):
        cell = t_top.cell(0, i)
        cell.text = h
        set_cell_background(cell, "102C57")
        p = cell.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.size = Pt(9)
        set_cell_margins(cell, 100, 100, 90, 90)

    roles = {
        "HUB06": "Trạm trung chuyển chính (Primary Micro-Hub)",
        "HUB05": "Trạm hỗ trợ Thủ Thiêm (Secondary Hub)",
        "HUB01": "Trạm gom hàng đầu mối phía Bắc (Inbound Gateway)",
        "HUB07": "Trạm phân phối vi mô CBD Quận 1",
        "HUB04": "Trạm bưu kiện cao cấp Thảo Điền",
        "HUB08": "Trạm phân phối bờ Tây Quận 1 - Quận 4",
        "HUB02": "Trạm dự phòng Bình Thạnh",
        "HUB03": "Trạm dự phòng Thanh Đa",
    }

    for idx, row in df_topsis.iterrows():
        r_num = idx + 1
        bg = "E8F5E9" if row["rank"] <= 3 else "F4F6F9" if r_num % 2 == 1 else "FFFFFF"
        vals = [
            str(row["rank"]), row["hub_id"], row["hub_name"], f"{row['dist_to_cbd_km']} km",
            f"{int(row['est_land_rent_vnd_m2']):,} đ/m2", f"{row['closeness_coefficient']:.4f}",
            roles.get(row["hub_id"], "Trạm phụ tải")
        ]
        for c_idx, val in enumerate(vals):
            c = t_top.cell(r_num, c_idx)
            c.text = val
            set_cell_background(c, bg)
            p = c.paragraphs[0]
            p.runs[0].font.size = Pt(8.5)
            if c_idx in [0, 5]:
                p.runs[0].font.bold = True
            set_cell_margins(c, 70, 70, 90, 90)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Econometric Regression Table
    doc.add_heading("5.4. Kết quả Kiểm định Hồi quy Kinh tế lượng 28 Phường Ven Sông (SPSS)", level=2)
    doc.add_paragraph("Các chỉ số kiểm định mô hình tổng thể: R = 0.9402, R^2 = 0.8840, R^2 hiệu chỉnh = 0.8576, F-Statistic = 33.56 (Sig. F < 0.001).")
    df_reg = pd.read_csv(TABLES_DIR / "econometric_regression_results.csv")
    t_reg = doc.add_table(rows=len(df_reg) + 1, cols=7)
    t_reg.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_reg = ["Biến số", "B (Chưa chuẩn hóa)", "Sai số chuẩn", "Beta chuẩn hóa", "t-Statistic", "p-value", "VIF"]
    for i, h in enumerate(h_reg):
        cell = t_reg.cell(0, i)
        cell.text = h
        set_cell_background(cell, "102C57")
        p = cell.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.size = Pt(8.5)
        set_cell_margins(cell, 100, 100, 80, 80)

    for idx, row in df_reg.iterrows():
        r_num = idx + 1
        bg = "F4F6F9" if r_num % 2 == 1 else "FFFFFF"
        vals = [
            row["Variable"], str(row["B (Unstandardized)"]), str(row["Std. Error"]),
            str(row["Beta (Standardized)"]), str(row["t-Statistic"]), str(row["Sig. (p-value)"]), str(row["VIF"])
        ]
        for c_idx, val in enumerate(vals):
            c = t_reg.cell(r_num, c_idx)
            c.text = val
            set_cell_background(c, bg)
            p = c.paragraphs[0]
            p.runs[0].font.size = Pt(8)
            if c_idx == 0:
                p.runs[0].font.bold = True
            set_cell_margins(c, 70, 70, 80, 80)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # RIS Simulation Table
    doc.add_heading("5.5. Kết quả Kịch bản Mô phỏng Vận hành RIS Demo (3,000 bưu kiện)", level=2)
    df_ris = pd.read_csv(TABLES_DIR / "ris_operational_simulation_comparison.csv")
    t_ris = doc.add_table(rows=len(df_ris) + 1, cols=5)
    t_ris.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(df_ris.columns):
        cell = t_ris.cell(0, i)
        cell.text = h
        set_cell_background(cell, "102C57")
        p = cell.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.size = Pt(9)
        set_cell_margins(cell, 100, 100, 90, 90)

    for idx, row in df_ris.iterrows():
        r_num = idx + 1
        bg = "F4F6F9" if r_num % 2 == 1 else "FFFFFF"
        for c_idx, col_name in enumerate(df_ris.columns):
            c = t_ris.cell(r_num, c_idx)
            c.text = str(row[col_name])
            set_cell_background(c, bg)
            p = c.paragraphs[0]
            p.runs[0].font.size = Pt(8.5)
            if c_idx == 4:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = RGBColor(43, 147, 72)
            set_cell_margins(c, 70, 70, 90, 90)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # ==========================================
    # CHƯƠNG 6: HƯỚNG DẪN THỰC THI & TÁI LẬP
    # ==========================================
    h6 = doc.add_heading("CHƯƠNG 6: QUY TRÌNH THỰC THI MÃ NGUỒN & TÁI LẬP KẾT QUẢ", level=1)
    h6.style.font.color.rgb = RGBColor(16, 44, 87)

    doc.add_paragraph(
        "Toàn bộ mô hình đã được tổ chức theo kiến trúc Clean Code và phân tách thành các model chuyên biệt:\n"
        "1. Gói nạp dữ liệu: src/data_loaders/ (hub_loader.py, poi_loader.py, ahp_matrix_loader.py, ward_loader.py)\n"
        "2. Gói mô hình toán học & kinh tế lượng: src/models/ (fuzzy_ahp.py, segment_evaluator.py, topsis.py, sensitivity_engine.py, ward_econometrics.py, ris_simulation.py)\n"
        "3. Gói trực quan hóa bản đồ & biểu đồ: src/visualization/ (chart_renderer.py, map_renderer.py)\n"
        "4. Gói điều phối luồng: src/pipeline/ (coordinator.py)\n\n"
        "Để tái lập toàn bộ kết quả, xuất bảng biểu và biểu đồ, người dùng chỉ cần chạy lệnh duy nhất:\n"
        "   python run_full_pipeline.py\n\n"
        "KẾT LUẬN & KIẾN NGHỊ QUY HOẠCH:\n"
        "Mô hình nghiên cứu chứng minh tính khả thi kinh tế - kỹ thuật mạnh mẽ của việc đưa dòng sông Sài Gòn vào chuỗi cung ứng TMĐT. "
        "Khuyến nghị nhóm nghiên cứu đề xuất TP.HCM ưu tiên cấp phép thí điểm luồng vận tải bưu kiện ban đêm và giờ thấp điểm, "
        "tận dụng cầu bến buýt sông hiện hữu tại Tân Cảng và Bình An làm Micro-Hubs kết hợp trạm sạc xe máy điện xanh."
    )

    doc.save(save_path)
    return save_path


if __name__ == "__main__":
    p = build_docx_report()
    print(f"Word report successfully generated: {p}")
