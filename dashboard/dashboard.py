import pandas as pd
import matplotlib.pyplot as mpl
import seaborn as sb
import streamlit as st

# Membaca dataset 
tabel_hari = pd.read_csv('data/day.csv')
tabel_jam = pd.read_csv('data/hour.csv')
tabel_hari['dteday'] = pd.to_datetime(tabel_hari['dteday'])
tabel_jam['dteday'] = pd.to_datetime(tabel_jam['dteday'])

# Mengonversi kolom 'date' ke tipe datetime untuk kedua tabel
tabel_hari['date'] = pd.to_datetime(tabel_hari['dteday'])
tabel_jam['date'] = pd.to_datetime(tabel_jam['dteday'])

# Memberi Judul
st.title("Analisis Dataset Bike Sharing")
# Blok Fungsi Filter
st.sidebar.header('Filters')
# Menentukan rentang tanggal untuk filter (misalnya, dari 1 Januari 2011 hingga 31 Desember 2012)
start_date = st.sidebar.date_input("Start Date", tabel_hari['dteday'].min())
end_date = st.sidebar.date_input("End Date", tabel_hari['dteday'].max())
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Memfilter data berdasarkan rentang tanggal
filtered_data_hari = tabel_hari[(tabel_hari['date'] >= start_date) & (tabel_hari['date'] <= end_date)]
filtered_data_jam = tabel_jam[(tabel_jam['date'] >= start_date) & (tabel_jam['date'] <= end_date)]

# Bagian 1: Menghitung total penyewa sepeda setiap bulan
filtered_data_hari['yr'] = filtered_data_hari['date'].dt.year - 2011  # Membuat tahun menjadi 0 untuk 2011 dan 1 untuk 2012
filtered_data_hari['mnth'] = filtered_data_hari['date'].dt.month

# Menghitung total penyewa sepeda per bulan
penyewa_sepeda_perbulan = filtered_data_hari.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()

# Menambahkan kolom 'year' yang bisa dibaca manusia
penyewa_sepeda_perbulan['year'] = penyewa_sepeda_perbulan['yr'].apply(lambda x: 2011 if x == 0 else 2012)

# Menggabungkan data tahun dan bulan dalam satu kolom untuk kemudahan visualisasi
penyewa_sepeda_perbulan['month_year'] = penyewa_sepeda_perbulan['year'].astype(str) + "-" + penyewa_sepeda_perbulan['mnth'].astype(str)

# Bagian 2: Menghitung total penyewaan per jam
penyewa_perjam = filtered_data_jam.groupby('hr')['cnt'].sum().reset_index()

# Membuat visualisasi

# Visualisasi total penyewaan per bulan
mpl.figure(figsize=(12, 6))
sb.barplot(x='month_year', y='cnt', data=penyewa_sepeda_perbulan, palette='coolwarm')

# Menambahkan label dan judul untuk diagram batang
mpl.xlabel('Bulan-Tahun')
mpl.ylabel('Total Penyewaan Sepeda')
mpl.title('Total Penyewaan Sepeda di Setiap Bulan (2011-2012)')
mpl.xticks(rotation=45)
mpl.tight_layout()
st.pyplot(mpl)

# Visualisasi total penyewaan per jam
mpl.figure(figsize=(10, 6))
sb.lineplot(x='hr', y='cnt', data=penyewa_perjam, marker='o', color='blue')

# Menambahkan label dan judul untuk diagram garis
mpl.xlabel('Jam')
mpl.ylabel('Total Penyewaan Sepeda')
mpl.title('Total Penyewaan Sepeda di Setiap Jam (Puncak Jam Penyewaan)')
mpl.xticks(range(0, 24))
mpl.tight_layout()
st.pyplot(mpl)
