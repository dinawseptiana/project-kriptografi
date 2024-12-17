import streamlit as st
import pandas as pd
from functions import nonlinearity, sac, lap, dap, bic_nl, bic_sac

# Judul aplikasi
st.title("GUI Proyek Kriptografi")
st.markdown("""
Alat untuk menguji S-Box berdasarkan:
- Nonlinearity (NL)
- Strict Avalanche Criterion (SAC)
- Linear Approximation Probability (LAP)
- Differential Approximation Probability (DAP)
- Bit Independence Criterion - Nonlinearity (BIC-NL)
- Bit Independence Criterion - SAC (BIC-SAC)
""")

# Pilihan import file
st.sidebar.header("1. Unggah S-Box")
uploaded_file = st.sidebar.file_uploader("Pilih file Excel dengan S-Box", type=["xlsx"])

if uploaded_file:
    # Membaca file dan memvalidasi
    try:
        sbox_df = pd.read_excel(uploaded_file)
        if sbox_df.shape[1] < 1:
            st.error("File Excel harus memiliki setidaknya satu kolom dengan nilai S-Box.")
            st.stop()
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
        st.stop()

    # Menampilkan S-Box
    st.write("S-Box yang diunggah:")
    st.dataframe(sbox_df)

    # Konversi S-Box ke list
    sbox = sbox_df.iloc[:, 0].tolist()

    # Validasi panjang S-Box
    n = 8  # Panjang input/output (default: AES)
    expected_length = 2**n
    if len(sbox) != expected_length:
        st.error(f"S-Box harus memiliki {expected_length} nilai, tetapi file Anda memiliki {len(sbox)} nilai.")
        st.stop()

    # Pilihan pengujian
    st.sidebar.header("2. Pilih Operasi")
    options = st.sidebar.multiselect(
        "Pilih pengujian:", ["NL", "SAC", "LAP", "DAP", "BIC-NL", "BIC-SAC"]
    )

    results = {}
    if "NL" in options:
        nl = nonlinearity(sbox, n, n)
        results["Nonlinearity"] = nl
        st.write(f"**Nonlinearity (NL):** {nl}")
    if "SAC" in options:
        sac_value = sac(sbox, n)
        results["SAC"] = sac_value
        st.write(f"**Strict Avalanche Criterion (SAC):** {sac_value:.5f}")
    if "LAP" in options:
        lap_value = lap(sbox, n)
        results["LAP"] = lap_value
        st.write(f"**Linear Approximation Probability (LAP):** {lap_value:.5f}")
    if "DAP" in options:
        dap_value = dap(sbox, n)
        results["DAP"] = dap_value
        st.write(f"**Differential Approximation Probability (DAP):** {dap_value:.6f}")
    if "BIC-NL" in options:
        bic_nl_value = bic_nl(sbox, n)
        results["BIC-NL"] = bic_nl_value
        st.write(f"**Bit Independence Criterion - Nonlinearity (BIC-NL):** {bic_nl_value}")
    if "BIC-SAC" in options:
        bic_sac_value = bic_sac(sbox, n)
        results["BIC-SAC"] = bic_sac_value
        st.write(f"**Bit Independence Criterion - SAC (BIC-SAC):** {bic_sac_value:.5f}")

    # Export hasil ke Excel
    if results:
        st.sidebar.header("3. Ekspor Hasil")
        export_button = st.sidebar.button("Download Hasil")

        if export_button:
            results_df = pd.DataFrame(results.items(), columns=["Metrik", "Nilai"])
            results_df.to_excel("hasil_pengujian.xlsx", index=False)
            st.success("Hasil pengujian berhasil diekspor!")
