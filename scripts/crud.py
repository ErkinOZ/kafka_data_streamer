
import pandas as pd
from db import engine

def get_all_activities(limit=500):
    query = f"""
        SELECT 
            a.user_id, r.name, r.city, r.device, r.tariff,
            a.datetime, a.basestation, a.hostname, a.lat, a.long
        FROM user_activity_log a
        JOIN user_registration_log r ON a.user_id = r.user_id
        ORDER BY a.datetime DESC
        LIMIT {limit}
    """
    return pd.read_sql(query, engine)

def get_activities_by_user(user_id: int):
    query = f"""
        SELECT 
            a.user_id, r.name, r.city, r.device, r.tariff,
            a.datetime, a.basestation, a.hostname, a.lat, a.long
        FROM user_activity_log a
        JOIN user_registration_log r ON a.user_id = r.user_id
        WHERE a.user_id = {user_id}
        ORDER BY a.datetime DESC
    """
    return pd.read_sql(query, engine)

def get_user_ids():
    query = "SELECT DISTINCT user_id FROM user_registration_log ORDER BY user_id"
    df = pd.read_sql(query, engine)
    return df["user_id"].tolist()

