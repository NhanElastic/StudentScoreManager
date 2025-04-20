from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from score.score_model import Score
from sqlalchemy.exc import SQLAlchemyError

class ScoreRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        try:
            result = await self.db.execute(select(Score))
            return result.scalars().all()
        except SQLAlchemyError:
            return {"status": "error", "message": "Failed to fetch scores"}

    async def get_by_student(self, student_id: int, ascending: bool):
        try:
            query = select(Score).filter(Score.student_id == student_id)
            query = query.order_by(Score.date.asc() if ascending else Score.date.desc())
            result = await self.db.execute(query)
            return result.scalars().all()
        except SQLAlchemyError:
            return {"status": "error", "message": "Failed to fetch student's scores"}

    async def get_avg_by_student(self, student_id: int):
        try:
            result = await self.db.execute(
                select(func.avg(Score.score)).filter(Score.student_id == student_id)
            )
            return result.scalar()
        except SQLAlchemyError:
            return {"status": "error", "message": "Failed to calculate average score"}

    async def get_max_score_subjects(self):
        try:
            result = await self.db.execute(
                select(Score.subject_id, func.max(Score.score)).group_by(Score.subject_id)
            )
            return result.all()
        except SQLAlchemyError:
            return {"status": "error", "message": "Failed to fetch max scores by subject"}

    async def add(self, score: Score):
        try:
            self.db.add(score)
            await self.db.commit()
            await self.db.refresh(score)
            return score
        except SQLAlchemyError:
            await self.db.rollback()
            return {"status": "error", "message": "Failed to add score"}

    async def get_by_id(self, score_id: int):
        try:
            result = await self.db.execute(select(Score).filter(Score.score_id == score_id))
            return result.scalars().first()
        except SQLAlchemyError:
            return {"status": "error", "message": "Failed to fetch score by ID"}

    async def delete(self, score: Score):
        try:
            await self.db.delete(score)
            await self.db.commit()
            return {"status": "success", "message": "Score deleted"}
        except SQLAlchemyError:
            await self.db.rollback()
            return {"status": "error", "message": "Failed to delete score"}

    async def update(self, score: Score):
        try:
            await self.db.commit()
            await self.db.refresh(score)
            return score
        except SQLAlchemyError:
            await self.db.rollback()
            return {"status": "error", "message": "Failed to update score"}
