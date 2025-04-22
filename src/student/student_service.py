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
            if existing.get("data"):
                return {"status": "error", "message": "Student already exists"}
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
            if not student.get("data"):
                return {"status": "error", "message": "Student not found"}
            await self.repo.delete(student.get("data"))
            return {"status": "success", "message": "Student deleted"}
        except SQLAlchemyError as e:
            return {"status": "error", "message": "Failed to delete student", "error": str(e)}
        

    async def update_student(self, student_id: int, name: str = None, birthdate: datetime.date = None, class_: str = None):
        try:
            student = await self.repo.get_by_id(student_id)
            if not student.get("data"):
                return {"status": "error", "message": "Student not found"}
            student = student.get("data")
            student.name = name if name else student.name
            student.birthdate = birthdate if birthdate else student.birthdate
            student.class_ = class_ if class_ else student.class_
            return await self.repo.update(student)
        except SQLAlchemyError as e:
            return {"status": "error", "message": "Failed to update student", "error": str(e)}
        
