from src.weather import get_forecast, get_weather_score, weather_dict
from src.models import manage_scores, get_avg_score
from src.gmaps import get_gmaps_reviews_by_name
import json

import streamlit as st

@st.cache_data
def get_prediction(df_selection):
    prediction_dict = {}

    for i, row in df_selection.iterrows():
        # get weather score
        forecast = get_forecast(row)
        weather_score = get_weather_score(forecast)
        weather_desc = [
            weather_dict[f['weather']] for f in forecast['forecast']
        ]

        # scrap gmaps reviews
        review_list = get_gmaps_reviews_by_name(row['nom'], row['latitude'], row['longitude'])
        #review_list = json.load(open('data/review_list_raw.json'))
        review_list = manage_scores(review_list)
        stars_avg, rating_avg = get_avg_score(review_list)
        
        # compute overall score
        prediction_scr = stars_avg / 5
        overall_score = [
            weather_scr + prediction_scr
            for weather_scr in weather_score
        ]

        # save scores
        prediction_dict[i] = {
            'city': forecast['city']['name'],
            'code': forecast['city']['cp'],
            'latitude': forecast['city']['latitude'],
            'longitude': forecast['city']['longitude'],
            'weather_desc': weather_desc,
            'weather_score' : weather_score,
            'review_list' : review_list,
            'rating_score' : rating_avg,
            'star_score': stars_avg,
            'overall_score' : overall_score
        }

    return prediction_dict


def sort_prediction_ids(prediction):
    daily_poi_ids = [] # for each days of the prevision (14 days)
    
    for day in range(14):
        id_score_dict = {id : poi['overall_score'][day] for id, poi in prediction.items()}
        id_score_dict_sorted = dict(sorted(id_score_dict.items(), key=lambda item: item[1], reverse=True))
        daily_poi_ids.append(id_score_dict_sorted.keys())
    
    return daily_poi_ids