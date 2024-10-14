import streamlit as st
import pandas as pd
import matplotlib.pyplot as mpl
import seaborn as sb

# Membaca dataset 
tabel_hari = pd.read_csv('data/day.csv')
tabel_jam = pd.read_csv('data/hour.csv')

tabel_hari['dteday'] = pd.to_datetime(tabel_hari['dteday'])
tabel_jam['dteday'] = pd.to_datetime(tabel_jam['dteday'])

st.title("Dashboard Sederhana - Penggunaan Sepeda")

st.sidebar.header("Filter Data")

year_filter = st.sidebar.selectbox('Pilih Tahun (0 = 2011, 1 = 2012)', tabel_hari['yr'].unique())

filtered_day_data = tabel_hari[tabel_hari['yr'] == year_filter]
filtered_hour_data = tabel_jam[tabel_jam['yr'] == year_filter]

#1 Pengaruh suhu harian pada pola penggunaan sepeda di berbagai jam pada hari
merged1 = pd.merge(tabel_jam, tabel_hari[['dteday', 'temp']], on='dteday', suffixes=('_jam', '_hari'))
avg = merged1.groupby(['temp_hari', 'hr'])['cnt'].mean().reset_index()

mpl.figure(figsize=(12, 6))
sb.lineplot(data = avg, x='hr', y='cnt', hue='temp_hari', palette='coolwarm', linewidth=2.5)

mpl.title('Pengaruh Suhu Harian terhadap Pola Penggunaan Sepeda per Jam')
mpl.xlabel('Jam (0-23)')
mpl.ylabel('Rata-rata Jumlah Pengguna')
mpl.legend(title='Suhu Harian', bbox_to_anchor=(1.05, 1), loc='upper left')
mpl.tight_layout()
st.pyplot(mpl)

#2 Pengaruh kelembaban harian terhadap variasi penggunaan sepeda per jam
merged2 = pd.merge(tabel_hari, tabel_jam[['dteday', 'hum', 'windspeed']], on = 'dteday', suffixes = ('_hourly', '_daily'))
print(merged2.head())

mpl.figure(figsize=(40, 18))
sb.barplot(x = 'hum_daily', y = ('cnt'), data = merged2, color = 'red')
mpl.title('Pengaruh Kelembapan Terhadap Jumlah Pengguna Sepeda Tiap Jam')
mpl.xlabel('Kelembapan Udara Harian')
mpl.ylabel('Jumlah Pengguna Sepeda Tiap Jam')
mpl.legend(title = 'Jam (hr)', loc = 'upper right')
st.pyplot(mpl)

st.sidebar.markdown("Data: Dataset Penggunaan Sepeda")