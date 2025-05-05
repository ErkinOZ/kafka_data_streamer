import streamlit as st
import pandas as pd
import requests
import time

API_URL = "http://localhost:8000"

# -----------------------------
# Fetching data via API
# -----------------------------
def get_all_activities():
    try:
        response = requests.get(f"{API_URL}/activities")
        return pd.DataFrame(response.json())
    except:
        return pd.DataFrame()

def get_user_ids():
    try:
        response = requests.get(f"{API_URL}/users")
        return response.json().get("users", [])
    except:
        return []

def get_activities_by_user(user_id: int):
    try:
        response = requests.get(f"{API_URL}/activities/{user_id}")
        return pd.DataFrame(response.json())
    except:
        return pd.DataFrame()

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="User Activity Dashboard", layout="wide")
st.title("Real-Time Telecom Activity via API")

placeholder = st.empty()
iteration = 0  # Counter for generating unique keys

while True:
    iteration += 1
    df = get_all_activities()
    if df.empty:
        st.warning("No data from API. Make sure FastAPI is running.")
        time.sleep(5)
        continue

    df = df.rename(columns={"long": "longitude"})

    with placeholder.container():
        #Metrics
        st.subheader("General Statistics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Unique Users", df["user_id"].nunique())
        col2.metric("Base Stations", df["basestation"].nunique())
        col3.metric("Visited Domains", df["hostname"].nunique())

        # General Table
        st.subheader("Latest Activities")
        st.dataframe(df, use_container_width=True)

        # Map for all users
        st.subheader("Activity Map (All Users)")
        st.map(df[['lat', 'longitude']], use_container_width=True)

        # Search by user_id
        st.subheader("Search by Specific User")
        user_ids = get_user_ids()
        selected_user = st.selectbox(
            "Select user_id",
            options=["All"] + user_ids,
            key=f"user_filter_{iteration}"  # Unique key
        )

        if selected_user != "All":
            user_df = get_activities_by_user(selected_user)
            if not user_df.empty:
                user_df = user_df.rename(columns={"long": "longitude"})
                st.success(f"Records Found: {len(user_df)} for user_id={selected_user}")
                st.dataframe(user_df, use_container_width=True)

                st.subheader("Activity Map for Selected User")
                st.map(user_df[['lat', 'longitude']], use_container_width=True)
            else:
                st.warning("No data for the selected user.")

    time.sleep(5)
