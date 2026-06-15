# backend/app/main.py
# FastAPI Main Application - SoulConnect Platform

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

load_dotenv()

# Import routes
from app.routes import auth, users, matching, chats, healers, sessions, meetups, admin

# Database
from app.database import engine, Base

# Create tables on startup
Base.metadata.create_all(bind=engine)

# Lifespan context
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 SoulConnect API Starting...")
    yield
    # Shutdown
    print("🛑 SoulConnect API Shutting down...")

# Initialize FastAPI app
app = FastAPI(
    title="SoulConnect API",
    description="Problem-solver peer support + healer platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(matching.router, prefix="/api/matches", tags=["Matching"])
app.include_router(chats.router, prefix="/api/chats", tags=["Chat"])
app.include_router(healers.router, prefix="/api/healers", tags=["Healers"])
app.include_router(sessions.router, prefix="/api/sessions", tags=["Sessions"])
app.include_router(meetups.router, prefix="/api/meetups", tags=["Meetups"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "🌟 SoulConnect API",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
