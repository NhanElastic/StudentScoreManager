from pydantic import BaseModel
from typing import Optional

class CreateUserReq(BaseModel):
    username: str
    password: str
    role: Optional[str] = "user"

class CreateUserRes(BaseModel):
    username: str
    scopes: str

    class Config:
        from_attributes = True
    
class UpdateUser(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str