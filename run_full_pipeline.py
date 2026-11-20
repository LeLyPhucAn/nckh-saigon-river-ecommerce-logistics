"""
Master Execution Pipeline: Runs the entire Saigon River E-commerce Logistics model.
Orchestrates:
1. Clean Data Loaders (data/raw/)
2. GIS Spatial Buffers & Feature Extraction (Day 1)
3. Fuzzy AHP Global Weight Synthesis (Chang 1996)
4. Corridor Segment Evaluation (Min-Max WLC)
5. TOPSIS Micro-Hub Site Selection (Hwang & Yoon 1981)
6. Sensitivity Analysis (Mazarakis et al. 2025)
7. Ward-Level Spatial Econometrics & SPSS Syntax Generation
8. RIS Multimodal Operational Simulation Demo
9. High-Resolution Visualizations (300 DPI) & Word Monograph (.docx)

Usage:
    python run_full_pipeline.py
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.pipeline.coordinator import run_full_pipeline_workflow
from generate_docx_report import build_docx_report


def main():
    print("=" * 80)
    print("🚀 BẮT ĐẦU CHẠY TOÀN BỘ MÔ HÌNH NCKH: ĐƯA DÒNG SÔNG VÀO CHUỖI CUNG ỨNG TMĐT TP.HCM")
    print("   (Kiến trúc Clean Code - Mô đun hóa Data Loaders, Models, Visualizers)")
    print("=" * 80)

    # 1. Run pipeline workflow
    artifacts = run_full_pipeline_workflow()

    print("\n" + "-" * 80)
    print("📄 ĐANG KHỞI TẠO BÁO CÁO KHOA HỌC ĐẶC TẢ CHI TIẾT ĐỊNH DẠNG WORD (.DOCX)...")
    doc_path = build_docx_report()
    print(f"  ✓ Tệp Word hoàn chỉnh đã được tạo tại: {doc_path}")

    print("\n" + "=" * 80)
    print("🎉 TOÀN BỘ QUY TRÌNH NGHIÊN CỨU ĐÃ THỰC THI HOÀN HẢO 100%!")
    print(f"📁 Tệp Word Báo cáo Khoa học: {doc_path.name}")
    print(f"📊 Bảng dữ liệu đầu ra: {len(list(Path('outputs/tables').glob('*.csv')))} tệp CSV")
    print(f"📈 Biểu đồ trực quan hóa: {len(list(Path('outputs/charts').glob('*.png')))} tệp PNG (300 DPI)")
    print(f"🗺️  Bản đồ Cartography GIS: outputs/maps/saigon_river_corridor_day1.png")
    print(f"💻 Dữ liệu & Cú pháp SPSS: spss_models/spss_ward_data.csv & regression_syntax.sps")
    print("=" * 80)


if __name__ == "__main__":
    main()
