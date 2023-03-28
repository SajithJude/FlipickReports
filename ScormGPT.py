import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins
import streamlit.components.v1 as components

# Read data from CSV files
# df_activity = pd.read_csv('AllLevelActivity_L1 - Sheet 1.csv')
# df_levelwise_assessment = pd.read_csv('LevelWiseAssement_Level1 - Sheet 1.csv')
# df_enrollment_metrics = pd.read_csv('EnrollmentMetrics - Sheet 1.csv')


def read_excel_file(file):
    df = pd.read_excel(file, engine='openpyxl')
    return df

# Allow the user to upload Excel files
df_activity_file = st.file_uploader('Upload ALL level activity XLSX file', type=['xlsx'])
df_levelwise_assessment_file = st.file_uploader('Upload Level Wise assessment for level1 XLSX file', type=['xlsx'])
df_enrollment_metrics_file = st.file_uploader('Upload EnrollmentMetrics XLSX file', type=['xlsx'])

# Read data from uploaded Excel files
if df_activity_file is not None:
    df_activity = read_excel_file(df_activity_file)
else:
    df_activity = pd.DataFrame()
    
if df_levelwise_assessment_file is not None:
    df_levelwise_assessment = read_excel_file(df_levelwise_assessment_file)
else:
    df_levelwise_assessment = pd.DataFrame()

if df_enrollment_metrics_file is not None:
    df_enrollment_metrics = read_excel_file(df_enrollment_metrics_file)
else:
    df_enrollment_metrics = pd.DataFrame()

# try:


df_activity['Total_Time_Spent'] = pd.to_timedelta(df_activity.iloc[:, 9])
# Calculate performance metrics
total_learners = len(df_enrollment_metrics)
total_attempts = df_activity['Total_No_Of_Attempts'].sum()
average_time_spent = df_activity['Total_Time_Spent'].mean()

# Create a bar chart of total attempts for each module
fig, ax = plt.subplots()
df_activity[['Modules Completed', 'Total_No_Of_Attempts']].groupby(['Modules Completed']).sum().plot(kind='bar', ax=ax)
ax.set_xlabel('Modules Completed')
ax.set_ylabel('Total_No_Of_Attempts')
plt.title('Total Attempts by Module')

# Convert the plot to an interactive chart using mpld3
html_graph = mpld3.fig_to_html(fig, template_type="simple")

activityhrs = df_activity['Total_Time_Spent'].dt.total_seconds() / 3600
ahrs = activityhrs.mean()
# Create the streamlit app
st.title('Overall Performance Dashboard')
st.subheader('Performance Metrics')
col1, col2, col3 = st.columns(3)
col1.metric(label='Total Number of Learners:', value=total_learners, delta="1.3%")
col2.metric(label='Total Number of Attempts:', value=total_attempts, delta="-1.5%")
col3.metric(label='Average Time Spent', value=ahrs, delta="7%")
st.subheader('Total Attempts by Module')
components.html(html_graph, height=600)



# except KeyError:
#     st.warning("Upload Files to View Analytics")