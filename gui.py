import streamlit as st
import pandas as pd
import io
from functions import nonlinearity, sac, lap, dap, bic_nl, bic_sac


# Atur halaman dan ikon aplikasi
st.set_page_config(
    page_title="S-Box Tester",
    page_icon=":lock:",
    layout="wide",
)

#Tambahkan Banner atau Gambar Header
st.image("https://via.placeholder.com/728x90.png?text=Welcome+to+S-Box+Tester", use_column_width=True)

# Judul Aplikasi
st.title(":lock: **S-Box Tester**")
st.markdown("""
<span style="color:blue; font-size:20px;">Selamat datang di aplikasi **S-Box Tester**!</span>  
Aplikasi ini dirancang untuk menguji kekuatan **S-Box** berdasarkan beberapa metrik, seperti:
- **Nonlinearity (NL)**
- **Strict Avalanche Criterion (SAC)**
- **Linear Approximation Probability (LAP)**
- **Differential Approximation Probability (DAP)**
- **Bit Independence Criterion - Nonlinearity (BIC-NL)**
- **Bit Independence Criterion - SAC (BIC-SAC)**

:bulb: **Tips:**  
Unggah file Excel Anda untuk memulai pengujian! 🚀
""", unsafe_allow_html=True)

# Sidebar untuk Navigasi
st.sidebar.header(":gear: **Langkah-Langkah**")
st.sidebar.markdown("""
1. **Unggah File:** Pilih file Excel dengan S-Box.  
2. **Pilih Operasi:** Pilih metrik pengujian.  
3. **Lihat Hasil:** Tampilkan hasil di layar.  
4. **Ekspor Hasil:** Unduh file Excel hasil pengujian.
""")

# Pilihan import file
st.sidebar.header("📂 Unggah S-Box")
uploaded_file = st.sidebar.file_uploader("Pilih file Excel (S-Box):", type=["xlsx"])

if uploaded_file:
    # Membaca file Excel
    try:
        sbox_df = pd.read_excel(uploaded_file)
        if sbox_df.shape[1] < 1:
            st.error("File Excel harus memiliki setidaknya satu kolom dengan nilai S-Box.")
            st.stop()
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
        st.stop()

    # Menampilkan tabel S-Box
    st.subheader("📊 S-Box yang Diunggah")
    st.dataframe(sbox_df)

    # Konversi ke list
    sbox = sbox_df.iloc[:, 0].tolist()

    # Validasi panjang S-Box
    n = 8  # Panjang input/output (default: AES)
    expected_length = 2**n
    if len(sbox) != expected_length:
        st.error(f"S-Box harus memiliki {expected_length} nilai, tetapi file Anda memiliki {len(sbox)} nilai.")
        st.stop()

    # Pilihan pengujian
    st.sidebar.header("🧪 Pilih Operasi Pengujian")
    options = st.sidebar.multiselect(
        "Pilih metrik untuk pengujian:", ["NL", "SAC", "LAP", "DAP", "BIC-NL", "BIC-SAC"]
    )

    # Hasil Pengujian
    st.subheader("📋 Hasil Pengujian")
    results = {}
    if "NL" in options:
        nl = nonlinearity(sbox, n, n)
        results["Nonlinearity (NL)"] = nl
        st.metric("Nonlinearity (NL)", f"{nl:.2f}")
    if "SAC" in options:
        sac_value = sac(sbox, n)
        results["Strict Avalanche Criterion (SAC)"] = sac_value
        st.metric("SAC", f"{sac_value:.5f}")
    if "LAP" in options:
        lap_value = lap(sbox, n)
        results["Linear Approximation Probability (LAP)"] = lap_value
        st.metric("LAP", f"{lap_value:.5f}")
    if "DAP" in options:
        dap_value = dap(sbox, n)
        results["Differential Approximation Probability (DAP)"] = dap_value
        st.metric("DAP", f"{dap_value:.6f}")
    if "BIC-NL" in options:
        bic_nl_value = bic_nl(sbox, n)
        results["Bit Independence Criterion - Nonlinearity (BIC-NL)"] = bic_nl_value
        st.metric("BIC-NL", f"{bic_nl_value:.2f}")
    if "BIC-SAC" in options:
        bic_sac_value = bic_sac(sbox, n)
        results["Bit Independence Criterion - SAC (BIC-SAC)"] = bic_sac_value
        st.metric("BIC-SAC", f"{bic_sac_value:.5f}")

    # Ekspor hasil ke Excel
    if results:
        st.sidebar.header("📤 Ekspor Hasil")
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            results_df = pd.DataFrame(results.items(), columns=["Metrik", "Nilai"])
            results_df.to_excel(writer, index=False, sheet_name="Hasil Pengujian")
        output.seek(0)

        # Tombol download
        st.download_button(
            label="Download Hasil Pengujian",
            data=output,
            file_name="hasil_pengujian.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("Unggah file S-Box dalam format Excel untuk memulai pengujian.")

# Footer
st.markdown("---")
st.markdown("**Dibuat dengan ❤️ oleh Kelompok 1 - Dina Wachidah S | Amirul Mustaqim | Rizqi Fitriyani | Farrel Akmal O**")
