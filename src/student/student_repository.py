from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from student.student_schema import StudentSchema
from student.student_model import Student

class StudentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(Student))
        return result.scalars().all()

    async def get_by_id(self, student_id: int):
        result = await self.db.execute(
            select(Student).filter(Student.student_id == student_id)
        )
        return result.scalar_one_or_none()
    
    async def add(self, student: StudentSchema):
        try:
            student = Student(**student.model_dump())
            existing_student = await self.get_by_id(student.student_id)
            if existing_student:
                raise ValueError("Student with this ID already exists.")
            
            self.db.add(student)
            await self.db.commit()
            await self.db.refresh(student)
            return student
        except SQLAlchemyError as e:
            await self.db.rollback()
            return None

    async def delete(self, student_id: int):
        try:
            student = await self.get_by_id(student_id)
            if not student:
                raise ValueError("Student not found.")
            await self.db.delete(student)
            await self.db.commit()
            return True
        except SQLAlchemyError as e:
            await self.db.rollback()
            return False
            

    async def update(self, student_id: int, student_data: StudentSchema):
        try:
            student = await self.get_by_id(student_id)
            if not student:
                raise ValueError("Student not found.")
            for key, value in student_data.model_dump().items():
                setattr(student, key, value)
            await self.db.commit()
            await self.db.refresh(student)
            return student
        except SQLAlchemyError as e:
            await self.db.rollback()
            print(f"Error updating student: {e}")
            return None