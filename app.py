import streamlit as st
import re
from collections import Counter
import random

# Konfigurasi halaman
st.set_page_config(page_title="Penganalisa & Prediksi 4D", layout="wide")

st.title("📊 Penganalisa & Prediksi Angka 4D")
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
        
        pilihan = st.selectbox("🎯 Pilih Grup Data yang Ingin Dianalisa & Diprediksi:", opsi_grup)
        
        if pilihan == "✨ Tampilkan Semua Grup (Gabungan Keseluruhan)":
            data_aktif = data_4d
            st.success("Menampilkan hasil analisa dari **Seluruh Data Gabungan**.")
        else:
            indeks_grup = opsi_grup.index(pilihan) - 1
            data_aktif = daftar_grup[indeks_grup]
            st.success(f"Menampilkan hasil analisa untuk **{pilihan}**.")
            
        st.markdown("---")
        
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Rangkum Terbanyak", "🔢 Analisa 2D Depan", "🎯 Analisa 2D Tengah", "🔮 Prediksi Angka"])
        
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
        groups_depan = {}
        with tab2:
            st.subheader("Analisa Pasangan 2D Belakang yang Belum Muncul")
            for num in data_aktif:
                depan = num[:2]
                belakang = num[2:]
                if depan not in groups_depan:
                    groups_depan[depan] = set()
                groups_depan[depan].add(belakang)
            
            for depan in sorted(groups_depan.keys()):
                muncul_belakang = groups_depan[depan]
                count_depan = len(muncul_belakang)
                
                semua_2d = [f"{i:02d}" for i in range(100)]
                belum_muncul = [depan + b for b in semua_2d if b not in muncul_belakang]
                
                contoh_belakang = list(muncul_belakang) if muncul_belakang else "00"
                contoh_full = depan + contoh_belakang
                
                with st.expander(f"Prefix 2D Depan: {depan} ({count_depan} variasi ditemukan)"):
                    st.write(f"**{contoh_full} ; {count_depan}x ; {contoh_full}**")
                    if belum_muncul:
                        st.markdown("**Belum Muncul:**")
                        st.write(" * ".join(belum_muncul))

        # --- TAB 3: ANALISA 2D TENGAH ---
        groups_tengah = {}
        contoh_4d_asli = {} 
        with tab3:
            st.subheader("Analisa Pasangan Ekor dari 2D Tengah")
            for num in data_aktif:
                tengah = num[1:3]
                ekor = num
                if tengah not in groups_tengah:
                    groups_tengah[tengah] = set()
                    contoh_4d_asli[tengah] = num
                groups_tengah[tengah].add(ekor)
            
            for tengah in sorted(groups_tengah.keys()):
                muncul_ekor = groups_tengah[tengah]
                count_tengah = len(muncul_ekor)
                
                semua_ekor = [str(i) for i in range(10)]
                belum_muncul_3d = [tengah + ekor for ekor in semua_ekor if ekor not in muncul_ekor]
                contoh_full = contoh_4d_asli[tengah]
                
                with st.expander(f"2D Tengah: {tengah} ({count_tengah} ekor ditemukan)"):
                    st.write(f"**{contoh_full} ; {count_tengah}x ; {contoh_full}**")
                    if belum_muncul_3d:
                        st.markdown(f"**Belum muncul dengan tengah {tengah}:**")
                        st.write(" * ".join(belum_muncul_3d) + " *")

        # --- TAB 4: PREDIKSI ANGKA (FITUR BARU) ---
        with tab4:
            st.subheader("🎲 Hasil Prediksi Algoritma Generator")
            
            # Pengumpulan Data untuk Algoritma
            # 1. Kumpulkan semua angka yang BELUM MUNCUL berdasarkan analisa 2D Depan (Kombinasi 4D penuh)
            semua_2d = [f"{i:02d}" for i in range(100)]
            pool_4d_belum_muncul = []
            for d_depan in groups_depan.keys():
                for d_belakang in semua_2d:
                    if d_belakang not in groups_depan[d_depan]:
                        pool_4d_belum_muncul.append(d_depan + d_belakang)
                        
            # 2. Kumpulkan semua angka kombinasi 3D yang BELUM MUNCUL dari analisa 2D Tengah
            pool_3d_belum_muncul = []
            semua_ekor = [str(i) for i in range(10)]
            for d_tengah in groups_tengah.keys():
                for d_ekor in semua_ekor:
                    if d_ekor not in groups_tengah[d_tengah]:
                        pool_3d_belum_muncul.append(d_tengah + d_ekor)
                        
            # 3. Kumpulkan tren 2D Belakang yang paling sering muncul
            list_2d_belakang = [num[2:] for num in data_aktif]
            counts_2d_belakang = Counter(list_2d_belakang)
            
            # Eksekusi Tampilan Kolom Prediksi
            col_p1, col_p2, col_p3 = st.columns(3)
            
            with col_p1:
                st.markdown("### 🔴 Prediksi 4D (100 Line)")
                # Jika pool angka unik kurang dari 100, campur dengan kombinasi acak terstruktur
                if len(pool_4d_belum_muncul) >= 100:
                    prediksi_4d = random.sample(pool_4d_belum_muncul, 100)
                else:
                    # Isi sisanya dengan acakan dari pola depan yang aktif
                    sisa = 100 - len(pool_4d_belum_muncul)
                    tambahan = [random.choice(list(groups_depan.keys())) + f"{random.randint(0,99):02d}" for _ in range(sisa)]
                    prediksi_4d = pool_4d_belum_muncul + tambahan
                
                # Tampilkan hasil
                st.text_area("Salin Angka 4D:", value=" ".join(sorted(prediksi_4d)), height=200)
                st.info("**Alasan Memilih:**\nAngka-angka ini dipilih berdasarkan pola **2D Depan** yang paling aktif pada data Anda, namun dipasangkan dengan variasi **2D Belakang yang belum pernah muncul sama sekali**. Secara statistik probabilitas, pola yang belum pecah memiliki potensi matang untuk keluar berikutnya.")

            with col_p2:
                st.markdown("### 🟡 Prediksi 3D (50 Line)")
                if len(pool_3d_belum_muncul) >= 50:
                    prediksi_3d = random.sample(pool_3d_belum_muncul, 50)
                else:
                    sisa_3d = 50 - len(pool_3d_belum_muncul)
                    tambahan_3d = [random.choice(list(groups_tengah.keys())) + str(random.randint(0,9)) for _ in range(sisa_3d)]
                    prediksi_3d = pool_3d_belum_muncul + tambahan_3d
                    
                st.text_area("Salin Angka 3D:", value=" ".join(sorted(prediksi_3d)), height=200)
                st.info("**Alasan Memilih:**\nMenggunakan basis data **2D Tengah** murni yang paling sering lewat di dalam grup Anda, kemudian dicarikan pasangan **Digit Ekor terakhir (0-9) yang masih kosong (belum ketemu)**. Ini mempersempit pencarian ekor lemah.")

            with col_p3:
                st.markdown("### 🟢 Prediksi 2D Belakang (20 Line)")
                # Ambil 20 nomor 2D belakang yang paling sering muncul (Tren Kuat)
                top_2d_belakang = [num for num, count in counts_2d_belakang.most_common(20)]
                
                # Jika data kurang dari 20 variasi, lengkapi acak
                if len(top_2d_belakang) < 20:
                    sisa_2d = 20 - len(top_2d_belakang)
                    while len(top_2d_belakang) < 20:
                        acak_2d = f"{random.randint(0,99):02d}"
                        if acak_2d not in top_2d_belakang:
                            top_2d_belakang.append(acak_2d)
                            
                st.text_area("Salin Angka 2D Belakang:", value=" ".join(sorted(top_2d_belakang)), height=200)
                st.info("**Alasan Memilih:**\nBerbeda dengan sistem 4D dan 3D yang mencari kesenjangan kosong, prediksi 2D belakang ini murni didasarkan pada **Hukum Tren/Arus Terkuat (Top Frequency)**. Angka puluhan dan satuan yang paling rajin keluar di data Anda cenderung memiliki efek domino untuk muncul kembali.")
else:
    st.warning("Silakan masukkan data angka terlebih dahulu pada kolom di atas.")
