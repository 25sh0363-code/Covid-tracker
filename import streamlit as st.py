import streamlit as st
import pandas as pd
from data import fetch_owid, last_date
from utils import plot_time_series, plot_latest_bar, plot_choropleth

st.set_page_config(layout="wide", page_title="COVID-19 Data Tracker")
st.title("🦠 COVID-19 Data Tracker")

# Load data
with st.spinner("Loading data..."):
	df = fetch_owid()

# Sidebar controls
st.sidebar.header("Controls")
metrics = {
	"New cases": "new_cases",
	"New deaths": "new_deaths",
	"Total cases": "total_cases",
	"Total deaths": "total_deaths",
	"New tests": "new_tests"
}
metric_label = st.sidebar.selectbox("Metric", list(metrics.keys()), index=0)
metric = metrics[metric_label]
per100k = st.sidebar.checkbox("Normalize per 100k population", value=False)

# Country selection
countries_all = sorted(df["location"].unique())
default_countries = ["United States", "India", "Brazil"] if all(c in countries_all for c in ["United States","India","Brazil"]) else countries_all[:3]
selected_countries = st.sidebar.multiselect("Countries (for comparison)", default_countries, options=countries_all)

# Date controls
min_date = df["date"].min().date()
max_date = last_date(df)
date_range = st.sidebar.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

# Main layout
col1, col2 = st.columns([2, 1])

with col1:
	st.subheader(f"Time series — {metric_label}")
	if not selected_countries:
		st.info("Select one or more countries from the sidebar to view comparison.")
	else:
		df_range = df[(df["date"] >= pd.to_datetime(date_range[0])) & (df["date"] <= pd.to_datetime(date_range[1]))]
		fig = plot_time_series(df_range, selected_countries, metric, per100k=per100k)
		st.plotly_chart(fig, use_container_width=True)

	st.subheader("Global choropleth")
	# date for map
	map_date = st.slider("Map date", min_value=min_date, max_value=max_date, value=max_date, format="YYYY-MM-DD")
	fig_map = plot_choropleth(df, map_date, metric, per100k=per100k)
	st.plotly_chart(fig_map, use_container_width=True)

with col2:
	st.subheader("Latest comparison (bar)")
	if not selected_countries:
		st.info("Choose countries to compare latest available values.")
	else:
		fig_bar = plot_latest_bar(df, selected_countries, metric, per100k=per100k)
		st.plotly_chart(fig_bar, use_container_width=True)

	st.markdown("### Quick stats")
	if selected_countries:
		latest = df[df["location"].isin(selected_countries)].groupby("location").last().reset_index()
		for _, row in latest.iterrows():
			val = row.get(metric, 0)
			if per100k and row.get("population", 0):
				val = (val / row["population"]) * 100000
			st.metric(label=row["location"], value=f"{val:,.0f}")
	else:
		global_latest = df.groupby("date").sum().reset_index().iloc[-1]
		val = global_latest.get(metric, 0)
		if per100k and df["population"].sum() > 0:
			val = (val / df["population"].sum()) * 100000
		st.metric(label="Global", value=f"{val:,.0f}")

st.markdown("---")
st.caption("Data source: Our World in Data (OWID). App built with Streamlit + Plotly.")
