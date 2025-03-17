from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from score.score_model import Score

class ScoreService:
    def __init__(self, db: AsyncSession):
        self.db = db

    