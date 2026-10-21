import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Simulasi & Kalkulator UV-Vis", layout="wide")

st.title("🧪 Simulasi & Kalkulator Spektrofotometer UV-Vis (Shimadzu UV-1800)")
st.markdown("Aplikasi web interaktif untuk simulasi bagian dalam alat, alur data, serta perhitungan kurva kalibrasi dan konsentrasi sampel.")

# Layout dibagi menjadi 2 kolom (Kiri: Komputer Data & Kalkulator, Kanan: Skema Bagian Dalam Alat)
col_input, col_alat = st.columns([1, 1])

with col_input:
    st.subheader("📊 Komputer Data (Input & Kalkulator)")
    
    # Form Input Data oleh Pengguna
    kons_input = st.text_input(
        "Konsentrasi Standar (pisahkan dengan koma):", 
        "0, 2, 4, 6, 8, 10"
    )
    abs_std_input = st.text_input(
        "Absorbansi Standar (pisahkan dengan koma):", 
        "0, 0.15, 0.31, 0.46, 0.61, 0.77"
    )
    abs_samp_input = st.text_input(
        "Absorbansi Sampel Tak Dikenal (pisahkan dengan koma):", 
        "0.40, 0.60"
    )
    
    proses_btn = st.button("Hitung Analisis & Tampilkan Kurva", type="primary")

with col_alat:
    st.subheader("🔬 Bagian Dalam Alat & Cara Kerja")
    st.info(
        "*1. Sumber Cahaya:* Memancarkan sinar polikromatik (Lampu Deuterium untuk UV dan Halogen untuk Visibel).\n\n"
        "*2. Monokromator & Beamsplitter:* Mengubah cahaya menjadi panjang gelombang tunggal ($\\lambda$) dan membaginya menjadi sistem Double-Beam (Jalur Referensi/Blangko & Sampel).\n\n"
        "*3. Detektor & Komputer Data:* Mengukur intensitas cahaya ($I_t$ dan $I_o$), mengonversinya menjadi nilai Absorbansi ($A = -\\log(I_t/I_o)$), lalu mengirimkannya ke komputer untuk diproses menjadi kurva kalibrasi."
    )

# Proses Perhitungan dan Plotting setelah tombol diklik
if proses_btn:
    try:
        # Mengonversi input teks menjadi array numerik numpy
        kons_standar = np.array([float(x.strip()) for x in kons_input.split(',')])
        abs_standar = np.array([float(y.strip()) for y in abs_std_input.split(',')])
        abs_sampel = np.array([float(y.strip()) for y in abs_samp_input.split(',')])
        
        if len(kons_standar) != len(abs_standar) or len(kons_standar) < 2:
            st.error("Jumlah data konsentrasi dan absorbansi standar harus sama dan minimal 2 data.")
        else:
            # Perhitungan Regresi Linear (Hukum Lambert-Beer: A = mC + c)
            slope, intercept, r_value, p_value, std_err = stats.linregress(kons_standar, abs_standar)
            r_squared = r_value**2
            
            # Hitung konsentrasi sampel: C = (A - intercept) / slope
            kons_sampel_dihitung = (abs_sampel - intercept) / slope
            
            st.markdown("---")
            st.subheader("📈 Hasil Analisis & Perhitungan")
            
            # Tampilkan metrik hasil regresi
            m1, m2, m3 = st.columns(3)
            m1.metric("Kemiringan (Slope / m)", f"{slope:.5f}")
            m2.metric("Intersep (c)", f"{intercept:.5f}")
            m3.metric("Koefisien Determinasi (R²)", f"{r_squared:.5f}")
            
            if r_squared < 0.99:
                st.warning("Peringatan: Kelinearan kurva kalibrasi kurang baik ($R^2 < 0.99$).")
            else:
                st.success("Status: Kurva kalibrasi valid dan linear.")
                
            # Tabel Hasil Konsentrasi Sampel
            st.write("*Hasil Konsentrasi Sampel Tak Dikenal:*")
            for i, (a_val, c_val) in enumerate(zip(abs_sampel, kons_sampel_dihitung)):
                st.write(f"- *Sampel {i+1}: Absorbansi = {a_val:.4f} $\rightarrow$ **Konsentrasi Terhitung = {c_val:.4f}*")
            
            # Visualisasi Diagram Kurva Kalibrasi menggunakan Matplotlib
            st.markdown("---")
            st.subheader("📉 Diagram Kurva Kalibrasi")
            
            fig, ax = plt.subplots(figsize=(8, 5))
            kons_fit = np.linspace(min(kons_standar), max(kons_standar), 100)
            abs_fit = slope * kons_fit + intercept
            
            # Plot titik data standar dan garis regresi
            ax.scatter(kons_standar, abs_standar, color='blue', label='Data Standar', s=80, zorder=3)
            ax.plot(kons_fit, abs_fit, color='red', linestyle='--', label=f'Regresi: A = {slope:.4f}C + {intercept:.4f}', zorder=2)
            
            # Plot titik sampel tak dikenal
            for i, (a_val, c_val) in enumerate(zip(abs_sampel, kons_sampel_dihitung)):
                ax.scatter(c_val, a_val, color='green', marker='X', s=100, label=f'Sampel {i+1}' if i == 0 else "", zorder=4)
                ax.plot([c_val, c_val], [0, a_val], color='green', linestyle=':', alpha=0.6)
                ax.plot([0, c_val], [a_val, a_val], color='green', linestyle=':', alpha=0.6)
            
            ax.set_title('Kurva Kalibrasi Spektrofotometer UV-Vis', fontsize=12, fontweight='bold')
            ax.set_xlabel('Konsentrasi', fontsize=10)
            ax.set_ylabel('Absorbansi (A)', fontsize=10)
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.legend(loc='lower right')
            
            st.pyplot(fig)
            
    except Exception as e:
        st.error(f"Terjadi kesalahan dalam format input data: {e}")
