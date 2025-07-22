# api/main.py
from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.routes.app_routes import app_router
from api.routes.public_routes import public_router
from api.routes.private_routes import private_router
from shared.db.database import create_table

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting the application...")
    create_table()
    yield
    print("Closing the application...")

app = FastAPI(
    lifespan=lifespan,
    title="FIAP ML API | Datathon",
    description="""
<h2>Welcome to the <strong>FIAP ML API | Datathon</strong> documentation.</h2>
<p>This API powers a job platform built for the FIAP Datathon challenge.</p>
<p><strong>Explore the available endpoints:</strong></p>
<ul>
    <li><b><a href="#/API Public Routes">API Public Routes</a></b>: Open access endpoints (e.g. job listings, public info).</li>
    <li><b><a href="#/API Private Routes">API Private Routes</a></b>: Authenticated routes for managing data (e.g. job creation).</li>
    <li><b><a href="#/App Routes">App Routes</a></b>: Web application-related endpoints (HTML rendering, static files).</li>
</ul>
<p>📚 For more details, visit our <a href="https://github.com/barravitor/fiap-ml-tech-challenge-stage-5" target="_blank">GitHub repository</a>.</p>
    """,
    version="1.0.0",
    openapi_tags=[{
        "name": "API Public Routes",
        "description": "Public API routes available without authentication, such as viewing job offers."
    }, {
        "name": "API Private Routes",
        "description": "Secure endpoints accessible only to authenticated users for managing jobs and profiles."
    }, {
        "name": "App Routes",
        "description": "Routes related to frontend behavior (HTML pages, static assets, and routing)."
    }]
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')
app.mount("/static", StaticFiles(directory=os.path.join(FRONTEND_DIR, 'static')), name="static")

app.include_router(public_router, prefix="/api/public", tags=["API Public Routes"])
app.include_router(private_router, prefix="/api/private", tags=["API Private Routes"])
app.include_router(app_router, prefix="/app", tags=["App Routes"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the API!"}