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
        is_existing_subject = await self.repo.get_by_id(subject_data.subject_id)
        if is_existing_subject:
            raise ValueError("Subject already exists.")
        subject = await self.repo.add(subject_data)
        return subject

    async def remove_subject(self, subject_id: int):
        subject = await self.repo.get_by_id(subject_id)
        if not subject:
            raise ValueError("Subject not found.")
        result = await self.repo.delete(subject)
        return result

    async def update(self, subject_id: int, subject_data: SubjectSchema):
        subject = await self.get_by_id(subject_id)
        if not subject:
            raise ValueError("Subject not found.")
        subject = await self.repo.update(subject, subject_data)
        return subject
        