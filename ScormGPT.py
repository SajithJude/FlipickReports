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
for filename in ['AllLevelActivity_L1.xlsx', 'LevelWiseAssesment_Level1.xlsx', 'EnrollmentMetrics.xlsx', 'LevelWiseReport_Level1.xlsx']:
    if os.path.isfile(filename):
        os.remove(filename)

