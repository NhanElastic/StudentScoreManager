from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.database import init_db
from student import student_model
from subject import subject_model
from score import score_model

# Lifespan event to initialize database
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔄 Initializing Database...")
    await init_db()  # Async database initialization
    yield
    print("🛑 Shutting down application...")

# Create FastAPI App with lifespan event
app = FastAPI(lifespan=lifespan)

# Register Routers