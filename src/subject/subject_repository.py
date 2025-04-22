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
            return {"status": "success", "data": result.scalars().all()}            
        except SQLAlchemyError as e:
            return {"status": "error", "message": "Failed to fetch subjects", "error": str(e)}

    async def get_by_id(self, subject_id: int):
        try:
            result = await self.db.execute(select(Subject).filter(Subject.subject_id == subject_id))
            subject = result.scalars().first()
            if subject:
                return {"status": "success", "data": subject}
            return {"status": "error", "message": "Subject not found"}
        except SQLAlchemyError as e:
            return {"status": "error", "message": "Failed to fetch subject by ID", "error": str(e)}

    async def add(self, subject: Subject):
        try:
            self.db.add(subject)
            await self.db.commit()
            await self.db.refresh(subject)
            return {"status": "success", "data": subject}
        except SQLAlchemyError as e:
            await self.db.rollback()
            return {"status": "error", "message": "Failed to add subject", "error": str(e)}
        
    async def delete(self, subject: Subject):
        try:
            await self.db.delete(subject)
            await self.db.commit()
            return {"status": "success", "message": "Subject deleted"}
        except SQLAlchemyError as e:
            await self.db.rollback()
            return {"status": "error", "message": "Failed to delete subject", "error": str(e)}

    async def update(self, subject: Subject):
        try:
            await self.db.commit()
            await self.db.refresh(subject)
            return {"status": "success", "data": subject}
        except SQLAlchemyError as e:
            await self.db.rollback()
            return {"status": "error", "message": "Failed to update subject", "error": str(e)}

    async def is_subject_name_exists(self, name: str):
        try:
            result = await self.db.execute(select(Subject).filter(Subject.name == name))
            return {"status": "success", "exists": result.scalars().first() is not None}
        except SQLAlchemyError as e:
            return {"status": "error", "message": "Failed to check subject name", "error": str(e)}
        