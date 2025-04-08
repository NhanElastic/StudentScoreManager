from sqlalchemy.ext.asyncio import AsyncSession
from subject.subject_model import Subject
from subject.subject_repository import SubjectRepository

class SubjectService:
    def __init__(self, db: AsyncSession):
        self.repository = SubjectRepository(db)

    async def get_subjects(self):
        return await self.repository.get_all()

    async def add_subject(self, subject_id: int, name: str, amount: int):
        new_subject = Subject(subject_id=subject_id, name=name, amount=amount)
        return await self.repository.add(new_subject)

    async def remove_subject(self, subject_id: int):
        subject = await self.repository.get_by_id(subject_id)
        if subject:
            await self.repository.delete(subject)
        return subject

    async def update(self, subject_id: int, name: str, amount: int):
        subject = await self.repository.get_by_id(subject_id)
        if not subject:
            return None
        
        subject.name = name
        subject.amount = amount
        return await self.repository.update(subject)
