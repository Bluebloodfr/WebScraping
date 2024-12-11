import os
import json
from dotenv import load_dotenv
import pandas as pd
import googlemaps

load_dotenv()
ROOT_DIR = os.getenv('ROOT_DIR')
API_KEY = os.getenv('GOOGLE_API_KEY')

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