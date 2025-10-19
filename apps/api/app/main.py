from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import health, resume

app = FastAPI(
    title="Career Intelligence API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router, prefix="/api/v1/health", tags=["health"])
app.include_router(resume.router, prefix="/api/v1/resume", tags=["resume"])

@app.get("/api/v1")
def root():
    return {"ok": True, "service": "career-intel-api"}
