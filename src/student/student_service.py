from sqlalchemy.ext.asyncio import AsyncSession
from student.student_repository import StudentRepository
from student.student_model import Student
from student.student_schema import StudentSchema

class StudentService:
    def __init__(self, db: AsyncSession):
        self.repo = StudentRepository(db)

    async def get_all_students(self):
        students = await self.repo.get_all()
        return students

    async def add_student(self, student_data: StudentSchema):
        is_existing_student = await self.repo.get_by_id(student_data.student_id)
        if is_existing_student:
            raise ValueError("Student already exists.")
        student = await self.repo.add(student_data)
        return student

    async def remove_student(self, student_id: int):
        student = await self.repo.get_by_id(student_id)
        if not student:
            raise ValueError("Student not found.")
        result = await self.repo.delete(student)
        return result
        
    async def update_student(self, student_id: int, student_data: StudentSchema):
        student = await self.get_by_id(student_id)
        if not student:
            raise ValueError("Student not found.")
        student = await self.repo.update(student, student_data)
        return student
    
    async def get_student_by_id(self, student_id: int):
        student = await self.repo.get_by_id(student_id)
        return student