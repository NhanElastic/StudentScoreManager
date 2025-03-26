from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.database import init_db, close_db
from student import student_controller
from subject import subject_controller
from score import score_controller
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔄 Initializing Database...")
    await init_db() 
    try:
        yield  
    finally:
        print("🛑 Shutting down application...")
        await close_db()

# Create FastAPI App with lifespan event
app = FastAPI(lifespan=lifespan)
 
# Register Routers
app.include_router(student_controller.router)
app.include_router(subject_controller.router)
app.include_router(score_controller.router)
