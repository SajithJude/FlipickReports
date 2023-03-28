import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins
import streamlit.components.v1 as components
import os

# Read data from Excel files
def read_excel_file(file):
    df = pd.read_excel(file, engine='openpyxl')
    return df

# Allow the user to upload Excel files
df_activity_file = st.file_uploader('Upload ALL level activity XLSX file', type=['xlsx'])
df_levelwise_assessment_file = st.file_uploader('Upload Level Wise assessment for level1 XLSX file', type=['xlsx'])
df_enrollment_metrics_file = st.file_uploader('Upload EnrollmentMetrics XLSX file', type=['xlsx'])

# If files already exist in the directory, load them
if os.path.isfile('AllLevelActivity_L1.xlsx'):
    df_activity = pd.read_excel('AllLevelActivity_L1.xlsx', engine='openpyxl')
    st.session_state['df_activity'] = df_activity
else:
    df_activity = pd.DataFrame()

if os.path.isfile('LevelWiseAssesment_Level1.xlsx'):
    df_levelwise_assessment = pd.read_excel('LevelWiseAssesment_Level1.xlsx', engine='openpyxl')
    st.session_state['df_levelwise_assessment'] = df_levelwise_assessment
else:
    df_levelwise_assessment = pd.DataFrame()

if os.path.isfile('EnrollmentMetrics.xlsx'):
    df_enrollment_metrics = pd.read_excel('EnrollmentMetrics.xlsx', engine='openpyxl')
    st.session_state['df_enrollment_metrics'] = df_enrollment_metrics
else:
    df_enrollment_metrics = pd.DataFrame()

# Read data from uploaded Excel files
if df_activity_file is not None:
    df_activity = read_excel_file(df_activity_file)
    df_activity.to_excel('df_activity.xlsx', index=False)
    st.session_state['df_activity'] = df_activity

if df_levelwise_assessment_file is not None:
    df_levelwise_assessment = read_excel_file(df_levelwise_assessment_file)
    df_levelwise_assessment.to_excel('df_levelwise_assessment.xlsx', index=False)
    st.session_state['df_levelwise_assessment'] = df_levelwise_assessment

if df_enrollment_metrics_file is not None:
    df_enrollment_metrics = read_excel_file(df_enrollment_metrics_file)
    df_enrollment_metrics.to_excel('df_enrollment_metrics.xlsx', index=False)
    st.session_state['df_enrollment_metrics'] = df_enrollment_metrics

try:
    df_activity['hours'] = pd.to_datetime(df_activity.iloc[:, 9]) - pd.to_datetime(df_activity.iloc[:, 9]).min()
    df_activity['hours'] = df_activity['hours'].dt.total_seconds() / 3600
    average_time_spent =  df_activity['hours'].mean()
    st.write(average_time_spent)



    # Calculate performance metrics
    total_learners = len(df_enrollment_metrics)
    total_attempts = df_activity.iloc[:, 8].sum()
    st.table(df_activity.head())

    # Create a bar chart of total attempts for each module
    fig, ax = plt.subplots()
    df_activity.iloc[:, [6, 9]].groupby(df_activity.iloc[:, 6]).sum().plot(kind='bar', ax=ax)
    ax.set_xlabel('Modules Completed')
    ax.set_ylabel('Total_No_Of_Attempts')
    plt.title('Total Attempts by Module')

    # Convert the plot to an interactive chart using mpld3
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

except IndexError:
    st.warning("Upload Files to View Analytics")


# except KeyError:
#     st.warning("Upload Files to View Analytics")