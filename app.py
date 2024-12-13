# frontend
import streamlit as st
from src import df, geojson, get_prediction, best_rows

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
sub_df = sub_df[:5]


if st.button('Get Weather'):
    if conditions.empty:
        st.error('Please enter at least one categorie & departement')

    else:
        df_prediction = get_prediction(sub_df)
        output = best_rows(df_prediction)

        st.success(f"The selection have been compute")
        st.table(output)
            