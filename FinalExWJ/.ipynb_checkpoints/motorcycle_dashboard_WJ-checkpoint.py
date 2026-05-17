import pandas as pd
import geopandas as gpd
import folium
import streamlit as st
from streamlit_folium import st_folium

st.title("Motorcycle Models by World Region")
st.write("This dashboard summarizes motorcycle models by geographic region using GeoPandas and Folium.")

# Load data
regions_summary = gpd.read_file("motorcycle_regions_summary.geojson")
summary = pd.read_csv("motorcycle_region_summary_WJ.csv")

# Summary statistics
total_models = int(summary["motorcycle_count"].sum())
top_region = summary.sort_values("motorcycle_count", ascending=False).iloc[0]["Region"]
top_count = int(summary.sort_values("motorcycle_count", ascending=False).iloc[0]["motorcycle_count"])

col1, col2, col3 = st.columns(3)

col1.metric("Total Motorcycle Models", total_models)
col2.metric("Top Region", top_region)
col3.metric("Top Region Count", top_count)

# Make map
m = folium.Map(location=[20, 0], zoom_start=2)

folium.Choropleth(
    geo_data=regions_summary,
    data=regions_summary,
    columns=["Region", "motorcycle_count"],
    key_on="feature.properties.Region",
    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Motorcycle Count by Region"
).add_to(m)

folium.LayerControl().add_to(m)

st.subheader("Map of Motorcycle Models by Region")
st_folium(m, width=900, height=500)

st.subheader("Summary Table")
st.dataframe(summary)