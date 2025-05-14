from pydantic import BaseModel
from typing import Optional
import datetime

class ScoreSchema(BaseModel):
    student_id: Optional[int] = None
    subject_id: Optional[int] = None
    score_id: Optional[int] = None
    score: Optional[int] = 0
    date: Optional[datetime.date] = datetime.date.today()

    class Config:
        from_attributes = True

class StudentScoreSchema(BaseModel):
    student_id: int
    isAscending: bool

    class Config:
        from_attributes = True