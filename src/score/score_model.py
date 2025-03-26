from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base


class Score(Base):
    __tablename__ = "score"

    score_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("student.student_id"), primary_key=True, autoincrement=False)
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey("subject.subject_id"), primary_key=True, autoincrement=False)
    score: Mapped[int] = mapped_column(Integer)
    date: Mapped[str] = mapped_column(Date)

    student = relationship("Student", back_populates="scores")
    subject = relationship("Subject", back_populates="scores")