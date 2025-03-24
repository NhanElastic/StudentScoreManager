from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from score.score_model import Score

class ScoreService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def get_max_score(self, subject_id: int):
        return self.db.execute(select(Score).filter(Score.subject_id == subject_id).order_by(Score.value.desc())).scalars().first()

    def get_average_student_score(self, student_id: int):
        return self.db.execute(select(func.avg(Score.value)).filter(Score.student_id == student_id)).scalar()
    
    def get_under_five_score(self):
        return self.db.execute(select(Score).filter(Score.value < 5)).scalars().all()
    
    def get_scores(self, type: str):
        if(type == 'default'):
            return self.db.execute(select(Score)).scalars().all()
        elif(type == 'asc'):
            return self.db.execute(select(Score).order_by(Score.value)).scalars().all()
        else:
            return self.db.execute(select(Score).order_by(Score.value.desc())).scalars().all()

    def get_student_score(self, student_id: int):
        return self.db.execute(select(Score).filter(Score.student_id == student_id)).scalars().all()
    
    def add_student_score(self, student_id: int, subject_id: int, value: int, date: str):
        score = Score(student_id=student_id, subject_id=subject_id, value=value, date=date)
        self.db.add(score)
        self.db.commit()
        self.db.refresh(score)
        return score
    
    def update(self, score_id: int, value: int, date: str):
        score = self.db.execute(select(Score).filter(Score.score_id == score_id)).scalars().first()
        score.value = value
        score.date = date
        self.db.commit()
        self.db.refresh(score)
        return score
    
    def remove(self, score_id: int):
        score = self.db.execute(select(Score).filter(Score.score_id == score_id)).scalars().first()
        self.db.delete(score)
        self.db.commit()
        return score
    
        