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
            if scores.get("status") == "error":
                return {"status": "error", "message": scores.get("message")}
            return scores
        except Exception:
            return {"status": "error", "message": "Failed to fetch scores"}

    async def get_student_scores(self, student_id: int, is_ascending: bool):
        if student_id is None:
            return {"status": "error", "message": "Missing student_id"}
        try:
            scores = await self.repository.get_by_student(student_id, is_ascending)
            if scores.get("status") == "error":
                return {"status": "error", "message": scores.get("message")}
            return {"status": "success", "data": scores.get("data")}
        except Exception:
            return {"status": "error", "message": "Failed to fetch student's scores"}

    async def get_avg_score(self, student_id: int):
        if student_id is None:
            return {"status": "error", "message": "Missing student_id"}
        try:
            avg_score = await self.repository.get_avg_by_student(student_id)
            if avg_score.get("status") == "error":
                return {"status": "error", "message": avg_score.get("message")}
            return avg_score
        except Exception:
            return {"status": "error", "message": "Failed to calculate average score"}

    async def max_score_subjects(self):
        try:
            max_scores = await self.repository.get_max_score_subjects()
            if max_scores.get("status") == "error":
                return {"status": "error", "message": max_scores.get("message")}
            return max_scores
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
            if added_score.get("status") == "error":
                return {"status": "error", "message": added_score.get("message")}
            return added_score
        except Exception:
            return {"status": "error", "message": "Failed to add score"}

    async def remove_score(self, score_id: int):
        if score_id is None:
            return {"status": "error", "message": "Missing score_id"}
        existing = await self.repository.get_by_id(score_id)
        if not existing:
            return {"status": "error", "message": "Score not found"}
        try:
            deleted_score = await self.repository.delete(existing.get("data"))
            if deleted_score.get("status") == "error":
                return {"status": "error", "message": deleted_score.get("message")}
            return deleted_score
        except Exception:
            return {"status": "error", "message": "Failed to delete score"}

    async def update_score(self, score_id: int, score: float, date: datetime.date, student_id: int, subject_id: int):
        if score_id is None:
            return {"status": "error", "message": "Missing score_id"}
        existing = await self.repository.get_by_id(score_id)
        if not existing:
            return {"status": "error", "message": "Score not found"}
        current_score = existing.get("data")
        current_score.score = score if score is not None else current_score.score
        current_score.date = date if date is not None else current_score.date
        current_score.student_id = student_id if student_id is not None else current_score.student_id
        current_score.subject_id = subject_id if subject_id is not None else current_score.subject_id
        updated_score = await self.repository.update(current_score)
        if updated_score.get("status") == "error":
            return {"status": "error", "message": updated_score.get("message")}
        return updated_score

