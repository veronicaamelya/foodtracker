import streamlit as st
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import matplotlib.pyplot as plt


# ----------------- SETUP -----------------
st.set_page_config(page_title="Food Calorie Tracker", layout="centered")
st.title("🍱 Food Calorie Tracker")

# Load data dari nutrition.csv
df_makanan = pd.read_csv("nutrition.csv")

# Inisialisasi session state
if 'log' not in st.session_state:
    st.session_state.log = []



# ----------------- MANUAL INPUT -----------------
st.markdown("---")
st.subheader("📂 Pilih Makanan")

selected_food = st.selectbox("Pilih jenis makanan", df_makanan['name'].tolist())

if st.button("➕ Tambahkan manual ke log hari ini"):
    selected_row = df_makanan[df_makanan['name'] == selected_food].iloc[0]
    macros = {
        'carbohydrate': selected_row['carbohydrate'],
        'proteins': selected_row['proteins'],
        'fat': selected_row['fat']
    }
    st.session_state.log.append({
        'tanggal': datetime.date.today().isoformat(),
        'makanan': selected_food,
        'kalori': selected_row['calories'],
        'karbo': macros['carbohydrate'],
        'protein': macros['proteins'],
        'lemak': macros['fat']
    })
    st.success(f"✅ {selected_food.title()} berhasil ditambahkan ke log!")

# ----------------- RINGKASAN HARI INI -----------------
st.header("📊 Ringkasan Konsumsi Hari Ini")
hari_ini = datetime.date.today().isoformat()
log_df = pd.DataFrame(st.session_state.log)

if not log_df.empty and 'tanggal' in log_df.columns:
    log_today = log_df[log_df['tanggal'] == hari_ini]

    if not log_today.empty:
        st.dataframe(log_today[['makanan', 'kalori', 'karbo', 'protein', 'lemak']])

        total_kal = log_today['kalori'].sum()
        total_k = log_today['karbo'].sum()
        total_p = log_today['protein'].sum()
        total_l = log_today['lemak'].sum()

        st.subheader(f"🔥 Total Kalori: {total_kal} kcal")
        st.write(f"💪 Karbo: {total_k}g | Protein: {total_p}g | Lemak: {total_l}g")

        fig, ax = plt.subplots()
        ax.pie([total_k, total_p, total_l], labels=['Karbo', 'Protein', 'Lemak'],
               autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)
    else:
        st.info("Belum ada makanan yang ditambahkan hari ini.")
else:
    st.info("Belum ada log konsumsi hari ini.")

# ----------------- SIMPAN LOG -----------------
if not log_df.empty:
    if st.button("📀 Simpan Log ke CSV"):
        log_df.to_csv("food_log.csv", index=False)
        st.success("📁 Log berhasil disimpan ke food_log.csv.")

# ----------------- RINGKASAN 7 HARI -----------------
st.markdown("---")
st.subheader("🗖 Riwayat Kalori 7 Hari Terakhir")

if not log_df.empty and 'tanggal' in log_df.columns:
    df = log_df.copy()
    df['tanggal'] = pd.to_datetime(df['tanggal'])
    last_7_days = df[df['tanggal'] >= (datetime.datetime.today() - pd.Timedelta(days=6))]

    if not last_7_days.empty:
        kal_per_hari = last_7_days.groupby(last_7_days['tanggal'].dt.date)['kalori'].sum()

        fig, ax = plt.subplots()
        kal_per_hari.plot(kind='bar', ax=ax, color='skyblue')
        ax.set_ylabel("Kalori")
        ax.set_xlabel("Tanggal")
        ax.set_title("Total Kalori per Hari")
        st.pyplot(fig)
    else:
        st.info("Belum ada data konsumsi 7 hari terakhir.")
else:
    st.info("Belum ada log untuk ditampilkan.")
