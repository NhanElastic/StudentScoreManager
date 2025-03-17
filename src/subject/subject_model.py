from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from score.score_model import Score

class Subject(SQLModel, table=True):
    subject_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, max_length=255)
    amount: int = Field(nullable=False)

    scores: List["Score"] = Relationship(back_populates="subject")
