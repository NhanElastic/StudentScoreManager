from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from student.student_model import Student
from subject.subject_model import Subject

class SubjectService:
    def __init__(self, db: AsyncSession):
        self.db = db

    