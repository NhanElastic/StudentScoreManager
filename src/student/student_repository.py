from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from student.student_model import Student

class StudentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        try:
            result = await self.db.execute(select(Student))
            return result.scalars().all()
        except SQLAlchemyError as e:
            return {"status": "error", "message": "Failed to fetch students", "error": str(e)}

    async def get_by_id(self, student_id: int):
        try:
            result = await self.db.execute(select(Student).filter(Student.student_id == student_id))
            return result.scalars().first()
        except SQLAlchemyError as e:
            return {"status": "error", "message": "Failed to fetch student by ID", "error": str(e)}

    async def add(self, student: Student):
        try:
            self.db.add(student)
            await self.db.commit()
            await self.db.refresh(student)
            return student
        except SQLAlchemyError as e:
            await self.db.rollback()
            return {"status": "error", "message": "Failed to add student", "error": str(e)}

    async def delete(self, student: Student):
        try:
            await self.db.delete(student)
            await self.db.commit()
            return {"status": "success", "message": "Student deleted"}
        except SQLAlchemyError as e:
            await self.db.rollback()
            return {"status": "error", "message": "Failed to delete student", "error": str(e)}

    async def update(self):
        try:
            await self.db.commit()
            return {"status": "success", "message": "Student updated"}
        except SQLAlchemyError as e:
            await self.db.rollback()
            return {"status": "error", "message": "Failed to update student", "error": str(e)}
