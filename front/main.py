import streamlit as st
from src import *

df = get_df()
geojson = get_geojson()
dept_dict = {f"{row['code']} - {row['nom']}" : row['code'] for i, row in geojson.iterrows()}


def print_result_table(daily_poi_sorted, day):
    st.subheader(f'Best activity in {day} days')           
    printed_table = []
    for poi in daily_poi_sorted[day]:
        # retrive the row in df
        row = df.loc[poi['index']].to_dict()
        
        printed_table.append({
            'name' : row['nom'],
            'ville': row['commune'],
            'adresse': row['adresse'],
            'weather_desc': poi['weather_desc'][day],
            'weather_score': poi['weather_score'][day],
            'review_score': poi['review_score'],
            'overall_score': poi['overall_score'][day],
        })
    st.table(printed_table)



def page():
    st.title('Tourism App')
    st.markdown('Tourism app that helps you find the best places to visit based on weather and Google Maps reviews.')
    st.markdown('By default, all the filter are selected.')

    # Form to select categories and departments
    with st.form("my_form"):
        # Choose a departement
        dept_dict = {f"{row['code']} - {row['nom']}" : row['code'] for i, row in geojson.iterrows()}
        dept_list = list(dept_dict.keys())
        dept_list.sort()
        dept_name = st.multiselect("Choose a department:", dept_list)
        
        submit_button = st.form_submit_button('Submit')

    # Return output
    if submit_button:
        sub_df = get_subdf(df, dept_dict, dept_name).iloc[:5]    # iloc for testing
        prediction_list = get_prediction(sub_df)
        
        st.success(f"The selection has been computed")
        result_table, review_table, graph_table = st.tabs(["Results", "Gmaps Reviews" ,"Graphiques"])
        
        with result_table:
            st.header('Results')
            daily_poi_sorted = sort_prediction(prediction_list)   # for each day, prediction sorted by overall score
            days_table_name = [f'{i} days' for i in range(14)]
            
            # Print table for each day
            for day, day_table in enumerate(st.tabs(days_table_name)):
                with day_table:
                    print_result_table(daily_poi_sorted, day)

        with review_table:
            st.header('Gmaps Reviews')
            st.markdown("""
            TODO :
            - get the names of the reviews and propose it on a select box
            - find the associate review
            - print the review description (in dataframe) 
            - print the review and review score
            """)

        with graph_table:
            st.header('Tourism Data Visualization')
            fig = print_density(sub_df) # Density Map
            st.plotly_chart(fig, use_container_width=True)
            st.write("This map shows the density of tourism data points based on the selected categories and region.")

            fig = print_choropleth(sub_df) # Choropleth Map
            st.plotly_chart(fig, use_container_width=True)
            st.write("This map shows the count of tourism data points per department based on the selected categories and region.")
    
