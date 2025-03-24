from pydantic import BaseModel

class SubjectSchema(BaseModel):
    subject_id: int
    name: str
    amount: int

    class Config:
        from_attributes = True