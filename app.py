import streamlit as st
import pandas as pd
import joblib

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Dashboard Harga Pangan AI",
    page_icon="🌾",
    layout="wide"
)

# 2. FUNGSI LOAD MODEL (CACHED)
@st.cache_resource
def load_model():
    # Memuat model yang sudah disimpan
    model_package = joblib.load('model_prediksi_harga_pangan.pkl')
    return model_package

# Load model saat aplikasi dibuka
try:
    package = load_model()
    model = package['model_rf']
    le_prov = package['le_prov']
    le_kom = package['le_kom']
    df_ref = package['data_ref']
except FileNotFoundError:
    st.error("File 'model_prediksi_harga_pangan.pkl' tidak ditemukan. Pastikan file ada di folder yang sama dengan app.py")
    st.stop()

# 3. JUDUL & SIDEBAR
st.title("🌾 Prediksi Harga Pangan Nasional")
st.markdown("Aplikasi berbasis AI untuk memprediksi harga komoditas pangan di Indonesia.")
st.write("---")

st.sidebar.header("Filter Prediksi")

# Input User: Pilih Provinsi
list_provinsi = le_prov.classes_
pilihan_provinsi = st.sidebar.selectbox("Pilih Provinsi", list_provinsi)

# Input User: Pilih Komoditas
list_komoditas = le_kom.classes_
pilihan_komoditas = st.sidebar.selectbox("Pilih Komoditas", list_komoditas)

# Input User: Pilih Bulan Target
bulan_dict = {
    'Januari': 1, 'Februari': 2, 'Maret': 3, 'April': 4, 'Mei': 5, 'Juni': 6,
    'Juli': 7, 'Agustus': 8, 'September': 9, 'Oktober': 10, 'November': 11, 'Desember': 12
}
pilihan_bulan = st.sidebar.selectbox("Prediksi untuk Bulan:", list(bulan_dict.keys()))
bulan_angka = bulan_dict[pilihan_bulan]

# Tombol Prediksi
tombol_prediksi = st.sidebar.button("Hitung Prediksi 🚀")

# 4. LOGIKA PREDIKSI (BACKEND)
if tombol_prediksi:
    # 1. Normalisasi Teks (Hapus Spasi Kiri/Kanan) agar pencarian akurat
    df_ref['Provinsi_Clean'] = df_ref['Nama Provinsi'].astype(str).str.strip()
    df_ref['Komoditas_Clean'] = df_ref['Komoditas'].astype(str).str.strip()
    
    provinsi_cari = pilihan_provinsi.strip()
    komoditas_cari = pilihan_komoditas.strip()

    # 2. Filter Data
    history_data = df_ref[
        (df_ref['Provinsi_Clean'] == provinsi_cari) & 
        (df_ref['Komoditas_Clean'] == komoditas_cari)
    ].sort_values(by=['Tahun', 'Bulan_Angka'], ascending=False)

    if history_data.empty:
        st.error(f"Maaf, data historis untuk **{pilihan_komoditas}** di **{pilihan_provinsi}** tidak ditemukan.")
        with st.expander("Lihat Data yang Tersedia di Database"):
            st.write(df_ref[['Nama Provinsi', 'Komoditas']].drop_duplicates().head(10))
    else:
        # Ambil harga terakhir
        data_terakhir = history_data.iloc[0]
        harga_bulan_lalu = data_terakhir['Harga']
        
        # Cari Harga Tahun Lalu (Seasonality)
        tahun_target_ref = data_terakhir['Tahun'] - 1
        data_tahun_lalu = df_ref[
            (df_ref['Provinsi_Clean'] == provinsi_cari) & 
            (df_ref['Komoditas_Clean'] == komoditas_cari) &
            (df_ref['Bulan_Angka'] == bulan_angka) & 
            (df_ref['Tahun'] == tahun_target_ref)
        ]

        if data_tahun_lalu.empty:
            harga_tahun_lalu = history_data['Harga'].mean()
        else:
            harga_tahun_lalu = data_tahun_lalu.iloc[0]['Harga']

        # Encoding ID
        try:
            prov_id = le_prov.transform([pilihan_provinsi])[0]
            komoditas_id = le_kom.transform([pilihan_komoditas])[0]
        except ValueError:
            try:
                prov_id = le_prov.transform([provinsi_cari])[0]
                komoditas_id = le_kom.transform([komoditas_cari])[0]
            except:
                st.error("Gagal mengenali ID Provinsi/Komoditas di dalam Model.")
                st.stop()

        # Susun Input Dataframe
        features = ['Harga_Bulan_Lalu', 'Harga_Tahun_Lalu', 'Bulan_Angka', 'Provinsi_ID', 'Komoditas_ID']
        input_data = pd.DataFrame([[
            harga_bulan_lalu,
            harga_tahun_lalu,
            bulan_angka,
            prov_id,
            komoditas_id
        ]], columns=features)

        # Lakukan Prediksi
        hasil_prediksi = model.predict(input_data)[0]
        selisih = hasil_prediksi - harga_bulan_lalu
        persen_selisih = (selisih / harga_bulan_lalu) * 100

        # 5. TAMPILKAN HASIL (FRONTEND)
        st.subheader(f"Hasil Prediksi: {pilihan_komoditas}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Harga Terakhir", 
                value=f"Rp {harga_bulan_lalu:,.0f}",
                help=f"Data bulan {data_terakhir['Bulan']} {data_terakhir['Tahun']}"
            )
        
        with col2:
            st.metric(
                label=f"Prediksi {pilihan_bulan}", 
                value=f"Rp {hasil_prediksi:,.0f}",
                delta=f"{selisih:,.0f} ({persen_selisih:.1f}%)",
                delta_color="inverse"
            )

        st.info(f"Prediksi ini menggunakan algoritma Random Forest dengan akurasi model ~93%.")

        # Tampilkan Grafik Tren
        st.write("---")
        st.subheader(f"📈 Tren Harga: {pilihan_komoditas} di {pilihan_provinsi}")

        chart_data = history_data.sort_values(by=['Tahun', 'Bulan_Angka'])
        chart_data['Periode'] = pd.to_datetime(dict(year=chart_data['Tahun'], month=chart_data['Bulan_Angka'], day=1))
        
        st.line_chart(chart_data, x='Periode', y='Harga')

else:
    st.info("Silakan pilih parameter di sebelah kiri dan tekan tombol 'Hitung Prediksi'.")