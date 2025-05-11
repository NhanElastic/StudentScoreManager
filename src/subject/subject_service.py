from sqlalchemy.ext.asyncio import AsyncSession
from subject.subject_model import Subject
from subject.subject_repository import SubjectRepository
from sqlalchemy.exc import SQLAlchemyError
from subject.subject_schema import SubjectSchema

class SubjectService:
    def __init__(self, db: AsyncSession):
        self.repo = SubjectRepository(db)

    async def get_all_subjects(self):
        subjects = await self.repo.get_all()
        return subjects

    async def add_subject(self, subject_data: SubjectSchema):
        subject = await self.repo.add(subject_data)
        return subject

    async def remove_subject(self, subject_id: int):
        result = await self.repo.delete(subject_id)
        return result

    async def update(self, subject_id: int, subject_data: SubjectSchema):
        subject = await self.repo.update(subject_id, subject_data)
        return subject
        