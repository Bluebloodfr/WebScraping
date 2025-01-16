import os
import json
from urllib.request import urlopen

import pandas as pd
import geopandas as gpd
import plotly.express as px 


def get_geojson():
    geojson_path = os.path.join('data', 'france_dept_geo.json')

    # Download json file if don't exist
    if not os.path.exists(geojson_path):
        poi_url = 'https://france-geojson.gregoiredavid.fr/repo/departements.geojson'
        france_geojson = json.load(urlopen(poi_url))
        json.dump(france_geojson, open(geojson_path, 'w'))
        print("Point of interest download")
    
    # Convert in GeoDataFrame
    france_geo = gpd.read_file(geojson_path)
    return france_geo


def zip_to_df():
    # Get all the zip file
    df_list = []
    name_list = ['df_produit', 'df_fete', 'df_lieu', 'df_it']
    for name in name_list:
        df_path = os.path.join('data', name + '.zip')
        if os.path.exists(df_path):
            new_df = pd.read_csv(df_path, sep=' ', low_memory = False)
            df_list.append(new_df)
        else:
            print(f"File {df_path} does not exist.")
    
    # Manage error
    if df_list == []:
        print("No files to concatenate.")
        print('Load dataframe.csv or run `src/dowload_zip.sh`')
        return None

    # Merdge and clean df  
    df = pd.concat(df_list)
    df['code_departement'] = df['code_departement'].astype(str)
    df.rename(columns={'categorie_mere':'categorie'}, inplace=True)
    df.rename(lambda x: str(x).lower(), axis='columns', inplace=True)
    df.reset_index(inplace=True)
    df.drop(columns=['index'], inplace=True)
    
    return df


def get_df():
    dataframe_path = os.path.join('data', 'dataframe.csv')
    if os.path.exists(dataframe_path):
        return pd.read_csv(dataframe_path, sep=',', index_col=0, low_memory = False)
    else:
        return zip_to_df()