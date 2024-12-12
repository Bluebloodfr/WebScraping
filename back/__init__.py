from pandas import DataFrame
from back.tourism import get_df, get_geojson
from back.weather import get_forecast, get_weather_score, weather_dict
from .gmaps import get_gmaps_reviews

df = get_df()
geojson = get_geojson()

def get_prediction(selection):
    selection = selection.iloc[:5]    # sampling
    output = []

    for i, row in selection.iterrow():
        forcast = get_forecast(row)
        weather_score = get_weather_score(forcast)
        weather_desc = [
            weather_dict[f['weather']] for f in forcast['forecast']
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
            'city': forcast['city']['name'],
            'code': forcast['city']['cp'],
            'latitude': forcast['city']['latitude'],
            'longitude': forcast['city']['longitude'],
            'update': forcast['update'],
            'weather_desc': weather_desc,
            'weather_score' : weather_score,
            'gmaps_score' : gmaps_score,
            'overall_score' : overall_score
        })

    df = DataFrame.from_dict(output)
    df.set_index('index', inplace=True)
    return df