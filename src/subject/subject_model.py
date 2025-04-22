from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base

class Subject(Base):
    __tablename__ = "subject"

    subject_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    amount: Mapped[int] = mapped_column(Integer)

    scores = relationship('Score', back_populates='subject', cascade='all, delete-orphan')