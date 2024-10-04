import pandas as pd
import matplotlib.pyplot as mpl
import seaborn as sb
import streamlit as sl

sb.set(style = 'dark')
tabel_hari = pd.read_csv('data/day.csv')
tabel_jam = pd.read_csv('data/hour.csv')

sl.title("ANALISIS BIKE SHARING DATASET")

tabel_hari['dteday'] = pd.to_datetime(tabel_hari['dteday'])
tabel_jam['dteday'] = pd.to_datetime(tabel_jam['dteday'])

sl.sidebar.header('Filters')

tgl_str = sl.sidebar.date_input("Start Date", tabel_hari['dteday'].min())
tgl_str =pd.to_datetime(tgl_str)

tgl_end = sl.sidebar.date_input("End Date", tabel_hari['dteday'].max())
tgl_end =pd.to_datetime(tgl_end)

filter_hari = tabel_hari[(tabel_hari['dteday'] >= tgl_str) & (tabel_hari['dteday'] <= tgl_end)]
filter_jam = tabel_jam[(tabel_jam['dteday'] >= tgl_str) & (tabel_jam['dteday'] <= tgl_end)]

#
tabel_jam.hist()

#
merged1 = pd.merge(tabel_hari, tabel_jam[['dteday', 'temp']], on = 'dteday', suffixes = ('_hour', '_day'))

daily_avg = tabel_hari.groupby('dteday')['temp'].mean().reset_index()

merged1 = pd.merge(tabel_jam, daily_avg, on = 'dteday')

mpl.figure(figsize=(14,7))
mpl.subplot(2,1,1)
mpl.plot(merged1['hr'], merged1['hr'], label = 'Hourly Temperature', color = 'orange')
mpl.xlabel('Hour of the Day')
mpl.ylabel('Hourly Temperature vs Total Bike Usage')
mpl.grid(True)

mpl.subplot(2,1,2)
mpl.plot(merged1['hr'], merged1['cnt'], label = 'Hourly Bike Usage', color = 'blue')
mpl.xlabel('Hour of the Day')
mpl.ylabel('Bike Usage')
mpl.grid(True)

mpl.tight_layout()
mpl.show()

#
merged2 = pd.merge(tabel_hari, tabel_jam[['dteday', 'hum', 'windspeed']], on = 'dteday', suffixes = ('_hourly', '_daily'))
print(merged2.head())

mpl.figure(figsize=(10,6))
sb.scatterplot(x = 'hum_daily', y = ('cnt'), data = merged2, palette = 'red')
mpl.title('Pengaruh Kelembapan Terhadap Jumlah Pengguna Sepeda Tiap Jam')
mpl.xlabel('Kelembapan Udara Harian')
mpl.ylabel('Jumlah Pengguna Sepeda Tiap Jam')
mpl.legend(title = 'Jam (hr)', loc = 'upper right')
mpl.show()