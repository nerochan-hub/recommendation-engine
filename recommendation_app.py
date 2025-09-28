from fastapi import FastAPI, Body
from fastapi import Request
from fastapi import Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi.staticfiles import StaticFiles




app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
sentence_model = SentenceTransformer("all-MiniLM-L6-v2")

class UserInfo(BaseModel):
    name: str
    dob: str
    location: str
    department: str
    college_name: str
    skills: List[str]
    email: str

class InternshipOffer(BaseModel):
    job_role: str
    skills_required: List[str]
    location: str
    stipend: str
    period: str
    mode: str


internship_offers = [
    InternshipOffer(job_role="Software Developer Intern",
                    skills_required=["Python", "Git", "Django"],
                    location="Bangalore",
                    stipend="10000 INR",
                    period="3 months",
                    mode="Remote"),
    InternshipOffer(job_role="Mechanical Design Intern",
                    skills_required=["AutoCAD", "SolidWorks"],
                    location="Chennai",
                    stipend="7000 INR",
                    period="2 months",
                    mode="In-office")
]

# embeddings
internship_embeddings = sentence_model.encode(
    [f"{offer.job_role} {' '.join(offer.skills_required)} {offer.location} {offer.stipend}" for offer in internship_offers]
)


@app.get("/", response_class=HTMLResponse)
def form_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/recommend", response_class=HTMLResponse)
def recommend(
    request: Request,
    name: str = Form(...),
    dob: str = Form(...),
    location: str = Form(...),
    department: str = Form(...),
    college_name: str = Form(...),
    skills: str = Form(...), 
    email: str = Form(...)
):
    user_skills = skills.split(",")
    qry = f"{department} {' '.join(user_skills)} {location}"
    qry_emb = sentence_model.encode([qry])
    sims = cosine_similarity(qry_emb, internship_embeddings)[0]
    top_indices = np.argsort(sims)[::-1][:5]
    recommendations = [internship_offers[i] for i in top_indices]

    return templates.TemplateResponse(
        "results.html",
        {"request": request, "name": name, "recommendations": recommendations}
    )


@app.post("/recommend-internships/")
def recommend_internships(user: UserInfo = Body(...)):
    # user query
    qry = f"{user.department} {' '.join(user.skills)} {user.location}"
    qry_emb = sentence_model.encode([qry])
    sims = cosine_similarity(qry_emb, internship_embeddings)[0]
    top_indices = np.argsort(sims)[::-1][:8]  
    recommendations = [internship_offers[i] for i in top_indices if sims[i] > 0.2]  
    return recommendations[:8] 
