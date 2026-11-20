"""
Tệp điều phối chính: Thực thi toàn bộ mô hình nghiên cứu NCKH sông Sài Gòn.
Quy trình thực hiện:
1. Nạp và kiểm tra dữ liệu đầu vào (data/raw/)
2. Giải tích không gian GIS & vùng đệm đa tầng (Ngày 1)
3. Tính toán trọng số toàn cục Fuzzy AHP (Chang 1996)
4. Chấm điểm tiềm năng 3 tiểu đoạn sông (Min-Max WLC)
5. Xếp hạng 8 trạm Micro-Hubs bằng TOPSIS (Hwang & Yoon 1981)
6. Phân tích độ nhạy biến động trọng số chi phí (Mazarakis et al. 2025)
7. Hồi quy kinh tế lượng 28 phường ven sông & xuất cú pháp SPSS (.sps)
8. Mô phỏng luồng vận hành RIS (3.000 bưu kiện vs xe tải đường bộ)
9. Xuất 7 biểu đồ khoa học 300 DPI & Tệp báo cáo Word hoàn chỉnh (.docx)

Cách chạy:
    python run_full_pipeline.py
"""

import sys
from pathlib import Path

# Thêm đường dẫn gốc vào sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate_docx_report import build_docx_report
from src.pipeline.coordinator import run_full_pipeline_workflow


def main() -> None:
    """Hàm chính điều phối toàn bộ quy trình nghiên cứu."""
    print("=" * 80)
    print("🚀 BẮT ĐẦU CHẠY TOÀN BỘ MÔ HÌNH NCKH: ĐƯA DÒNG SÔNG VÀO CHUỖI CUNG ỨNG TMĐT TP.HCM")
    print("   (Kiến trúc Clean Code - Mô đun hóa Data Loaders, Models, Visualizers)")
    print("=" * 80)

    # Chạy toàn bộ các giai đoạn nghiên cứu
    run_full_pipeline_workflow()

    print("\n" + "-" * 80)
    print("📄 ĐANG KHỞI TẠO BÁO CÁO KHOA HỌC ĐẶC TẢ CHI TIẾT ĐỊNH DẠNG WORD (.DOCX)...")
    doc_path = build_docx_report()
    print(f"  ✓ Tệp Word hoàn chỉnh đã được tạo tại: {doc_path}")

    # Đếm số lượng tệp kết quả
    csv_count = len(list(Path("outputs/tables").glob("*.csv")))
    png_count = len(list(Path("outputs/charts").glob("*.png")))

    print("\n" + "=" * 80)
    print("🎉 TOÀN BỘ QUY TRÌNH NGHIÊN CỨU ĐÃ THỰC THI HOÀN HẢO 100%!")
    print(f"📁 Tệp Word Báo cáo Khoa học: {doc_path.name}")
    print(f"📊 Bảng dữ liệu đầu ra: {csv_count} tệp CSV")
    print(f"📈 Biểu đồ trực quan hóa: {png_count} tệp PNG (300 DPI)")
    print("🗺️  Bản đồ Cartography GIS: outputs/maps/saigon_river_corridor_day1.png")
    print("💻 Dữ liệu & Cú pháp SPSS: spss_models/spss_ward_data.csv & regression_syntax.sps")
    print("=" * 80)


if __name__ == "__main__":
    main()
