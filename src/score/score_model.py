from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from student.student_model import Student

class Score(SQLModel, table=True):
    score_id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.student_id")
    subject_id: int = Field(foreign_key="subject.subject_id")
    score: int = Field(nullable=False)

    student: Optional[Student] = Relationship(back_populates="scores")
