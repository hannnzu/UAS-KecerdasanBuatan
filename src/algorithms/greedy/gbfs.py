"""
Module: Greedy Best First Search (GBFS) Implementation
Project: UAS Kecerdasan Buatan
Reference: Implementasi Penggunaan Algoritma Greedy Best First Search (Jurnal)
Skill Archetype: karpathy-coder (Clean, functional, directly solves the problem)
"""

import pandas as pd
import os
import heapq

class GBFSSolver:
    def __init__(self, heuristic_path, adjacency_path):
        """
        Inisialisasi solver dengan me-load data dari CSV.
        """
        self.node_info = {}  # {node_id: {'nama': str, 'h': float}}
        self.graph = {}      # {node_id: [neighbor_ids]}
        
        self._load_data(heuristic_path, adjacency_path)

    def _load_data(self, h_path, adj_path):
        """Internal loader parsing CSV ke struktur python."""
        # 1. Load Heuristik & Nama
        df_h = pd.read_csv(h_path)
        for _, row in df_h.iterrows():
            node_id = int(row['Node'])
            self.node_info[node_id] = {
                'nama': row['Nama_Lokasi'],
                'h': float(row['Heuristik'])
            }
            # Inisialisasi node di graph
            if node_id not in self.graph:
                self.graph[node_id] = []

        # 2. Load Adjacency List (Graf dua arah/bidirectional biasanya, tapi kita asumsikan sesuai list)
        df_adj = pd.read_csv(adj_path)
        for _, row in df_adj.iterrows():
            u = int(row['Node_Asal'])
            v = int(row['Node_Tujuan'])
            
            if u not in self.graph: self.graph[u] = []
            if v not in self.graph: self.graph[v] = []
            
            # Tambahkan koneksi (asumsi graf berarah searah rute di jurnal, atau buat bidirectional untuk safety)
            self.graph[u].append(v)
            # Jika jurnal menyiratkan navigasi dua arah, uncomment baris di bawah:
            # self.graph[v].append(u)

    def solve(self, start_node, goal_node):
        """
        Mencari rute menggunakan Greedy Best First Search (f(n) = h'(n)).
        """
        print(f"\n{'='*50}")
        print(f"MEMULAI GBFS SEARCH: Node {start_node} -> Node {goal_node}")
        print(f"{'='*50}")

        # OPEN list: berisi (nilai_heuristik, current_node, path_so_far)
        # Kita gunakan heapq (priority queue) agar otomatis memilih nilai terkecil
        initial_h = self.node_info[start_node]['h']
        open_list = [(initial_h, start_node, [start_node])]
        
        # CLOSED list: untuk mencatat node yang sudah dieksekusi/dikunjungi
        closed_list = set()
        
        step = 0

        while open_list:
            step += 1
            # 1. Pilih node dengan f(n) = h'(n) terkecil dari OPEN
            current_f, current_node, path = heapq.heappop(open_list)
            
            node_name = self.node_info[current_node]['nama']
            print(f"[Langkah {step}] Memproses Node: {current_node} ({node_name}) | f(n)=h'(n)={current_f}")

            # Cek apakah sampai tujuan
            if current_node == goal_node:
                print("\n✅ GOAL REACHED!")
                return {
                    'path': path,
                    'steps': step,
                    'closed': list(closed_list)
                }

            # Masukkan ke CLOSED
            closed_list.add(current_node)

            # 2. Ekspansi tetangga (Generate Successors)
            neighbors = self.graph.get(current_node, [])
            print(f"   └─ Mengecek tetangga: {neighbors}")

            # Filter tetangga yang valid (belum ada di CLOSED)
            found_successor = False
            for neighbor in neighbors:
                if neighbor not in closed_list:
                    neighbor_h = self.node_info[neighbor]['h']
                    new_path = path + [neighbor]
                    # Push ke OPEN
                    heapq.heappush(open_list, (neighbor_h, neighbor, new_path))
                    print(f"      -> Node {neighbor} ({self.node_info[neighbor]['nama']}) ditambahkan ke OPEN dengan h={neighbor_h}")
                    found_successor = True
            
            if not found_successor and not open_list:
                 print(f"   ❌ Dead end reached di node {current_node} dan tidak ada kandidat di OPEN.")

        print("\n❌ Pencarian selesai: Jalur tidak ditemukan.")
        return None

    def display_result(self, result):
        """Mencetak output yang user-friendly."""
        if not result:
            return
        
        path = result['path']
        print(f"\n{'='*50}")
        print("HASIL RUTE FINAL (URUTAN PERJALANAN)")
        print(f"{'='*50}")
        
        for i, node in enumerate(path):
            name = self.node_info[node]['nama']
            symbol = "🏁" if i == len(path) - 1 else "📍" if i == 0 else "➡️"
            print(f"{symbol} [{node}] {name}")
            
        print("-" * 50)
        print(f"Total Node Dilewati: {len(path)}")
        print(f"Urutan Node: {' -> '.join(map(str, path))}")
        print(f"{'='*50}\n")

if __name__ == "__main__":
    # Setup file paths (menghindari error cwd)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    data_dir = os.path.join(base_dir, "data")
    
    h_path = os.path.join(data_dir, "node_heuristik.csv")
    adj_path = os.path.join(data_dir, "adjacency_list.csv")
    
    print(f"Mencari data di: {data_dir}...")
    
    if not os.path.exists(h_path) or not os.path.exists(adj_path):
        print("Error: File CSV tidak ditemukan! Pastikan berada di direktori root project.")
    else:
        # Jalankan Solver
        solver = GBFSSolver(h_path, adj_path)
        
        # Target Jurnal: Start=1 (Kesugihan), End=83 (Yogyakarta)
        result = solver.solve(start_node=1, goal_node=83)
        
        # Tampilkan Visualisasi Hasil
        solver.display_result(result)
