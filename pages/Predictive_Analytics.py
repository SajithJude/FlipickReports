import streamlit as st 



df_levelwise_assessment  = st.session_state['df_levelwise_assessment'] 
df_enrollment_metrics  = st.session_state['df_enrollment_metrics'] 
df_activity  = st.session_state['df_activity'] 

st.table(df_activity.head())
st.table(df_levelwise_assessment.head())
st.table(df_enrollment_metrics.head())
