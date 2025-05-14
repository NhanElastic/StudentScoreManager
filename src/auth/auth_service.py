from user.user_repository import UserRepository
from auth.auth_schema import SignInSchema, Token, AccessToken
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import os
from sqlalchemy.ext.asyncio import AsyncSession

class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret = os.getenv("SECRET_KEY")
        self.algorithm = os.getenv("ALGORITHM")

    async def verify_password(self, password, hashed_password):
        return self.pwd_context.verify(password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret, self.algorithm)
        return encoded_jwt
    
    def create_refresh_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes = 30)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret, self.algorithm)
        return encoded_jwt

    async def authenticate_user(self, username: str, password: str):
        user = await self.user_repository.get_user_by_username(username)
        if not user or not await self.verify_password(password, user.password):
            raise ValueError("Invalid username or password")
        return user

    async def sign_in(self, sign_in_data: SignInSchema) -> Token:
        user = await self.authenticate_user(sign_in_data.username, sign_in_data.password)

        acces_token_expires = timedelta(minutes=15)
        refresh_token_expires = timedelta(days=30)
        access_token = self.create_access_token(
            data={"sub": user.username, "role": user.role}, expires_delta=acces_token_expires
        )
        refresh_token = self.create_refresh_token(
            data={"sub": user.username}, expires_delta=refresh_token_expires
        )
        return Token(access_token=access_token, refresh_token=refresh_token)
    
    async def refresh_access_token(self, refresh_token: str) -> AccessToken:
        try:
            payload = jwt.decode(refresh_token, self.secret, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise ValueError("Invalid refresh token")
            user = await self.user_repository.get_user_by_username(username)
            if user is None:
                raise ValueError("User not found")
        except jwt.ExpiredSignatureError:
            raise ValueError("Refresh token has expired")
        except jwt.JWTError:
            raise ValueError("Invalid refresh token")

        access_token_expires = timedelta(minutes=15)
        access_token = self.create_access_token(
            data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
        )
        return AccessToken(access_token=access_token)