import streamlit as st
import re
from collections import Counter

# Konfigurasi halaman
st.set_page_config(page_title="Penganalisa 4D Multi-Grup", layout="wide")

st.title("📊 Penganalisa Angka 4D (Sistem Grup per 100 Baris)")
st.markdown("---")

# Input Area
input_data = st.text_area("Tempel ribuan angka 4 digit di sini (urutan paling atas = paling lama):", height=200)

def get_clean_data(raw_text):
    return re.findall(r'\b\d{4}\b', raw_text)

if input_data:
    data_4d = get_clean_data(input_data)
    total_angka = len(data_4d)
    
    if total_angka == 0:
        st.warning("Tidak ditemukan angka 4 digit yang valid.")
    else:
        st.info(f"Total angka 4D terdeteksi: {total_angka} angka.")
        
        # --- PROSES PEMBAGIAN GRUP (PER 100 ANGKA) ---
        ukuran_grup = 100
        daftar_grup = [data_4d[i:i + ukuran_grup] for i in range(0, total_angka, ukuran_grup)]
        
        opsi_grup = [f"Grup {i+1} (Angka ke-{i*ukuran_grup+1} sampai {min((i+1)*ukuran_grup, total_angka)})" for i in range(len(daftar_grup))]
        opsi_grup.insert(0, "✨ Tampilkan Semua Grup (Gabungan Keseluruhan)")
        
        pilihan = st.selectbox("🎯 Pilih Grup Data yang Ingin Dianalisa:", opsi_grup)
        
        if pilihan == "✨ Tampilkan Semua Grup (Gabungan Keseluruhan)":
            data_aktif = data_4d
            st.success("Menampilkan hasil analisa dari **Seluruh Data Gabungan**.")
        else:
            indeks_grup = opsi_grup.index(pilihan) - 1
            data_aktif = daftar_grup[indeks_grup]
            st.success(f"Menampilkan hasil analisa untuk **{pilihan}**.")
            
        st.markdown("---")
        
        tab1, tab2, tab3 = st.tabs(["📋 Rangkum Terbanyak", "🔢 Analisa 2D Depan", "🎯 Analisa 2D Tengah"])
        
        # --- TAB 1: RANGKUM TERBANYAK ---
        with tab1:
            st.subheader("Urutan Muncul Terbanyak")
            counts = Counter(data_aktif)
            col_r1, col_r2, col_r3 = st.columns(3)
            items = counts.most_common()
            
            for idx, (num, count) in enumerate(items):
                teks_tampil = f"**{num}** : {count}x"
                if idx % 3 == 0:
                    col_r1.write(teks_tampil)
                elif idx % 3 == 1:
                    col_r2.write(teks_tampil)
                else:
                    col_r3.write(teks_tampil)

        # --- TAB 2: ANALISA 2D DEPAN ---
        with tab2:
            st.subheader("Analisa Pasangan 2D Belakang yang Belum Muncul")
            
            groups_depan = {}
            contoh_4d_depan = {} # Menyimpan contoh angka 4D utuh untuk display
            
            for num in data_aktif:
                depan = num[:2]
                belakang = num[2:]
                if depan not in groups_depan:
                    groups_depan[depan] = set()
                    contoh_4d_depan[depan] = num
                groups_depan[depan].add(belakang)
            
            for depan in sorted(groups_depan.keys()):
                muncul_belakang = groups_depan[depan]
                count_depan = len(muncul_belakang)
                
                semua_2d = [f"{i:02d}" for i in range(100)]
                belum_muncul = [depan + b for b in semua_2d if b not in muncul_belakang]
                
                # Menggunakan contoh angka asli utuh yang terdeteksi
                contoh_full = contoh_4d_depan[depan]
                
                with st.expander(f"Prefix 2D Depan: {depan} ({count_depan} variasi ditemukan)"):
                    st.write(f"**{contoh_full} ; {count_depan}x ; {contoh_full}**")
                    if belum_muncul:
                        st.markdown("**Belum Muncul:**")
                        st.write(" * ".join(belum_muncul) + " *")

        # --- TAB 3: ANALISA 2D TENGAH ---
        with tab3:
            st.subheader("Analisa Pasangan Ekor dari 2D Tengah")
            st.caption("Mencari angka belakang (digit ke-4) dari 0-9 yang belum pernah berpasangan dengan 2D Tengah (digit ke-2 & ke-3).")
            
            groups_tengah = {}
            contoh_4d_tengah = {} # Menyimpan contoh angka 4D utuh untuk display
            
            for num in data_aktif:
                tengah = num[1:3]     # Digit ke-2 dan ke-3
                ekor = num[3]         # Digit ke-4 (Ekor)
                
                if tengah not in groups_tengah:
                    groups_tengah[tengah] = set()
                    contoh_4d_tengah[tengah] = num
                
                groups_tengah[tengah].add(ekor)
            
            for tengah in sorted(groups_tengah.keys()):
                muncul_ekor = groups_tengah[tengah]
                count_tengah = len(muncul_ekor)
                
                semua_ekor = [str(i) for i in range(10)]
                belum_muncul_3d = [tengah + e for e in semua_ekor if e not in muncul_ekor]
                
                contoh_full = contoh_4d_tengah[tengah]
                
                with st.expander(f"2D Tengah: {tengah} ({count_tengah} ekor ditemukan)"):
                    st.write(f"**{contoh_full} ; {count_tengah}x ; {contoh_full}**")
                    if belum_muncul_3d:
                        st.markdown(f"**Belum muncul dengan tengah {tengah}:**")
                        st.write(" * ".join(belum_muncul_3d) + " *")
                    else:
                        st.info(f"Semua ekor (0-9) sudah berpasangan dengan angka tengah {tengah}.")
else:
    st.warning("Silakan masukkan data angka terlebih dahulu pada kolom di atas.")
