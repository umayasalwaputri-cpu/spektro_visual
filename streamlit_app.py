import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Simulasi UV-Vis Shimadzu UV-1800", layout="wide")

st.title("🧪 Simulasi & Kalkulator Spektrofotometer UV-Vis")
st.markdown("Aplikasi web interaktif untuk analisis kurva kalibrasi dan penentuan konsentrasi sampel menggunakan *Shimadzu UV-1800*.")

# Layout dibagi menjadi 2 kolom (Kiri: Input Data, Kanan: Informasi Alat)
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Komputer Data (Input & Kalkulator)")
    
    # Form Input dari pengguna
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
    
    proses_btn = st.button("Hitung Regresi & Tampilkan Kurva", type="primary")

with col2:
    st.subheader("🔬 Bagian Dalam Alat & Alur Data")
    st.info(
        "*1. Sumber Cahaya:* Menggabungkan Lampu Deuterium ($D_2$) untuk UV (190-350 nm) & Lampu Halogen untuk Visible (320-1100 nm).\n\n"
        "*2. Monokromator & Beamsplitter:* Mengubah cahaya polikromatik menjadi monokromatik dan membaginya menjadi sistem Double-Beam (Jalur Referensi/Blangko & Sampel).\n\n"
        "*3. Detektor & Komputer:* Mengonversi sisa cahaya ($I_t$ & $I_o$) menjadi nilai Absorbansi ($A = -\\log(I_t/I_o)$) yang dikirim ke komputer data untuk dianalisis."
    )

# Proses Perhitungan & Plotting setelah tombol diklik
if proses_btn:
    try:
        # Mengubah teks input menjadi array numerik
        kons_standar = np.array([float(x.strip()) for x in kons_input.split(',')])
        abs_standar = np.array([float(y.strip()) for y in abs_std_input.split(',')])
        abs_sampel = np.array([float(y.strip()) for y in abs_samp_input.split(',')])
        
        if len(kons_standar) != len(abs_standar) or len(kons_standar) < 2:
            st.error("Jumlah data konsentrasi dan absorbansi standar harus sama dan minimal 2 data.")
        else:
            # Perhitungan Regresi Linear (Hukum Lambert-Beer: y = mx + c)
            slope, intercept, r_value, p_value, std_err = stats.linregress(kons_standar, abs_standar)
            r_squared = r_value**2
            
            # Hitung konsentrasi sampel: C = (A - intercept) / slope
            kons_sampel_dihitung = (abs_sampel - intercept) / slope
            
            st.markdown("---")
            st.subheader("📈 Hasil Analisis")
            
            # Tampilkan metrik hasil
            m_col1, m_col2, m_col3 = st.columns(3)
            m_col1.metric("Kemiringan (Slope)", f"{slope:.5f}")
            m_col2.metric("Intersep", f"{intercept:.5f}")
            m_col3.metric("Koefisien Determinasi (R²)", f"{r_squared:.5f}")
            
            if r_squared < 0.99:
                st.warning("Peringatan: Kelinearan kurva kalibrasi kurang baik ($R^2 < 0.99$).")
            else:
                st.success("Status: Kurva kalibrasi valid dan linear.")
                
            # Tabel Hasil Konsentrasi Sampel
            st.write("*Konsentrasi Sampel Terhitung:*")
            for i, (a_val, c_val) in enumerate(zip(abs_sampel, kons_sampel_dihitung)):
                st.write(f"- *Sampel {i+1}: Absorbansi = {a_val:.4f} $\rightarrow$ **Konsentrasi = {c_val:.4f}*")
            
            # Visualisasi Grafik menggunakan Matplotlib di Streamlit
            st.markdown("---")
            st.subheader("📉 Diagram Kurva Kalibrasi")
            
            fig, ax = plt.subplots(figsize=(8, 5))
            kons_fit = np.linspace(min(kons_standar), max(kons_standar), 100)
            abs_fit = slope * kons_fit + intercept
            
            ax.scatter(kons_standar, abs_standar, color='blue', label='Data Standar', s=80, zorder=3)
            ax.plot(kons_fit, abs_fit, color='red', linestyle='--', label=f'Regresi: A = {slope:.4f}C + {intercept:.4f}', zorder=2)
            
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
