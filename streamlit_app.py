import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Simulasi 3D & Kalkulator UV-Vis", layout="wide")

st.title("🧪 Simulasi 3D & Kalkulator Spektrofotometer UV-Vis Shimadzu UV-1800")
st.markdown("Aplikasi web interaktif dengan visualisasi bagian dalam alat, alur gerak sinar optik, dan komputer data analisis.")

# Layout Utama dibagi 2 Kolom (Kiri: Visualisasi 3D/Animasi Alat, Kanan: Komputer Data & Kalkulator)
col_visual, col_data = st.columns([1.2, 1])

with col_visual:
    st.subheader("🖥️ Visualisasi 3D & Bagian Dalam Alat")
    
    # Menggunakan HTML & CSS/JavaScript Interaktif untuk simulasi visual bergerak ala 3D web
    html_3d_simulation = """
    <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; color: white; text-align: center; font-family: sans-serif;">
        <h4>Simulasi Jalur Optik & Komponen Dalam (Double-Beam)</h4>
        <canvas id="uvCanvas" width="450" height="220" style="background-color: #111; border-radius: 8px;"></canvas>
        <p style="font-size: 12px; color: #aaa; margin-top: 5px;">*Animasi titik merah menunjukkan pergerakan sinar dari sumber cahaya menuju detektor.</p>
    </div>

    <script>
        const canvas = document.getElementById('uvCanvas');
        const ctx = canvas.getContext('2d');
        
        let posX = 40;
        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // 1. Sumber Cahaya
            ctx.fillStyle = "orange";
            ctx.fillRect(20, 90, 30, 40);
            ctx.fillStyle = "white";
            ctx.font = "10px Arial";
            ctx.fillText("Sumber", 15, 85);
            
            // 2. Monokromator
            ctx.fillStyle = "lightblue";
            ctx.fillRect(80, 80, 40, 60);
            ctx.fillStyle = "white";
            ctx.fillText("Monokromator", 70, 70);
            
            // 3. Beamsplitter (Pemisah Berkas)
            ctx.fillStyle = "purple";
            ctx.beginPath();
            ctx.moveTo(150, 70); ctx.lineTo(170, 110); ctx.lineTo(160, 110); ctx.lineTo(140, 70);
            ctx.fill();
            
            // 4. Kuvet (Sampel & Blangko)
            ctx.fillStyle = "yellow";
            ctx.fillRect(230, 45, 30, 30); // Referensi
            ctx.fillStyle = "lightgreen";
            ctx.fillRect(230, 125, 30, 30); // Sampel
            ctx.fillStyle = "white";
            ctx.fillText("Blangko", 225, 38);
            ctx.fillText("Sampel", 225, 170);
            
            // 5. Detektor
            ctx.fillStyle = "salmon";
            ctx.fillRect(330, 45, 30, 30);
            ctx.fillRect(330, 125, 30, 30);
            ctx.fillStyle = "white";
            ctx.fillText("Detektor", 325, 38);
            
            // Garis Jalur Optik Tetap
            ctx.strokeStyle = "rgba(255, 255, 255, 0.3)";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(50, 110); ctx.lineTo(80, 110);
            ctx.moveTo(120, 110); ctx.lineTo(145, 90);
            ctx.moveTo(155, 90); ctx.lineTo(230, 60); ctx.moveTo(260, 60); ctx.lineTo(330, 60);
            ctx.moveTo(155, 90); ctx.lineTo(230, 140); ctx.moveTo(260, 140); ctx.lineTo(330, 140);
            ctx.stroke();
            
            // Sinar Cahaya Bergerak (Animasi Titik Merah)
            ctx.fillStyle = "red";
            ctx.beginPath();
            ctx.arc(posX, posX > 150 ? (posX < 230 ? 60 : 60) : 110, 5, 0, Math.PI * 2);
            // Sederhanakan animasi bolak-balik titik cahaya
            ctx.arc(posX, 110, 4, 0, Math.PI * 2);
            ctx.fill();
            
            posX += 2;
            if (posX > 350) posX = 40;
            
            requestAnimationFrame(draw);
        }
        draw();
    </script>
    """
    st.components.v1.html(html_3d_simulation, height=270)
    
    st.info(
        "*Keterangan Bagian Dalam Alat:*\n"
        "- *Sumber Cahaya:* Memancarkan sinar Polikromatik ($D_2$ dan Halogen).\n"
        "- *Monokromator:* Mengubah cahaya menjadi panjang gelombang tunggal spesifik ($\lambda$).\n"
        "- *Beamsplitter:* Membagi berkas cahaya menjadi jalur referensi dan sampel (Double-Beam).\n"
        "- *Detektor:* Mengubah intensitas cahaya menjadi sinyal elektrik untuk dikirim ke Komputer Data."
    )

with col_data:
    st.subheader("📊 Komputer Data (Input & Kalkulator)")
    
    # Form Input Data oleh Pengguna
    kons_input = st.text_input("Konsentrasi Standar (pisahkan koma):", "0, 2, 4, 6, 8, 10")
    abs_std_input = st.text_input("Absorbansi Standar (pisahkan koma):", "0, 0.15, 0.31, 0.46, 0.61, 0.77")
    abs_samp_input = st.text_input("Absorbansi Sampel Tak Dikenal (pisahkan koma):", "0.40, 0.60")
    
    proses_btn = st.button("Hitung Analisis & Tampilkan Kurva", type="primary")

# Eksekusi Perhitungan & Grafik Kurva
if proses_btn:
    try:
        kons_standar = np.array([float(x.strip()) for x in kons_input.split(',')])
        abs_standar = np.array([float(y.strip()) for y in abs_std_input.split(',')])
        abs_sampel = np.array([float(y.strip()) for y in abs_samp_input.split(',')])
        
        if len(kons_standar) != len(abs_standar) or len(kons_standar) < 2:
            st.error("Jumlah data konsentrasi dan absorbansi standar harus sama dan minimal 2 data.")
        else:
            # Regresi Linear (Hukum Lambert-Beer: A = mC + c)
            slope, intercept, r_value, p_value, std_err = stats.linregress(kons_standar, abs_standar)
            r_squared = r_value**2
            
            # Hitung Konsentrasi Sampel
            kons_sampel_dihitung = (abs_sampel - intercept) / slope
            
            st.markdown("---")
            st.subheader("📈 Hasil Perhitungan & Kurva Kalibrasi")
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Slope (m)", f"{slope:.5f}")
            m2.metric("Intercept (c)", f"{intercept:.5f}")
            m3.metric("R² (Rasio Kelinearan)", f"{r_squared:.5f}")
            
            if r_squared < 0.99:
                st.warning("Peringatan: Kelinearan kurva kurang baik ($R^2 < 0.99$).")
            else:
                st.success("Status: Kurva kalibrasi valid dan linear.")
                
            st.write("*Konsentrasi Sampel Terhitung:*")
            for i, (a_val, c_val) in enumerate(zip(abs_sampel, kons_sampel_dihitung)):
                st.write(- f"*Sampel {i+1}: Absorbansi = {a_val:.4f} $\rightarrow$ **Konsentrasi = {c_val:.4f}*")
            
            # Plot Kurva Menggunakan Matplotlib
            fig, ax = plt.subplots(figsize=(8, 4.5))
            kons_fit = np.linspace(min(kons_standar), max(kons_standar), 100)
            abs_fit = slope * kons_fit + intercept
            
            ax.scatter(kons_standar, abs_standar, color='blue', label='Data Standar', s=80, zorder=3)
            ax.plot(kons_fit, abs_fit, color='red', linestyle='--', label=f'Regresi: A = {slope:.4f}C + {intercept:.4f}', zorder=2)
            
            for i, (a_val, c_val) in enumerate(zip(abs_sampel, kons_sampel_dihitung)):
                ax.scatter(c_val, a_val, color='green', marker='X', s=100, label=f'Sampel {i+1}' if i == 0 else "", zorder=4)
                ax.plot([c_val, c_val], [0, a_val], color='green', linestyle=':', alpha=0.6)
                ax.plot([0, c_val], [a_val, a_val], color='green', linestyle=':', alpha=0.6)
            
            ax.set_title('Kurva Kalibrasi Spektrofotometer UV-Vis', fontsize=11, fontweight='bold')
            ax.set_xlabel('Konsentrasi', fontsize=9)
            ax.set_ylabel('Absorbansi (A)', fontsize=9)
            ax.grid(True, linestyle='--', alpha=0.5)
            ax.legend(loc='lower right', fontsize=8)
            
            st.pyplot(fig)
            
    except Exception as e:
        st.error(f"Terjadi kesalahan pada format input data: {e}")
