from src.weather import get_forecast, get_weather_score, weather_dict

def get_prediction(df_selection):
    forecast_list = []

    for i, row in df_selection.iterrows():
        forecast = get_forecast(row)
        weather_score = get_weather_score(forecast)
        weather_desc = [
            weather_dict[f['weather']] for f in forecast['forecast']
        ]

        # get gmaps_score
        review_score = 0 # get_gmaps_reviews(row)
        
        overall_score = [
            weather_scr + 0 * review_score
            for weather_scr in weather_score
        ]

        # save scores
        forecast_list.append({
            'index' : i,
            'city': forecast['city']['name'],
            'code': forecast['city']['cp'],
            'latitude': forecast['city']['latitude'],
            'longitude': forecast['city']['longitude'],
            'weather_desc': weather_desc,
            'weather_score' : weather_score,
            'review_list' : [],
            'review_score' : review_score,
            'overall_score' : overall_score
        })

    return forecast_list


def sorted_activity_id(forecast_list):
    days_activity_sorted = [] # for each days of the prevision (14 days)
    for day in range(14):
        # list the best activities for this days
        day_overview = {
            f['index'] : f['overall_score'][day] for f in forecast_list
        }
        day_overview_sorted = dict(sorted(day_overview.items(), key=lambda x: x[1], reverse=True))
        day_overview_sorted_id = day_overview_sorted.keys()
        days_activity_sorted.append(day_overview_sorted_id)

    return days_activity_sorted