import streamlit as st
import pandas as pd
import numpy as np

from src import *

@st.cache_data
def get_prediction(df_sub):
    prediction_dict = {}

    for i, row in df_sub.iterrows():
        # get weather score
        forecast = get_forecast(row)
        weather_score = get_weather_score(forecast)
        weather_desc = [
            weather_dict[f['weather']] for f in forecast['forecast']
        ]

        # scrap gmaps reviews
        review_list = get_reviews(row)
        review_list = add_sentiment_score(review_list)
        stars_avg, rating_avg = get_avg_score(review_list)
        
        # compute overall score
        if stars_avg:
            s_scr = stars_avg / 5
            r_scr = rating_avg / 5
            overall_score = [np.mean([w_scr, s_scr, r_scr]) for w_scr in weather_score]
        else:
            overall_score = weather_score.copy()

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

    df_prediction = pd.DataFrame(prediction_dict).T
    return df_prediction


def sort_prediction_ids(prediction):
    daily_poi_ids = [] # for each days of the prevision (14 days)
    
    for day in range(14):
        id_score_dict = {id : poi['overall_score'][day] for id, poi in prediction.iterrows()}
        id_score_dict_sorted = dict(sorted(id_score_dict.items(), key=lambda item: item[1], reverse=True))
        daily_poi_ids.append(id_score_dict_sorted.keys())
    
    return daily_poi_ids