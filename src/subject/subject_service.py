from sqlalchemy.ext.asyncio import AsyncSession
from subject.subject_model import Subject
from subject.subject_repository import SubjectRepository
from sqlalchemy.exc import SQLAlchemyError

class SubjectService:
    def __init__(self, db: AsyncSession):
        self.repository = SubjectRepository(db)

    async def get_subjects(self):
        try:
            return await self.repository.get_all()
        except Exception as e:
            raise Exception(f"Error fetching subjects: {str(e)}")

    async def add_subject(self, subject_id: int, name: str, amount: int):
        try:
            existing_subject = await self.repository.get_by_id(subject_id)
            if existing_subject:
                raise ValueError(f"Subject with ID {subject_id} already exists.")
            
            new_subject = Subject(subject_id=subject_id, name=name, amount=amount)
            return await self.repository.add(new_subject)
        except ValueError as e:
            raise e  
        except SQLAlchemyError as e:
            raise Exception(f"Error adding subject: {str(e)}")

    async def remove_subject(self, subject_id: int):
        try:
            subject = await self.repository.get_by_id(subject_id)
            if not subject:
                return {"message": "Subject not found"}
            await self.repository.delete(subject)
            return {"message": "Subject removed successfully"}
        except SQLAlchemyError as e:
            raise Exception(f"Error deleting subject: {str(e)}")

    async def update(self, subject_id: int, name: str, amount: int):
        try:
            subject = await self.repository.get_by_id(subject_id)
            if not subject:
                return {"message": "Subject not found"}
            
            subject.name = name
            subject.amount = amount
            updated_subject = await self.repository.update(subject)
            return updated_subject
        except SQLAlchemyError as e:
            raise Exception(f"Error updating subject: {str(e)}")
