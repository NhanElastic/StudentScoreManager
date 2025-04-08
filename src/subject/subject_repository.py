from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from subject.subject_model import Subject

class SubjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(Subject))
        return result.scalars().all()

    async def get_by_id(self, subject_id: int):
        result = await self.db.execute(select(Subject).filter(Subject.subject_id == subject_id))
        return result.scalars().first()

    async def add(self, subject: Subject):
        self.db.add(subject)
        await self.db.commit()
        await self.db.refresh(subject)
        return subject

    async def delete(self, subject: Subject):
        await self.db.delete(subject)
        await self.db.commit()

    async def update(self, subject: Subject):
        await self.db.commit()
        await self.db.refresh(subject)
        return subject
