import streamlit as st
from src import get_gmaps_reviews
import re

def page():
    place_url = st.text_input('Enter Google Maps URL of the place:')

    # extract_place_id
    match = re.search(r'place_id:([a-zA-Z0-9_-]+)', place_url)
    if match:
        place_id = match.group(1)

        # Get reviews
        reviews_df = get_gmaps_reviews(place_id)
        if not reviews_df.empty:
            st.success('Reviews have been fetched successfully')
            st.table(reviews_df)
        
        else:
            st.error('No reviews found or an error occurred')
    else:
        st.error('Invalid Google Maps URL')