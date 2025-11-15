import streamlit as st
import pandas as pd
from datetime import datetime
from data_fetcher import load_covid_data, get_latest_metrics, filter_by_country
from visualizations import (
    plot_daily_metrics,
    plot_country_comparison,
    plot_global_map,
    plot_metrics_cards
)

st.set_page_config(page_title="COVID-19 Data Tracker", layout="wide")

st.title("🦠 COVID-19 Data Tracker")
st.markdown("Interactive visualization of global and regional pandemic trends")

# Refresh data button in sidebar
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# Load data
@st.cache_data
def get_data():
    return load_covid_data()

data = get_data()
last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.sidebar.caption(f"Last updated: {last_update}")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select View", [
    "Country Dashboard",
    "Daily Metrics",
    "Country Comparison",
    "Global Map",
    "About"
])

if page == "Country Dashboard":
    st.header("🌐 Country Dashboard")
    
    # Country selector
    selected_country = st.selectbox("Select Country", sorted(data['country'].unique()))
    
    # Get country data
    country_data = filter_by_country(data, selected_country)
    latest = get_latest_metrics(data, selected_country)
    
    if latest is not None:
        # Display metric cards
        plot_metrics_cards(latest, selected_country)
        
        # Tabbed interface
        tab1, tab2, tab3 = st.tabs(["📊 Graphics", "📋 Table Data", "📈 Chart Data"])
        
        with tab1:
            st.subheader(f"Visual Analytics - {selected_country}")
            col1, col2 = st.columns(2)
            
            with col1:
                metric_type = st.selectbox("Select Metric", ["Cases", "Deaths"], key="graphics_metric")
            
            plot_daily_metrics(country_data, selected_country, metric_type)
        
        with tab2:
            st.subheader(f"Data Table - {selected_country}")
            
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                rows_display = st.slider("Rows to Display", 10, len(country_data), 20)
            with col2:
                sort_by = st.selectbox("Sort By", ["Date (Newest)", "Date (Oldest)", "Cases (High to Low)"])
            
            # Apply sorting
            if sort_by == "Date (Newest)":
                display_data = country_data.tail(rows_display).sort_values('date', ascending=False)
            elif sort_by == "Date (Oldest)":
                display_data = country_data.head(rows_display).sort_values('date', ascending=True)
            else:
                display_data = country_data.nlargest(rows_display, 'cumulative_cases')
            
            # Format and display table
            table_display = display_data[['date', 'daily_cases', 'daily_deaths', 'cumulative_cases', 'cumulative_deaths', 'cfr']].copy()
            table_display['date'] = table_display['date'].dt.strftime('%Y-%m-%d')
            table_display.columns = ['Date', 'Daily Cases', 'Daily Deaths', 'Cumulative Cases', 'Cumulative Deaths', 'CFR (%)']
            table_display = table_display.fillna(0).astype({"Daily Cases": "int", "Daily Deaths": "int", "Cumulative Cases": "int", "Cumulative Deaths": "int"})
            
            st.dataframe(table_display, use_container_width=True, hide_index=True)
            
            # Download button
            csv = table_display.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"{selected_country}_covid_data.csv",
                mime="text/csv"
            )
        
        with tab3:
            st.subheader(f"Chart Analysis - {selected_country}")
            
            chart_type = st.selectbox("Select Chart Type", 
                ["Daily Cases Trend", "Cumulative Cases", "Daily Deaths Trend", "Case Fatality Rate"])
            
            if chart_type == "Daily Cases Trend":
                plot_daily_metrics(country_data, selected_country, "Cases")
            elif chart_type == "Cumulative Cases":
                plot_daily_metrics(country_data, selected_country, "Recoveries")
            elif chart_type == "Daily Deaths Trend":
                plot_daily_metrics(country_data, selected_country, "Deaths")
            else:
                # CFR chart
                import plotly.express as px
                fig = px.line(country_data, x='date', y='cfr', 
                             title=f"Case Fatality Rate - {selected_country}",
                             markers=True, labels={'cfr': 'CFR (%)', 'date': 'Date'})
                fig.update_layout(height=500, template='plotly_white', hovermode='x unified')
                st.plotly_chart(fig, use_container_width=True)

elif page == "Daily Metrics":
    st.header("📊 Daily Metrics")
    st.markdown("Visualize daily confirmed cases, deaths, and recoveries")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_country = st.selectbox("Select Country", data['country'].unique(), key="daily_country")
    with col2:
        metric_type = st.selectbox("Select Metric", ["Cases", "Deaths", "Recoveries"], key="daily_metric")
    
    country_data = filter_by_country(data, selected_country)
    plot_daily_metrics(country_data, selected_country, metric_type)

elif page == "Country Comparison":
    st.header("🌍 Country-wise Comparisons")
    st.markdown("Compare trends across multiple countries")
    
    countries = st.multiselect("Select Countries", sorted(data['country'].unique()), 
                               default=["United States", "India", "Brazil"])
    normalize = st.checkbox("Normalize by Population")
    
    if countries:
        plot_country_comparison(data, countries, normalize)

elif page == "Global Map":
    st.header("🗺️ Global Maps")
    st.markdown("Choropleth maps showing case density and mortality rates")
    
    col1, col2 = st.columns(2)
    with col1:
        map_type = st.selectbox("Select Map Type", ["Cases", "Deaths", "Case Fatality Rate"])
    with col2:
        date_slider = st.select_slider("Select Date", 
                                       options=sorted(data['date'].unique()), 
                                       value=data['date'].max())
    
    plot_global_map(data, map_type, pd.to_datetime(date_slider))

elif page == "About":
    st.header("ℹ️ About This Project")
    st.markdown("""
    ### 📌 Project Summary
    The COVID-19 Data Tracker is a dynamic dashboard for visualizing pandemic trends across countries and regions.
    
    ### 🎯 Key Features
    - **Country Dashboard**: Real-time metrics with tabbed interface (Graphics, Table, Charts)
    - **Daily Metrics**: Visualize cases, deaths, and recoveries by country
    - **Country Comparisons**: Compare trends with population normalization
    - **Interactive Charts**: Line graphs, bar charts, with zoom and hover tooltips
    - **Global Maps**: Choropleth maps showing statistics over time
    - **Live Updates**: Refresh button to get latest data
    
    ### 📊 Data Sources
    - Our World in Data (OWID)
    - Johns Hopkins University COVID-19 Dataset
    
    ### 🔄 Last Update
    Data refreshes automatically from Our World in Data. Click "Refresh Data" to get the latest statistics.
    """)
