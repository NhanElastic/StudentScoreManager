from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from subject.subject_model import Subject

class SubjectService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_subject(self, subject_id: int, name: str, amount: int):
        subject = Subject(subject_id=subject_id, name=name, amount=amount)
        self.db.add(subject)
        await self.db.commit()
        await self.db.refresh(subject)
        return subject
    
    async def remove_subject(self, subject_id: int):
        result = await self.db.execute(select(Subject).filter(Subject.subject_id == subject_id))
        subject = result.scalars().first()
        if subject:
            await self.db.delete(subject)
            await self.db.commit()
        return subject
    
    async def update(self, subject_id: int, name: str, amount: int):
        result = await self.db.execute(select(Subject).filter(Subject.subject_id == subject_id))
        subject = result.scalars().first()
        if not subject:
            return None
        
        if name:
            subject.name = name
        if amount:
            subject.amount = amount

        await self.db.commit()
        await self.db.refresh(subject)
        return subject
    
    async def get_subjects(self):
        result = await self.db.execute(select(Subject))
        subjects = result.scalars().fetchall()
        return subjects