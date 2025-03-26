from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from score.score_model import Score
from student.student_model import Student
from subject.subject_model import Subject
class ScoreService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_scores(self):
        result = await self.db.execute(
            select(Score.score_id.label('score_id'), Student.student_id, Student.name.label('student_name'), Subject.name.label('subject_name'), Score.score, Score.date)
            .join(Score, Student.student_id == Score.student_id)
            .join(Subject, Score.subject_id == Subject.subject_id)
        )
        scores = [dict(row) for row in result.mappings()]
        return scores
    
    async def get_student_scores(self, student_id: int, isAscending: bool = False):
        result = await self.db.execute(
            select(Score.score_id.label('score_id'), Student.student_id, Student.name.label('student_name'), Subject.name.label('subject_name'), Score.score, Score.date)
            .join(Score, Student.student_id == Score.student_id)
            .join(Subject, Score.subject_id == Subject.subject_id)
            .filter(Student.student_id == student_id).order_by(Score.score.asc() if isAscending else Score.score.desc())
        )
        scores = [dict(row) for row in result.mappings()]
        return scores
    
    async def get_avg_score(self, student_id: int):
        result = await self.db.execute(
            select(Score.score_id.label('score_id'), Student.student_id, Student.name.label('student_name'), func.avg(Score.score).label('avg_score'))
            .join(Score, Student.student_id == Score.student_id)
            .filter(Student.student_id == student_id)
        )
        scores = [dict(row) for row in result.mappings()]
        return scores

    async def max_score_subjects(self):
        result = await self.db.execute(
            select(Score.score_id.label('score_id'), Student.student_id, Student.name,Subject.name.label('subject_name'), func.max(Score.score).label('score'))
            .join(Score, Student.student_id == Score.student_id)
            .join(Subject, Score.subject_id == Subject.subject_id)
            .group_by(Subject.name)

        )
        scores = [dict(row) for row in result.mappings()]
        return scores
    
    async def add_score(self, student_id: int, subject_id: int, score: int, date: str):
        score = Score(student_id=student_id, subject_id=subject_id, score=score, date=date)
        self.db.add(score)
        await self.db.commit()
        await self.db.refresh(score)
        return score
    
    async def remove_score(self, score_id: int):
        result = await self.db.execute(select(Score).filter(Score.score_id == score_id))
        score = result.scalars().first()
        if score:
            await self.db.delete(score)
            await self.db.commit()
        return score
    
    async def update_score(self, score_id: int, score: int = None, date: str = None, student_id: int = None, subject_id: int = None):
        result = await self.db.execute(select(Score).filter(Score.score_id == score_id))
        student_score = result.scalars().first()
        if not student_score:
            return None
        if score:
            student_score.score = score
        if date:
            student_score.date = date
        if student_id:
            student_score.student_id = student_id
        if subject_id:
            student_score.subject_id = subject_id
        await self.db.commit()
        await self.db.refresh(student_score)
        return student_score
    