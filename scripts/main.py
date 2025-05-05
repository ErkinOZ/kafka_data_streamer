from fastapi import FastAPI
from crud import get_all_activities, get_activities_by_user, get_user_ids

app = FastAPI()

@app.get("/")
def root():
    return {"message": "User Activity API is running"}

@app.get("/users")
def users():
    return {"users": get_user_ids()}

@app.get("/activities")
def activities():
    df = get_all_activities()
    return df.to_dict(orient="records")

@app.get("/activities/{user_id}")
def user_activity(user_id: int):
    df = get_activities_by_user(user_id)
    return df.to_dict(orient="records")

