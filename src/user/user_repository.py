from sqlalchemy.ext.asyncio import AsyncSession
from user.user_model import User
from sqlalchemy import select

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_username(self, username):
        result = await self.db.execute(
            select(User).filter(User.username == username)
        )
        return result.scalar_one_or_none()

    async def create_user(self, username: str, password: str, role: str = "user"):
        try:
            user = User(username=username, password=password, role=role)
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except Exception as e:
            await self.db.rollback()
            print(f"Error creating user: {e}")
            raise
    
    
    def update_user(self, user_id, user_data):
        # Logic to update an existing user in the database
        pass

    def delete_user(self, user_id):
        # Logic to delete a user from the database
        pass

