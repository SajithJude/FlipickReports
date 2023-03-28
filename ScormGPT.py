import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins
import streamlit.components.v1 as components
import os
import zipfile

# Define function to extract zip files
def extract_zip_file(file):
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall()

# Allow the user to upload a zip file
file = st.file_uploader('Upload zip file', type=['zip'])
if file is not None:
    extract_zip_file(file)

# Read data from Excel files
df_activity = pd.read_excel('AllLevelActivity_L1.xlsx', engine='openpyxl') if os.path.isfile('AllLevelActivity_L1.xlsx') else pd.DataFrame()
df_levelwise_assessment = pd.read_excel('LevelWiseAssesment_Level1.xlsx', engine='openpyxl') if os.path.isfile('LevelWiseAssesment_Level1.xlsx') else pd.DataFrame()
df_enrollment_metrics = pd.read_excel('EnrollmentMetrics.xlsx', engine='openpyxl') if os.path.isfile('EnrollmentMetrics.xlsx') else pd.DataFrame()
df_levelReport = pd.read_excel('LevelWiseReport_Level1.xlsx', engine='openpyxl') if os.path.isfile('LevelWiseReport_Level1.xlsx') else pd.DataFrame()



# Create session state if it does not exist
if 'df_activity' not in st.session_state:
    st.session_state['df_activity'] = df_activity
if 'df_levelwise_assessment' not in st.session_state:
    st.session_state['df_levelwise_assessment'] = df_levelwise_assessment
if 'df_enrollment_metrics' not in st.session_state:
    st.session_state['df_enrollment_metrics'] = df_enrollment_metrics
if 'df_levelReport' not in st.session_state:
    st.session_state['df_levelReport'] = df_levelReport

# Calculate performance metrics and create charts
if not df_activity.empty and not df_enrollment_metrics.empty:
    df_activity['hours'] = pd.to_datetime(df_activity.iloc[:, 9]) - pd.to_datetime(df_activity.iloc[:, 9]).min()
    df_activity['hours'] = df_activity['hours'].dt.total_seconds() / 3600
    average_time_spent = df_activity['hours'].mean()

    total_learners = len(df_enrollment_metrics)
    total_attempts = df_activity.iloc[:, 8].sum()

    fig, ax = plt.subplots()
    df_activity.iloc[:, [6, 9]].groupby(df_activity.iloc[:, 6]).sum().plot(kind='bar', ax=ax)
    ax.set_xlabel('Modules Completed')
    ax.set_ylabel('Total_No_Of_Attempts')
    plt.title('Total Attempts by Module')
    html_graph = mpld3.fig_to_html(fig, template_type="simple")

    # Create the streamlit app
    st.title('Overall Performance Dashboard')
    st.caption("This provides an overview of the performance metrics like total number of learners, average time spent, and total number of attempts for each module can be created to provide an overview of the institute's LMS usage")
    st.subheader('Performance Metrics')
    col1, col2, col3 = st.columns(3)
    col1.metric(label='Total Number of Learners:', value=total_learners, delta="1.3%")
    col2.metric(label='Total Number of Attempts:', value=total_attempts, delta="-1.5%")
    col3.metric(label='Average Time Spent', value=average_time_spent, delta="7%")
    st.subheader('Total Attempts by Module')
    components.html(html_graph, height=600)

# Delete Excel files at the end



df_levelReport.columns = [c.replace(' ', '_') for c in df_levelReport.columns]
df_levelwise_assessment.columns = [c.replace(' ', '_') for c in df_levelwise_assessment.columns]
df_enrollment_metrics.columns = [c.replace(' ', '_') for c in df_enrollment_metrics.columns]
df_activity.columns = [c.replace(' ', '_') for c in df_activity.columns]


df_enrollment_metrics = df_enrollment_metrics.rename(columns={'Learner_Email': 'Email_Id'})

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

st.caption("Predictive analytics")
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

