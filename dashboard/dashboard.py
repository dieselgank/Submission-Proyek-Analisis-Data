import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

sns.set(style='dark')

#Menyiapkan DataFrame
def create_count_by_hour_df(df):
    hour_count_df = df.groupby(by='hour').agg({
        'count_rental': 'sum'
    })
    return hour_count_df

def create_count_by_day_df(df):
    day_count_df_2011 = df.query(
        str('date_day >= "2011-01-01" and date_day < "2012-12-31"')
    )
    return day_count_df_2011

def create_total_registered_df(df):
    registered_df = df.groupby(by='date_day').agg({
        'registered':'sum'
    })
    registered_df = registered_df.reset_index()
    registered_df.rename(columns={
        'registered': 'registered_sum'
    }, inplace=True)
    return registered_df

def create_total_casual_df(df):
    casual_df = df.groupby(by='date_day').agg({
        'casual':['sum']
    })
    casual_df = casual_df.reset_index()
    casual_df.rename(columns={
        'casual': 'casual_sum'
    }, inplace=True)
    return casual_df

def create_sum_order(df):
    sum_order_items_df = df.groupby(by='hour').count_rental.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def create_season(df):
    season_df = df.groupby(by='season').count_rental.sum().reset_index()
    return season_df

day_df = pd.read_csv('../dashboard/day_clean_df.csv')
hour_df = pd.read_csv('hour_clean_df.csv')  

datetime_columns = ['date_day']

day_df.sort_values(by='date_day', inplace=True)
day_df.reset_index(inplace=True)

hour_df.sort_values(by='date_day', inplace=True)
hour_df.reset_index(inplace=True)

for column in datetime_columns:
    day_df['column'] = pd.to_datetime(day_df[column])
    hour_df['column'] = pd.to_datetime(hour_df[column])
    
#Membuat Komponen Filter
min_date_day = day_df['date_day'].min()
max_date_day = day_df['date_day'].max()

min_date_hour = hour_df['date_day'].min()
max_date_hour = hour_df['date_day'].max()

with st.sidebar:
    #menambahkan logo
    st.image('img/image_apr.png')
    
    #mengambil start_date & end_date dari date_input
    start_date, end_date =  st.date_input(
        label='Rentang Waktu', min_value=min_date_day,
        max_value=max_date_day,
        value=[min_date_day, max_date_day]
    )
    
main_df_day = day_df[(day_df['date_day'] >= str(start_date)) &
                     (day_df['date_day'] <= str(end_date))]

main_df_hour = hour_df[(hour_df['date_day'] >= str(start_date)) &
                       (hour_df['date_day'] <= str(start_date))]

day_count_df = create_count_by_day_df(main_df_day)
hour_count_df = create_count_by_hour_df(main_df_hour)
registered_df = create_total_registered_df(main_df_day)
casual_df = create_total_casual_df(main_df_day)
sum_order_items_df = create_sum_order(main_df_hour)
season_df = create_season(main_df_day)

#Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header('Bike Sharing :sparkles:')

st.subheader('Bike Daily Sharing')

col1, col2, col3 = st.columns(3)

with col1:
    total_order = day_count_df.count_rental.sum()
    st.metric("Total Sharing Bike", value=total_order)
    
with col2:
    total_sum_registered = registered_df.registered_sum.sum()
    st.metric("Total Registered", value=total_sum_registered)
    
with col3:
    total_sum_casual = casual_df.casual_sum.sum()
    st.metric("Total Casual", value=total_sum_casual)
    
st.subheader("Performa Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(25,12))
ax.plot(
    day_df['date_day'],
    day_df['count_rental'],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)

st.subheader('Jam Yang Paling Banyak dan Paling Sedikit Disewa')
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

sns.barplot(x='hour', y='count_rental', data=sum_order_items_df.head(5), palette=["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3"], ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel('Jam', fontsize=30)
ax[0].set_title('Jam dengan banyak penyewa sepeda', loc='center', fontsize=30)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x='hour', y='count_rental', data=sum_order_items_df.sort_values(by='hour', ascending=True).head(5), palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#90CAF9"], ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel('Jam', fontsize=30)
ax[1].set_title('Jam dengan sedikit penyewa sepeda', loc='center', fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position('right')
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

st.subheader('Musim Dengan Penyewaan Paling Banyak')
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
        x="season",
        y="count_rental", 
        data=season_df.sort_values(by="season", ascending=False),
        palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#90CAF9"],
        ax=ax
    )
ax.set_title("Grafik Antar Musim", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

st.subheader('Perbadingan Customer Registered dan Casual')
labels = 'casual', 'registered'
sizes = [18.8, 81.2]
explode = [0, 0.1]

fig, ax = plt.subplots()
ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', colors=["#D3D3D3", "#90CAF9"], shadow=True)
ax.axis('equal')

st.pyplot(fig)

