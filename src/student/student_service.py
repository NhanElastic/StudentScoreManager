from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from .student_repository import StudentRepository
from student.student_model import Student
import datetime

class StudentService:
    def __init__(self, db: AsyncSession):
        self.repo = StudentRepository(db)

    async def get_all_students(self):
        try:
            return await self.repo.get_all()
        except SQLAlchemyError as e:
            return {"status": "error", "message": "Failed to fetch students", "error": str(e)}

    async def add_student(self, student_id: int, name: str, birthdate: datetime.date, class_: str):
        try:
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
        except ValueError as e:
            return {"status": "error", "message": str(e)}
        except SQLAlchemyError as e:
            return {"status": "error", "message": "Failed to add student", "error": str(e)}

    async def remove_student(self, student_id: int):
        try:
            student = await self.repo.get_by_id(student_id)
            if not student:
                return {"status": "error", "message": "Student not found"}
            await self.repo.delete(student)
            return {"status": "success", "message": "Student removed"}
        except SQLAlchemyError as e:
            return {"status": "error", "message": "Failed to remove student", "error": str(e)}

    async def update_student(self, student_id: int, name: str = None, birthdate: datetime.date = None, class_: str = None):
        try:
            student = await self.repo.get_by_id(student_id)
            if not student:
                return {"status": "error", "message": "Student not found"}

            if name is not None:
                student.name = name
            if birthdate is not None:
                student.birthdate = birthdate
            if class_ is not None:
                student.class_ = class_

            await self.repo.update()
            return {"status": "success", "message": "Student updated", "student": student}
        except SQLAlchemyError as e:
            return {"status": "error", "message": "Failed to update student", "error": str(e)}
