from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from student.student_model import Student
from subject.subject_model import Subject

class SubjectService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def add_subject(self, subject_id: int, name: str, amount: int):
        subject = Subject(subject_id=subject_id, name=name, amount=amount)
        self.db.add(subject)
        self.db.commit()
        self.db.refresh(subject)
        return subject
    
    def remove_subject(self, subject_id: int):
        subject = self.db.execute(select(Subject).filter(Subject.subject_id == subject_id)).scalars().first()
        self.db.delete(subject)
        self.db.commit()
        return subject
    
    def update(self, subject_id: int, name: str, amount: int):
        subject = self.db.execute(select(Subject).filter(Subject.subject_id == subject_id)).scalars().first()
        subject.name = name if name else subject.name
        subject.amount = amount if amount else subject.amount
        self.db.commit()
        self.db.refresh(subject)
        return subject
    
    def get_subjects(self):
        return self.db.execute(select(Subject)).scalars().all()