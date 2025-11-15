import pandas as pd
import requests
import os
from datetime import datetime

def load_covid_data():
    """
    Load COVID-19 data from Our World in Data.
    Downloads if not cached locally.
    """
    local_file = "covid_data.csv"
    
    # Check if local file exists
    if os.path.exists(local_file):
        df = pd.read_csv(local_file)
    else:
        # Download from OWID
        owid_url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
        df = pd.read_csv(owid_url)
        # Save locally
        df.to_csv(local_file, index=False)
    
    # Select relevant columns
    df = df[['iso_code', 'continent', 'location', 'date', 'new_cases', 
             'new_deaths', 'total_cases', 'total_deaths', 'population']]
    
    # Rename for clarity
    df.rename(columns={
        'location': 'country',
        'new_cases': 'daily_cases',
        'new_deaths': 'daily_deaths',
        'total_cases': 'cumulative_cases',
        'total_deaths': 'cumulative_deaths'
    }, inplace=True)
    
    # Data cleaning
    df['date'] = pd.to_datetime(df['date'])
    df = df.dropna(subset=['country', 'date'])
    df = df.fillna(0)
    
    # Calculate case fatality rate
    df['cfr'] = (df['cumulative_deaths'] / df['cumulative_cases'] * 100).replace([float('inf'), -float('inf')], 0)
    
    return df

def filter_by_country(data, country):
    """Filter data for a specific country."""
    return data[data['country'] == country].sort_values('date')

def filter_by_date_range(data, start_date, end_date):
    """Filter data for a date range."""
    return data[(data['date'] >= start_date) & (data['date'] <= end_date)]

def get_latest_metrics(data, country):
    """Get latest metrics for a country."""
    country_data = filter_by_country(data, country)
    if country_data.empty:
        return None
    return country_data.iloc[-1]
