from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Ghost Dashboard v4.0", version="4.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routers import repos, ai, stats, local, docker_monitor

app.include_router(repos.router, prefix="/api/repos", tags=["repos"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
app.include_router(stats.router, prefix="/api/stats", tags=["stats"])
app.include_router(local.router, prefix="/api/local", tags=["local"])
app.include_router(docker_monitor.router, prefix="/api/docker", tags=["docker"])

@app.get("/")
def root():
    return {"status": "Ghost Dashboard v4.0 running", "ai": os.getenv("AI_NAME")}
