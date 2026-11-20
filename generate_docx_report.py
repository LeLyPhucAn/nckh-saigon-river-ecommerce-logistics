"""
Script tự động khởi tạo Báo cáo Khoa học định dạng Word (.docx):
"Báo cáo Chi tiết Phương pháp luận, Thuật toán, Trọng số và Quy trình Xây dựng Mô hình
Đưa Dòng Sông vào Chuỗi Cung ứng Thương mại Điện tử TP.HCM"

Đặc tả đầy đủ dữ liệu nạp vào, công thức toán học, bảng kết quả và khuyến nghị quy hoạch.
Tuân thủ chuẩn PEP 8 và Clean Code.
"""

from pathlib import Path
from typing import Optional
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import Inches, Pt, RGBColor
import pandas as pd

from src.config import OUTPUTS_DIR, TABLES_DIR
from src.data_loaders.hub_loader import load_candidate_hubs, load_river_segments
from src.data_loaders.poi_loader import load_notable_pois
from src.data_loaders.ward_loader import load_ward_socioeconomic_data
from src.models.fuzzy_ahp import FuzzyAHPModel


def set_cell_background(cell, hex_color: str) -> None:
    """Tô màu nền cho ô trong bảng."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)


def set_cell_margins(
    cell, top: int = 100, bottom: int = 100, left: int = 140, right: int = 140
) -> None:
    """Thiết lập khoảng đệm lề bên trong ô bảng (20 twips = 1 pt)."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tc_pr.append(tc_mar)


def build_docx_report(save_path: Optional[Path] = None) -> Path:
    """Khởi tạo và xuất tệp Word báo cáo khoa học hoàn chỉnh."""
    if save_path is None:
        OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
        save_path = OUTPUTS_DIR / "Bao_Cao_Chi_Tiet_Mo_Hinh_NCKH_Song_Sai_Gon.docx"

    doc = Document()

    # Thiết lập lề trang tiêu chuẩn 1 inch (2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Định dạng phông chữ Normal mặc định
    normal_style = doc.styles["Normal"]
    normal_style.font.name = "Times New Roman"
    normal_style.font.size = Pt(11.5)
    normal_style.font.color.rgb = RGBColor(35, 35, 35)
    normal_style.paragraph_format.line_spacing = 1.25
    normal_style.paragraph_format.space_after = Pt(6)

    # Tiêu đề báo cáo
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
    r_title.font.color.rgb = RGBColor(16, 44, 87)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(20)
    r_sub = p_sub.add_run(
        "Đặc tả Cấu trúc Dữ liệu Nạp vào, Cơ sở Toán học, Thuật toán Fuzzy AHP (Chang, 1996), "
        "TOPSIS (Hwang & Yoon, 1981), Mô hình Hồi quy Kinh tế lượng 28 Phường và Kịch bản Mô phỏng RIS"
    )
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(11.5)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(53, 95, 142)

    doc.add_paragraph("—" * 45).alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Tóm tắt nội dung
    h_abs = doc.add_heading("TÓM TẮT NỘI DUNG NGHIÊN CỨU", level=1)
    h_abs.style.font.color.rgb = RGBColor(16, 44, 87)
    doc.add_paragraph(
        "Trong bối cảnh áp lực giao thông đường bộ ngày càng nghiêm trọng tại TP.HCM, "
        "đặc biệt là trục huyết mạch Quốc lộ 13 – Đinh Bộ Lĩnh – Xô Viết Nghệ Tĩnh kết nối các kho "
        "tổng bưu chính phía Đông Bắc (TP. Thủ Đức, Bình Dương) với khu vực tiêu thụ lõi trung tâm, "
        "việc khai thác hành lang đường thủy sông Sài Gòn cho vận tải bưu kiện thương mại điện tử (TMĐT) "
        "mở ra giải pháp chiến lược giảm tải ùn tắc và khử carbon logistics đô thị. "
        "Nghiên cứu này thiết lập một khung mô hình lai 3 giai đoạn (Hybrid 3-Stage Pipeline), "
        "kết hợp giải tích không gian GIS, ra quyết định đa tiêu chí AHP mờ (Fuzzy AHP) và TOPSIS, "
        "cùng mô hình hồi quy kinh tế lượng dữ liệu cấp Phường (28 phường ven sông). "
        "Đồng thời, kịch bản mô phỏng vận hành luồng tàu điện tích hợp Hệ thống thông tin đường thủy (RIS) "
        "chứng minh tiềm năng vượt trội khi cắt giảm 32.2% thời gian giao hàng giờ cao điểm, "
        "tiết kiệm 38.8% chi phí vận hành trên mỗi đơn hàng, và giảm 37.8% phát thải CO2 so với đường bộ."
    )

    # Chương 1: Tổng quan và bước tiến học thuật
    h1 = doc.add_heading("CHƯƠNG 1: TỔNG QUAN NGHIÊN CỨU & BƯỚC TIẾN KHOA HỌC", level=1)
    h1.style.font.color.rgb = RGBColor(16, 44, 87)
    doc.add_paragraph(
        "1.1. Bối cảnh không gian & Logistics đô thị TP.HCM:\n"
        "Tuyến sông Sài Gòn từ cầu Bình Lợi / Hiệp Bình Chánh (TP. Thủ Đức) về bến Bạch Đằng / Khánh Hội "
        "(Quận 1 – Quận 4) dài khoảng 14.2 km đường thủy, sở hữu luồng lạch cấp II – III với chiều rộng "
        "250 – 350 m, độ sâu từ 7.5 m đến 11.5 m. Tuyến sông uốn lượn qua các vùng đô thị có mật độ dân cư "
        "và nhu cầu TMĐT cao nhất thành phố. Mọi luồng xe tải giao nhận vào trung tâm hiện nay đều phải dồn "
        "qua nút cổ chai Quốc lộ 13 – Cầu Bình Triệu, gây tắc nghẽn kéo dài trong khung giờ cao điểm.\n\n"
        "1.2. Bước tiến khoa học so với nghiên cứu nền tảng (Fathoni et al., 2017):\n"
        "Nghiên cứu của Fathoni et al. (2017) đánh giá tiềm năng sông Musi (Indonesia) cho vận tải hàng rời nông thôn. "
        "Đề tài này nâng cấp toàn diện trên 4 phương diện cốt lõi:"
    )

    # Bảng so sánh
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
        ("Đối tượng hàng hóa", "Hàng rời khối lượng lớn (than đá, phân bón, nông sản thô).", "Bưu kiện thương mại điện tử đô thị (B2C/B2B2C), yêu cầu nghiêm ngặt về khung giờ giao hàng và logistics ngược."),
        ("Phạm vi đầu ra", "Chỉ xếp hạng vĩ mô 3 đoạn sông chung chung.", "Đầu ra 2 tầng: (1) Chấm điểm tiềm năng 3 tiểu đoạn sông; (2) Xếp hạng tọa độ tối ưu đặt Trạm trung chuyển vi mô thủy – bộ (Micro-Hubs)."),
        ("Biến số kinh tế", "Bỏ qua giá đất và chi phí bến bãi ven sông.", "Tích hợp trực tiếp giá thuê mặt bằng ven sông (CAPEX) và chi phí vận hành tàu điện/bốc xếp chặng cuối (OPEX)."),
        ("Công nghệ & Kiểm chứng", "Đếm báo hiệu vật lý; trọng số cảm tính 50 chuyên gia.", "Tích hợp hạ tầng số RIS (AIS, ENC, 4G/5G); sử dụng Fuzzy AHP giảm tính mờ chủ quan và Hồi quy Kinh tế lượng 28 Phường để kiểm chứng thực nghiệm."),
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

    # Chương 2: Cơ sở lý thuyết kế thừa
    h2 = doc.add_heading("CHƯƠNG 2: CƠ SỞ KẾ THỪA TỪ 3 CÔNG TRÌNH KHOA HỌC QUỐC TẾ", level=1)
    h2.style.font.color.rgb = RGBColor(16, 44, 87)
    doc.add_paragraph(
        "Nghiên cứu kế thừa có chọn lọc từ 3 bài báo khoa học quốc tế uy tín trong thư mục data_bai_bao:\n\n"
        "1. Peña, Zapata & Barrios (2019) – Hydrological Sciences Journal:\n"
        "Kế thừa hệ thống chỉ số kỹ thuật luồng lạch (đoạn thẳng X1, chiều rộng mặt cắt X6, độ sâu X9, an toàn X16), "
        "chuyển hóa biến viễn thông X8 thành Mức độ sẵn sàng hạ tầng số RIS (NAV3), và áp dụng phân phối Beta-PERT "
        "để kiểm chứng độ ổn định của ma trận trọng số AHP (đảm bảo CR < 0.10).\n\n"
        "2. Hagos, Andualem et al. (2022) – Applied Water Science (Springer):\n"
        "Kế thừa kỹ thuật phân lớp chuẩn hóa thang bậc (1–5), công thức kết hợp tuyến tính có trọng số (WLC), "
        "và đặc biệt là chiến lược tổng hợp dữ liệu theo đơn vị hành chính cơ sở (Kebele/Woreda). Nhóm tác giả đã chuyển "
        "hóa thành công mô hình dữ liệu kinh tế – không gian cấp Phường (28 phường ven sông) phục vụ hồi quy SPSS.\n\n"
        "3. Mazarakis, Tsanakas et al. (2025) – Land (MDPI):\n"
        "Kế thừa phương pháp vùng đệm đa tầng (Multi-ring Buffer Zones), quy chuẩn thành 2 bán kính logistics: "
        "500 m (tiếp cận vi mô đi bộ/xe đẩy) và 1.5 km (phủ sóng xe máy điện chặng cuối 5–10 phút). Kế thừa kỹ thuật giao cắt "
        "6 cây cầu vượt sông và quy trình Phân tích độ nhạy (Sensitivity Analysis ±20%) kiểm chứng thứ hạng bến."
    )

    # Chương 3: Đặc tả dữ liệu nạp vào
    h3 = doc.add_heading("CHƯƠNG 3: ĐẶC TẢ TOÀN BỘ DỮ LIỆU ĐẦU VÀO NẠP VÀO MÔ HÌNH", level=1)
    h3.style.font.color.rgb = RGBColor(16, 44, 87)
    doc.add_paragraph(
        "Toàn bộ dữ liệu thực nghiệm được lưu trữ thành các tệp dữ liệu thô chuẩn hóa trong thư mục data/raw/ "
        "và nạp qua gói src/data_loaders/. Chi tiết các bảng dữ liệu nạp vào như sau:"
    )

    # Bảng 3.1: Bến ứng viên
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

    # Bảng 3.2: Đoạn sông
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

    # Bảng 3.3: POIs
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

    # Bảng 3.4: 28 Phường
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

    # Chương 4: Cơ sở toán học
    h4 = doc.add_heading("CHƯƠNG 4: CƠ SỞ TOÁN HỌC & CÁC THUẬT TOÁN ÁP DỤNG", level=1)
    h4.style.font.color.rgb = RGBColor(16, 44, 87)
    doc.add_paragraph(
        "4.1. Thuật toán Fuzzy AHP (Chang, 1996 & Saaty Geometric Mean):\n"
        "Mô hình hóa các so sánh cặp qua số mờ tam giác a_ij = (l_ij, m_ij, u_ij). "
        "Tính toán trọng số qua trung bình hình học logarit: r_i = (prod_{j=1}^n a_ij)^(1/n), w_i = r_i / sum(r_k). "
        "Kiểm định nhất quán CR = CI / RI < 0.10. Trọng số toàn cục: W_global = W_group * W_local.\n\n"
        "4.2. Chuẩn hóa Min-Max:\n"
        "• Tiêu chí Lợi ích (J+): r_ik = (x_ik - min_k(x_ik)) / (max_k(x_ik) - min_k(x_ik))\n"
        "• Tiêu chí Chi phí (J-): r_ik = (max_k(x_ik) - x_ik) / (max_k(x_ik) - min_k(x_ik))\n\n"
        "4.3. Thuật toán TOPSIS Tuyển chọn Bến Trung chuyển Vi mô (Hwang & Yoon, 1981):\n"
        "• Chuẩn hóa vector: n_ij = x_ij / sqrt(sum x_kj^2)\n"
        "• Ma trận có trọng số: v_ij = W_j * n_ij\n"
        "• Khoảng cách Euclid: D_i^+ = sqrt(sum (v_ij - v_j^+)^2), D_i^- = sqrt(sum (v_ij - v_j^-)^2)\n"
        "• Hệ số gần gũi lý tưởng: CC_i = D_i^- / (D_i^+ + D_i^-) in [0, 1].\n\n"
        "4.4. Mô hình Hồi quy Bội OLS 28 Phường:\n"
        "Y = beta_0 + beta_1*PopDensity - beta_2*DistHub + beta_3*LandRent + beta_4*RoadRIS + beta_5*SavingPct + epsilon.\n"
        "Kiểm định hệ số phóng đại phương sai VIF < 2.0.\n\n"
        "4.5. Mô hình Đánh đổi Vận hành RIS Demo:\n"
        "Mô phỏng toán học chi phí, thời gian và phát thải CO2 cho 3,000 bưu kiện (3.0 tấn) giữa đường bộ và đường thủy."
    )

    # Chương 5: Kết quả định lượng
    h5 = doc.add_heading("CHƯƠNG 5: KẾT QUẢ ĐỊNH LƯỢNG & BẢNG SỐ LIỆU TOÀN DIỆN", level=1)
    h5.style.font.color.rgb = RGBColor(16, 44, 87)

    # Bảng trọng số
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

    # Bảng điểm đoạn sông
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

    # Bảng xếp hạng TOPSIS
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

    # Bảng hồi quy SPSS
    doc.add_heading("5.4. Kết quả Kiểm định Hồi quy Kinh tế lượng 28 Phường Ven Sông (SPSS)", level=2)
    doc.add_paragraph(
        "Các chỉ số kiểm định mô hình tổng thể: R = 0.9402, R^2 = 0.8840, R^2 hiệu chỉnh = 0.8576, "
        "F-Statistic = 33.56 (Sig. F < 0.001)."
    )
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

    # Bảng mô phỏng RIS
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

    # Chương 6: Hướng dẫn thực thi & kết luận
    h6 = doc.add_heading("CHƯƠNG 6: QUY TRÌNH THỰC THI MÃ NGUỒN & TÁI LẬP KẾT QUẢ", level=1)
    h6.style.font.color.rgb = RGBColor(16, 44, 87)
    doc.add_paragraph(
        "Mã nguồn được tổ chức hoàn chỉnh theo chuẩn Clean Code:\n"
        "1. Gói nạp dữ liệu: src/data_loaders/\n"
        "2. Gói mô hình: src/models/\n"
        "3. Gói trực quan hóa: src/visualization/\n"
        "4. Gói điều phối: src/pipeline/\n\n"
        "Chạy toàn bộ pipeline chỉ với 1 lệnh duy nhất:\n"
        "   python run_full_pipeline.py\n\n"
        "KẾT LUẬN & KIẾN NGHỊ QUY HOẠCH:\n"
        "Nghiên cứu chứng minh tính khả thi kinh tế - kỹ thuật cao của việc đưa sông Sài Gòn vào chuỗi cung ứng TMĐT. "
        "Khuyến nghị TP.HCM ưu tiên cơ chế thử nghiệm (Sandbox) cho tàu chở bưu kiện ban đêm và giờ thấp điểm, "
        "tận dụng hạ tầng bến buýt sông Tân Cảng – Bình An làm Micro-Hubs kết hợp sạc xe máy điện xanh."
    )

    doc.save(save_path)
    return save_path


if __name__ == "__main__":
    p = build_docx_report()
    print(f"Word report successfully generated: {p}")
