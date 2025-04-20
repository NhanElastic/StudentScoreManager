from sqlalchemy.ext.asyncio import AsyncSession
from score.score_model import Score
from score.score_repository import ScoreRepository
import datetime

class ScoreService:
    def __init__(self, db: AsyncSession):
        self.repository = ScoreRepository(db)

    async def get_all_scores(self):
        return await self.repository.get_all()

    async def get_student_scores(self, student_id_dict: dict, is_ascending: bool):
        student_id = student_id_dict.get("student_id")
        return await self.repository.get_by_student(student_id, is_ascending)

    async def get_avg_score(self, student_id_dict: dict):
        student_id = student_id_dict.get("student_id")
        return await self.repository.get_avg_by_student(student_id)

    async def max_score_subjects(self):
        return await self.repository.get_max_score_subjects()

    async def add_score(self, student_id: int, subject_id: int, score: float, date: datetime.date):
        new_score = Score(
            student_id=student_id,
            subject_id=subject_id,
            score=score,
            date=date
        )
        return await self.repository.add(new_score)

    async def remove_score(self, score_id: int):
        score = await self.repository.get_by_id(score_id)
        if score:
            await self.repository.delete(score)
        return score

    async def update_score(self, score_id: int, score: float, date: datetime.date, student_id: int, subject_id: int):
        existing = await self.repository.get_by_id(score_id)
        if not existing:
            return None
        existing.score = score
        existing.date = date
        existing.student_id = student_id
        existing.subject_id = subject_id
        return await self.repository.update(existing)
