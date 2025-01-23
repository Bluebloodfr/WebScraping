import streamlit as st

#from src import *
from src.prediction import sort_prediction_ids
from src.print_maps import *


def print_result_table(df_sub, df_pred):
    st.header('Results')
    daily_ids_sorted = sort_prediction_ids(df_pred)
    
    days_table_name = [f'{i} days' for i in range(14)]
    for day, day_table in enumerate(st.tabs(days_table_name)):
    
        with day_table:
            st.subheader(f'Best activity in {day} days')           
            printed_table = []
            for ids in daily_ids_sorted[day]:
                # retrive the row in df
                row = df_sub.loc[ids].to_dict()
                poi = df_pred.loc[ids].to_dict()
                
                printed_table.append({
                    'name' : row['nom'],
                    'adresse': f"{row['adresse']}, {row['commune']}",
                    'weather_desc': poi['weather_desc'][day],
                    'weather_score': round(poi['weather_score'][day], 1),
                    'rating_score': round(poi['rating_score'], 1),
                    'star_score': round(poi['star_score'], 1),
                    'overall_score': round(poi['overall_score'][day], 1),
                })
            st.table(printed_table)


def print_review_table(df_sub, df_pred):
    st.header('Gmaps Reviews')
    review_name = st.session_state.review_name
    selected_name = st.selectbox("Choose an option", options=df_sub['nom'].unique(), key='review_name')
    review_name = review_name if review_name else selected_name

    if review_name and review_name != '':
        # Get review_list
        df_row = df_sub[df_sub['nom'] == review_name].iloc[0]
        review_list = df_pred.loc[int(df_row.name), 'review_list']

        # Print
        st.markdown(f"""
        Adresse : {df_row['adresse']}, {df_row['codepostal']} - {df_row['commune']}  
        More info : {df_row['url']}  
        Description :  
        {df_row['description']}""")
        st.write('---')
        length = min(40, len(review_list)-1)
        for review in review_list[:length]:
            st.markdown(f"""
            Reviewer : {review["reviewer"]}  
            Scraped rating score: {"⭐" * review["rating"]}  
            Compute star score: {"⭐" * review["star"]}  
            {review["review"]}
            """)
            st.write('---')




def print_graph_table(df_sub):
    st.header('Tourism Data Visualization')
    fig = print_density(df_sub) # Density Map
    st.plotly_chart(fig, use_container_width=True)
    st.write("This map shows the density of tourism data points based on the selected categories and region.")

    fig = print_choropleth(df_sub) # Choropleth Map
    st.plotly_chart(fig, use_container_width=True)
    st.write("This map shows the count of tourism data points per department based on the selected categories and region.")