
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# KONFIGURASI

BASE_DIR = Path(__file__).resolve().parent
FILE_EXCEL = BASE_DIR / "IDN.xlsx"
OUTPUT_DIR = BASE_DIR / "output"

SHEET_NAME = "Subnational 1 drivers"
PROVINSI = "Bengkulu"
THRESHOLD = 30
JUMLAH_TAHUN_PREDIKSI = 5

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. MEMBACA DATA EXCEL

def baca_data():
    print("\n" + "=" * 60)
    print("ANALISIS DEFORESTASI PROVINSI BENGKULU")
    print("=" * 60)

    if not FILE_EXCEL.exists():
        raise FileNotFoundError(
            f"File tidak ditemukan: {FILE_EXCEL}\n"
            "Pastikan IDN.xlsx berada di folder yang sama "
            "dengan webinar_6.py."
        )

    df = pd.read_excel(
        FILE_EXCEL,
        sheet_name=SHEET_NAME
    )

    # Normalisasi nama kolom agar lebih mudah dicocokkan
    df.columns = [str(k).strip() for k in df.columns]

    print(f"File Excel       : {FILE_EXCEL.name}")
    print(f"Nama sheet       : {SHEET_NAME}")
    print(f"Jumlah baris awal: {len(df)}")

    # Filter provinsi jika kolom tersedia
    if "subnational1" in df.columns:
        df = df[
            df["subnational1"]
            .astype(str)
            .str.strip()
            .str.casefold()
            == PROVINSI.casefold()
        ].copy()
    else:
        print(
            "Peringatan: kolom subnational1 tidak ditemukan. "
            "Filter provinsi dilewati."
        )

    # Filter threshold jika kolom tersedia
    if "threshold" in df.columns:
        nilai_threshold = pd.to_numeric(
            df["threshold"], errors="coerce"
        )

        df = df[nilai_threshold == THRESHOLD].copy()
    else:
        print(
            "Peringatan: kolom threshold tidak ditemukan. "
            "Filter threshold dilewati."
        )

    # Validasi kolom yang diperlukan
    kolom_wajib = ["year", "tc_loss_ha"]

    for kolom in kolom_wajib:
        if kolom not in df.columns:
            raise ValueError(
                f"Kolom '{kolom}' tidak ditemukan pada Excel."
            )

    # Memastikan tahun dan luas kehilangan berbentuk angka
    df["year"] = pd.to_numeric(
        df["year"], errors="coerce"
    )

    df["tc_loss_ha"] = pd.to_numeric(
        df["tc_loss_ha"], errors="coerce"
    )

    df = df.dropna(
        subset=["year", "tc_loss_ha"]
    ).copy()

    df["year"] = df["year"].astype(int)

    if df.empty:
        raise ValueError(
            "Data kosong setelah filter. "
            "Periksa isi Excel dan nilai threshold."
        )

    # Jika kolom driver tidak tersedia, gunakan satu kategori umum
    if "driver" not in df.columns:
        df["driver"] = "Kategori tidak tersedia"

    df.to_csv(
        OUTPUT_DIR / "data_bengkulu_terfilter.csv",
        index=False
    )

    print(f"Jumlah data akhir: {len(df)}")
    print(
        f"Periode data     : "
        f"{df['year'].min()}–{df['year'].max()}"
    )

    return df

# 2. ANALISIS KEHILANGAN TUTUPAN POHON

def analisis_data(df):
    print("\n" + "=" * 60)
    print("HASIL ANALISIS DATA")
    print("=" * 60)

    # Menghitung kehilangan berdasarkan tahun
    tahunan = (
        df.groupby("year", as_index=False)["tc_loss_ha"]
        .sum()
        .sort_values("year")
    )

    tahunan.to_csv(
        OUTPUT_DIR / "kehilangan_tahunan.csv",
        index=False
    )

    print("\nKehilangan tutupan pohon per tahun (hektare):")
    print(tahunan.to_string(index=False))

    # Menghitung kehilangan berdasarkan kategori penyebab
    penyebab = (
        df.groupby("driver", as_index=False)["tc_loss_ha"]
        .sum()
        .sort_values("tc_loss_ha", ascending=False)
    )

    penyebab.to_csv(
        OUTPUT_DIR / "total_per_penyebab.csv",
        index=False
    )

    print("\nKehilangan berdasarkan kategori (hektare):")
    print(penyebab.to_string(index=False))

    total = tahunan["tc_loss_ha"].sum()

    print(
        f"\nTotal penjumlahan baris kategori: "
        f"{total:,.2f} hektare"
    )

    # Grafik kehilangan tahunan
    plt.figure(figsize=(10, 5))

    plt.plot(
        tahunan["year"],
        tahunan["tc_loss_ha"],
        marker="o",
        linewidth=2
    )

    plt.title(
        "Kehilangan Tutupan Pohon di Bengkulu per Tahun"
    )
    plt.xlabel("Tahun")
    plt.ylabel("Kehilangan (hektare)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "grafik_tahunan.png",
        dpi=160
    )

    plt.close()

    # Grafik kategori penyebab
    penyebab_plot = penyebab.sort_values("tc_loss_ha")

    plt.figure(figsize=(10, 6))

    plt.barh(
        penyebab_plot["driver"],
        penyebab_plot["tc_loss_ha"]
    )

    plt.title(
        "Kehilangan Tutupan Pohon Berdasarkan Kategori"
    )
    plt.xlabel("Kehilangan (hektare)")
    plt.ylabel("Kategori")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "grafik_penyebab.png",
        dpi=160
    )

    plt.close()

    return tahunan

# 3. PREDIKSI DENGAN LINEAR REGRESSION

def prediksi_deforestasi(tahunan):
    print("\n" + "=" * 60)
    print("PREDIKSI LINEAR REGRESSION")
    print("=" * 60)

    if len(tahunan) < 2:
        print(
            "Prediksi tidak dapat dilakukan karena "
            "dibutuhkan minimal dua tahun data."
        )
        return

    # Data input dan target
    X = tahunan[["year"]].to_numpy()
    y = tahunan["tc_loss_ha"].to_numpy()

    # Membuat dan melatih model
    model = LinearRegression()
    model.fit(X, y)

    # Evaluasi kecocokan pada data historis
    prediksi_historis = model.predict(X)

    mae = mean_absolute_error(
        y, prediksi_historis
    )

    rmse = np.sqrt(
        mean_squared_error(y, prediksi_historis)
    )

    r2 = r2_score(y, prediksi_historis)

    print("\nEvaluasi kecocokan tren historis:")
    print(f"MAE  : {mae:,.2f} hektare")
    print(f"RMSE : {rmse:,.2f} hektare")
    print(f"R²   : {r2:.4f}")

    # Membuat prediksi lima tahun berikutnya
    tahun_terakhir = int(tahunan["year"].max())

    tahun_prediksi = np.arange(
        tahun_terakhir + 1,
        tahun_terakhir + JUMLAH_TAHUN_PREDIKSI + 1
    )

    X_prediksi = tahun_prediksi.reshape(-1, 1)

    nilai_prediksi = model.predict(X_prediksi)

    hasil = pd.DataFrame({
        "year": tahun_prediksi,
        "prediksi_awal_ha": nilai_prediksi,
        "prediksi_nonnegatif_ha": np.maximum(
            nilai_prediksi, 0
        )
    })

    hasil.to_csv(
        OUTPUT_DIR / "hasil_prediksi.csv",
        index=False
    )

    print("\nPrediksi kehilangan tutupan pohon:")
    print(hasil.to_string(index=False))

    # Grafik historis dan prediksi
    plt.figure(figsize=(10, 5))

    plt.plot(
        tahunan["year"],
        tahunan["tc_loss_ha"],
        marker="o",
        label="Data historis"
    )

    plt.plot(
        tahunan["year"],
        prediksi_historis,
        linestyle="--",
        label="Garis regresi"
    )

    plt.plot(
        tahun_prediksi,
        nilai_prediksi,
        marker="o",
        linestyle="--",
        label="Prediksi"
    )

    plt.axvline(
        tahun_terakhir,
        linestyle=":",
        alpha=0.7
    )

    plt.title(
        "Prediksi Tren Kehilangan Tutupan Pohon di Bengkulu"
    )
    plt.xlabel("Tahun")
    plt.ylabel("Kehilangan (hektare)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "grafik_prediksi.png",
        dpi=160
    )

    plt.close()

# 4. PROGRAM UTAMA

def main():
    try:
        df = baca_data()

        tahunan = analisis_data(df)

        prediksi_deforestasi(tahunan)

        print("\n" + "=" * 60)
        print("PROGRAM SELESAI")
        print("=" * 60)

        print(f"Semua hasil tersimpan di: {OUTPUT_DIR}")

        print("\nFile yang dihasilkan:")
        print("- data_bengkulu_terfilter.csv")
        print("- kehilangan_tahunan.csv")
        print("- total_per_penyebab.csv")
        print("- hasil_prediksi.csv")
        print("- grafik_tahunan.png")
        print("- grafik_penyebab.png")
        print("- grafik_prediksi.png")

    except Exception as error:
        print(f"\nTerjadi kesalahan: {error}")


if __name__ == "__main__":
    main()
