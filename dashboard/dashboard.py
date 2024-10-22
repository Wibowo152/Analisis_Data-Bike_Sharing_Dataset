import streamlit as st
import pandas as pd
import matplotlib.pyplot as mpl
import seaborn as sb

# Membaca dataset 
tabel_hari = pd.read_csv('data/day.csv')
tabel_jam = pd.read_csv('data/hour.csv')

tabel_hari['dteday'] = pd.to_datetime(tabel_hari['dteday'])
tabel_jam['dteday'] = pd.to_datetime(tabel_jam['dteday'])

# Memberi judul 
st.title("Dashboard Sederhana - Penggunaan Sepeda")

# Pertanyaan pertama
# Berapa total sewa sepeda di setiap bulan dari tahun 2011 hingga 2012?
# Menghitung total penyewa sepeda setiap bulan
penyewa_sepeda_perbulan = tabel_hari.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()
# Menambahkan kolom 'year' yang bisa dibaca manusia (2011 jika 'yr' == 0, dan 2012 jika 'yr' == 1)
penyewa_sepeda_perbulan['year'] = penyewa_sepeda_perbulan['yr'].apply(lambda x: 2011 if x == 0 else 2012)
# Menggabungkan data tahun dan bulan dalam satu kolom untuk kemudahan visualisasi
penyewa_sepeda_perbulan['month_year'] = penyewa_sepeda_perbulan['year'].astype(str) + "-" + penyewa_sepeda_perbulan['mnth'].astype(str)
# Membuat diagram batang untuk total penyewaan per bulan dari 2011 hingga 2012
mpl.figure(figsize=(12, 6))
sb.barplot(x = 'month_year', y = 'cnt', data = penyewa_sepeda_perbulan, palette = 'coolwarm')
# Menambahkan label dan judul
mpl.xlabel('Bulan-Tahun')
mpl.ylabel('Total Penyewaan Sepeda')
mpl.title('Total Penyewaan Sepeda di Setiap Bulan (2011-2012)')
mpl.xticks(rotation=45)
# Menampilkan diagram
mpl.tight_layout()
st.pyplot(mpl)

# Pertanyaan kedua
# Pada jam berapa penyewaan sepeda mengalami puncaknya?
# Menghitung total penyewaan per jam
penyewa_perjam = tabel_jam.groupby('hr')['cnt'].sum().reset_index()
# Membuat line chart untuk jam penyewaan
mpl.figure(figsize=(10, 6))
sb.lineplot(x = 'hr', y = 'cnt', data = penyewa_perjam, marker = 'o', color = 'blue')
# Menambahkan label dan judul
mpl.xlabel('Jam')
mpl.ylabel('Total Penyewaan Sepeda')
mpl.title('Total Penyewaan Sepeda di Setiap Jam (Puncak Jam Penyewaan)')
mpl.xticks(range(0, 24)) 
# Menampilkan diagram
mpl.tight_layout()
st.pyplot(mpl)