import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import pandas as pd
from data_fetcher import filter_by_country

def plot_metrics_cards(latest, country):
    """Display metric cards with current statistics."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        cumulative_cases = int(latest['cumulative_cases']) if pd.notna(latest['cumulative_cases']) else 0
        daily_cases = int(latest['daily_cases']) if pd.notna(latest['daily_cases']) else 0
        st.metric(
            label="Total Cases",
            value=f"{cumulative_cases:,}",
            delta=f"+{daily_cases:,}" if daily_cases > 0 else "0 new cases"
        )
    
    with col2:
        cumulative_deaths = int(latest['cumulative_deaths']) if pd.notna(latest['cumulative_deaths']) else 0
        daily_deaths = int(latest['daily_deaths']) if pd.notna(latest['daily_deaths']) else 0
        st.metric(
            label="Total Deaths",
            value=f"{cumulative_deaths:,}",
            delta=f"+{daily_deaths:,}" if daily_deaths > 0 else "0 new deaths"
        )
    
    with col3:
        cfr_value = float(latest['cfr']) if pd.notna(latest['cfr']) and latest['cfr'] != float('inf') else 0
        st.metric(
            label="Case Fatality Rate",
            value=f"{cfr_value:.2f}%",
            delta="Per confirmed case"
        )
    
    with col4:
        population = float(latest['population']) if pd.notna(latest['population']) and latest['population'] > 0 else 1
        cumulative_cases_val = float(latest['cumulative_cases']) if pd.notna(latest['cumulative_cases']) else 0
        cases_per_100k = (cumulative_cases_val / population * 100000) if population > 1 else 0
        st.metric(
            label="Cases per 100K",
            value=f"{cases_per_100k:.1f}",
            delta="Population normalized"
        )

def plot_daily_metrics(data, country, metric_type):
    """Create line chart for daily metrics."""
    country_data = filter_by_country(data, country)
    
    # Check if we have data
    if country_data.empty:
        st.warning(f"No data available for {country}")
        return
    
    if metric_type == "Cases":
        column = "daily_cases"
        title = f"Daily New Cases - {country}"
        y_label = "Daily New Cases"
    elif metric_type == "Deaths":
        column = "daily_deaths"
        title = f"Daily New Deaths - {country}"
        y_label = "Daily New Deaths"
    else:
        column = "cumulative_cases"
        title = f"Cumulative Cases - {country}"
        y_label = "Cumulative Cases"
    
    # Remove rows where the column value is NaN
    plot_data = country_data[country_data[column].notna()].copy()
    
    if plot_data.empty:
        st.info(f"No {metric_type.lower()} data available for {country}")
        return
    
    # Create the plot with proper hover data
    fig = px.line(plot_data, x='date', y=column, title=title)
    
    # Update traces for better hover
    fig.update_traces(
        mode='lines+markers',
        hovertemplate='<b>Date:</b> %{x|%Y-%m-%d}<br><b>' + y_label + ':</b> %{y:,.0f}<extra></extra>',
        line=dict(width=2),
        marker=dict(size=4)
    )
    
    fig.update_layout(
        hovermode='x unified',
        template='plotly_white',
        height=500,
        xaxis_title='Date',
        yaxis_title=y_label,
        yaxis=dict(tickformat=','),
        showlegend=False
    )
    
    # Add range slider
    fig.update_xaxes(rangeslider_visible=True)
    
    st.plotly_chart(fig, use_container_width=True)

def plot_country_comparison(data, countries, normalize=False):
    """Create comparison chart across multiple countries."""
    if not countries:
        st.warning("Please select at least one country")
        return
    
    fig = go.Figure()
    
    for country in countries:
        country_data = filter_by_country(data, country)
        
        if country_data.empty:
            st.warning(f"No data available for {country}")
            continue
        
        if normalize and 'population' in country_data.columns:
            # Avoid division by zero
            country_data = country_data[country_data['population'] > 0].copy()
            if not country_data.empty:
                y_val = (country_data['cumulative_cases'] / country_data['population'] * 100000).fillna(0)
                y_label = "Cases per 100K Population"
            else:
                continue
        else:
            y_val = country_data['cumulative_cases'].fillna(0)
            y_label = "Cumulative Cases"
        
        fig.add_trace(go.Scatter(
            x=country_data['date'],
            y=y_val,
            name=country,
            mode='lines+markers',
            hovertemplate='<b>%{fullData.name}</b><br>Date: %{x}<br>Count: %{y:,.0f}<extra></extra>'
        ))
    
    if len(fig.data) == 0:
        st.warning("No data available for selected countries")
        return
    
    fig.update_layout(
        title="Country Comparison - Cumulative Cases",
        xaxis_title='Date',
        yaxis_title=y_label,
        hovermode='x unified',
        template='plotly_white',
        height=500,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_global_map(data, map_type, selected_date):
    """Create choropleth map visualization."""
    # Get data for selected date
    map_data = data[data['date'] == selected_date].drop_duplicates(subset=['country']).copy()
    
    if map_data.empty:
        st.warning(f"No data available for {selected_date}")
        return
    
    if map_type == "Cases":
        column = "cumulative_cases"
        title = f"Global COVID-19 Cases - {selected_date.strftime('%Y-%m-%d')}"
        color_scale = 'Reds'
    elif map_type == "Deaths":
        column = "cumulative_deaths"
        title = f"Global COVID-19 Deaths - {selected_date.strftime('%Y-%m-%d')}"
        color_scale = 'Purples'
    else:
        column = "cfr"
        title = f"Case Fatality Rate (%) - {selected_date.strftime('%Y-%m-%d')}"
        color_scale = 'YlOrRd'
    
    # Remove rows with invalid data
    map_data = map_data[map_data[column].notna() & (map_data[column] >= 0)]
    
    if map_data.empty or map_data[column].sum() == 0:
        st.info(f"No {map_type.lower()} data available for this date")
        return
    
    fig = px.choropleth(
        map_data,
        locations='iso_code',
        color=column,
        hover_name='country',
        hover_data={
            'iso_code': False,
            column: ':,.0f' if map_type != "Case Fatality Rate" else ':.2f'
        },
        color_continuous_scale=color_scale,
        title=title,
        labels={column: map_type}
    )
    
    fig.update_layout(
        height=600,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
