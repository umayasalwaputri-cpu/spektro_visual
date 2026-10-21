import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

class UVVisSimulasiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulasi & Kalkulator Spektrofotometer UV-Vis Shimadzu UV-1800")
        self.root.geometry("1000x680")
        
        # Header Judul
        title_label = tk.Label(root, text="SIMULASI INTERAKTIF & KALKULATOR DATA UV-VIS", font=("Arial", 14, "bold"), fg="darkblue")
        title_label.pack(pady=10)
        
        # Frame Utama (Dibagi 2 Sisi: Kiri untuk Input & Hasil, Kanan untuk Penjelasan Alat & Alur Data)
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ==================== PANEL KIRI: INPUT & KALKULATOR ====================
        left_frame = tk.LabelFrame(main_frame, text=" Komputer Data (Input & Kalkulator) ", font=("Arial", 11, "bold"))
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        tk.Label(left_frame, text="Konsentrasi Standar (pisahkan dengan koma):", anchor="w").pack(fill="x", padx=5, pady=2)
        self.entry_kons = tk.Entry(left_frame, width=45)
        self.entry_kons.pack(padx=5, pady=2)
        self.entry_kons.insert(0, "0, 2, 4, 6, 8, 10")
        
        tk.Label(left_frame, text="Absorbansi Standar (pisahkan dengan koma):", anchor="w").pack(fill="x", padx=5, pady=2)
        self.entry_abs_std = tk.Entry(left_frame, width=45)
        self.entry_abs_std.pack(padx=5, pady=2)
        self.entry_abs_std.insert(0, "0, 0.15, 0.31, 0.46, 0.61, 0.77")
        
        tk.Label(left_frame, text="Absorbansi Sampel Tak Dikenal (pisahkan koma):", anchor="w").pack(fill="x", padx=5, pady=2)
        self.entry_abs_samp = tk.Entry(left_frame, width=45)
        self.entry_abs_samp.pack(padx=5, pady=2)
        self.entry_abs_samp.insert(0, "0.40, 0.60")
        
        btn_hitung = tk.Button(left_frame, text="Hitung Regresi & Tampilkan Kurva", bg="#28a745", fg="white", font=("Arial", 10, "bold"), command=self.hitung_dan_plot)
        btn_hitung.pack(pady=10)
        
        tk.Label(left_frame, text="Hasil Analisis:", font=("Arial", 10, "bold"), anchor="w").pack(fill="x", padx=5, pady=2)
        self.text_hasil = tk.Text(left_frame, height=13, width=48, font=("Consolas", 9))
        self.text_hasil.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        # ==================== PANEL KANAN: BAGIAN DALAM ALAT & ALUR DATA ====================
        right_frame = tk.LabelFrame(main_frame, text=" Bagian Dalam Alat & Cara Input ke Komputer ", font=("Arial", 11, "bold"))
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        info_teks = (
            "1. SUMBER CAHAYA (Internal Alat):\n"
            "   - Lampu Deuterium (D2) untuk daerah UV (190-350 nm).\n"
            "   - Lampu Halogen/Tungsten untuk daerah Vis (320-1100 nm).\n\n"
            "2. MONOKROMATOR & BEAMSPLITTER:\n"
            "   - Mengubah cahaya polikromatik menjadi monokromatik.\n"
            "   - Membagi berkas cahaya menjadi Double-Beam (Jalur Referensi/Blangko & Jalur Sampel).\n\n"
            "3. DETEKTOR & PROSESOR:\n"
            "   - Menangkap sisa intensitas cahaya (It & Io).\n"
            "   - Mengonversi sinyal optik menjadi nilai Absorbansi (A = -log(It/Io)).\n\n"
            "4. CARA INPUT DATA KE KOMPUTER:\n"
            "   - Data pembacaan dari mikrokontroler alat dikirim melalui kabel komunikasi (USB/RS-232).\n"
            "   - Software di Komputer Data menerima angka Absorbansi secara otomatis atau manual.\n"
            "   - Nilai dimasukkan ke sistem regresi linear untuk menentukan konsentrasi sampel dan menampilkan diagram kurva."
        )
        
        lbl_info = tk.Label(right_frame, text=info_teks, justify=tk.LEFT, anchor="nw", font=("Arial", 9), bg="#f8f9fa", relief="sunken", bd=1)
        lbl_info.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def hitung_dan_plot(self):
        try:
            # Mengambil nilai dari kolom input
            kons_str = self.entry_kons.get()
            abs_std_str = self.entry_abs_std.get()
            abs_samp_str = self.entry_abs_samp.get()
            
            kons_standar = np.array([float(x.strip()) for x in kons_str.split(',')])
            abs_standar = np.array([float(y.strip()) for y in abs_std_str.split(',')])
            abs_sampel = np.array([float(y.strip()) for y in abs_samp_str.split(',')])
            
            if len(kons_standar) != len(abs_standar) or len(kons_standar) < 2:
                raise ValueError("Jumlah data konsentrasi dan absorbansi standar harus sama dan minimal 2 data.")
            
            # Perhitungan Regresi Linear (Hukum Lambert-Beer: y = mx + c)
            slope, intercept, r_value, p_value, std_err = stats.linregress(kons_standar, abs_standar)
            r_squared = r_value**2
            
            # Perhitungan Konsentrasi Sampel: C = (A - intercept) / slope
            kons_sampel_dihitung = (abs_sampel - intercept) / slope
            
            # Format Teks Hasil ke Textbox GUI
            hasil_str = f"=== HASIL PERHITUNGAN ===\n"
            hasil_str += f"Persamaan : A = {slope:.5f} * C + {intercept:.5f}\n"
            hasil_str += f"R²        : {r_squared:.5f}\n"
            if r_squared < 0.99:
                hasil_str += "Status    : Peringatan (R² < 0.99)\n\n"
            else:
                hasil_str += "Status    : Kurva Linear & Valid\n\n"
            
            hasil_str += "Konsentrasi Sampel Terhitung:\n"
            for i, (a_val, c_val) in enumerate(zip(abs_sampel, kons_sampel_dihitung)):
                hasil_str += f"• Sampel {i+1} (Abs={a_val}) -> C = {c_val:.4f}\n"
            
            self.text_hasil.delete("1.0", tk.END)
            self.text_hasil.insert(tk.END, hasil_str)
            
            # Visualisasi Diagram Kurva Kalibrasi menggunakan Matplotlib
            plt.figure(figsize=(8, 5))
            kons_fit = np.linspace(min(kons_standar), max(kons_standar), 100)
            abs_fit = slope * kons_fit + intercept
            
            plt.scatter(kons_standar, abs_standar, color='blue', label='Data Standar', s=90, zorder=3)
            plt.plot(kons_fit, abs_fit, color='red', linestyle='--', label=f'Regresi: A = {slope:.4f}C + {intercept:.4f}', zorder=2)
            
            for i, (a_val, c_val) in enumerate(zip(abs_sampel, kons_sampel_dihitung)):
                plt.scatter(c_val, a_val, color='green', marker='X', s=110, label=f'Sampel {i+1}' if i == 0 else "", zorder=4)
                plt.plot([c_val, c_val], [0, a_val], color='green', linestyle=':', alpha=0.6)
                plt.plot([0, c_val], [a_val, a_val], color='green', linestyle=':', alpha=0.6)
            
            plt.title('Kurva Kalibrasi Spektrofotometer UV-Vis', fontsize=12, fontweight='bold')
            plt.xlabel('Konsentrasi', fontsize=10)
            plt.ylabel('Absorbansi (A)', fontsize=10)
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.legend(loc='lower right')
            plt.tight_layout()
            
            # Menampilkan jendela grafik
            plt.show()
            
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan pada input data:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = UVVisSimulasiApp(root)
    root.mainloop()
