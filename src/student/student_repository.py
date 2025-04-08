from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from student.student_model import Student

class StudentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(Student))
        return result.scalars().all()

    async def get_by_id(self, student_id: int):
        result = await self.db.execute(select(Student).filter(Student.student_id == student_id))
        return result.scalars().first()

    async def add(self, student: Student):
        self.db.add(student)
        await self.db.commit()
        await self.db.refresh(student)
        return student

    async def delete(self, student: Student):
        await self.db.delete(student)
        await self.db.commit()

    async def update(self):
        await self.db.commit()
