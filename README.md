# Analisis Deforestasi Provinsi Bengkulu

## Deskripsi Proyek

Proyek ini merupakan analisis data kehilangan tutupan pohon (*tree cover loss*) di Provinsi Bengkulu menggunakan Python dan dataset `IDN.xlsx`. Analisis dilakukan untuk mengetahui perubahan kehilangan tutupan pohon dari tahun ke tahun, mengidentifikasi kategori penyebab kehilangan, serta memperkirakan tren kehilangan tutupan pohon selama lima tahun berikutnya menggunakan metode Linear Regression.

Proyek ini berkaitan dengan materi seminar mengenai pemantauan kehilangan tutupan pohon, klasifikasi penyebab deforestasi, dan pemanfaatan data untuk mendukung pengawasan lingkungan.

## Tujuan

1. Menganalisis kehilangan tutupan pohon di Provinsi Bengkulu berdasarkan data historis.
2. Mengidentifikasi kategori penyebab kehilangan tutupan pohon yang tercatat dalam dataset.
3. Memvisualisasikan tren tahunan dan distribusi kehilangan berdasarkan kategori penyebab.
4. Menerapkan Linear Regression untuk memperkirakan tren kehilangan tutupan pohon selama lima tahun berikutnya.
5. Mengevaluasi kecocokan model menggunakan MAE, RMSE, dan R².

## Teknologi yang Digunakan

- **Python** — bahasa pemrograman untuk analisis data.
- **Pandas** — membaca, memfilter, dan mengolah data Excel.
- **NumPy** — melakukan perhitungan numerik.
- **Matplotlib** — membuat visualisasi data.
- **Scikit-learn** — membangun model Linear Regression dan menghitung metrik evaluasi.
- **OpenPyXL** — membaca file Excel melalui Pandas.

## Dataset

- **Nama file:** `IDN.xlsx`
- **Sheet:** `Subnational 1 drivers`
- **Wilayah analisis:** Provinsi Bengkulu
- **Threshold:** 30
- **Periode data:** 2001–2025, berdasarkan hasil eksekusi program.
- **Kolom utama:** `subnational1`, `threshold`, `year`, `driver`, dan `tc_loss_ha`.

Kolom `year` menunjukkan tahun pengamatan, `driver` menunjukkan kategori penyebab yang tercatat, dan `tc_loss_ha` menyimpan nilai kehilangan tutupan pohon dalam hektare.

Program memfilter data berdasarkan nama provinsi dan nilai threshold, kemudian mengolah data untuk analisis tahunan dan kategori penyebab.

**Catatan:** data yang digunakan berasal dari sheet `Subnational 1 drivers`. Oleh karena itu, hasil penjumlahan kategori penyebab tidak otomatis sama dengan total kehilangan tutupan pohon keseluruhan. Interpretasi angka harus mengikuti definisi dan struktur dataset sumber.

## Metode Analisis

### 1. Pengolahan Data

Data dibaca dari file Excel, kemudian difilter untuk memilih Provinsi Bengkulu dan threshold 30. Kolom tahun dan kehilangan tutupan pohon dikonversi menjadi tipe numerik. Baris dengan nilai tahun atau kehilangan yang tidak valid dihapus.

### 2. Analisis Kehilangan Tahunan

Data dikelompokkan berdasarkan tahun untuk menghitung jumlah nilai kehilangan tutupan pohon yang tercatat pada setiap tahun. Hasilnya digunakan untuk melihat perubahan kehilangan tutupan pohon selama periode pengamatan.

### 3. Analisis Kategori Penyebab

Data dikelompokkan berdasarkan kategori `driver` untuk menghitung akumulasi nilai kehilangan yang tercatat pada setiap kategori. Hasilnya digunakan untuk membandingkan kontribusi kategori penyebab dalam dataset.

### 4. Prediksi Linear Regression

Linear Regression digunakan untuk memodelkan hubungan antara tahun pengamatan dan nilai kehilangan tutupan pohon. Model kemudian digunakan untuk memperkirakan tren selama lima tahun setelah tahun terakhir yang tersedia.

Prediksi merupakan estimasi berdasarkan pola historis, bukan kepastian kondisi deforestasi pada masa mendatang.

### 5. Evaluasi Model

Model dievaluasi menggunakan tiga metrik:

- **MAE (Mean Absolute Error):** rata-rata nilai absolut selisih antara data aktual dan prediksi.
- **RMSE (Root Mean Squared Error):** ukuran kesalahan prediksi yang memberikan penalti lebih besar pada kesalahan yang tinggi.
- **R² (Coefficient of Determination):** ukuran kecocokan model terhadap variasi data yang dievaluasi.

Pada versi kode saat ini, evaluasi dilakukan menggunakan data yang sama dengan data pelatihan. Karena itu, nilai evaluasi belum menunjukkan kemampuan model dalam memprediksi data yang belum pernah dilihat.

## Hasil Program

Berdasarkan eksekusi program yang tersedia, diperoleh hasil berikut:

| Komponen | Hasil |
|---|---:|
| Jumlah data setelah filter | 173 baris |
| Periode pengamatan | 2001–2025 |
| Kategori penyebab dengan nilai terbesar | Permanent agriculture |
| Nilai kategori Permanent agriculture | 418.411 ha |
| MAE | 4.202,21 ha |
| RMSE | 5.021,48 ha |
| R² | 0,2243 |

Hasil tersebut merupakan keluaran dari versi program yang digunakan. Total 503.842 hektare yang tercetak pada program merupakan penjumlahan nilai kategori dalam sheet yang dianalisis, bukan otomatis total kehilangan tutupan pohon keseluruhan.

Nilai evaluasi perlu ditafsirkan dengan memperhatikan bahwa model diuji pada data pelatihan yang sama.

## Struktur Folder

```text
webinar6/
├── webinar_6.py
├── IDN.xlsx
├── README.md
└── output/
    ├── data_bengkulu_terfilter.csv
    ├── kehilangan_tahunan.csv
    ├── total_per_penyebab.csv
    ├── hasil_prediksi.csv
    ├── grafik_tahunan.png
    ├── grafik_penyebab.png
    └── grafik_prediksi.png
```

Folder `output` dibuat secara otomatis oleh program. File CSV berisi hasil pengolahan data, sedangkan file PNG berisi visualisasi hasil analisis.

## Instalasi dan Cara Menjalankan

### 1. Instal dependensi

Pastikan Python sudah terpasang. Buka terminal pada folder proyek, kemudian jalankan:

```bash
python -m pip install pandas numpy matplotlib scikit-learn openpyxl
```

### 2. Siapkan dataset

Letakkan `IDN.xlsx` pada folder yang sama dengan `webinar_6.py`.

### 3. Jalankan program

```bash
python webinar_6.py
```

Jika menggunakan Python dengan lokasi instalasi khusus di Windows, sesuaikan perintah dengan lokasi Python yang digunakan.

### 4. Periksa hasil

Hasil analisis, prediksi, dan grafik akan disimpan di folder `output`.

## Keterkaitan dengan Materi Seminar

Materi seminar membahas pemantauan kehilangan tutupan pohon menggunakan citra satelit, klasifikasi penyebab gangguan hutan, pembaruan informasi secara berkala, serta penggunaan informasi untuk membantu pengawasan dan pengelolaan lingkungan.

Proyek ini menggunakan data kehilangan tutupan pohon dan kategori penyebab untuk melakukan analisis historis dan prediksi tren. Dengan demikian, proyek ini merupakan pengembangan analisis data yang relevan dengan topik seminar, tetapi bukan reproduksi penuh sistem klasifikasi peringatan deforestasi yang dijelaskan dalam seminar.

Program ini belum mengolah citra satelit secara langsung, menghasilkan peringatan deforestasi secara real-time, atau melatih model klasifikasi penyebab menggunakan citra satelit.

## Pengembangan Selanjutnya

Beberapa pengembangan yang dapat dilakukan meliputi:

1. Memperbaiki evaluasi model dengan memisahkan data pelatihan dan pengujian berdasarkan waktu.
2. Memvalidasi agregasi data serta membedakan data total kehilangan tutupan pohon dari data kategori penyebab.
3. Membandingkan Linear Regression dengan metode prediksi lainnya.
4. Mengembangkan visualisasi spasial untuk menunjukkan lokasi kehilangan tutupan pohon.
5. Mengintegrasikan data peringatan satelit berkala agar analisis lebih mendekati sistem pemantauan deforestasi yang dibahas dalam seminar.

## Kesimpulan

Program ini mengimplementasikan pengolahan data, analisis kategori penyebab, visualisasi, dan prediksi tren kehilangan tutupan pohon di Provinsi Bengkulu. Hasilnya dapat digunakan sebagai analisis awal untuk memahami pola kehilangan tutupan pohon. Ketepatan interpretasi hasil bergantung pada struktur dataset, validitas agregasi, dan evaluasi model yang digunakan.
