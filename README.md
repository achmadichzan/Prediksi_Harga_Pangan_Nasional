# 🌾 Prediksi Harga Pangan Nasional

### Dashboard Analisis & Prediksi Harga Komoditas Pangan di Indonesia Berbasis Machine Learning

🔗 **Live Demo:**\
https://prediksi-harga-pangan-nasional.streamlit.app/

------------------------------------------------------------------------

## 📘 Tentang Proyek

Proyek ini bertujuan untuk membantu memantau dan memprediksi pergerakan
harga pangan di berbagai provinsi di Indonesia.\
Menggunakan data historis *time series*, sistem mampu:

-   Memprediksi harga komoditas bulan berikutnya
-   Mengidentifikasi tren inflasi/deflasi pangan
-   Melihat pola musiman yang berulang

Model dibangun menggunakan **Random Forest Regressor** yang mampu
menangkap fluktuasi harga dengan akurasi tinggi.

------------------------------------------------------------------------

## 📂 Sumber Data

Dataset berasal dari sumber resmi pemerintah Indonesia:

-   **Nama Dataset:** Rata-rata Harga Pangan Bulanan Tingkat Konsumen
    Provinsi
-   **Sumber:** Badan Pangan Nasional (National Food Agency)\
    https://data.badanpangan.go.id/datasetpublications/178/rata-rata-harga-pangan-bulanan-konsumen-provinsi
-   **Cakupan:** Harga berbagai komoditas strategis untuk seluruh
    provinsi Indonesia (2021--Sekarang)

------------------------------------------------------------------------

## ✨ Fitur Utama

-   **Multi-Komoditas & Multi-Provinsi**: Mendukung berbagai komoditas
    (beras, cabai, bawang, daging, dll)
-   **Time Series Forecasting**: Prediksi harga bulan depan
-   **Analisis Tren Visual**: Grafik interaktif untuk melihat pola antar
    tahun
-   **Indikator Inflasi/Deflasi**: Persentase perubahan harga
-   **Dashboard Interaktif**: Dibangun dengan Streamlit (wide layout,
    responsive)

------------------------------------------------------------------------

## 🧠 Metodologi Machine Learning

### **1. Data Preprocessing**

-   Pembersihan format mata uang dan tipe data
-   Menangani missing values dengan **Interpolasi Linear** berdasarkan
    Provinsi & Komoditas
-   Normalisasi nama wilayah

### **2. Feature Engineering**

Model mempelajari konteks waktu menggunakan fitur:

-   **Lag Features:**
    -   `Harga_Bulan_Lalu (t-1)`
    -   `Harga_3Bulan_Lalu (t-3)`
-   **Seasonality:**
    -   `Harga_Tahun_Lalu (t-12)`
-   **Encoding:** Label Encoding untuk Provinsi & Jenis Komoditas

### **3. Model & Evaluasi**

-   **Algoritma:** Random Forest Regressor
-   **Evaluasi:** Time Series Split (Train \< 2024, Test ≥ 2024)
-   **Hasil Performa Model:**
    -   **MAPE:** \~6.92% (akurasi ±93%)
    -   **R²:** 0.97
    -   **MAE:** \~Rp 2.592

------------------------------------------------------------------------

## 🛠️ Instalasi & Cara Menjalankan (Lokal)

### **1. Clone Repository**

``` bash
git clone https://github.com/achmadichzan/Prediksi_Harga_Pangan_Nasional.git
cd prediksi-harga-pangan
```

### **2. Buat Virtual Environment**

#### Windows

``` bash
python -m venv venv
venv\Scripts\activate
```

#### Mac/Linux

``` bash
python3 -m venv venv
source venv/bin/activate
```

### **3. Install Dependencies**

``` bash
pip install -r requirements.txt
```

### **4. Jalankan Aplikasi**

``` bash
streamlit run app.py
```

------------------------------------------------------------------------

## 📁 Struktur Direktori

    prediksi-harga-pangan/
    ├── app.py                           # Kode utama aplikasi Streamlit
    ├── model_prediksi_harga_pangan.pkl  # Model ML yang sudah dilatih
    ├── requirements.txt                 # Daftar library Python
    ├── harga_pangan.csv                 # Dataset mentah (backup)
    └── README.md                        # Dokumentasi proyek

------------------------------------------------------------------------

## 👨‍💻 Dikembangkan oleh

**Achmad Ichzan --- Machine Learning Enthusiast**
