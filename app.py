import streamlit as st
import pandas as pd

def app():
    st.set_page_config(page_title="IncidentInsight App", layout="wide")
    st.title("IncidentInsight: Incident Event Log Viewer")

    st.write(
        """
        This app allows you to view and explore your incident event log data.
        """
    )

    # Load the dataset
    try:
        df = pd.read_csv("incident_event_log.csv")
        st.success("Dataset loaded successfully!")
    except FileNotFoundError:
        st.error("Error: 'incident_event_log.csv' not found. Please make sure the file is in the same directory as the app.")
        return

    st.header("Dataset Overview")

    st.subheader("First 5 Rows of the Dataset")
    st.dataframe(df.head())

    st.subheader("Dataset Information")
    st.write(f"Number of rows: {df.shape[0]}")
    st.write(f"Number of columns: {df.shape[1]}")

    st.subheader("Summary Statistics")
    st.write(df.describe())

    st.subheader("Column Information")
    st.write(df.info())

    st.subheader("Null Values per Column")
    st.write(df.isnull().sum())

    st.header("Interactive Data Exploration")

    # Select columns to display
    all_columns = df.columns.tolist()
    selected_columns = st.multiselect("Select columns to display", all_columns, default=all_columns[:5])

    if selected_columns:
        st.dataframe(df[selected_columns])
    else:
        st.warning("Please select at least one column to display.")

    # Filter by a specific column (example: 'Category' if it exists)
    if 'Category' in df.columns:
        st.subheader("Filter by Category")
        unique_categories = df['Category'].unique().tolist()
        selected_category = st.selectbox("Select a Category", ['All'] + unique_categories)

        if selected_category != 'All':
            filtered_df = df[df['Category'] == selected_category]
            st.dataframe(filtered_df)
            st.write(f"Showing {len(filtered_df)} incidents in '{selected_category}' category.")
        else:
            st.dataframe(df)

if __name__ == "__main__":
    app()