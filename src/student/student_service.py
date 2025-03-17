from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from student.student_model import Student

class StudentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    