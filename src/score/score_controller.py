from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from score.score_service import ScoreService
from database.database import get_db
from score.score_schema import ScoreSchema

router = APIRouter(
    prefix="/scores",
    tags=["scores"],
    responses={404: {"description": "Not found"}},
)

@router.get("/student")
async def get_student_scores(student_id: dict, isAscending: bool = False, db: AsyncSession = Depends(get_db)):
    try:
        score_service = ScoreService(db)
        scores = await score_service.get_student_scores(student_id, isAscending)
        return scores
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "An error occurred", "error": str(e)})
    
@router.get("/list")
async def get_all_scores(db: AsyncSession = Depends(get_db)):
    try:
        score_service = ScoreService(db)
        scores = await score_service.get_all_scores()
        return scores
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "An error occurred", "error": str(e)})
    
@router.get("/avg")
async def get_avg_score(student_id: dict, db: AsyncSession = Depends(get_db)):
    try:
        score_service = ScoreService(db)
        scores = await score_service.get_avg_score(student_id)
        return scores
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "An error occurred", "error": str(e)})
    
@router.get("/max")
async def max_score_subjects(db: AsyncSession = Depends(get_db)):
    try:
        score_service = ScoreService(db)
        scores = await score_service.max_score_subjects()
        return scores
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "An error occurred", "error": str(e)})
    
@router.post("/add")
async def add_score(score_data: ScoreSchema, db: AsyncSession = Depends(get_db)):
    try:
        score_service = ScoreService(db)
        score = await score_service.add_score(
            student_id=score_data.student_id,
            subject_id=score_data.subject_id,
            score=score_data.score,
            date=score_data.date
        )
        return JSONResponse(content={"message": "Score added successfully"})
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "An error occurred", "error": str(e)})
    
@router.delete("/remove")
async def remove_score(score_id: dict, db: AsyncSession = Depends(get_db)):
    try:
        score_service = ScoreService(db)
        score = await score_service.remove_score(score_id['score_id'])
        if score:
            return JSONResponse(content={"message": "Score removed successfully"})
        return JSONResponse(content={"message": "Score not found"})
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "An error occurred", "error": str(e)})
    
@router.put("/update")
async def update_score(score_data: ScoreSchema, db: AsyncSession = Depends(get_db)):
    try:
        score_service = ScoreService(db)
        print(score_data)
        score = await score_service.update_score(
            score_id=score_data.score_id,
            score=score_data.score,
            date=score_data.date,
            student_id=score_data.student_id,   
            subject_id=score_data.subject_id
        )
        if score:
            return JSONResponse(content={"message": "Score updated successfully"})
        return JSONResponse(content={"message": "Score not found"})
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "An error occurred", "error": str(e)})