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
dropout = len(df_filtered)
total = len(df_enrollment_metrics)

# Select the columns with user names and emails
df_filtered = df_filtered[['Learner_Name', 'Email_Id']]

# Show the filtered dataframe
st.table(df_filtered)

st.title("Predictive analytics")
st.subheader("learners who are at risk of dropping out of the course")

col1, col2 = st.columns(2)
col1.metric("Predicted Dropout Count",value=dropout)
col2.metric("Percentage of Dropout Count",value=str((dropout/total)*100)+" %")

st.write("From the available data usage reports, we have predicted that " + str(dropout) + " Number of students are in the likelihood of dropping out, Click the button bellow to take proactive measures in retaining the learners.")

with st.expander("Take Proactive measures to retain Users"):
    proact = st.button("start")
    if proact:
        st.success("Generating Motivational Email and studyplan")

with st.expander("Keep pushing the persistent Users"):
    proact = st.button("Generate Email")
    if proact:
        st.success("Generating Motivational Email follow up questions")