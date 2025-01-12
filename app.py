# frontend
import streamlit as st
from src import df, geojson, get_prediction, best_rows
from src.gmaps import get_gmaps_reviews
from src.tourism.print import print_density, print_choropleth
import re

st.title('Weather and Reviews App')

categorie_list = df['categorie'].unique()
dept_list = geojson['nom'].unique()
dept_list.sort()

categories = st.multiselect("Choose one or more categories:", categorie_list)
dept_name = st.selectbox("Choose a region:", dept_list)
dept_code = geojson[geojson['nom'] == dept_name]['code'].iloc[0]

conditions = (
    df['code_departement'] == dept_code) & (
    df['categorie'].isin(categories))
sub_df = df[conditions]
sub_df = sub_df[:5]

if st.button('Get Weather'):
    if sub_df.empty:
        st.error('Please enter at least one category & department')
    else:
        df_prediction = get_prediction(sub_df)
        output = best_rows(df_prediction)

        st.success(f"The selection has been computed")
        st.table(output)

# Add a text input for Google Maps URL
st.header('Google Maps Reviews')
place_url = st.text_input('Enter Google Maps URL of the place:')

def extract_place_id(url):
    match = re.search(r'place_id:([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    else:
        st.error('Invalid Google Maps URL')
        return None

if st.button('Get Reviews'):
    place_id = extract_place_id(place_url)
    if place_id:
        reviews_df = get_gmaps_reviews(place_id)
        if not reviews_df.empty:
            st.success('Reviews have been fetched successfully')
            st.table(reviews_df)
        else:
            st.error('No reviews found or an error occurred')

# Add options to display density and choropleth maps
st.header('Tourism Data Visualization')

if st.button('Show Density Map'):
    if sub_df.empty:
        st.error('Please enter at least one category & department')
    else:
        fig = print_density(sub_df)
        st.plotly_chart(fig)

if st.button('Show Choropleth Map'):
    if sub_df.empty:
        st.error('Please enter at least one category & department')
    else:
        fig = print_choropleth(sub_df)
        st.plotly_chart(fig)