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


def process_df(df):
    # Define action
    rename_dict = {
        'Nom_du_POI' : 'nom',
        'Latitude' : 'latitude',
        'Longitude' : 'longitude',
        'Adresse_postale' : 'adresse',
        'Description' : 'description',
        'URI_ID_du_POI' : 'url'
    }
    drop_list = [ 'Categories_de_POI',  'Covid19_mesures_specifiques',  'Createur_de_la_donnee',  'SIT_diffuseur',  'Classements_du_POI', 'Code_postal_et_commune', 'Contacts_du_POI', 'Date_de_mise_a_jour']
    order_list = [ 'nom', 'latitude','longitude','adresse', 'codepostal', 'commune', 'URL', 'description' ]

    # Apply modifications
    df[['codepostal', 'commune']] = df['Code_postal_et_commune'].str.split('#', expand=True)
    df.rename(rename_dict,axis=1, inplace=True)
    df.drop(drop_list, axis=1, inplace=True)
    df = df.reindex(columns=order_list)

    # Filtering with None
    df = df.map(lambda value: None if pd.isna(value) else value)
    df['adresse'] = df['adresse'].apply(lambda x: x.strip() if x is not None else None)
    df['description'] = df['description'].apply(lambda x:
        None if (x is None or len(x) <= 1 or x in ['...', '- ...']) else x
    )

    return df


def get_df():
    dataframe_path = os.path.join('data', 'dataframe.csv')
    if os.path.exists(dataframe_path):
        return pd.read_csv(dataframe_path, sep=',', index_col=0)
    else:
        print('First run, load dataset from data.gouv.fr...')
        df = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/cf247ad9-5bcd-4c8a-8f4d-f49f0803bca1', low_memory=False)
        df = process_df(df)
        df.to_csv(dataframe_path, sep=',')
        return df


def get_subdf(df, dept_dict, dept_name=[]):
    # By default, select all
    dept_list = list(dept_dict.keys())
    dept_name = dept_list if dept_name  == [] else dept_name

    # Filter data
    dept_code = [dept_dict[name] for name in dept_name]
    sub_df = df[df['codepostal'].str.startswith(tuple(dept_code))]

    return sub_df