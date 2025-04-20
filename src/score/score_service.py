from sqlalchemy.ext.asyncio import AsyncSession
from score.score_model import Score
from score.score_repository import ScoreRepository
import datetime

class ScoreService:
    def __init__(self, db: AsyncSession):
        self.repository = ScoreRepository(db)

    async def get_all_scores(self):
        try:
            scores = await self.repository.get_all()
            return {"status": "success", "data": scores}
        except Exception:
            return {"status": "error", "message": "Failed to fetch scores"}

    async def get_student_scores(self, student_id_dict: dict, is_ascending: bool):
        student_id = student_id_dict.get("student_id")
        if student_id is None:
            return {"status": "error", "message": "Missing student_id"}
        try:
            scores = await self.repository.get_by_student(student_id, is_ascending)
            return {"status": "success", "data": scores}
        except Exception:
            return {"status": "error", "message": "Failed to fetch student's scores"}

    async def get_avg_score(self, student_id_dict: dict):
        student_id = student_id_dict.get("student_id")
        if student_id is None:
            return {"status": "error", "message": "Missing student_id"}
        try:
            avg_score = await self.repository.get_avg_by_student(student_id)
            return {"status": "success", "data": avg_score}
        except Exception:
            return {"status": "error", "message": "Failed to calculate average score"}

    async def max_score_subjects(self):
        try:
            max_scores = await self.repository.get_max_score_subjects()
            return {"status": "success", "data": max_scores}
        except Exception:
            return {"status": "error", "message": "Failed to fetch max scores by subject"}

    async def add_score(self, student_id: int, subject_id: int, score: float, date: datetime.date):
        if not all([student_id, subject_id, score, date]):
            return {"status": "error", "message": "Missing one or more required fields"}
        new_score = Score(
            student_id=student_id,
            subject_id=subject_id,
            score=score,
            date=date
        )
        try:
            added_score = await self.repository.add(new_score)
            return {"status": "success", "data": added_score}
        except Exception:
            return {"status": "error", "message": "Failed to add score"}

    async def remove_score(self, score_id: int):
        score = await self.repository.get_by_id(score_id)
        if not score:
            return {"status": "error", "message": "Score not found"}
        try:
            await self.repository.delete(score)
            return {"status": "success", "message": "Score deleted"}
        except Exception:
            return {"status": "error", "message": "Failed to delete score"}

    async def update_score(self, score_id: int, score: float, date: datetime.date, student_id: int, subject_id: int):
        existing = await self.repository.get_by_id(score_id)
        if not existing:
            return {"status": "error", "message": "Score not found"}
        existing.score = score
        existing.date = date
        existing.student_id = student_id
        existing.subject_id = subject_id
        try:
            updated_score = await self.repository.update(existing)
            return {"status": "success", "data": updated_score}
        except Exception:
            return {"status": "error", "message": "Failed to update score"}
