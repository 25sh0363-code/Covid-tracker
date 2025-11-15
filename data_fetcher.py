import pandas as pd
import requests
import streamlit as st
from datetime import datetime
import io

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_covid_data():
    """
    Load COVID-19 data from Our World in Data.
    Uses Streamlit caching instead of local file storage.
    """
    # Try multiple URLs in case one fails
    urls = [
        "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv",
        "https://github.com/owid/covid-19-data/raw/master/public/data/owid-covid-data.csv",
        "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    ]
    
    df = None
    last_error = None
    
    for url in urls:
        try:
            # Use requests with proper headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Read CSV from response content
            df = pd.read_csv(io.StringIO(response.text))
            st.success(f"✅ Successfully loaded data from: {url.split('/')[2]}")
            break  # Success! Exit loop
            
        except Exception as e:
            last_error = e
            continue  # Try next URL
    
    if df is None:
        st.error(f"❌ Failed to load COVID-19 data from all sources.")
        st.error(f"Last error: {last_error}")
        st.info("The data source might be temporarily unavailable. Please try again later.")
        st.stop()
        return None
    
    # Select relevant columns
    required_columns = ['iso_code', 'continent', 'location', 'date', 'new_cases', 
                       'new_deaths', 'total_cases', 'total_deaths', 'population']
    
    # Check if all required columns exist
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        st.error(f"Missing columns in data: {missing_cols}")
        st.stop()
        return None
    
    df = df[required_columns]
    
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
    filtered = data[data['country'] == country].sort_values('date').copy()
    
    # Replace NaN with 0
    filtered = filtered.fillna(0)
    
    # Only keep rows where we have at least cumulative data
    # Don't filter out rows with 0 daily cases - those are valid!
    filtered = filtered[filtered['cumulative_cases'] >= 0]
    
    return filtered

def filter_by_date_range(data, start_date, end_date):
    """Filter data for a date range."""
    return data[(data['date'] >= start_date) & (data['date'] <= end_date)]

def get_latest_metrics(data, country):
    """Get latest metrics for a country."""
    country_data = filter_by_country(data, country)
    if country_data.empty:
        return None
    return country_data.iloc[-1]
