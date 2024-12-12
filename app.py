# frontend
import streamlit as st
from back import df, geojson, get_prediction


st.title('Weather App')

categorie_list = df['categorie'].unique()
dept_list = geojson['nom'].unique()
dept_list.sort()

categories = st.multiselect("Choose one or more categories:", categorie_list)
dept_name = st.selectbox("Choose a region:", dept_list)
dept_code = geojson[geojson['nom'] == 'Aisne']['code'].iloc[0]

conditions = (
    df['code_departement'] == dept_code) & (
    df['categorie'].isin(categories))
sub_df = df[conditions]


if st.button('Get Weather'):
    if conditions == None:
        st.error('Please enter at least one categorie & departement')

    else:
        prediction = get_prediction(sub_df)
        
        if 'error' in prediction:
            st.error(weather_data['error'])
        else:
            st.success(f"Weather in {weather_data['city']}:")
            st.write(f"Temperature: {weather_data['temperature']}°C")
            st.write(f"Description: {weather_data['description']}")
            st.write(f"Humidity: {weather_data['humidity']}%")