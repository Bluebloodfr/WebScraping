import streamlit as st
from front import *


st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Pages", ["Full App", "Scrapping Only", "About"], index=0)

# Display the selected page
if page == "Full App":
    main_page()
elif page == "Scrapping Only":
    scrapping_page()
else:
    st.markdown("""
    # Welcome to the Tourism App!
    This app helps you find the best places to visit based on weather and Google Maps reviews.
    You can use the full app to get personalized recommendations or just use the scrapping tool to get reviews from Google Maps.

    ## How it works
    ### APIs
    We use the APIs from 
    - [DataTourisme](https://gitlab.adullact.net/adntourisme/datatourisme/api) for points of interest (or POI)
    - [MeteoConcept](https://api.meteo-concept.com/documentation_openapi) for weather forecasts (need account, free 500 credits per day)

    We get all the POI in France once and we keep them in a csv file. The DataTourisme API if to get the name of the POI for the scrapping.
    
    ### Scrapping the reviews
    We also scrape [Google Maps](https://www.google.com/maps) for reviews and use NLP to analyze them.  
    Almost each times, the Datatoursime and Google Maps coordinate don't match exactly and many place in France have the same name.
    So the protocol to get the right reviews if the folowing:
    1. Search the GPS coordinates of the POI you want to visit.
    2. Enter the name of the POI
    3. Clic on the first link that appears
    4. Scrape the reviews from the link.

    ### Compute score
    To get the score for a POI:
    1. Request the weather forecast score (equivalent dict on src/weather.py dict_weather) for it localisation.
    2. Scrapp the review and pass an NLP analysis to get the review score.
    3. Use a log function on weather score and ponderate the review score with it.
    4. Return the score.

    ## Team
    - Louis-Melchior Giraud DIA2 - [GitHub](https://github.com/Bluebloodfr)
    - Ruben Leon DIA3 - [GitHub](https://github.com/ruben-wleon)  
    
    ESILV - A5 - 2024/2025
    """)