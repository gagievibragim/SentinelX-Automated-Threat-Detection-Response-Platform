from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path

from app.database import Base, engine
from app.api.events import router as events_router
from app.api.incidents import router as incidents_router
from app.api.stats import router as stats_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SentinelX",
    version="1.0.0",
    description="Automated Threat Detection & Response Platform",
)

app.include_router(events_router)
app.include_router(incidents_router)
app.include_router(stats_router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "sentinelx"}

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="dashboard"), name="static")

@app.get("/dashboard.css")
def dashboard_css():
    return FileResponse("dashboard/dashboard.css", media_type="text/css")

@app.get("/dashboard.js")
def dashboard_js():
    return FileResponse("dashboard/dashboard.js", media_type="application/javascript")

@app.get("/", response_class=HTMLResponse)
def dashboard():
    path = Path("dashboard/index.html")
    return path.read_text(encoding="utf-8")
