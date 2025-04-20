from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from subject.subject_model import Subject
from sqlalchemy.exc import SQLAlchemyError

class SubjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        try:
            result = await self.db.execute(select(Subject))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise Exception(f"Error fetching all subjects: {str(e)}")

    async def get_by_id(self, subject_id: int):
        try:
            result = await self.db.execute(select(Subject).filter(Subject.subject_id == subject_id))
            return result.scalars().first()
        except SQLAlchemyError as e:
            raise Exception(f"Error fetching subject by ID: {str(e)}")

    async def add(self, subject: Subject):
        try:
            self.db.add(subject)
            await self.db.commit()
            await self.db.refresh(subject)
            return subject
        except SQLAlchemyError as e:
            raise Exception(f"Error adding subject: {str(e)}")

    async def delete(self, subject: Subject):
        try:
            await self.db.delete(subject)
            await self.db.commit()
        except SQLAlchemyError as e:
            raise Exception(f"Error deleting subject: {str(e)}")

    async def update(self, subject: Subject):
        try:
            await self.db.commit()
            await self.db.refresh(subject)
            return subject
        except SQLAlchemyError as e:
            raise Exception(f"Error updating subject: {str(e)}")
