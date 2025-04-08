from sqlalchemy.ext.asyncio import AsyncSession
from .student_repository import StudentRepository
from student.student_model import Student
import datetime

class StudentService:
    def __init__(self, db: AsyncSession):
        self.repo = StudentRepository(db)

    async def get_all_students(self):
        return await self.repo.get_all()

    async def add_student(self, student_id: int, name: str, birthdate: datetime.date, class_: str):
        existing = await self.repo.get_by_id(student_id)
        if existing:
            raise ValueError("Student already exists")

        student = Student(
            student_id=student_id,
            name=name,
            birthdate=birthdate,
            class_=class_
        )
        return await self.repo.add(student)

    async def remove_student(self, student_id: int):
        student = await self.repo.get_by_id(student_id)
        if not student:
            return None
        await self.repo.delete(student)
        return student

    async def update_student(self, student_id: int, name: str = None, birthdate: datetime.date = None, class_: str = None):
        student = await self.repo.get_by_id(student_id)
        if not student:
            return None

        if name is not None:
            student.name = name
        if birthdate is not None:
            student.birthdate = birthdate
        if class_ is not None:
            student.class_ = class_

        await self.repo.update()
        return student
