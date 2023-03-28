import streamlit as st 


import pandas as pd

df_levelwise_assessment  = st.session_state['df_levelwise_assessment'] 
df_enrollment_metrics  = st.session_state['df_enrollment_metrics'] 
df_activity  = st.session_state['df_activity'] 


df_levelwise_assessment.columns = [c.replace(' ', '_') for c in df_levelwise_assessment.columns]
df_enrollment_metrics.columns = [c.replace(' ', '_') for c in df_enrollment_metrics.columns]
df_enrollment_metrics = df_enrollment_metrics.rename(columns={'Learner_Email': 'Email_Id'})
df_activity.columns = [c.replace(' ', '_') for c in df_activity.columns]

df_enrollment_metrics['target'] = df_enrollment_metrics.apply(lambda row: 1 if row['Diagnostic_Or_First_Level_Assigned'] == row['Current_Level'] else 0, axis=1)
# df_enrollment_metrics['DaysCount_after_enrolling'] = str( pd.to_datetime('today') - df_enrollment_metrics['Enrollment_Date']).dt.days

df_enrollment_metrics['Enrollment_Date'] = pd.to_datetime(df_enrollment_metrics['Enrollment_Date'])
df_enrollment_metrics['DaysCount_after_enrolling'] = (pd.to_datetime('today') - df_enrollment_metrics['Enrollment_Date']).dt.days

averagedayscount = df_enrollment_metrics['DaysCount_after_enrolling'].mean()

df_filtered = df_enrollment_metrics.loc[(df_enrollment_metrics['target'] == 1) & (df_enrollment_metrics['DaysCount_after_enrolling'] >= averagedayscount)]

# Select the columns with user names and emails
df_filtered = df_filtered[['Learner_Name', 'Email_Id']]

# Show the filtered dataframe
st.table(df_filtered)


# st.table(df_activity.head())
# st.table(df_enrollment_metrics.head())


# df = pd.merge(df_activity, df_levelwise_assessment, on=['Learner_Name', 'Email_Id'])

# st.table(df.head())

# df = df.drop(['Institute_x', 'Enrolled_By', 'Enrollment_Date'], axis=1)

# # Merge the dataframes using iloc to select columns 1 and 2
# df = pd.merge(df_activity, df_levelwise_assessment, on=[df_activity.iloc[:,1], df_activity.iloc[:,2]])
# df = pd.merge(df, df_enrollment_metrics, on=[df_activity.iloc[:,1], df_activity.iloc[:,2]])

# st.table(df.head())
