import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

sns.set(style='dark')

def create_count_by_hour_df(df):
    hour_count_df = df.groupby(by='hour').agg({
        'count_rental': 'sum'
    })
    return hour_count_df

def create_count_by_day_df(df):
    day_count_df_2011 = df.query(
        str('date_day >= "2011-01-01" and date_day < "2012-12-31')
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
    sum_order_items_df = df.groupby('hour').count_rental.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def create_season(df):
    season_df = df.groupby('season').count_rental.sum().reset_index()
    return season_df

day_df = pd.read_csv('day_clean_df.csv')
hour_df = pd.read_csv('hour_clean_df.csv')

datetime_columns = ['date_day']

day_df.sort_values(by='date_day', inplace=True)
day_df.reset_index(inplace=True)

hour_df.sort_values(by='date_day', inplace=True)
hour_df.reset_index(inplace=True)

for column in datetime_columns:
    day_df['column'] = pd.to_datetime(day_df[column])
    hour_df['column'] = pd.to_datetime(hour_df[column])
    
min_date_day = day_df['date_day'].min()
max_date_day = day_df['date_day'].max()

min_date_hour = hour_df['date_day'].min()
max_date_hour = hour_df['date_day'].max()

with st.sidebar:
    #menambahkan logo
    st.image('img/image_apr.png')