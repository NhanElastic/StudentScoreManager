from user.user_schema import CreateUserReq
import os
from passlib.context import CryptContext
from user.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from auth.auth_service import AuthService

class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db)
        self.auth_service = AuthService(db)
        self.secret_key = os.getenv("SECRET_KEY")
        self.algorithm = os.getenv("ALGORITHM")
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
    async def get_user_by_username(self, username):
        return await self.user_repository.get_user_by_username(username)

    async def create_user(self, user_data: CreateUserReq):
        username = user_data.username
        password = user_data.password
        role = user_data.role if user_data.role else "user"
        existing_user = await self.user_repository.get_user_by_username(username)
        if existing_user:
            raise ValueError("User already exists.")
        
        hashed_password = self.pwd_context.hash(password)
        user = await self.user_repository.create_user(username, hashed_password, role)
        return user
    
    async def change_password(self, username: str, old_password: str, new_password: str):
        user = await self.auth_service.authenticate_user(username, old_password)
        print(f"User authenticated: {user.username}")
        hashed_password = self.pwd_context.hash(new_password)
        updated_user = await self.user_repository.change_password(user, hashed_password)
        return updated_user

    async def update_user(self, user_id, user_data):
        return await self.user_repository.update_user(user_id, user_data)

    async def delete_user(self, user_id):
        return await self.user_repository.delete_user(user_id)