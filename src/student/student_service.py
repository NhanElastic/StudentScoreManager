from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from student.student_model import Student

class StudentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_students(self):
        result = await self.db.execute(select(Student))
        students = result.scalars().fetchall() 
        return students 

    async def add_student(self, student_id: int, name: str, birthdate: str, class_: str):
        student = Student(student_id=student_id, name=name, birthdate=birthdate, class_=class_)
        self.db.add(student)
        await self.db.commit()
        await self.db.refresh(student)
        return student

    async def remove_student(self, student_id: int):
        result = await self.db.execute(select(Student).filter(Student.student_id == student_id))
        student = result.scalars().first()
        if student:
            await self.db.delete(student)
            await self.db.commit()
        return student

    async def update_student(self, student_id: int, name: str = None, birthdate: str = None, class_: str = None):
        result = await self.db.execute(select(Student).filter(Student.student_id == student_id))
        student = result.scalars().first()
        if not student:
            return None
        
        if name:
            student.name = name
        if birthdate:
            student.birthdate = birthdate
        if class_:
            student.class_ = class_

        await self.db.commit()
        await self.db.refresh(student)
        return student
