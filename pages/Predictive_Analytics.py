import streamlit as st 
import os

import pandas as pd
import openai

# st.session_state['df_levelwise_assessment'] = {}
# st.session_state['df_enrollment_metrics'] = {}
# st.session_state['df_activity'] = {}
# st.session_state['df_levelReport'] = {}

openai.api_key = os.getenv("API_KEY")

df_levelwise_assessment  = st.session_state['df_levelwise_assessment'] 
df_enrollment_metrics  = st.session_state['df_enrollment_metrics'] 
df_activity  = st.session_state['df_activity'] 
df_levelReport = st.session_state['df_levelReport']


df_levelwise_assessment  = pd.DataFrame(df_levelwise_assessment)
df_enrollment_metrics  = pd.DataFrame(df_enrollment_metrics)
df_activity  = pd.DataFrame(df_activity)
df_levelReport = pd.DataFrame(df_levelReport)

st.table(df_enrollment_metrics)


df_levelReport.columns = [c.replace(' ', '_') for c in df_levelReport.columns]
df_levelwise_assessment.columns = [c.replace(' ', '_') for c in df_levelwise_assessment.columns]
df_enrollment_metrics.columns = [c.replace(' ', '_') for c in df_enrollment_metrics.columns]
df_activity.columns = [c.replace(' ', '_') for c in df_activity.columns]


# df_enrollment_metrics = df_enrollment_metrics.rename(columns={'Learner_Email': 'Email_Id'})

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

df_filtered_names = df_filtered['Learner_Name']
df_levelReport_filtered = df_levelReport[df_levelReport['Learner_Name'].isin(df_filtered_names)]

# Show the filtered dataframe
st.table(df_levelReport_filtered)

st.title("Predictive analytics")
st.subheader("learners who are at risk of dropping out of the course")

col1, col2 = st.columns(2)
col1.metric("Predicted Dropout Count",value=dropout)
col2.metric("Percentage of Dropout Count",value=str((round(dropout/total,2)*100))+" %")

st.write("From the available data usage reports, we have predicted that " + str(dropout) + " Number of students are in the likelihood of dropping out, Click the button bellow to take proactive measures in retaining the learners.")

with st.expander("Take Proactive measures to retain Users"):
    proact = st.button("start")
    moodules = st.multiselect("Select Weak modules",['Green', 'Yellow', 'Red', 'Blue'],)
    if proact:
        st.success("Generating Motivational Email and studyplan")
        inut = "Generate a Motivational followup email for students who feel lack of motivation due to low score on modules like :"+ str(moodules)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=inut,
            temperature=0.56,
            max_tokens=2100,
            top_p=1,
            frequency_penalty=0.35,
            presence_penalty=0
        )
        st.code(response.choices[0].text, language=None)

with st.expander("Congrajulate Active users"):
    proact = st.button("generate wish")
    if proact:
        st.success("Generating Motivational Email and studyplan")
        it = "Generate a Motivational followup email for students who feel lack of motivation due to low score on modules like "
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=it,
            temperature=0.56,
            max_tokens=2100,
            top_p=1,
            frequency_penalty=0.35,
            presence_penalty=0
        )
        st.code(response.choices[0].text, language=None)


with st.expander("Keep pushing the persistent Users"):
    proact = st.button("Generate Email")
    if proact:
        st.success("Generating Motivational Email follow up questions")




for filename in ['AllLevelActivity_L1.xlsx', 'LevelWiseAssesment_Level1.xlsx', 'EnrollmentMetrics.xlsx', 'LevelWiseReport_Level1.xlsx']:
    if os.path.isfile(filename):
        os.remove(filename)

