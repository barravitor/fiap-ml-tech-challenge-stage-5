# api/routes/app_routes.py
import os
from fastapi import APIRouter, Depends, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from requests import Session
from sqlalchemy import desc
from shared.utils.dependencies import get_current_user
from shared.db.database import get_session_local
from shared.db.models.index_models import ApplicationModelDb, JobModelDb

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '..', '..', 'frontend')

app_router = APIRouter()

templates = Jinja2Templates(directory=os.path.join(FRONTEND_DIR, 'templates'))

@app_router.get("/", response_class=HTMLResponse)
async def get_app(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app_router.get("/login", response_class=HTMLResponse)
async def get_app(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app_router.get("/create-account", response_class=HTMLResponse)
async def get_app(request: Request):
    return templates.TemplateResponse("create-account.html", {"request": request})

@app_router.get("/recruiters/jobs", response_class=HTMLResponse)
async def get_app(request: Request):
    return templates.TemplateResponse("recruiter.html", {"request": request})

@app_router.get("/recruiters/jobs/{job_id}", response_class=HTMLResponse)
async def get_app(request: Request):
    return templates.TemplateResponse("recruiter.html", {"request": request})

@app_router.get("/candidates/jobs")
def get_candidate_jobs(request: Request, current_user: dict = Depends(get_current_user), db: Session = Depends(get_session_local)):
    jobs = (
        # db.query(JobModelDb)
        #     .order_by(desc(JobModelDb.created_at))
        #     .limit(10)
        #     .all(),
        {
            'id': 1,
            'job_title': 'teste 1'
        },
                {
            'id': 2,
            'job_title': 'teste 2'
        }
    )

    return templates.TemplateResponse("candidate.html", {
        "request": request,
        "jobs": jobs
    })

@app_router.get("/candidates/jobs/{job_id}")
def serve_chatbot(job_id: int, request: Request):
    # vaga = vagas.get(vaga_id)
    # if not vaga:
    #     return JSONResponse({"error": "Vaga não encontrada"}, status_code=404)
    return templates.TemplateResponse("chatbot.html", {"request": request, "vaga": 1})