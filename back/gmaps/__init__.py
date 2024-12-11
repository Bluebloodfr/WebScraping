import os
import json
from urllib.request import urlopen
from dotenv import load_dotenv
import pandas as pd
import geopandas as gpd
import plotly.express as px
import requests
from bs4 import BeautifulSoup
import googlemaps

load_dotenv()
ROOT_DIR = os.getenv('ROOT_DIR')
API_KEY = os.getenv('GOOGLE_API_KEY')

##########################
########## POI ###########
##########################

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

##########################
########## DATA ##########
##########################

def get_df():
    # Get all the df & merge them
    df_list = []
    name_list = ['df_produit', 'df_fete', 'df_lieu', 'df_it']
    for name in name_list:
        df_path = os.path.join(ROOT_DIR, 'data', name + '.zip')
        new_df = pd.read_csv(df_path, sep=' ', low_memory=False)
        df_list.append(new_df)
    df = pd.concat(df_list)
        
    # Preprocess df
    df['code_departement'] = df['code_departement'].astype(str)
    df.rename(columns={'categorie_mere':'categorie'}, inplace=True)
    df.rename(lambda x: str(x).lower(), axis='columns', inplace=True)
    df.reset_index(inplace=True)
    
    return df

##########################
########## PRINT #########
##########################

def print_density(df):
    fig = px.density_mapbox(df, 
        lat='latitude', lon='longitude', radius=4,
        center={"lat": 46.037763, "lon": 4.4}, 
        zoom=4, color_continuous_midpoint=5,
        mapbox_style='carto-positron', 
        color_continuous_scale=['grey','darkgrey','grey','red','red']
    )
    fig.update_layout(coloraxis_showscale=False, margin=dict(l=0, r=0, b=0, t=0, pad=4))
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

##########################
########### API ##########
##########################

# For explanation, check LandDayForecast on https://api.meteo-concept.com/documentation_openapi
url = f"https://api.meteo-concept.com/api/forecast/daily"
headers = {"X-AUTH-TOKEN": os.getenv('API_KEY')}

def get_forecast(df_row):
    # Build query
    latlng = f"{df_row['latitude']},{df_row['longitude']}"
    querystring = {"latlng": latlng }
    
    # Call API
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

##########################
########## SCORE #########
##########################

def log_score(X, alpha=1/8):  
    beta = (10**(1/alpha) - 1) / 235
    bad_weather_score = alpha * np.log10(beta * X + 1)
    
    return 1 - bad_weather_score

def weather_score(response):
    forecast_list = response['forecast']
    weather_score = [
        forecast['weather'].apply(log_score)
        for forecast in forecast_list
    ]
    
    return weather_score

weather_dict = {
    # (weather codes and descriptions)
}

##########################
####### GMAPS REVIEWS ####
##########################

def get_gmaps_reviews(place_id):
    gmaps = googlemaps.Client(key=API_KEY)
    place_details = gmaps.place(place_id=place_id, fields=['reviews'])
    reviews = place_details.get('result', {}).get('reviews', [])
    
    reviews_data = []
    for review in reviews:
        reviews_data.append({
            'author_name': review.get('author_name'),
            'rating': review.get('rating'),
            'text': review.get('text'),
            'time': review.get('relative_time_description')
        })
    
    df_reviews = pd.DataFrame(reviews_data)
    return df_reviews

# Example usage
place_id = 'ChIJdUyx15R95kcRj85ZX8H8OAU' # Chateau de Versailles
reviews_df = get_gmaps_reviews(place_id)
print(reviews_df)