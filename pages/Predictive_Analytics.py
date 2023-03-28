import streamlit as st 


import pandas as pd

df_levelwise_assessment  = st.session_state['df_levelwise_assessment'] 
df_enrollment_metrics  = st.session_state['df_enrollment_metrics'] 
df_activity  = st.session_state['df_activity'] 


df_levelwise_assessment.columns = [c.replace(' ', '_') for c in df_levelwise_assessment.columns]
df_enrollment_metrics.columns = [c.replace(' ', '_') for c in df_enrollment_metrics.columns]
df_enrollment_metrics = df_enrollment_metrics.rename(columns={'Learner_Email': 'Email_Id'})
df_activity.columns = [c.replace(' ', '_') for c in df_activity.columns]


st.table(df_activity.head())
st.table(df_enrollment_metrics.head())

# st.table(df_levelwise_assessment.head())
# st.table(df_enrollment_metrics.head())

# st.write(df_activity.iloc[:, 1])
# Merge the dataframes
df = pd.merge(df_activity, df_levelwise_assessment, on=['Learner_Name', 'Email_Id'])

st.table(df.head())
df2 = pd.merge(df, df_enrollment_metrics, on=['Learner_Name', 'Email_Id'])


st.table(df2.head())
df = df2.drop(['Institute_x', 'Institute_y', 'Enrolled_By', 'Enrollment_Date'], axis=1)

# # Merge the dataframes using iloc to select columns 1 and 2
# df = pd.merge(df_activity, df_levelwise_assessment, on=[df_activity.iloc[:,1], df_activity.iloc[:,2]])
# df = pd.merge(df, df_enrollment_metrics, on=[df_activity.iloc[:,1], df_activity.iloc[:,2]])

st.table(df.head())
