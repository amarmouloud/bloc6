import streamlit as st
import pandas as pd
import numpy as np
import leafmap.foliumap as leafmap
import geopandas as gpd
import osmnx as ox

### Config
st.set_page_config(
    page_title="Explore the dataset",
    page_icon="🌍",
    layout="wide"
)


### App

st.header("Explore the dataset 🌍")
st.sidebar.header("Explore the dataset")


@st.cache
def load_data(nrows):
    data = pd.read_csv('data/train.csv', nrows=nrows, index_col=0)
    data = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.longitude, data.latitude), crs='EPSG:4326')
    return data

with st.spinner(text="Data loading in progress...") : 
    train = load_data(1000)
    st.success('Data loaded', icon="✅")


# Filter by region
regions_gpd = gpd.read_file('data/regions.geojson')
regions_gpd=regions_gpd[~regions_gpd['code'].isin(['01', '02', '03', '04', '06'])]
list_regions = regions_gpd['nom'].sort_values()
region = st.selectbox('Please select a region to zoom on the map',list_regions)
#region_geom = ox.geocode_to_gdf(region)
region_geom = regions_gpd[regions_gpd['nom'] == region]
#center = regions_gpd['geometry'].centroid
xmin, ymin, xmax, ymax = region_geom.total_bounds
train_region = train.cx[xmin:xmax, ymin:ymax]

m2 = leafmap.Map(center=[region_geom.centroid.y.iloc[0], region_geom.centroid.x.iloc[0]],
    measure_control=False,
    fullscreen_control=True,
    attribution_control=True)

m2.split_map(
    left_layer='OpenStreetMap.France', right_layer='GeoportailFrance.orthos'

)
m2.zoom_to_bounds([xmin, ymin, xmax, ymax])
m2.add_points_from_xy(
    train_region,
    icon_names=['leaf'],
    add_legend=True
)

m2.to_streamlit()