from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import projects, blog, auth
from app.core.config import settings

app = FastAPI(
    title="Portfolio API",
    description="Backend API for personal portfolio website",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,     prefix="/api/auth",     tags=["Auth"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(blog.router,     prefix="/api/blog",     tags=["Blog"])


@app.get("/")
def root():
    return {"status": "ok", "message": "Portfolio API v2 is running 🚀"}
