# UAS Kecerdasan Buatan

> Implementasi ulang dua metode kecerdasan buatan dari jurnal ilmiah sebagai pemenuhan Tugas Akhir Semester 4 Program Studi D4 TRPL.

## 📖 Deskripsi Proyek

Proyek ini adalah implementasi dari dua jurnal ilmiah menggunakan ekosistem Python dan PyQt6. Bertujuan untuk mensimulasikan sistem kecerdasan buatan dari teori menjadi aplikasi desktop nyata.

### 1. Greedy Best First Search (GBFS)
**Jurnal:** *Implementasi Penggunaan Algoritma Greedy Best First Search untuk Menentukan Rute Terpendek dari Cilacap ke Yogyakarta*
- **Karakteristik:** Pencarian rute pada peta (Graph) yang terdiri dari 83 node kecamatan/lokasi.
- **Evaluasi Heuristik:** Memilih node selanjutnya secara eksklusif menggunakan `f(n) = h'(n)` tanpa mempertimbangkan *cost* masa lalu.
- **Mekanisme:** Iterasi state dengan pengelolaan **OPEN List** dan **CLOSED List**.
- **Validasi Target:** Menemukan rute berjarak total **345.8 km**.

### 2. Logika Fuzzy (Metode Mamdani)
**Jurnal:** *Penerapan Metode Fuzzy Mamdani dalam Menentukan Harga Jual Ponsel Pintar Bekas (Studi Kasus: Kayyis Cellular Depok)*
- **Variabel Input:** Kondisi fisik (%), Harga Pasar (Rupiah), Kelengkapan aksesoris (%).
- **Variabel Output:** Harga Jual (Rupiah).
- **Proses Inferensi:** Fuzzifikasi (Kurva Shoulder/Triangular) → Rule Evaluation (MIN) → Komposisi (MAX) → Defuzzifikasi (Centroid / Center of Gravity).
- **Validasi Target:** Output yang presisi dan sesuai dengan tabel referensi jurnal.

---

## 🛠️ Teknologi & Stack

Aplikasi ini dikembangkan dengan *clean code guidelines* dan arsitektur modular (Separation of Concerns).

- **Core & Logic:** Python 3.10+
- **Desktop UI Framework:** PyQt6
- **Data & Scientific Computation:** NumPy, Pandas, scikit-fuzzy
- **Data Visualization:** Matplotlib

---

## 📂 Struktur Direktori

```text
UAS/
├── data/               # Kumpulan dataset (Graph, tabel Heuristik, Data ponsel)
├── docs/               # PDF Jurnal Referensi
├── src/                # Source Code utama
│   ├── algorithms/     # Implementasi core algoritma
│   │   ├── greedy/     # GBFS: graph.py, heuristic.py, gbfs.py
│   │   └── fuzzy/      # Mamdani: membership.py, rules.py, mamdani.py
│   └── shared/
│       └── utils/      # Helper & GUI utilities
├── tests/              # Unit Test (Validasi Algoritma)
└── requirements.txt    # Daftar dependensi library
```

---

## 🚀 Panduan Instalasi dan Penggunaan

1. **Clone repositori proyek ini**
   ```bash
   git clone https://github.com/hannnzu/UAS-KecerdasanBuatan.git
   cd UAS-KecerdasanBuatan
   ```

2. **Buat Virtual Environment & Install Dependensi**
   Sangat disarankan menggunakan virtual environment agar library tidak konflik.
   ```bash
   # Pembuatan Virtual Environment
   python -m venv venv
   
   # Aktivasi (Windows)
   venv\Scripts\activate
   # Aktivasi (Linux/Mac)
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Menjalankan Unit Test (Validasi Code Reviewer)**
   Pastikan seluruh logika dasar sudah valid (Sesuai output Jurnal) sebelum menjalankan GUI.
   ```bash
   pytest tests/
   ```

4. **Jalankan Aplikasi GUI**
   ```bash
   python src/main.py
   ```

---
