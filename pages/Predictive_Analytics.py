import streamlit as st 


import pandas as pd

df_levelwise_assessment  = st.session_state['df_levelwise_assessment'] 
df_enrollment_metrics  = st.session_state['df_enrollment_metrics'] 
df_activity  = st.session_state['df_activity'] 

# st.table(df_activity.head())
# st.table(df_levelwise_assessment.head())
# st.table(df_enrollment_metrics.head())

st.write(df_activity.columns[2])
# Merge the dataframes
# Merge the dataframes using iloc to select columns 1 and 2
# df = pd.merge(df_activity, df_levelwise_assessment, on=[df_activity.columns[2], df_activity.columns[3]])
# df = pd.merge(df, df_enrollment_metrics, on=[df_activity.columns[2], df_activity.columns[3]])

st.table(df_activity.head())
