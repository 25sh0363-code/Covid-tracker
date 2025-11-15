import plotly.express as px
import pandas as pd

def plot_time_series(df, countries, metric, per100k=False):
	df_sub = df[df["location"].isin(countries)]
	if per100k:
		df_sub = df_sub.copy()
		df_sub[metric] = (df_sub[metric] / df_sub["population"]) * 100000
	fig = px.line(df_sub, x="date", y=metric, color="location",
			  labels={"date": "Date", metric: metric, "location": "Country"})
	fig.update_layout(legend_title_text="Country")
	return fig

def plot_latest_bar(df, countries, metric, per100k=False):
	# take last available value per country
	df_last = df[df["location"].isin(countries)].groupby("location").last().reset_index()
	if per100k:
		df_last = df_last.copy()
		df_last[metric] = (df_last[metric] / df_last["population"]) * 100000
	fig = px.bar(df_last, x="location", y=metric, labels={metric: metric, "location": "Country"})
	return fig

def plot_choropleth(df, date, metric, per100k=False):
	df_date = df[df["date"] == pd.to_datetime(date)].copy()
	if df_date.empty:
		# fallback to last available date
		df_date = df.groupby("iso_code").last().reset_index()
	if per100k:
		df_date[metric] = (df_date[metric] / df_date["population"]) * 100000
	fig = px.choropleth(df_date, locations="iso_code", color=metric,
	                    hover_name="location", color_continuous_scale="OrRd",
	                    labels={metric: metric})
	return fig
