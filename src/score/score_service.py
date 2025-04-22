from sqlalchemy.ext.asyncio import AsyncSession
from score.score_model import Score
from score.score_repository import ScoreRepository
import datetime
from fastapi.responses import JSONResponse

class ScoreService:
    def __init__(self, db: AsyncSession):
        self.repository = ScoreRepository(db)

    async def get_all_scores(self):
        try:
            scores = await self.repository.get_all()
            return JSONResponse(content={"data": scores}, status_code=200)
        except Exception:
            return JSONResponse(content={"message": "Failed to fetch scores"}, status_code=500)
        
    async def get_student_scores(self, student_id: int, is_ascending: bool):
        if student_id is None:
            return JSONResponse(content={"message": "Missing student_id"}, status_code=400)
        try:
            scores = await self.repository.get_by_student(student_id, is_ascending)
            if scores is None:
                return JSONResponse(content={"message": "No scores found for the student"}, status_code=404)
            return JSONResponse(content={"data": scores}, status_code=200)
        except Exception:
            return JSONResponse(content={"message": "Failed to fetch student's scores"}, status_code=500)
        
    async def get_avg_score(self, student_id: int):
        if student_id is None:
            return JSONResponse(content={"message": "Missing student_id"}, status_code=400)
        try:
            avg_score = await self.repository.get_avg_by_student(student_id)
            if avg_score is None:
                return JSONResponse(content={"message": "No scores found for the student"}, status_code=404)
            return JSONResponse(content={"data": avg_score}, status_code=200)
        except Exception:
            return JSONResponse(content={"message": "Failed to calculate average score"}, status_code=500)
        
    async def max_score_subjects(self):
        try:
            max_scores = await self.repository.get_max_score_subjects()
            if max_scores is None:
                return JSONResponse(content={"message": "No scores found"}, status_code=404)
            return JSONResponse(content={"data": max_scores}, status_code=200)
        except Exception:
            return JSONResponse(content={"message": "Failed to fetch max score subjects"}, status_code=500)

    async def add_score(self, student_id: int, subject_id: int, score: float, date: datetime.date):
        if not all([student_id, subject_id, score, date]):
            return JSONResponse(content={"message": "Missing required fields"}, status_code=400)
        new_score = Score(
            student_id=student_id,
            subject_id=subject_id,
            score=score,
            date=date
        )
        try:
            added_score = await self.repository.add(new_score)
            if added_score is None:
                return JSONResponse(content={"message": "Failed to add score"}, status_code=500)
            return JSONResponse(content={"message": "Score added successfully", "data": added_score}, status_code=201)
        except Exception:
            return JSONResponse(content={"message": "Failed to add score"}, status_code=500)

    async def remove_score(self, score_id: int):
        score = await self.repository.get_by_id(score_id)
        if not score:
            return JSONResponse(content={"message": "Score not found"}, status_code=404)
        try:
            await self.repository.delete(score)
            return JSONResponse(content={"message": "Score removed successfully"}, status_code=200)
        except Exception:
            return JSONResponse(content={"message": "Failed to remove score"}, status_code=500)
        
    async def update_score(self, score_id: int, score: float, date: datetime.date, student_id: int, subject_id: int):
        existing = await self.repository.get_by_id(score_id)
        if not existing:
            return JSONResponse(content={"message": "Score not found"}, status_code=404)
        existing.score = score
        existing.date = date
        existing.student_id = student_id
        existing.subject_id = subject_id
        try:
            updated_score = await self.repository.update(existing)
            if updated_score is None:
                return JSONResponse(content={"message": "Failed to update score"}, status_code=500)
        except Exception:
            return JSONResponse(content={"message": "Failed to update score"}, status_code=500)
        return JSONResponse(content={"message": "Score updated successfully"}, status_code=200)
    
    async def calculate_all_avg_scores(self):
        try:
            avg_scores = await self.repository.calculate_all_avg_scores()
            if avg_scores is None:
                return JSONResponse(content={"message": "No scores found"}, status_code=404)
            return JSONResponse(content={"data": avg_scores}, status_code=200)
        except Exception:
            return JSONResponse(content={"message": "Failed to calculate average scores"}, status_code=500)