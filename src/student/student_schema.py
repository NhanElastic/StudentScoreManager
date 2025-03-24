from pydantic import BaseModel
import datetime

class StudentSchema(BaseModel):
    student_id: int
    name: str
    birthdate: datetime.date
    class_: str

    class Config:
        from_attributes = True 