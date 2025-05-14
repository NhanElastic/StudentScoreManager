from abc import ABC, abstractmethod
from fastapi import Depends, HTTPException, status, Request
import jwt
import os
from typing import List, Annotated
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
class BaseGuard(ABC):
    @abstractmethod
    async def validate(self, request: Request):
        pass

class APIRoleGuard(BaseGuard):
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def credentials_exception(self, detail: str):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

    def extract_token_from_header(self, request: Request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        return auth_header.split(" ")[1]
    
    def decode_jwt(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise self.credentials_exception("Token has expired")
        except jwt.InvalidTokenError:
            raise self.credentials_exception("Invalid token")
    
    async def validate(self, request: Request):
        token = self.extract_token_from_header(request)
        if not token:
            raise self.credentials_exception("Not authenticated")
        
        payload = self.decode_jwt(token)
        role = payload.get("role")
        if not role or role not in self.allowed_roles:
            raise self.credentials_exception("Forbidden: Insufficient permissions")
        
def RoleGuard(allowed_roles: List[str]):
    async def guard(request: Request):
        guard = APIRoleGuard(allowed_roles)
        await guard.validate(request)
    return Depends(guard)


def get_current_username(token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))]):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception

    return username