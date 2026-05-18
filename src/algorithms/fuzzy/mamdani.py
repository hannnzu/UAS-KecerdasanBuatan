"""
Module: Fuzzy Mamdani Inference System
Project: UAS Kecerdasan Buatan
Reference: Penerapan Metode Fuzzy Mamdani dalam Menentukan Harga Jual Ponsel
Skill Archetype: statistical-analyst (Precise logic, validated against numerical data)
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd
import os

class FuzzyMamdaniPricing:
    def __init__(self, membership_csv, rules_csv):
        # Define Universes (Domains) based on Journal
        self.univ_kondisi = np.arange(0, 101, 1)         # 0-100 %
        self.univ_pasar = np.arange(0, 5501, 1)         # 0-5500 (ribu)
        self.univ_kelengkapan = np.arange(0, 101, 1)    # 0-100 %
        self.univ_jual = np.arange(0, 5001, 1)          # 0-5000 (ribu)

        # Initialize Antecedents and Consequents
        self.kondisi = ctrl.Antecedent(self.univ_kondisi, 'kondisi')
        self.harga_pasar = ctrl.Antecedent(self.univ_pasar, 'harga_pasar')
        self.kelengkapan = ctrl.Antecedent(self.univ_kelengkapan, 'kelengkapan')
        self.harga_jual = ctrl.Consequent(self.univ_jual, 'harga_jual')

        # Store mapping mapping for dynamic lookups
        self.vars_map = {
            'kondisi': self.kondisi,
            'harga_pasar': self.harga_pasar,
            'kelengkapan': self.kelengkapan,
            'harga_jual': self.harga_jual
        }

        # Load components
        self._load_membership_functions(membership_csv)
        self.system_ctrl = self._build_rule_base(rules_csv)
        self.simulator = ctrl.ControlSystemSimulation(self.system_ctrl)

    def _load_membership_functions(self, csv_path):
        """Parse CSV and apply membership function formulas."""
        df = pd.read_csv(csv_path)
        
        for _, row in df.iterrows():
            var_name = row['variabel'].strip().lower()
            set_name = row['set_name'].strip().upper()
            type_mf = row['tipe'].strip().lower()
            
            # Handle the antecedent/consequent object
            target_var = self.vars_map[var_name]
            universe = target_var.universe

            # Parse params, handle nan safely
            p1 = float(row['p1']) if not pd.isna(row['p1']) else None
            p2 = float(row['p2']) if not pd.isna(row['p2']) else None
            p3 = float(row['p3']) if not pd.isna(row['p3']) else None

            # Apply appropriate scikit-fuzzy function
            if type_mf == 'shoulder_kiri':
                # 1 at start, falls to 0 at p2. represented as trapezoid: [min, min, p1, p2]
                # In the journal data, p1 is often 0.
                p_min = universe[0]
                target_var[set_name] = fuzz.trapmf(universe, [p_min, p_min, p1, p2])
            
            elif type_mf == 'triangular':
                # Standard triangle [p1, p2, p3]
                target_var[set_name] = fuzz.trimf(universe, [p1, p2, p3])
                
            elif type_mf == 'shoulder_kanan':
                # Starts climbing at p1, reaches 1 and stays until end.
                p_max = universe[-1]
                target_var[set_name] = fuzz.trapmf(universe, [p1, p2, p_max, p_max])

        print("✅ Membership functions loaded successfully.")

    def _build_rule_base(self, csv_path):
        """Dynamically construct fuzzy control rules from CSV."""
        df = pd.read_csv(csv_path)
        rules_list = []

        for _, row in df.iterrows():
            rule_id = row['rule_no']
            antecedents = []
            
            # Check Input Variables (Kondisi, Harga Pasar, Kelengkapan)
            if not pd.isna(row['kondisi']) and row['kondisi'] != "":
                antecedents.append(self.kondisi[str(row['kondisi']).strip().upper()])
            
            if not pd.isna(row['harga_pasar']) and row['harga_pasar'] != "":
                antecedents.append(self.harga_pasar[str(row['harga_pasar']).strip().upper()])
                
            if not pd.isna(row['kelengkapan']) and row['kelengkapan'] != "":
                antecedents.append(self.kelengkapan[str(row['kelengkapan']).strip().upper()])

            # Get Consequent (Output)
            consequent = self.harga_jual[str(row['harga_jual']).strip().upper()]

            # Combine antecedents using AND operator (&)
            if len(antecedents) == 1:
                final_ant = antecedents[0]
            elif len(antecedents) == 2:
                final_ant = antecedents[0] & antecedents[1]
            elif len(antecedents) == 3:
                final_ant = antecedents[0] & antecedents[1] & antecedents[2]
            else:
                print(f"⚠️ Warning: Rule {rule_id} has no antecedents, skipping.")
                continue
            
            # Create rule object
            new_rule = ctrl.Rule(final_ant, consequent, label=rule_id)
            rules_list.append(new_rule)

        print(f"✅ Loaded {len(rules_list)} fuzzy rules.")
        
        # Compile logic engine
        return ctrl.ControlSystem(rules_list)

    def compute(self, val_kondisi, val_pasar, val_lengkap):
        """Run inference simulation."""
        self.simulator.input['kondisi'] = val_kondisi
        self.simulator.input['harga_pasar'] = val_pasar
        self.simulator.input['kelengkapan'] = val_lengkap
        
        # Compute simulation (Mamandi Inference + Centroid Defuzzification)
        try:
            self.simulator.compute()
            return self.simulator.output['harga_jual']
        except Exception as e:
            print(f"Error during computation: {e}")
            return None

if __name__ == "__main__":
    # Setup paths
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    data_dir = os.path.join(base_dir, "data")
    
    mf_path = os.path.join(data_dir, "fuzzy_membership.csv")
    rules_path = os.path.join(data_dir, "fuzzy_rules.csv")
    valid_path = os.path.join(data_dir, "fuzzy_validation.csv")
    
    print("\n" + "="*60)
    print("FUZZY MAMDANI SYSTEM - STARTING ENGINE")
    print("="*60)
    
    if not os.path.exists(mf_path) or not os.path.exists(rules_path):
        print("Error: Required CSV files not found!")
    else:
        # 1. Initialize Engine
        engine = FuzzyMamdaniPricing(mf_path, rules_path)
        
        # 2. Verify with Validation Cases
        print("\n" + "-"*60)
        print("RUNNING VALIDATION AGAINST JOURNAL DATA (MATLAB)")
        print("-"*60)
        
        if os.path.exists(valid_path):
            val_df = pd.read_csv(valid_path)
            for idx, row in val_df.iterrows():
                knd = row['kondisi_pct']
                psr = row['harga_pasar_ribu']
                lkp = row['kelengkapan_pct']
                exp = row['expected_harga_jual_ribu']
                desc = row['keterangan']
                
                print(f"\n▶️ Test Case {idx+1}: {desc}")
                print(f"   Inputs: Kondisi={knd}%, Harga Pasar=Rp.{psr*1000:,.0f}, Kelengkapan={lkp}%")
                
                result = engine.compute(knd, psr, lkp)
                
                if result is not None:
                    print(f"   🎯 System Output : Rp.{result*1000:,.2f}")
                    print(f"   📊 Jurnal Target : Rp.{exp*1000:,.2f}")
                    
                    # Hitung margin error (biasanya ada sedikit perbedaan tipis karena presisi pembulatan decimal/integer centroid)
                    diff = abs(result - exp)
                    print(f"   📈 Difference    : {diff:.2f} (K-Rupiah)")
                else:
                     print("   ❌ Calculation Failed.")
        
        print("\n" + "="*60)
        print("VALIDATION RUN FINISHED")
        print("="*60 + "\n")
