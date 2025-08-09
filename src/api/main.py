from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.routes.public_routes import public_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting the application...")
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
    <li><b><a href="#/API Public Routes">API Public Routes</a></b>: Open access endpoints (e.g. predict).</li>
</ul>
<p>📚 For more details, visit our <a href="https://github.com/barravitor/fiap-ml-tech-challenge-stage-5" target="_blank">GitHub repository</a>.</p>
    """,
    version="1.0.0",
    openapi_tags=[{
        "name": "API Public Routes",
        "description": "Public API routes available without authentication."
    }]
)

app.include_router(public_router, prefix="/api/public", tags=["API Public Routes"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the API!"}