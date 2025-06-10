import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuration ---
st.set_page_config(
    page_title="Incident Log Analyzer",
    page_icon=":bar_chart:",
    layout="wide"
)

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv('incident_event_log.csv')
    # Convert date columns to datetime objects
    date_cols = ['opened_at', 'sys_created_at', 'sys_updated_at', 'resolved_at', 'closed_at']
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce', dayfirst=True)
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("Filter Options")

# Date range filter
min_date = df['opened_at'].min().date()
max_date = df['opened_at'].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range (Opened At)",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range
    df_filtered = df[(df['opened_at'].dt.date >= start_date) & (df['opened_at'].dt.date <= end_date)]
else:
    df_filtered = df.copy()


# Multi-select filters for categorical columns
selected_incident_states = st.sidebar.multiselect(
    "Select Incident State(s)",
    options=df_filtered['incident_state'].unique(),
    default=df_filtered['incident_state'].unique()
)

selected_categories = st.sidebar.multiselect(
    "Select Category(ies)",
    options=df_filtered['category'].unique(),
    default=df_filtered['category'].unique()
)

selected_priorities = st.sidebar.multiselect(
    "Select Priority(ies)",
    options=df_filtered['priority'].unique(),
    default=df_filtered['priority'].unique()
)

selected_assignment_groups = st.sidebar.multiselect(
    "Select Assignment Group(s)",
    options=df_filtered['assignment_group'].unique(),
    default=df_filtered['assignment_group'].unique()
)

# Apply filters
df_filtered = df_filtered[
    (df_filtered['incident_state'].isin(selected_incident_states)) &
    (df_filtered['category'].isin(selected_categories)) &
    (df_filtered['priority'].isin(selected_priorities)) &
    (df_filtered['assignment_group'].isin(selected_assignment_groups))
]

# --- Main Dashboard ---
st.title("Incident Log Analyzer :bar_chart:")
st.markdown("Analyze incident trends and key metrics.")

# --- Key Metrics ---
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)

total_incidents = len(df_filtered['number'].unique())
active_incidents = df_filtered[df_filtered['active'] == True]['number'].nunique()
resolved_incidents = df_filtered[df_filtered['incident_state'] == 'Resolved']['number'].nunique()
closed_incidents = df_filtered[df_filtered['incident_state'] == 'Closed']['number'].nunique()


col1.metric("Total Unique Incidents", total_incidents)
col2.metric("Active Incidents", active_incidents)
col3.metric("Resolved Incidents", resolved_incidents)
col4.metric("Closed Incidents", closed_incidents)


st.markdown("---")

# --- Visualizations ---
st.subheader("Incident Trends and Distributions")

# Incidents by Incident State
incident_state_counts = df_filtered['incident_state'].value_counts().reset_index()
incident_state_counts.columns = ['Incident State', 'Count']
fig_state = px.bar(
    incident_state_counts,
    x='Incident State',
    y='Count',
    title='Incident Count by State',
    color='Incident State'
)
st.plotly_chart(fig_state, use_container_width=True)

# Incidents by Category
category_counts = df_filtered['category'].value_counts().reset_index()
category_counts.columns = ['Category', 'Count']
fig_category = px.bar(
    category_counts.head(10), # Show top 10 categories
    x='Category',
    y='Count',
    title='Top 10 Incident Categories',
    color='Category'
)
st.plotly_chart(fig_category, use_container_width=True)

# Incidents by Priority
priority_counts = df_filtered['priority'].value_counts().reset_index()
priority_counts.columns = ['Priority', 'Count']
# Ensure a consistent order for priority if possible (e.g., Critical, High, Medium, Low)
priority_order = ['1 - Critical', '2 - High', '3 - Moderate', '4 - Low']
priority_counts['Priority'] = pd.Categorical(priority_counts['Priority'], categories=priority_order, ordered=True)
priority_counts = priority_counts.sort_values('Priority')
fig_priority = px.pie(
    priority_counts,
    names='Priority',
    values='Count',
    title='Incident Distribution by Priority'
)
st.plotly_chart(fig_priority, use_container_width=True)

# Incidents over Time
# Group by day for plotting
df_filtered['opened_date_only'] = df_filtered['opened_at'].dt.date
incidents_over_time = df_filtered.groupby('opened_date_only').size().reset_index(name='Count')
incidents_over_time.columns = ['Date', 'Count']
fig_time = px.line(
    incidents_over_time,
    x='Date',
    y='Count',
    title='Incidents Opened Over Time'
)
st.plotly_chart(fig_time, use_container_width=True)

# --- Display Filtered Data (Optional) ---
st.subheader("Filtered Incident Data Sample")
st.dataframe(df_filtered.head(100)) # Display first 100 rows of filtered data