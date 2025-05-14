from pydantic import BaseModel

class SignInSchema(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class AccessToken(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel):
    refresh_token: str