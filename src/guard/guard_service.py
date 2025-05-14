from abc import ABC, abstractmethod
from fastapi import Depends, HTTPException, status, Request
import jwt
import os
from typing import List

class BaseGuard(ABC):
    @abstractmethod
    async def validate(self, request: Request):
        pass

class APIRoleGuard(BaseGuard):
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles
        self.secret_key = os.getenv("SECRET_KEY")
        self.algorithm = os.getenv("ALGORITHM")

    def decode_jwt(self, token: str):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def validate(self, request: Request):
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unautherized",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        token = token.split(" ")[1]
        payload = self.decode_jwt(token)
        role = payload.get("role")
        if not role or role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: Insufficient permissions",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
def RoleGuard(allowed_roles: List[str]):
    async def guard(request: Request):
        guard = APIRoleGuard(allowed_roles)
        await guard.validate(request)
    return Depends(guard)