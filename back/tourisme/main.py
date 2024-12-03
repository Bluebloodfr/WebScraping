import os
import json
from urllib.request import urlopen

import pandas as pd
import geopandas as gpd
import plotly.express as px 


data_path = os.path.join('..', '..', 'data')


##########################
########## POI ###########
##########################


def get_geojson():
    geojson_path = os.path.join(data_path, 'france_dept_geo.json')

    # Download json file if don't exist
    if not os.path.exists(geojson_path):
        poi_url = 'https://france-geojson.gregoiredavid.fr/repo/departements.geojson'
        france_geojson = json.load(urlopen(poi_url))
        json.dump(france_geojson, open(geojson_path, 'w'))
        print("Point of interest download")
    
    # Convert in GeoDataFrame
    france_geo = gpd.read_file(geojson_path)
    return france_geo


##########################
########## DATA ##########
##########################

def get_df():
    # Get all the df & merdge them
    df_list = []
    name_list = ['df_produit', 'df_fete', 'df_lieu', 'df_it']
    for name in name_list:
        df_path = os.path.join(data_path, name + '.zip')
        new_df = pd.read_csv(df_path, sep=' ', low_memory = False)
        df_list.append(new_df)
    df = pd.concat(df_list)
        
    # Preprocess df
    df['code_departement'] = df['code_departement'].astype(str)
    df = df.rename(columns={'categorie_mere':'categorie'})
    df.rename(lambda x: str(x).lower(), axis='columns', inplace=True)
    
    return df



##########################
########## PRINT #########
##########################

def print_density(df):
    fig = px.density_mapbox(df, 
        lat='latitude', lon='longitude', radius=4,
        center={"lat": 46.037763, "lon": 4.4}, 
        zoom=4, color_continuous_midpoint = 5,
        mapbox_style='carto-positron', 
        color_continuous_scale=['grey','darkgrey','grey','red','red']
    )
    fig.update_layout(coloraxis_showscale=False,margin=dict(l=0, r=0, b=0, t=0, pad=4))
    fig.update_traces(hoverinfo='skip', hovertemplate=None)
    fig.show()


def print_choropleth(df):
    # Prepare the data
    counts = df['code_departement'].value_counts().reset_index()
    counts.columns = ['code_departement', 'count']
    france_geo = get_geojson()

    # Choropleth map
    fig = px.choropleth_mapbox(
        counts,
        geojson=france_geo,                 # Your geojson file
        locations='code_departement',       # Match with geojson keys
        color='count',                      # Count of occurrences
        featureidkey='properties.code',     # Match geojson property
        opacity=1,
        center={"lat": 46.037763, "lon": 2.062783},
        mapbox_style="carto-positron",
        zoom=4
    )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()