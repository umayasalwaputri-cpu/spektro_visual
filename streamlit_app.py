import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def tampilkan_simulasi_alat():
    """Menampilkan jendela visualisasi skema alat UV-Vis dan bagian dalamnya."""
    fig, (ax_alat, ax_grafik) = plt.subplots(1, 2, figsize=(15, 6))
    
    # --- PANEL 1: Skema Bagian Dalam Alat UV-Vis ---
    ax_alat.set_xlim(0, 10)
    ax_alat.set_ylim(0, 10)
    ax_alat.axis('off')
    ax_alat.set_title("Bagian Dalam & Jalur Optik (Double-Beam UV-Vis)", fontsize=12, fontweight='bold')
    
    # Kotak Utama Alat
    alat_box = plt.Rectangle((0.5, 1.5), 9, 7, facecolor='#f0f0f0', edgecolor='black', linewidth=1.5, linestyle='--')
    ax_alat.add_patch(alat_box)
    
    # Komponen-komponen di dalam alat
    # 1. Sumber Cahaya
    sumber = plt.Rectangle((1.0, 4.2), 1.0, 1.6, facecolor='orange', edgecolor='black')
    ax_alat.text(1.5, 5.0, 'Sumber\nCahaya', ha='center', va='center', fontsize=8, fontweight='bold')
    ax_alat.add_patch(sumber)
    
    # 2. Monokromator
    mono = plt.Rectangle((2.5, 4.0), 1.2, 2.0, facecolor='lightblue', edgecolor='black')
    ax_alat.text(3.1, 5.0, 'Monokro-\nmator', ha='center', va='center', fontsize=8, fontweight='bold')
    ax_alat.add_patch(mono)
    
    # 3. Beamsplitter (Pembagi Berkas)
    bs = plt.Polygon([[4.3, 4.2], [4.7, 5.8], [4.9, 5.8], [4.5, 4.2]], color='purple')
    ax_alat.text(4.6, 6.2, 'Beamsplitter', ha='center', va='center', fontsize=8)
    ax_alat.add_patch(bs)
    
    # 4. Kompartemen Sampel & Referensi
    # Jalur Referensi (Atas)
    ref_cuv = plt.Rectangle((6.0, 5.2), 0.8, 1.2, facecolor='yellow', edgecolor='black')
    ax_alat.text(6.4, 5.8, 'Blangko\n(Ref)', ha='center', va='center', fontsize=7)
    ax_alat.add_patch(ref_cuv)
    
    # Jalur Sampel (Bawah)
    samp_cuv = plt.Rectangle((6.0, 3.2), 0.8, 1.2, facecolor='lightgreen', edgecolor='black')
    ax_alat.text(6.4, 3.8, 'Sampel', ha='center', va='center', fontsize=7)
    ax_alat.add_patch(samp_cuv)
    
    # 5. Detektor
    det1 = plt.Rectangle((7.8, 5.3), 0.8, 1.0, facecolor='salmon', edgecolor='black')
    det2 = plt.Rectangle((7.8, 3.3), 0.8, 1.0, facecolor='salmon', edgecolor='black')
    ax_alat.text(8.2, 5.8, 'Detektor', ha='center', va='center', fontsize=7)
    ax_alat.text(8.2, 3.8, 'Detektor', ha='center', va='center', fontsize=7)
    ax_alat.add_patch(det1)
    ax_alat.add_patch(det2)
    
    # Garis Jalur Cahaya
    ax_alat.plot([2.0, 2.5], [5.0, 5.0], 'r-', lw=2)
    ax_alat.plot([3.7, 4.3], [5.0, 5.0], 'r-', lw=2)
    ax_alat.plot([4.7, 6.0], [5.8, 5.8], 'r-', lw=1.5) # ke referensi
    ax_alat.plot([4.7, 6.0], [4.2, 3.8], 'r-', lw=1.5) # ke sampel
    ax_alat.plot([6.8, 7.8], [5.8, 5.8], 'r-', lw=1.5)
    ax_alat.plot([6.8, 7.8], [3.8, 3.8], 'r-', lw=1.5)
    
    # Keterangan Panel Komputer di luar alat
    pc_box = plt.Rectangle((6.5, 0.2), 2.5, 1.0, facecolor='darkslategray', edgecolor='black')
    ax_alat.text(7.75, 0.7, 'Komputer Data\n(Input / Output)', ha='center', va='center', color='white', fontsize=8, fontweight='bold')
    ax_alat.add_patch(pc_box)
    ax_alat.plot([8.2, 8.2], [1.2, 3.3], 'b:', lw=1.5) # Koneksi data ke detektor
    
    ax_alat.text(5.0, 0.8, '*Simulasi Bagian Dalam Alat & Alur Sinar', ha='center', style='italic', fontsize=9)

    return fig, ax_grafik

def main():
    print("\n==========================================================")
    print("  SIMULASI 3D/SKEMA & KALKULATOR SPEKTROFOTOMETER UV-VIS")
    print("==========================================================")
    
    panjang_gelombang = 540 # nm
    
    # 1. Input Data Kurva Kalibrasi
    print("\n[1] Masukkan data kurva kalibrasi standar")
    try:
        data_kons_str = input("Konsentrasi Standar (pisahkan koma, contoh: 0, 2, 4, 6, 8, 10): ")
        data_abs_str = input("Absorbansi Standar (pisahkan koma, contoh: 0, 0.15, 0.31, 0.46, 0.61, 0.77): ")
        
        kons_standar = np.array([float(x.strip()) for x in data_kons_str.split(',')])
        abs_standar = np.array([float(y.strip()) for y in data_abs_str.split(',')])
        
        if len(kons_standar) != len(abs_standar) or len(kons_standar) < 2:
            raise ValueError("Jumlah data konsentrasi dan absorbansi harus sama dan minimal 2 data.")
            
    except ValueError as e:
        print(f"Error pada input data standar: {e}")
        return

    # 2. Input Data Sampel Tak Dikenal
    print("\n[2] Masukkan data pengukuran sampel")
    try:
        abs_sampel_str = input("Absorbansi Sampel (pisahkan koma, contoh: 0.4, 0.6): ")
        abs_sampel = np.array([float(y.strip()) for y in abs_sampel_str.split(',')])
    except ValueError as e:
        print(f"Error pada input data sampel: {e}")
        return

    # 3. Perhitungan Regresi Linear & Hukum Lambert-Beer
    slope, intercept, r_value, p_value, std_err = stats.linregress(kons_standar, abs_standar)
    r_squared = r_value**2
    
    # Rumus Konsentrasi Sampel: C = (A - intercept) / slope
    kons_sampel_dihitung = (abs_sampel - intercept) / slope
    
    # 4. Tampilkan Hasil di Terminal
    print(f"\n---------------- HASIL ANALISIS (λ = {panjang_gelombang} nm) ----------------")
    print(f"Persamaan Regresi Linear : A = {slope:.5f} * C + {intercept:.5f}")
    print(f"Koefisien Determinasi (R²) : {r_squared:.5f}")
    
    if r_squared < 0.99:
        print("STATUS: Peringatan - Kelinearan kurva kurang baik (R² < 0.99).")
    else:
        print("STATUS: Kurva kalibrasi valid dan linear.")

    print("\nHasil Perhitungan Konsentrasi Sampel:")
    for i, (abs_val, kons_val) in enumerate(zip(abs_sampel, kons_sampel_dihitung)):
        print(f" -> Sampel {i+1}: Absorbansi = {abs_val:.4f}  ==>  Konsentrasi Terhitung = {kons_val:.4f}")

    # 5. Visualisasi Grafik Kurva Kalibrasi (Disatukan dalam satu jendela dengan skema alat)
    fig, ax_grafik = tampilkan_simulasi_alat()
    
    kons_fit = np.linspace(min(kons_standar), max(kons_standar), 100)
    abs_fit = slope * kons_fit + intercept
    
    # Plot Titik Standar & Garis Regresi di ax_grafik kedua
    ax_grafik.scatter(kons_standar, abs_standar, color='blue', label='Data Standar', s=80, zorder=3)
    ax_grafik.plot(kons_fit, abs_fit, color='red', linestyle='--', label=f'Regresi: A = {slope:.4f}C + {intercept:.4f}', zorder=2)
    
    # Plot Titik Sampel
    for i, (abs_val, kons_val) in enumerate(zip(abs_sampel, kons_sampel_dihitung)):
        ax_grafik.scatter(kons_val, abs_val, color='green', marker='X', s=100, label=f'Sampel {i+1}' if i == 0 else "", zorder=4)
        ax_grafik.plot([kons_val, kons_val], [0, abs_val], color='green', linestyle=':', alpha=0.6)
        ax_grafik.plot([0, kons_val], [abs_val, abs_val], color='green', linestyle=':', alpha=0.6)
        ax_grafik.text(kons_val + (max(kons_standar)*0.01), abs_val + (max(abs_standar)*0.01), f'S{i+1} ({kons_val:.2f})', fontsize=9, fontweight='bold')
    
    ax_grafik.set_title(f'Kurva Kalibrasi UV-Vis ($\lambda$ = {panjang_gelombang} nm)', fontsize=12, fontweight='bold')
    ax_grafik.set_xlabel('Konsentrasi', fontsize=10)
    ax_grafik.set_ylabel('Absorbansi (A)', fontsize=10)
    
    teks_regresi = f'A = {slope:.4f}C + {intercept:.4f}\nR² = {r_squared:.4f}'
    ax_grafik.annotate(teks_regresi, xy=(0.05, 0.75), xycoords='axes fraction',
                       bbox=dict(boxstyle="round", fc="white", ec="red", alpha=0.9), fontsize=9)
    
    ax_grafik.grid(True, linestyle='--', linewidth=0.5)
    ax_grafik.legend(loc='lower right', fontsize=8)
    ax_grafik.set_xlim(0, max(max(kons_standar), max(kons_sampel_dihitung)) * 1.15)
    ax_grafik.set_ylim(0, max(max(abs_standar), max(abs_sampel)) * 1.15)
    
    plt.tight_layout()
    print("\nMembuka jendela visualisasi skema alat dan grafik kurva kalibrasi...")
    plt.show()

if __name__ == "__main__":
    main()
