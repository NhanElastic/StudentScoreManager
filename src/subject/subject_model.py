from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class Subject(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, max_length=255)
    amount: int = Field(nullable=False)

