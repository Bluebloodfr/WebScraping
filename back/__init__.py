from pandas import DataFrame
from back.tourism import get_df, get_geojson
from back.weather import get_forecast, get_weather_score, weather_dict

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
        gmaps_score = 0
        
        overall_score = weather_score + 0 * gmaps_score

        # save scores
        output.append({
            'index' : i,
            'city': forcast['city'],
            'weather_desc': weather_desc,
            'weather_score' : weather_score,
            'gmaps_score' : gmaps_score,
            'overall_score' : overall_score
        })

    df = DataFrame.from_dict(output, orient='columns')
    return df