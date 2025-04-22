from sqlalchemy.ext.asyncio import AsyncSession
from subject.subject_model import Subject
from subject.subject_repository import SubjectRepository
from sqlalchemy.exc import SQLAlchemyError

class SubjectService:
    def __init__(self, db: AsyncSession):
        self.repository = SubjectRepository(db)

    async def get_all_subjects(self):
        try:
            return await self.repository.get_all()
        except Exception as e:
            raise Exception(f"Error fetching subjects: {str(e)}")

    async def add_subject(self, subject_id: int, name: str, amount: int):
        try:
            is_existing_id = await self.repository.get_by_id(subject_id)
            is_existing_name = await self.repository.is_subject_name_exists(name)
            if is_existing_id.get("data") or is_existing_name.get("exists"):
                return {"status": "error", "message": "Subject already exists"}
            
            subject = Subject(subject_id=subject_id, name=name, amount=amount)
            return await self.repository.add(subject)
        except SQLAlchemyError as e:
            raise Exception(f"Error adding subject: {str(e)}")

    async def remove_subject(self, subject_id: int):
        try:
            subject = await self.repository.get_by_id(subject_id)
            if not subject.get("data"):
                return {"status": "error", "message": "Subject not found"}
            
            return await self.repository.delete(subject.get("data"))
        except SQLAlchemyError as e:
            raise Exception(f"Error deleting subject: {str(e)}")

    async def update(self, subject_id: int, name: str, amount: int):
        try:
            subject = await self.repository.get_by_id(subject_id)
            if not subject.get("data"):
                return {"status": "error", "message": "Subject not found"}
            
            subject = subject.get("data")
            subject.name = name if name else subject.name
            subject.amount = amount if amount else subject.amount
            
            updated_subject = await self.repository.update(subject)
            return updated_subject
        except SQLAlchemyError as e:
            raise Exception(f"Error updating subject: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
        