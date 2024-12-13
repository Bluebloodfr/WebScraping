import os
import json
from urllib.request import urlopen
from dotenv import load_dotenv

import pandas as pd
import geopandas as gpd
import plotly.express as px 


load_dotenv()
ROOT_DIR = os.getenv('ROOT_DIR')

def get_geojson():
    geojson_path = os.path.join(ROOT_DIR, 'data', 'france_dept_geo.json')

    # Download json file if don't exist
    if not os.path.exists(geojson_path):
        poi_url = 'https://france-geojson.gregoiredavid.fr/repo/departements.geojson'
        france_geojson = json.load(urlopen(poi_url))
        json.dump(france_geojson, open(geojson_path, 'w'))
        print("Point of interest download")
    
    # Convert in GeoDataFrame
    france_geo = gpd.read_file(geojson_path)
    return france_geo


def get_df():
    # Get all the df & merdge them
    df_list = []
    name_list = ['df_produit', 'df_fete', 'df_lieu', 'df_it']
    for name in name_list:
        df_path = os.path.join(ROOT_DIR, 'data', name + '.zip')
        new_df = pd.read_csv(df_path, sep=' ', low_memory = False)
        df_list.append(new_df)
    df = pd.concat(df_list)
        
    # Postprocess df
    df['code_departement'] = df['code_departement'].astype(str)
    df.rename(columns={'categorie_mere':'categorie'}, inplace=True)
    df.rename(lambda x: str(x).lower(), axis='columns', inplace=True)
    df.reset_index(inplace=True)
    df.drop(columns=['index'], inplace=True)
    
    return df