import io
import requests
import pandas as pd
import datetime
import streamlit as st

OWID_URL = "https://covid.ourworldindata.org/data/owid-covid-data.csv"

@st.cache_data(ttl=3600)
def fetch_owid():
	"""
	Download OWID CSV and perform lightweight cleaning.
	Returns a DataFrame with parsed dates and filtered iso_code (3-letter).
	"""
	r = requests.get(OWID_URL, timeout=30)
	r.raise_for_status()
	df = pd.read_csv(io.StringIO(r.text), parse_dates=["date"])
	# Keep country-level records with ISO3 codes
	df = df[df["iso_code"].str.len() == 3].copy()
	# Ensure population exists
	df["population"] = df["population"].fillna(0)
	# Sort for later groupby operations
	df = df.sort_values(["location", "date"])
	return df

def last_date(df):
	return df["date"].max().date()

def compute_per_100k(series, population_series):
	# avoid division by zero
	pop = population_series.replace(0, pd.NA)
	return (series / pop) * 100000
