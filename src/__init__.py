from src.tourism import get_df, get_geojson
from src.weather import get_forecast, get_weather_score, weather_dict
from src.gmaps import get_gmaps_reviews

from src.print_maps import *

from pandas import DataFrame
import pandas as pd

#df = get_df()
df = pd.read_csv('data/dataframe.csv', sep=',', low_memory = False)
geojson = get_geojson()

def get_prediction(df_selection):
    output = []

    for i, row in df_selection.iterrows():
        forecast = get_forecast(row)
        weather_score = get_weather_score(forecast)
        weather_desc = [
            weather_dict[f['weather']] for f in forecast['forecast']
        ]

        # get gmaps_score
        gmaps_score = 0 # get_gmaps_reviews(row)
        
        overall_score = [
            weather_scr + 0 * gmaps_score
            for weather_scr in weather_score
        ]

        # save scores
        output.append({
            'index' : i,
            'city': forecast['city']['name'],
            'code': forecast['city']['cp'],
            'latitude': forecast['city']['latitude'],
            'longitude': forecast['city']['longitude'],
            'weather_desc': weather_desc,
            'weather_score' : weather_score,
            'gmaps_score' : gmaps_score,
            'overall_score' : overall_score
        })

    df_prediction = DataFrame.from_dict(output)
    df_prediction.set_index('index', inplace=True)
    return df_prediction


def best_rows(df_prediction):
    output = []

    for delay in range(14):
        nth_elements = df_prediction['overall_score'].apply(lambda x: x[delay])
        output_sorted = df_prediction.iloc[nth_elements.argsort()[::-1]]
        best_row = output_sorted.iloc[0].copy()
        
        best_row['weather_desc'] = best_row['weather_desc'][delay]
        best_row['weather_score'] = best_row['weather_score'][delay]
        best_row['overall_score'] = best_row['overall_score'][delay]
        
        output.append(best_row)
    
    df = DataFrame(output)
    return df