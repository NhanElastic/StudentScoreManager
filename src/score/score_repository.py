from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from score.score_model import Score

class ScoreRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(Score))
        return result.scalars().all()

    async def get_by_student(self, student_id: int, ascending: bool):
        query = select(Score).filter(Score.student_id == student_id)
        query = query.order_by(Score.date.asc() if ascending else Score.date.desc())
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_avg_by_student(self, student_id: int):
        result = await self.db.execute(
            select(func.avg(Score.score)).filter(Score.student_id == student_id)
        )
        return result.scalar()

    async def get_max_score_subjects(self):
        result = await self.db.execute(
            select(Score.subject_id, func.max(Score.score)).group_by(Score.subject_id)
        )
        return result.all()

    async def add(self, score: Score):
        self.db.add(score)
        await self.db.commit()
        await self.db.refresh(score)
        return score

    async def get_by_id(self, score_id: int):
        result = await self.db.execute(select(Score).filter(Score.score_id == score_id))
        return result.scalars().first()

    async def delete(self, score: Score):
        await self.db.delete(score)
        await self.db.commit()

    async def update(self, score: Score):
        await self.db.commit()
        await self.db.refresh(score)
        return score
