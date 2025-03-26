from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base
class Student(Base):
    __tablename__ = "student" 

    student_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(255))
    birthdate: Mapped[str] = mapped_column(Date)
    class_: Mapped[str] = mapped_column(String(255))

    scores = relationship("Score", back_populates="student", cascade="all, delete-orphan")
    