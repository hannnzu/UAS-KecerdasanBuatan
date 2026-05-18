"""
Application: Dashboard UAS Kecerdasan Buatan
Logic Stack: Greedy Best First Search & Fuzzy Mamdani
GUI Stack: PyQt6
Created dynamically via Antigravity Coding Assistant
"""

import sys
import os
from pathlib import Path

# Fix imports: Add root project path to sys.path to prevent import errors
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTabWidget, QLabel, QComboBox, QPushButton, QTextEdit, 
    QSpinBox, QFormLayout, QGroupBox, QFrame, QMessageBox, QScrollArea,
    QDoubleSpinBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPalette

# Import Logika Backend yang sudah kita buat
try:
    from src.algorithms.greedy.gbfs import GBFSSolver
    from src.algorithms.fuzzy.mamdani import FuzzyMamdaniPricing
except ImportError:
    print("⚠️ Mencoba import fallback...")
    # Fallback jika dipanggil dari dalam folder src
    sys.path.append(str(Path(__file__).resolve().parent))
    from algorithms.greedy.gbfs import GBFSSolver
    from algorithms.fuzzy.mamdani import FuzzyMamdaniPricing

# Tentukan Path Data
DATA_DIR = os.path.join(BASE_DIR, "data")
GREEDY_H = os.path.join(DATA_DIR, "node_heuristik.csv")
GREEDY_ADJ = os.path.join(DATA_DIR, "adjacency_list.csv")
FUZZY_MF = os.path.join(DATA_DIR, "fuzzy_membership.csv")
FUZZY_RULES = os.path.join(DATA_DIR, "fuzzy_rules.csv")

class ModernUASApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard Inteligensi Buatan - UAS Program")
        self.resize(900, 650)
        self.setStyleSheet(self._get_modern_style())
        
        # Data Inisialisasi
        self.load_engines()
        
        # Main Widget & Layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        self.setCentralWidget(main_widget)
        
        # Header Title
        header = QLabel("UAS KECERDASAN BUATAN")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setFont(QFont("Montserrat", 20, QFont.Weight.Bold))
        header.setStyleSheet("color: #2c3e50; margin-bottom: 5px; letter-spacing: 2px;")
        main_layout.addWidget(header)
        
        subtitle = QLabel("Implementasi Jurnal Greedy & Fuzzy Mamdani")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #7f8c8d; font-size: 12px; margin-bottom: 15px;")
        main_layout.addWidget(subtitle)

        # Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabBar::tab { height: 40px; width: 300px; font-size: 14px; font-weight: bold; }")
        
        # Init Tabs
        self.init_tab_greedy()
        self.init_tab_fuzzy()
        
        main_layout.addWidget(self.tabs)

    def _get_modern_style(self):
        return """
            QMainWindow { background-color: #ecf0f1; }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                margin-top: 15px;
                padding: 10px;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 15px;
                padding: 0 5px;
                color: #2980b9;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2980b9; }
            QPushButton#btn_calculate {
                background-color: #27ae60;
                font-size: 14px;
                min-height: 35px;
            }
            QPushButton#btn_calculate:hover { background-color: #2ecc71; }
            QComboBox, QSpinBox, QDoubleSpinBox {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
            }
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                background-color: #fdfdfd;
                font-family: 'Courier New';
                font-size: 12px;
            }
        """

    def load_engines(self):
        """Memuat data csv dan menyalakan backend logic"""
        try:
            # Cek ketersediaan file
            for f in [GREEDY_H, GREEDY_ADJ, FUZZY_MF, FUZZY_RULES]:
                if not os.path.exists(f):
                    raise FileNotFoundError(f"File data tidak ditemukan: {f}")

            # Load Greedy Backend
            self.greedy_solver = GBFSSolver(GREEDY_H, GREEDY_ADJ)
            
            # Load Fuzzy Backend
            self.fuzzy_engine = FuzzyMamdaniPricing(FUZZY_MF, FUZZY_RULES)
            print("✅ Seluruh mesin kecerdasan buatan berhasil dimuat.")
            
        except Exception as e:
            QMessageBox.critical(self, "Error Kritis", f"Gagal memuat data algoritma:\n{str(e)}")
            sys.exit(1)

    def init_tab_greedy(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        
        # --- SISI KIRI: Input Control ---
        left_panel = QWidget()
        left_vbox = QVBoxLayout(left_panel)
        
        group_input = QGroupBox("Konfigurasi Navigasi")
        form = QFormLayout(group_input)
        form.setSpacing(15)
        
        self.cb_start = QComboBox()
        self.cb_dest = QComboBox()
        
        # Isi combo box dengan Nama Lokasi yang diambil dari backend
        # Mengurutkan berdasarkan key ID node
        sorted_nodes = sorted(self.greedy_solver.node_info.items())
        for node_id, info in sorted_nodes:
            text = f"{node_id} - {info['nama']}"
            self.cb_start.addItem(text, node_id)
            self.cb_dest.addItem(text, node_id)
            
        # Set Default: Start 1 (Kesugihan), Goal 83 (Yogyakarta)
        index_start = self.cb_start.findData(1)
        index_dest = self.cb_dest.findData(83)
        if index_start != -1: self.cb_start.setCurrentIndex(index_start)
        if index_dest != -1: self.cb_dest.setCurrentIndex(index_dest)

        form.addRow("📍 Lokasi Asal:", self.cb_start)
        form.addRow("🏁 Lokasi Tujuan:", self.cb_dest)
        
        btn_find = QPushButton("Cari Rute Terpendek (GBFS)")
        btn_find.setObjectName("btn_calculate")
        btn_find.clicked.connect(self.run_greedy)
        form.addRow("", btn_find)
        
        left_vbox.addWidget(group_input)
        
        # Info Info Metodologi
        info_box = QGroupBox("Metodologi Jurnal")
        info_txt = QLabel(
            "Metode: Greedy Best First Search\n"
            "Kriteria Seleksi: Nilai Heuristik terkecil.\n"
            "Rumus: f(n) = h'(n)\n"
            "Keterangan: Mencari rute terpendek Cilacap ke Yogyakarta."
        )
        info_txt.setWordWrap(True)
        vbox_info = QVBoxLayout(info_box)
        vbox_info.addWidget(info_txt)
        left_vbox.addWidget(info_box)
        left_vbox.addStretch()
        
        # --- SISI KANAN: Output Window ---
        right_panel = QWidget()
        right_vbox = QVBoxLayout(right_panel)
        
        lbl_out = QLabel("🔍 Log Perjalanan / Jalur Ditemukan:")
        lbl_out.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        self.txt_output_greedy = QTextEdit()
        self.txt_output_greedy.setReadOnly(True)
        self.txt_output_greedy.setPlaceholderText("Klik tombol Cari Rute untuk memulai kalkulasi...")
        
        right_vbox.addWidget(lbl_out)
        right_vbox.addWidget(self.txt_output_greedy)
        
        # Add to layout splitter (40% control, 60% output)
        layout.addWidget(left_panel, 40)
        layout.addWidget(right_panel, 60)
        
        self.tabs.addTab(tab, "🗺️ RUTE GREEDY")

    def init_tab_fuzzy(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        
        # --- SISI KIRI: Parameter HP ---
        left_panel = QWidget()
        left_vbox = QVBoxLayout(left_panel)
        
        group_params = QGroupBox("Spesifikasi Ponsel Pintar Bekas")
        form = QFormLayout(group_params)
        form.setVerticalSpacing(20)
        
        # Input 1: Kondisi %
        self.sp_kondisi = QSpinBox()
        self.sp_kondisi.setRange(0, 100)
        self.sp_kondisi.setValue(90)
        self.sp_kondisi.setSuffix(" %")
        
        # Input 2: Harga Pasar (Dalam Jutaan agar user interface bagus, tapi konversi ke Ribuan di backend)
        self.sp_pasar = QDoubleSpinBox()
        self.sp_pasar.setRange(0.0, 5.5)
        self.sp_pasar.setSingleStep(0.1)
        self.sp_pasar.setValue(4.5)
        self.sp_pasar.setPrefix("Rp. ")
        self.sp_pasar.setSuffix(" Juta")
        
        # Input 3: Kelengkapan %
        self.sp_lengkap = QSpinBox()
        self.sp_lengkap.setRange(0, 100)
        self.sp_lengkap.setValue(100)
        self.sp_lengkap.setSuffix(" %")
        
        form.addRow("📱 Fisik & Kondisi:", self.sp_kondisi)
        form.addRow("🏪 Tren Harga Pasar:", self.sp_pasar)
        form.addRow("📦 Kelengkapan Aksesori:", self.sp_lengkap)
        
        btn_calc = QPushButton("📊 Hitung Prediksi Harga")
        btn_calc.setObjectName("btn_calculate")
        btn_calc.clicked.connect(self.run_fuzzy)
        form.addRow("", btn_calc)
        
        left_vbox.addWidget(group_params)
        
        # Info Rules
        rules_info = QLabel("Inferensi menggunakan metode Mamdani (Min-Max) dengan Defuzzifikasi Centroid sesuai studi kasus Kayyis Cellular Depok.")
        rules_info.setWordWrap(True)
        rules_info.setStyleSheet("color: gray; font-style: italic; font-size: 11px; margin-top: 10px;")
        left_vbox.addWidget(rules_info)
        left_vbox.addStretch()
        
        # --- SISI KANAN: Panel Hasil Mencolok ---
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #bdc3c7;")
        right_vbox = QVBoxLayout(right_panel)
        right_vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        lbl_res = QLabel("ESTIMASI HARGA JUAL TERBAIK")
        lbl_res.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        lbl_res.setStyleSheet("color: #7f8c8d;")
        lbl_res.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.lbl_fuzzy_price = QLabel("Rp 0")
        self.lbl_fuzzy_price.setFont(QFont("Impact", 36))
        self.lbl_fuzzy_price.setStyleSheet("color: #27ae60; margin: 20px 0;")
        self.lbl_fuzzy_price.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.lbl_fuzzy_details = QLabel("- Siap menerima input data -")
        self.lbl_fuzzy_details.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_fuzzy_details.setStyleSheet("color: #34495e; font-size: 13px;")
        
        right_vbox.addStretch()
        right_vbox.addWidget(lbl_res)
        right_vbox.addWidget(self.lbl_fuzzy_price)
        right_vbox.addWidget(self.lbl_fuzzy_details)
        right_vbox.addStretch()
        
        layout.addWidget(left_panel, 45)
        layout.addWidget(right_panel, 55)
        
        self.tabs.addTab(tab, "💰 KALKULATOR HARGA FUZZY")

    # ================= ACTORS / CONTROLLERS =================
    
    def run_greedy(self):
        start_id = self.cb_start.currentData()
        dest_id = self.cb_dest.currentData()
        
        start_name = self.greedy_solver.node_info[start_id]['nama']
        dest_name = self.greedy_solver.node_info[dest_id]['nama']
        
        self.txt_output_greedy.clear()
        self.txt_output_greedy.append(f"=== MEMULAI PENCARIAN GREEDY ===")
        self.txt_output_greedy.append(f"Start: {start_name}")
        self.txt_output_greedy.append(f"Target: {dest_name}\n")
        
        # Capture terminal logic output (simulated here into txt area)
        result = self.greedy_solver.solve(start_id, dest_id)
        
        if result:
            path = result['path']
            self.txt_output_greedy.append("-" * 40)
            self.txt_output_greedy.append(f"✅ RUTE DITEMUKAN!")
            self.txt_output_greedy.append(f"Dilewati {len(path)} Titik Perjalanan.\n")
            
            for idx, node in enumerate(path):
                name = self.greedy_solver.node_info[node]['nama']
                pref = "📍 [Mulai] " if idx == 0 else "🏁 [Tujuan]" if idx == len(path)-1 else f"   ➤ "
                self.txt_output_greedy.append(f"{pref} Node {node}: {name}")
            
            # Formatting final string chain
            self.txt_output_greedy.append("\nURUTAN NODE CHAIN:")
            self.txt_output_greedy.append(" -> ".join(map(str, path)))
        else:
            self.txt_output_greedy.append("\n❌ MAAF, JALUR TIDAK DITEMUKAN DI DATA GRAF.")

    def run_fuzzy(self):
        try:
            # Ambil nilai input
            kondisi = self.sp_kondisi.value()
            
            # Ubah kembali dari skala Jutaan visual ke skala Ribuan backend (4.5 Juta -> 4500 Ribu)
            harga_pasar_ribu = int(self.sp_pasar.value() * 1000)
            
            kelengkapan = self.sp_lengkap.value()
            
            # Hitung di Backend
            res_ribu = self.fuzzy_engine.compute(kondisi, harga_pasar_ribu, kelengkapan)
            
            if res_ribu is not None:
                # Tampilkan dengan formatting rupiah yang indah
                final_price = res_ribu * 1000
                self.lbl_fuzzy_price.setText(f"Rp {final_price:,.0f}")
                self.lbl_fuzzy_details.setText(
                    f"Input Diterima:\n"
                    f"• Kondisi: {kondisi}%\n"
                    f"• Pasar: Rp {harga_pasar_ribu*1000:,.0f}\n"
                    f"• Kelengkapan: {kelengkapan}%"
                )
            else:
                self.lbl_fuzzy_price.setText("Error")
                self.lbl_fuzzy_details.setText("Perhitungan gagal diproses oleh engine.")
                
        except Exception as e:
             QMessageBox.warning(self, "Kalkulasi Gagal", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set modern look & feel for overall app
    app.setStyle("Fusion")
    
    window = ModernUASApp()
    window.show()
    sys.exit(app.exec())
