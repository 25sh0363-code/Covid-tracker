import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from data_fetcher import filter_by_country

def plot_metrics_cards(latest, country):
    """Display metric cards with current statistics."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Cases",
            value=f"{int(latest['cumulative_cases']):,}" if latest['cumulative_cases'] > 0 else "N/A",
            delta=f"+{int(latest['daily_cases']):,}" if latest['daily_cases'] > 0 else "No new cases"
        )
    
    with col2:
        st.metric(
            label="Total Deaths",
            value=f"{int(latest['cumulative_deaths']):,}" if latest['cumulative_deaths'] > 0 else "N/A",
            delta=f"+{int(latest['daily_deaths']):,}" if latest['daily_deaths'] > 0 else "No new deaths"
        )
    
    with col3:
        cfr_value = latest['cfr'] if latest['cfr'] > 0 else 0
        st.metric(
            label="Case Fatality Rate",
            value=f"{cfr_value:.2f}%" if cfr_value > 0 else "N/A",
            delta="Per confirmed case"
        )
    
    with col4:
        population = latest['population'] if latest['population'] > 0 else 1
        cases_per_100k = (latest['cumulative_cases'] / population * 100000) if population > 0 else 0
        st.metric(
            label="Cases per 100K",
            value=f"{cases_per_100k:.1f}" if cases_per_100k > 0 else "N/A",
            delta="Population normalized"
        )

def plot_daily_metrics(data, country, metric_type):
    """Create line chart for daily metrics."""
    country_data = filter_by_country(data, country)
    
    if metric_type == "Cases":
        column = "daily_cases"
        title = f"Daily New Cases - {country}"
    elif metric_type == "Deaths":
        column = "daily_deaths"
        title = f"Daily New Deaths - {country}"
    else:
        column = "cumulative_cases"
        title = f"Cumulative Cases - {country}"
    
    fig = px.line(country_data, x='date', y=column, title=title,
                  labels={'date': 'Date', column: 'Count'},
                  markers=True)
    
    fig.update_layout(
        hovermode='x unified',
        template='plotly_white',
        height=500,
        xaxis_title='Date',
        yaxis_title='Count'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_country_comparison(data, countries, normalize=False):
    """Create comparison chart across multiple countries."""
    fig = go.Figure()
    
    for country in countries:
        country_data = filter_by_country(data, country)
        
        if normalize and 'population' in country_data.columns:
            y_val = (country_data['cumulative_cases'] / country_data['population'] * 100000).fillna(0)
            y_label = "Cases per 100K Population"
        else:
            y_val = country_data['cumulative_cases']
            y_label = "Cumulative Cases"
        
        fig.add_trace(go.Scatter(
            x=country_data['date'],
            y=y_val,
            name=country,
            mode='lines+markers'
        ))
    
    fig.update_layout(
        title="Country Comparison - Cumulative Cases",
        xaxis_title='Date',
        yaxis_title=y_label,
        hovermode='x unified',
        template='plotly_white',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_global_map(data, map_type, selected_date):
    """Create choropleth map visualization."""
    # Get latest data or data for selected date
    map_data = data[data['date'] == selected_date].drop_duplicates(subset=['country'])
    
    if map_type == "Cases":
        column = "cumulative_cases"
        title = "Global COVID-19 Cases"
    elif map_type == "Deaths":
        column = "cumulative_deaths"
        title = "Global COVID-19 Deaths"
    else:
        column = "cfr"
        title = "Case Fatality Rate (%)"
    
    fig = px.choropleth(
        map_data,
        locations='iso_code',
        color=column,
        hover_name='country',
        color_continuous_scale='Reds',
        title=title
    )
    
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
