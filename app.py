import streamlit as st
from src import *


st.title('Tourism App')
st.markdown(ABOUT)
df = get_df() # dataframe with all POI (Point of Interest)

# Initialize session state variables
if 'dept_name' not in st.session_state:
    st.session_state.dept_name = []
if 'select_table' not in st.session_state:
    st.session_state.table = None
if 'review_name' not in st.session_state:
    st.session_state.review_name = None

st.header('Full App')
dept_name = st.session_state.dept_name

if dept_name == []:
    st.write('By default, all the filter are selected.')
    dept_name = st.multiselect("Choose a department:", sorted(dept_dict.keys()), key='dept_name')
    # page automatically refreshes when a selection is made
else:
    st.write('You have selected: ', dept_name)
    sub_df = get_subdf(df, dept_name).iloc[:5]  # iloc to limit API use
    prediction_list = get_prediction(sub_df)
    st.session_state.compute = (sub_df, prediction_list)
    st.success("The selection has been computed")
    
    # Choose between different table
    select_table = st.tabs(["Results", "Reviews", "Graph"])
    memory_table = st.session_state.table 
    select_table = memory_table if memory_table else select_table
    result_table, review_table, graph_table = select_table
    
    with result_table:
        st.session_state.table = result_table
        print_result_table(prediction_list, sub_df)
    with review_table:
        st.session_state.table = review_table
        print_review_table(prediction_list, sub_df)
    with graph_table:
        st.session_state.table = graph_table
        print_graph_table(sub_df)

#st.header('Scrapping only')
#print_scrapping_only()
