import streamlit as st
from src import *

df = get_df()
geojson = get_geojson()

categorie_list = df['categorie'].unique()
dept_list = geojson['nom'].unique()

def get_subdf(categories=[], dept_name=[]):
    # By default, select all
    categories = categorie_list if categories == [] else categories
    dept_name = dept_list if dept_name  == [] else dept_name

    # Convert name to postal code
    dept_code = [
        geojson[geojson['nom'] == name]['code'].iloc[0]
        for name in dept_name
    ]

    # Filter data
    sub_df = df[(
        df['code_departement'].isin(dept_code)  ) & (
        df['categorie'].isin(categories) 
    )]
    
    return sub_df


def page():
    st.title('Tourism App')
    st.markdown('Tourism app that helps you find the best places to visit based on weather and Google Maps reviews.')
    st.markdown('By default, all the filter are selected.')

    # Form to select categories and departments
    with st.form("my_form"):
        # Load data
        categorie_list = df['categorie'].unique()
        dept_list = geojson['nom'].unique()
        dept_list.sort()

        categories = st.multiselect("Choose one or more categories:", categorie_list)
        dept_name = st.multiselect("Choose a region:", dept_list)
        
        submit_button = st.form_submit_button('Submit')

    # Return output
    if submit_button:
        sub_df = get_subdf(categories, dept_name)
        sub_df = sub_df.iloc[:5]    # for testing

        forecast_list = get_prediction(sub_df)
        days_activity_sorted = sorted_activity_id(forecast_list)
        st.success(f"The selection has been computed")

        raw_table, review_table, graph_table = st.tabs(["Results", "Gmaps Reviews" ,"Graphiques"])
        with raw_table:
            st.header('Results')
            days_table_name = [f'{i} days' for i in range(14)]
            for day, day_table in enumerate(st.tabs(days_table_name)):
                
                with day_table:
                    st.subheader(f'Best activity in {day} days')
                    for activity_id in days_activity_sorted[day]:
                        best_activity = [f for f in forecast_list if f['index'] == activity_id][0]
                        best_activity_print = {
                            'index': best_activity['index'],
                            'coor': f"{best_activity['latitude']} ; {best_activity['longitude']}",
                            'weather_desc': best_activity['weather_desc'][day],
                            'weather_score': best_activity['weather_score'][day],
                            'review_score': best_activity['review_score'],
                            'overall_score': best_activity['overall_score'][day],
                        }
                        st.table(best_activity_print)
                        # TODO : add reviews & stars
                        # Change le dataframes pour y ajouter le nom des activités et l'affichier ici

        with review_table:
            st.header('Gmaps Reviews')
            st.markdown('TODO')
            # TODO

        with graph_table:
            st.header('Tourism Data Visualization')
            fig = print_density(sub_df) # Density Map
            st.plotly_chart(fig, use_container_width=True)
            st.write("This map shows the density of tourism data points based on the selected categories and region.")

            fig = print_choropleth(sub_df) # Choropleth Map
            st.plotly_chart(fig, use_container_width=True)
            st.write("This map shows the count of tourism data points per department based on the selected categories and region.")
    
