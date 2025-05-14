from pydantic import BaseModel
from typing import Optional

class CreateUserReq(BaseModel):
    username: str
    password: str
    role: Optional[str] = "user"

class CreateUserRes(BaseModel):
    username: str
    role: str

    class Config:
        from_attributes = True
    
class UpdateUser(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None

