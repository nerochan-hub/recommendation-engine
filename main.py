from fastapi import FastAPI, HTTPException # type: ignore
from database import get_all_internships, get_user_history
from recommender import recommend_internships

app = FastAPI(title="Internship Recommendation Engine")

@app.get("/")
def root():
    return {"message": "Welcome to the Internship Recommendation API!"}

@app.get("/internships/")
def list_internships():
    return get_all_internships()

@app.get("/recommend/{user_id}")
def recommend(user_id: int):
    history = get_user_history(user_id)
    if history is None:
        raise HTTPException(status_code=404, detail="User not found")
    recommendations = recommend_internships(history)
    return {"recommended_internships": recommendations}