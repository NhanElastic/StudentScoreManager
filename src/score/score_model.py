from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from student.student_model import Student
import datetime
from subject.subject_model import Subject

class Score(SQLModel, table=True):
    score_id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    subject_id: int = Field(foreign_key="subject.id")
    score: int = Field(nullable=False)
    date: datetime.date = Field(nullable=False)

    student: Student = Relationship(back_populates="scores")  
    subject: Subject = Relationship(back_populates="scores")