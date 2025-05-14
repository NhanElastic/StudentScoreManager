from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base

class User(Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, primary_key=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)