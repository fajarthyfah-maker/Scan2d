import streamlit as st
import re
from collections import Counter

# Set halaman agar lebih lebar
st.set_page_config(page_title="Penganalisa 4D", layout="wide")

st.title("📊 Penganalisa Angka 4D")
st.markdown("---")

# Input Area
input_data = st.text_area("Tempel ribuan angka 4 digit di sini:", height=250, placeholder="Contoh: 1234 5678 1234 1122...")

def get_clean_data(raw_text):
    # Regex untuk ambil angka tepat 4 digit
    return re.findall(r'\b\d{4}\b', raw_text)

if input_data:
    data_4d = get_clean_data(input_data)
    total_data = len(data_4d)
    
    st.info(f"Total angka 4D terdeteksi: {total_data}")
    
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚀 Rangkum Terbanyak", use_container_width=True):
            counts = Counter(data_4d)
            st.subheader("Urutan Muncul Terbanyak")
            for num, count in counts.most_common():
                st.write(f"**{num}** : {count}x")

    with col2:
        if st.button("🔍 Rangkum 2D Depan", use_container_width=True):
            st.subheader("Analisa 2D Depan & Pasangan Kosong")
            
            # Kelompokkan berdasarkan 2 digit depan
            groups = {}
            for num in data_4d:
                depan = num[:2]
                belakang = num[2:]
                if depan not in groups:
                    groups[depan] = set() # Pakai set agar unik
                groups[depan].add(belakang)
            
            # Urutkan berdasarkan 2D depan (00-99)
            for depan in sorted(groups.keys()):
                muncul_belakang = groups[depan]
                count_depan = len(muncul_belakang)
                
                # Cari yang belum muncul
                semua_2d = [f"{i:02d}" for i in range(100)]
                belum_muncul = [depan + b for b in semua_2d if b not in muncul_belakang]
                
                # Ambil contoh satu angka lengkap untuk label
                contoh_full = depan + list(muncul_belakang)[0]
                
                with st.expander(f"Depan {depan} ({count_depan} variasi muncul)"):
                    st.write(f"**{contoh_full} ; {count_depan}x ; {contoh_full}**")
                    if belum_muncul:
                        st.markdown("**Belum Muncul:**")
                        st.write(" * ".join(belum_muncul))
else:
    st.warning("Silakan masukkan data angka dulu ya!")
