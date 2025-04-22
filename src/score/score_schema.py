from pydantic import BaseModel
from typing import Optional
import datetime

class ScoreSchema(BaseModel):
    student_id: Optional[int] = None
    subject_id: Optional[int] = None
    score_id: Optional[int] = None
    score: Optional[int] = None
    date: Optional[datetime.date] = None

    class Config:
        from_attributes = True

class StudentScoreSchema(BaseModel):
    student_id: int
    isAscending: bool

    class Config:
        from_attributes = True