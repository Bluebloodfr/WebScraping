from src.weather import get_forecast, get_weather_score, weather_dict
from src.models import compute_sentiment_score, get_avg_score
from src.gmaps import get_gmaps_reviews_by_name

def get_prediction(df_selection):
    forecast_list = []

    for i, row in df_selection.iterrows():
        forecast = get_forecast(row)
        weather_score = get_weather_score(forecast)
        weather_desc = [
            weather_dict[f['weather']] for f in forecast['forecast']
        ]

        # get gmaps_score
        reviews = get_gmaps_reviews_by_name(row['nom'], row['latitude'], row['longitude'])
        review_ratings = []
        for review in reviews:
            try:
                rating = int(review['rating'][0])
                review_ratings.append(rating)
            except (ValueError, TypeError):
                review_ratings.append(0)
        review_score = sum(review_ratings) / len(review_ratings) if review_ratings else 0
        
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
            'review_list' : reviews,
            'review_score' : review_score,
            'overall_score' : overall_score
        })

    return forecast_list


def sort_prediction(prediction_list):
    daily_poi_sorted = [] # for each days of the prevision (14 days)
    id2poi = {poi['index'] : poi for poi in prediction_list}
    
    for day in range(14):
        id_score_dict = {poi['index'] : poi['overall_score'][day] for poi in prediction_list}
        id_score_dict_sorted = dict(sorted(id_score_dict.items(), key=lambda item: item[1], reverse=True))
        poi_sorted = [id2poi[id] for id in id_score_dict_sorted.keys()]
        daily_poi_sorted.append(poi_sorted)
    
    return daily_poi_sorted