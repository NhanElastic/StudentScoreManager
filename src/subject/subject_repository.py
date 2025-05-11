from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from subject.subject_model import Subject
from sqlalchemy.exc import SQLAlchemyError
from subject.subject_schema import SubjectSchema
class SubjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(Subject))
        return result.scalars().all()

    async def get_by_id(self, subject_id: int):
        result = await self.db.execute(
            select(Subject).filter(Subject.subject_id == subject_id)
        )
        return result.scalar_one_or_none()

    async def add(self, subject: SubjectSchema):
        try:
            subject = Subject(**subject.model_dump())
            is_existing = await self.get_by_id(subject.subject_id)
            if is_existing:
                raise ValueError("Subject with this ID already exists.")
            
            self.db.add(subject)
            await self.db.commit()
            await self.db.refresh(subject)
            return subject
        except SQLAlchemyError as e:
            await self.db.rollback()
            print(f"Error adding subject: {e}")
            return None
        
    async def delete(self, subject_id: int):
        try:
            subject = await self.get_by_id(subject_id)
            if not subject:
                raise ValueError("Subject not found.")
            await self.db.delete(subject)
            await self.db.commit()
            return True
        except SQLAlchemyError as e:
            await self.db.rollback()
            print(f"Error deleting subject: {e}")
            return False
        
    async def update(self, subject_id: int, subject_data: SubjectSchema):
        try:
            subject = await self.get_by_id(subject_id)
            if not subject:
                raise ValueError("Subject not found.")
            for key, value in subject_data.model_dump().items():
                setattr(subject, key, value)
            await self.db.commit()
            await self.db.refresh(subject)
            return subject
        except SQLAlchemyError as e:
            await self.db.rollback()
            print(f"Error updating subject: {e}")
            return None
        