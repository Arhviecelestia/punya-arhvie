import base64
import os
import pandas as pd
import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Minecraft Biome Explorer", layout="wide")


# --- 1. KOSTUMISASI BACKGROUND MINECRAFT (FILE LOKAL) ---
# Fungsi khusus untuk mengubah gambar lokal menjadi format teks Base64 agar bisa dibaca CSS
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


# Tentukan nama file gambar lokal untuk background di sini
nama_file_bg = "background_minecraft.png"

# Jalankan pengecekan file background lokal
if os.path.exists(nama_file_bg):
    img_base64 = get_base64_image(nama_file_bg)
    bg_style = f"url('data:image/png;base64,{img_base64}')"
else:
    # Cadangan warna abu-abu gelap khas batuan Minecraft jika file tidak ditemukan
    bg_style = "linear-gradient(#2c2c2c, #1a1a1a)"

st.markdown(
    f"""
    <style>
    /* Mengubah background halaman utama website menggunakan gambar lokal */
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), {bg_style};
        background-attachment: fixed;
        background-size: cover;
        background-position: center;
    }}
    
    /* Membuat teks judul, subheader, dan teks tab berwarna putih dengan bayangan hitam agar mudah dibaca */
    h1, h2, h3, p, span, .stTabs button {{
        color: #ffffff !important;
        text-shadow: 2px 2px 4px #000000;
    }}
    
    /* Memberikan efek kotak transparan gelap di sekitar informasi biome */
    [data-testid="stColumn"] {{
        background-color: rgba(0, 0, 0, 0.55);
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #3c3c3c;
        margin-bottom: 20px;
    }}
    
    /* Mengatur gaya garis pembatas (divider) agar terlihat serasi */
    hr {{
        border-color: #555555 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# --- 2. BANNER ATAS (VIDEO MP4) ---
# Pastikan file 'banner_minecraft.mp4' sudah diletakkan di folder yang sama
if os.path.exists("banner_minecraft.mp4"):
    st.video(
        "banner_minecraft.mp4",
        autoplay=True,  # Otomatis berputar saat web dibuka
        loop=True,  # Berputar terus-menerus tanpa berhenti (looping)
        muted=True,  # Suara dimatikan secara otomatis agar estetik
        subtitles=None,
    )
elif os.path.exists("anggrekku.jpeg"):
    # Cadangan gambar lama jika file mp4 belum ada di folder agar tidak error
    st.image("anggrekku.jpeg", use_container_width=True)

st.title("🧭 Minecraft Biome Explorer")
st.write(
    "Jelajahi berbagai karakteristik, ekosistem, dan rahasia di dalam setiap jengkal dunia kotak-kotak."
)
st.divider()


# --- 3. PROSES DATA BIOME ---
try:
    if os.path.exists("data_anggrek1.csv"):
        # Membaca data dari file CSV yang sama
        df = pd.read_csv("data_anggrek1.csv")

        # Bersihkan data dari baris kosong pada kolom nama dan foto
        df = df.dropna(subset=["nama", "foto"])

        # Ambil daftar kategori dimensi unik (Overworld, Nether, The End)
        daftar_kategori = df["kategori"].unique()

        # Looping Per Dimensi
        for kat in daftar_kategori:
            st.header(f"🪐 Dimensi: {str(kat).upper()}")
            data_per_kat = df[df["kategori"] == kat]

            # Membuat grid 2 kolom (menyamping) agar deskripsi teks biome punya ruang yang luas
            cols = st.columns(2)

            for index, row in data_per_kat.reset_index().iterrows():
                # Menentukan kolom utama tempat biome akan muncul (kiri atau kanan)
                with cols[index % 2]:

                    # Membuat sub-kolom internal di dalam kotak produk: Kiri untuk gambar, Kanan untuk penjelasan
                    sub_col_foto, sub_col_detail = st.columns([5, 6])

                    # --- SUB-KOLOM KIRI: FOTO / PREVIEW BIOME ---
                    with sub_col_foto:
                        list_foto = [
                            f.strip()
                            for f in str(row["foto"]).split(",")
                            if f.strip()
                        ]

                        if len(list_foto) > 1:
                            # Jika foto biome lebih dari 1, otomatis pakai sistem Tab
                            tabs = st.tabs(
                                [f"View {i+1}" for i in range(len(list_foto))]
                            )
                            for i, file_foto in enumerate(list_foto):
                                with tabs[i]:
                                    if os.path.exists(file_foto):
                                        st.image(
                                            file_foto, use_container_width=True
                                        )
                                    else:
                                        st.caption(
                                            f"⚠️ {file_foto} tidak ditemukan"
                                        )

                        elif len(list_foto) == 1:
                            # Jika hanya ada 1 foto, tampilkan langsung tanpa tab
                            file_foto = list_foto[0]
                            if os.path.exists(file_foto):
                                st.image(file_foto, use_container_width=True)
                            else:
                                st.warning(
                                    f"Foto {file_foto} tidak ditemukan"
                                )
                        else:
                            st.error("Gambar biome tidak tersedia")

                    # --- SUB-KOLOM KANAN: PENJELASAN BIOME ---
                    with sub_col_detail:
                        st.subheader(row["nama"])

                        # Mengambil data deskripsi penjelasan biome dari CSV
                        if "deskripsi" in row and pd.notna(row["deskripsi"]):
                            deskripsi_teks = row["deskripsi"]
                        else:
                            deskripsi_teks = "*Belum ada penjelasan deskripsi untuk biome ini. Silakan update di file CSV Anda.*"

                        st.write(deskripsi_teks)

                    # Memberi garis penutup tipis antar biome di dalam grid
                    st.write("---")

            st.divider()  # Garis tebal pembatas antar jenis dimensi

    else:
        st.error(
            "❌ File 'data_anggrek1.csv' tidak ditemukan. Pastikan file CSV berada di folder yang sama."
        )

except Exception as e:
    st.error(f"❌ Terjadi kesalahan sistem: {e}")


# --- 4. FOOTER ---
st.write("")
st.write("")
st.divider()
st.caption("© 2026 Minecraft Biome Wiki & Explorer - Dibuat dengan Streamlit")