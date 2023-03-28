import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins
import streamlit.components.v1 as components

# Read data from CSV files
df_activity = pd.read_csv('AllLevelActivity_L1 - Sheet 1.csv')
df_levelwise_assessment = pd.read_csv('LevelWiseAssement_Level1 - Sheet 1.csv')
df_enrollment_metrics = pd.read_csv('EnrollmentMetrics - Sheet 1.csv')

df_activity['Total_Time_Spent'] = pd.to_timedelta(df_activity['Total_Time_Spent'])

# Calculate performance metrics
total_learners = len(df_enrollment_metrics)
total_attempts = df_activity['Total_No_Of_Attempts'].sum()
average_time_spent = df_activity['Total_Time_Spent'].mean()

# Create a bar chart of total attempts for each module
fig, ax = plt.subplots()
df_activity[['Modules Completed', 'Total No Of Attempts']].groupby(['Modules Completed']).sum().plot(kind='bar', ax=ax)
ax.set_xlabel('Modules Completed')
ax.set_ylabel('Total No Of Attempts')
plt.title('Total Attempts by Module')

# Convert the plot to an interactive chart using mpld3
html_graph = mpld3.fig_to_html(fig, template_type="simple")

# Create the streamlit app
st.title('Overall Performance Dashboard')
st.subheader('Performance Metrics')
st.write('Total Number of Learners:', total_learners)
st.write('Total Number of Attempts:', total_attempts)
st.write('Average Time Spent:', average_time_spent)
st.subheader('Total Attempts by Module')
components.html(html_graph)
