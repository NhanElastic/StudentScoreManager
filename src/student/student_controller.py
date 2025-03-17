from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from student.student_service import StudentService
from database.database import get_db

router = APIRouter(
    prefix="/students",
    tags=["students"],
    responses={404: {"description": "Not found"}},
)

