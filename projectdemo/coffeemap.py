import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Set page title
st.set_page_config(page_title="Coffee Production Dashboard", layout="wide")

st.title("☕ Arabica Production Summary: 1960 vs 2010")

# 1. Load Data
@st.cache_data
def load_data():
    # Load CSV for metrics
    df = pd.read_csv('Arabicabyregion_with_percentages.csv')
    return df

@st.cache_data
def load_geodata():
    # Load Shapefile
    gdf = gpd.read_file("Regions/worldregions.shp")
    return gdf

df = load_data()
data = load_geodata()

# 2. Calculate Totals & Metrics
sum_cols = ['Sum1960', 'Sum1970', 'Sum1980', 'Sum1990', 'Sum 2000', 'Sum2010', 'Sum2020']
totals = df[sum_cols].sum()

total_1960 = totals['Sum1960']
total_2010 = totals['Sum2010']
percent_increase = ((total_2010 - total_1960) / total_1960) * 100

# 3. Display Metrics in Columns
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Production 1960s", value=f"{total_1960:,.0f}")
with col2:
    st.metric(label="Total Production 2010s", value=f"{total_2010:,.0f}")
with col3:
    st.metric(label="Percent Increase", value=f"{percent_increase:.2f}%", delta=f"{percent_increase:.2f}%")

st.divider()

# 4. Map Section
st.subheader("Visual Comparison: 1960 vs 2010 Production Density")
st.info("Use the slider in the center of the map to compare 1960 (Left) and 2010 (Right).")

# Prepare Map Data
merged_gdf = data.merge(df, on='Region', suffixes=('_left', '_right'))
filtered_gdf = merged_gdf[merged_gdf['Per2010'] > 0]

# Initialize Map
m = folium.Map(location=[0, 0], zoom_start=2)

# Create Layer 1 (1960)
myscale1 = (filtered_gdf['Per1960'].quantile((0, 0.01, 0.5, 0.7, 0.98, 1))).tolist()
layer1 = folium.Choropleth(
    geo_data=filtered_gdf,
    data=filtered_gdf,
    columns=['Region', 'Per1960'],
    key_on='feature.properties.Region', 
    fill_color='YlGn',
    threshold_scale=myscale1,
    fill_opacity=0.7,
    line_opacity=0.2,
    name='1960 Production',
    nan_fill_opacity=0
).add_to(m)

# Create Layer 2 (2010)
myscale2 = (filtered_gdf['Per2010'].quantile((0, 0.01, 0.5, 0.7, 0.98, 1))).tolist()
layer2 = folium.Choropleth(
    geo_data=filtered_gdf,
    data=filtered_gdf,
    columns=['Region', 'Per2010'],
    key_on='feature.properties.Region', 
    fill_color='YlGn',
    threshold_scale=myscale2,
    fill_opacity=0.7,
    line_opacity=0.2,
    name='2010 Production', 
    nan_fill_opacity=0    
).add_to(m)

# Add Side-by-Side Control
# Note: Using .geojson attribute to ensure the plugin recognizes the layers

folium.LayerControl().add_to(m)

# Render Folium map in Streamlit
st_folium(m, width=1400, height=600)

st.divider()

# 5. Data Table Section
st.subheader("Regional Production Breakdown")
df['Growth % (1960 to 2010)'] = ((df['Sum2010'] - df['Sum1960']) / df['Sum1960'] * 100).fillna(0)
display_df = df[['Region', 'Sum1960', 'Sum2010', 'Growth % (1960 to 2010)']]

st.dataframe(
    display_df.style.format({
        'Sum1960': '{:,.0f}',
        'Sum2010': '{:,.0f}',
        'Growth % (1960 to 2010)': '{:.2f}%'
    }),
    use_container_width=True
)