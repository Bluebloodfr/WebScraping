import streamlit as st
from src import *

df = get_df()
geojson = get_geojson()

def get_subdf():
    # Load data
    categorie_list = df['categorie'].unique()
    dept_list = geojson['nom'].unique()
    dept_list.sort()

    # Ask filter
    categories = st.multiselect("Choose one or more categories:", categorie_list)
    dept_name = st.selectbox("Choose a region:", dept_list)
    dept_code = geojson[geojson['nom'] == dept_name]['code'].iloc[0]

    # Filter data
    sub_df = df[(
        df['code_departement'] == dept_code) & (
        df['categorie'].isin(categories)
    )]
    sub_df = sub_df[:5] # Limit to 5 rows for demonstration purposes
    return sub_df


def page():
    st.title('Tourism App')
    st.markdown('Tourism app that helps you find the best places to visit based on weather and Google Maps reviews.')
    
    sub_df = get_subdf()

    if st.button('Run selection') and sub_df is not None:
        df_prediction = get_prediction(sub_df)
        output = best_rows(df_prediction)
        st.success(f"The selection has been computed")

        st.header('Raw Results')
        st.table(output)

        st.header('Tourism Data Visualization')
        fig = print_density(sub_df) # Density Map
        st.plotly_chart(fig, use_container_width=True)
        st.write("This map shows the density of tourism data points based on the selected categories and region.")

        fig = print_choropleth(sub_df) # Choropleth Map
        st.plotly_chart(fig, use_container_width=True)
        st.write("This map shows the count of tourism data points per department based on the selected categories and region.")
