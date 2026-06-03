"""
Application: Dashboard UAS Kecerdasan Buatan
Logic Stack: Greedy Best First Search & Fuzzy Mamdani
GUI Stack: PyQt6
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
    QLabel, QComboBox, QPushButton, QTextEdit, 
    QSpinBox, QFormLayout, QGroupBox, QFrame, QMessageBox, QScrollArea,
    QDoubleSpinBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPalette

# Import Logika Backend yang sudah kita buat
try:
    from src.algorithms.fuzzy.mamdani import FuzzyMamdaniPricing
except ImportError:
    print("⚠️ Mencoba import fallback...")
    # Fallback jika dipanggil dari dalam folder src
    sys.path.append(str(Path(__file__).resolve().parent))
    from algorithms.fuzzy.mamdani import FuzzyMamdaniPricing

# Tentukan Path Data
DATA_DIR = os.path.join(BASE_DIR, "data")
FUZZY_MF = os.path.join(DATA_DIR, "fuzzy_membership.csv")
FUZZY_RULES = os.path.join(DATA_DIR, "fuzzy_rules.csv")

class ModernUASApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard Inteligensi Buatan - UAS Program")
        self.resize(800, 500)
        self.setStyleSheet(self._get_modern_style())
        
        # Data Inisialisasi
        self.load_engines()
        
        # Main Widget & Layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        self.setCentralWidget(main_widget)
        
        # Header Title
        header = QLabel("UAS KECERDASAN BUATAN")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setFont(QFont("Montserrat", 20, QFont.Weight.Bold))
        header.setStyleSheet("color: #2c3e50; margin-bottom: 5px; letter-spacing: 2px;")
        main_layout.addWidget(header)
        
        subtitle = QLabel("Implementasi Jurnal Fuzzy Mamdani (Estimasi Harga Jual HP)")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #7f8c8d; font-size: 12px; margin-bottom: 15px;")
        main_layout.addWidget(subtitle)

        # Init Fuzzy UI
        fuzzy_widget = self.init_fuzzy_ui()
        main_layout.addWidget(fuzzy_widget)

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
            for f in [FUZZY_MF, FUZZY_RULES]:
                if not os.path.exists(f):
                    raise FileNotFoundError(f"File data tidak ditemukan: {f}")
            
            # Load Fuzzy Backend
            self.fuzzy_engine = FuzzyMamdaniPricing(FUZZY_MF, FUZZY_RULES)
            print("✅ Mesin logika Fuzzy Mamdani berhasil dimuat.")
            
        except Exception as e:
            QMessageBox.critical(self, "Error Kritis", f"Gagal memuat data algoritma:\n{str(e)}")
            sys.exit(1)

    def init_fuzzy_ui(self):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # --- SISI KIRI: Parameter HP ---
        left_panel = QWidget()
        left_vbox = QVBoxLayout(left_panel)
        left_vbox.setContentsMargins(0, 0, 0, 0)
        
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
        self.sp_pasar.setRange(0.0, 5.0)
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
        
        return container

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
