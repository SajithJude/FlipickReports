import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins
import streamlit.components.v1 as components
import os
import zipfile

# Define function to read Excel files
def read_excel_file(file):
    df = pd.read_excel(file, engine='openpyxl')
    return df

# Define function to extract zip files
def extract_zip_file(file):
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall()

# Define file uploaders
file_uploaders = {
    'Upload ALL level activity XLSX file': 'df_activity.xlsx',
    'Upload Level Wise assessment for level1 XLSX file': 'df_levelwise_assessment.xlsx',
    'Upload EnrollmentMetrics XLSX file': 'df_enrollment_metrics.xlsx',
    'Upload LevelWiseReport_Level1': 'df_levelReport.xlsx',
    'Upload zip file': 'data.zip'
}

# Create session state if it does not exist
if 'df_activity' not in st.session_state:
    st.session_state['df_activity'] = pd.DataFrame()
if 'df_levelwise_assessment' not in st.session_state:
    st.session_state['df_levelwise_assessment'] = pd.DataFrame()
if 'df_enrollment_metrics' not in st.session_state:
    st.session_state['df_enrollment_metrics'] = pd.DataFrame()
if 'df_levelReport' not in st.session_state:
    st.session_state['df_levelReport'] = pd.DataFrame()

# Allow the user to upload files and extract zip file
for title, filename in file_uploaders.items():
    file = st.file_uploader(title, type=['xlsx', 'zip'])
    if file is not None:
        if file.name.endswith('.zip'):
            extract_zip_file(file)
        else:
            df = read_excel_file(file)
            df.to_excel(filename, index=False)
            st.session_state[filename.replace('.xlsx', '')] = df

# Read data from Excel files
df_activity = st.session_state['df_activity']
df_levelwise_assessment = st.session_state['df_levelwise_assessment']
df_enrollment_metrics = st.session_state['df_enrollment_metrics']
df_levelReport = st.session_state['df_levelReport']

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
for filename in ['df_activity.xlsx', 'df_levelwise_assessment.xlsx', 'df_enrollment_metrics.xlsx', 'df_levelReport.xlsx']:
    if os.path.isfile(filename):
        os.remove(filename)
