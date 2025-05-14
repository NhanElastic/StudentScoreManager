from sqlalchemy.ext.asyncio import AsyncSession
from score.score_model import Score
from score.score_repository import ScoreRepository
import datetime
from student.student_repository import StudentRepository
from score.score_schema import ScoreSchema
class ScoreService:
    def __init__(self, db: AsyncSession):
        self.repository = ScoreRepository(db)
        self.student_repo = StudentRepository(db)

    async def get_all_scores(self):
        result = await self.repository.get_all()
        return result

    async def get_student_scores(self, student_id: int, is_ascending: bool):
        is_existing_student = await self.student_repo.get_by_id(student_id)
        if not is_existing_student:
            raise ValueError("Student not found.")
        result = await self.repository.get_student_scores(student_id, is_ascending)
        return result

    async def get_student_avg_score(self, student_id: int):
        is_existing_student = await self.student_repo.get_by_id(student_id)
        if not is_existing_student:
            raise ValueError("Student not found.")
        result = await self.repository.get_student_avg_score(student_id)
        return result
    

    async def get_max_subject_scores(self):
        result = await self.repository.get_max_subject_scores()
        return result

    async def add_score(self, score: ScoreSchema):
        if score is not None:
            is_existing_score = await self.repository.get_by_id(score.score_id)
            if is_existing_score:
                raise ValueError("Score already exists.")
        student = await self.student_repo.get_by_id(score.student_id)
        subject = await self.repository.get_subject_by_id(score.subject_id)
        if not student:
            raise ValueError("Student not found.")
        if not subject:
            raise ValueError("Subject not found.")
        score = self.repository.add(score)
        return score        

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

