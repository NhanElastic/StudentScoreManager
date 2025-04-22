from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from .student_repository import StudentRepository
from student.student_model import Student
import datetime
from fastapi.responses import JSONResponse
class StudentService:
    def __init__(self, db: AsyncSession):
        self.repo = StudentRepository(db)

    async def get_all_students(self):
        try:
            students = await self.repo.get_all()
            return JSONResponse(content={"data": students}, status_code=200)
        except SQLAlchemyError as e:
            return JSONResponse(content={"message": "Failed to fetch students", "error": str(e)}, status_code=500)

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
            added_student = await self.repo.add(student)
            return JSONResponse(content={"message": "Student added successfully", "data": added_student}, status_code=201)
        except ValueError as e:
            return JSONResponse(content={"message": str(e)}, status_code=400)
        except SQLAlchemyError as e:
            return JSONResponse(content={"message": "Failed to add student", "error": str(e)}, status_code=500)

    async def remove_student(self, student_id: int):
        try:
            student = await self.repo.get_by_id(student_id)
            if not student:
                return JSONResponse(content={"message": "Student not found"}, status_code=404)
            await self.repo.delete(student)
            return JSONResponse(content={"message": "Student removed successfully"}, status_code=200)
        except SQLAlchemyError as e:
            return JSONResponse(content={"message": "Failed to delete student", "error": str(e)}, status_code=500)

    async def update_student(self, student_id: int, name: str = None, birthdate: datetime.date = None, class_: str = None):
        try:
            student = await self.repo.get_by_id(student_id)
            if not student:
                return JSONResponse(content={"message": "Student not found"}, status_code=404)
            if name is not None:
                student.name = name
            if birthdate is not None:
                student.birthdate = birthdate
            if class_ is not None:
                student.class_ = class_

            await self.repo.update()
            return JSONResponse(content={"message": "Student updated successfully"}, status_code=200)
        except SQLAlchemyError as e:
            return JSONResponse(content={"message": "Failed to update student", "error": str(e)}, status_code=500)