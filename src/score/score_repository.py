from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from score.score_model import Score
from sqlalchemy.exc import SQLAlchemyError
from score.score_schema import ScoreSchema

class ScoreRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(Score))
        return result.scalars().all()

    async def get_student_scores(self, student_id: int, isAscending: bool = True):
        order_by = Score.score.asc() if isAscending else Score.score.desc()
        result = await self.db.execute(
            select(Score).filter(Score.student_id == student_id).order_by(order_by)
        )
        return result.scalars().all()

    async def get_student_avg_score(self, student_id: int):
        result = await self.db.execute(
            select(func.avg(Score.score)).filter(Score.student_id == student_id)
        )
        avg_score = result.scalar_one_or_none()
        return avg_score if avg_score is not None else 0
    
    async def get_max_subject_scores(self):
        subquery = (
            select(
                Score.subject_id,
                Score.student_id,
                Score.score,
                func.rank().over(
                    partition_by=Score.subject_id,
                    order_by=Score.score.desc()
                ).label("rank")
            )
            .subquery()
        )
        result = await self.db.execute(
            select(subquery).filter(subquery.c.rank == 1)
        )
        return result.mappings().all()

    async def add(self, score: ScoreSchema):
        try:
            score = Score(**score.model_dump())
            self.db.add(score)
            await self.db.commit()
            await self.db.refresh(score)
            return score
        except SQLAlchemyError as e:
            await self.db.rollback()
            print(f"Error adding score: {e}")
            return None

    async def get_by_id(self, score_id: int):
        result = await self.db.execute(
            select(Score).filter(Score.score_id == score_id)
        )
        return result.scalar_one_or_none()

    async def delete(self, score: Score):
        try:
            await self.db.delete(score)
            await self.db.commit()
            return True
        except SQLAlchemyError as e:
            await self.db.rollback()
            print(f"Error deleting score: {e}")
            return False

    async def update(self, score: Score, score_data: ScoreSchema):
        try:
            for key, value in score_data.model_dump().items():
                setattr(score, key, value)
            await self.db.commit()
            await self.db.refresh(score)
            return score
        except Exception as e:
            print(f"Error updating score: {e}")
            return None

    async def get_top_scores(self, limit: int = 10):
        result = await self.db.execute(
            select(Score).order_by(Score.score.desc()).limit(limit)
        )
        return result.scalars().all()
        
    async def calculate_all_avg_scores(self):
        try:
            result = await self.db.execute(
                select(
                    Score.subject_id,
                    func.avg(Score.score).label("avg_score")
                ).group_by(Score.subject_id)
            )
            return result.mappings().all()
        except SQLAlchemyError as e:
            print(f"Error calculating average scores: {e}")
            return None