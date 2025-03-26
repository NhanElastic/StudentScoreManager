from pydantic import BaseModel
from typing import Optional
import datetime

class ScoreSchema(BaseModel):
    student_id: Optional[int] = None
    subject_id: Optional[int] = None
    score_id: int
    score: Optional[int] = None
    date: Optional[datetime.date] = None

    class Config:
        from_attributes = True