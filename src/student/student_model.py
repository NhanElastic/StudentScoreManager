from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class Student(SQLModel, table=True):
    student_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, max_length=100)
    class_name: str = Field(nullable=False, max_length=50)
    birth: str = Field(nullable=False)


