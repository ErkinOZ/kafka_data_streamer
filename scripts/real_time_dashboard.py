import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# --------------------------
def get_engine():
    return create_engine('postgresql://dev:dev123@localhost:5432/demo')

# --------------------------
#Fetching joined data
# --------------------------
def fetch_joined_data():
    engine = get_engine()
    query = """
        SELECT 
            a.user_id,
            r.name,
            r.city,
            r.device,
            r.tariff,
            a.datetime,
            a.basestation,
            a.hostname,
            a.lat,
            a.long
        FROM user_activity_log a
        JOIN user_registration_log r ON a.user_id = r.user_id
        ORDER BY a.datetime DESC
        LIMIT 500
    """
    df = pd.read_sql(query, engine)
    return df

# --------------------------
# Streamlit settings
# --------------------------
st.set_page_config(page_title="User Activity Dashboard", layout="wide")
st.title("Real-Time Telecom User Activity")

# Fetching and preparing data
df = fetch_joined_data()

if df.empty:
    st.warning("No data available.")
    st.stop()

df = df.rename(columns={"long": "longitude"})

#Metrics
st.subheader("General Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Unique Users", df["user_id"].nunique())
col2.metric("Base Stations", df["basestation"].nunique())
col3.metric("Domains", df["hostname"].nunique())

#General Activity Table
st.subheader("General Activity Table")
st.dataframe(df, use_container_width=True)

#Search by user_id
st.subheader("Search by User")
user_ids = sorted(df["user_id"].unique())
selected_user_id = st.selectbox("Select user_id", options=["All"] + user_ids)

#Filtered data by selected user_id
filtered_df = df if selected_user_id == "All" else df[df["user_id"] == selected_user_id]

#Activity Map
st.subheader("Activity Map")
if not filtered_df.empty:
    st.map(filtered_df[['lat', 'longitude']], use_container_width=True)
else:
    st.info("No activity for the selected user.")

#Additional Table for Selected User
st.subheader("Details for Selected user_id")
st.write(f"Records Found: **{len(filtered_df)}**")
st.dataframe(filtered_df, use_container_width=True)
