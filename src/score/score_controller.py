from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from score.score_service import ScoreService
from database.database import get_db
from score.score_schema import ScoreSchema, StudentScoreSchema
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/api/scores",
    tags=["scores"],
    responses={404: {"description": "Not found"}},
)

@router.get("/student/{student_id}/{isAscending}")
async def get_student_scores(student_id: int, isAscending: bool = True, db: AsyncSession = Depends(get_db)):
    try:
        score_service = ScoreService(db)

        if student_id is None:
            raise HTTPException(status_code=400, detail="Student ID is required")
        scores = await score_service.get_student_scores(student_id, isAscending)
        if scores.get("status") == "error":
            raise HTTPException(status_code=500, detail=scores.get("message"))
        if not scores.get("data"):
            raise HTTPException(status_code=404, detail="No scores found for the student")
        lst: list[StudentScoreSchema] = [ScoreSchema.model_validate(score) for score in scores.get("data", [])]
        return JSONResponse(content={"data": jsonable_encoder(lst)}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "An unexpected error occurred", "error": str(e)}, status_code=500)
    
@router.get("/list")
async def get_all_scores(db: AsyncSession = Depends(get_db)):
    try:
        score_service = ScoreService(db)
        scores = await score_service.get_all_scores()
        if scores.get("status") == "error":
            raise HTTPException(status_code=500, detail=scores.get("message"))
        if not scores.get("data"):
            raise HTTPException(status_code=404, detail="No scores found")
        lst: list[StudentScoreSchema] = [ScoreSchema.model_validate(score) for score in scores.get("data", [])]
        return JSONResponse(content={"data": jsonable_encoder(lst)}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "An unexpected error occurred", "error": str(e)}, status_code=500)
    
@router.get("/avg/{student_id}")
async def get_avg_score(student_id: int, db: AsyncSession = Depends(get_db)):
    try:
        if student_id is None:
            raise HTTPException(status_code=400, detail="Student ID is required")
        score_service = ScoreService(db)
        avg_score = await score_service.get_avg_score(student_id)
        if avg_score.get("status") == "error":
            raise HTTPException(status_code=500, detail=avg_score.get("message"))
        return JSONResponse(content={"data": jsonable_encoder(avg_score.get("data"))}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "An unexpected error occurred", "error": str(e)}, status_code=500)


    
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
        if score.get("status") == "error":
            raise HTTPException(status_code=500, detail=score.get("message"))
        return JSONResponse(content={"message": "Score added successfully", "data": jsonable_encoder(score.get('data'))}, status_code=201)
    except ValueError as e:
        return JSONResponse(content={"message": "Invalid input", "error": str(e)}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"message": "An unexpected error occurred", "error": str(e)}, status_code=500)

@router.delete("/remove/{score_id}")
async def remove_score(score_id: int, db: AsyncSession = Depends(get_db)):
    try:
        if score_id is None:
            raise HTTPException(status_code=400, detail="Score ID is required")
        score_service = ScoreService(db)
        score = await score_service.remove_score(score_id)
        if score.get("status") == "error":
            raise HTTPException(status_code=500, detail=score.get("message"))
        return JSONResponse(content={"message": score.get("message")}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "An unexpected error occurred", "error": str(e)}, status_code=500)
    
@router.put("/update")
async def update_score(score_data: ScoreSchema, db: AsyncSession = Depends(get_db)):
    try:
        if score_data.score_id is None:
            raise HTTPException(status_code=400, detail="Score ID is required")
        score_service = ScoreService(db)
        score = await score_service.update_score(
            score_id=score_data.score_id,
            score=score_data.score,
            date=score_data.date,
            student_id=score_data.student_id,
            subject_id=score_data.subject_id
        )
        if score.get("status") == "error":
            raise HTTPException(status_code=500, detail=score.get("message"))
        return JSONResponse(content={"message": "Score updated successfully", "data": jsonable_encoder(score.get('data'))}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "An unexpected error occurred", "error": str(e)}, status_code=500)

@router.get("/top/{limit}")
async def get_top_scores(limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        if limit is None or limit <= 0:
            raise HTTPException(status_code=400, detail="Limit is required and must be an positive integer")
        score_service = ScoreService(db)
        scores = await score_service.get_top_scores(limit)
        if scores is None:
            raise HTTPException(status_code=404, detail="No scores found")
        return JSONResponse(content={"data": scores}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "An unexpected error occurred", "error": str(e)}, status_code=500)
    
@router.get("/avg_all")
async def calculate_all_avg_scores(db: AsyncSession = Depends(get_db)):
    try:
        score_service = ScoreService(db)
        scores = await score_service.calculate_all_avg_scores()
        if scores is None:
            raise HTTPException(status_code=404, detail="No scores found")
        return JSONResponse(content={"data": scores}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "An unexpected error occurred", "error": str(e)}, status_code=500)
    
