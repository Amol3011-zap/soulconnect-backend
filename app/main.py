from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

load_dotenv()

from app.routes import auth, users, matching, chats, healers, sessions, meetups, admin
from app.routes import journey
from app.routes import challenges
from app.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    import os
    from sqlalchemy import text
    db_url = os.getenv("DATABASE_URL", "NOT SET")
    print(f"DATABASE_URL starts with: {db_url[:40]}...")
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Running column migrations...")
    try:
        from app.database import get_engine
        with get_engine().connect() as conn:
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS age INTEGER"))
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS gender VARCHAR"))
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR DEFAULT 'user'"))
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS state VARCHAR"))
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS country VARCHAR"))
            conn.commit()
        print("Column migrations complete!")
    except Exception as e:
        print(f"Migration note: {e}")
    print("SoulConnect API started successfully!")
    yield
    print("SoulConnect API shutting down...")


app = FastAPI(
    title="SoulConnect API",
    description="Problem-solver peer support + healer platform",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(matching.router, prefix="/api/matches", tags=["Matching"])
app.include_router(chats.router, prefix="/api/chats", tags=["Chat"])
app.include_router(healers.router, prefix="/api/healers", tags=["Healers"])
app.include_router(sessions.router, prefix="/api/sessions", tags=["Sessions"])
app.include_router(meetups.router, prefix="/api/meetups", tags=["Meetups"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(journey.router, prefix="/api/journey", tags=["Soul Journey"])
app.include_router(challenges.router, prefix="/api/challenges", tags=["Daily Challenges"])


@app.get("/")
async def root():
    return {"message": "SoulConnect API", "status": "running", "docs": "/docs"}


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
