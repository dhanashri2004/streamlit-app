import pandas as pd
import plotly.express as px

# Load the dataset
try:
    df = pd.read_csv('incident_event_log.csv')
except FileNotFoundError:
    print("Error: incident_event_log.csv not found. Please ensure the file is in the same directory as the script.")
    exit()

# Convert 'opened_at' to datetime for potential time-based analysis if needed, though not strictly for this plot
df['opened_at'] = pd.to_datetime(df['opened_at'], errors='coerce', dayfirst=True)

# Count incidents by category
category_counts = df['category'].value_counts().reset_index()
category_counts.columns = ['Category', 'Count']

# Create a bar chart using plotly.express
fig = px.bar(
    category_counts.head(10), # Show top 10 categories for clarity
    x='Category',
    y='Count',
    title='Top 10 Incident Categories',
    labels={'Category': 'Incident Category', 'Count': 'Number of Incidents'},
    color='Category'
)

# Display the plot (this will open in your default browser if run in an environment that supports it)
fig.show()

# You can also save the plot to an HTML file
fig.write_html("incident_categories_plot.html")
print("Plot saved to incident_categories_plot.html")