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
#dept_name = st.session_state.dept_name

st.write('By default, all the filter are selected.')
dept_name = st.multiselect("Choose a department:", 
    options=sorted(dept_dict.keys()), 
    default=st.session_state.dept_name)
st.session_state.dept_name = dept_name


if dept_name and dept_name != []:
    df_sub = get_subdf(df, dept_name).iloc[:5]  # iloc to limit API use
    df_pred = get_prediction(df_sub)
    #st.session_state.compute = (df_sub, df_pred)
    st.success("The selection has been computed")
    
    # Choose between different table
    select_table = st.tabs(["Results", "Reviews", "Graph"])
    memory_table = st.session_state.table 
    select_table = memory_table if memory_table else select_table
    result_table, review_table, graph_table = select_table
    
    with result_table:
        st.session_state.table = result_table
        print_result_table(df_sub, df_pred)
    with review_table:
        st.session_state.table = review_table
        print_review_table(df_sub, df_pred)
    with graph_table:
        st.session_state.table = graph_table
        print_graph_table(df_sub)

#st.header('Scrapping only')
#print_scrapping_only()
