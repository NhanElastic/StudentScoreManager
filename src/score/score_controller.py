from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from score.score_service import ScoreService
from database.database import get_db
from score.score_schema import ScoreSchema, StudentScoreSchema
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(
    prefix="/api/scores",
    tags=["scores"],
    responses={404: {"description": "Not found"}},
)

async def handle_exception(e: Exception):
    if isinstance(e, HTTPException):
        return JSONResponse(content={"message": e.detail}, status_code=e.status_code)
    elif isinstance(e, SQLAlchemyError):
        return JSONResponse(content={"message": "Database error", "error": str(e)}, status_code=500)
    else:
        return JSONResponse(content={"message": "An unexpected error occurred", "error": str(e)}, status_code=500)

@router.get("/student/{student_id}/{isAscending}")
async def get_student_scores(student_id: int, isAscending: bool = True, db: AsyncSession = Depends(get_db)):
    try:
        if student_id is None:
            raise HTTPException(status_code=400, detail="Student ID is required")
        score_service = ScoreService(db)
        scores = await score_service.get_student_scores(student_id, isAscending)
        result = [ScoreSchema.model_validate(score) for score in scores]
        return JSONResponse(content={"data": jsonable_encoder(result)}, status_code=200)
    except Exception as e:
        return await handle_exception(e)
    
@router.get("/list")
async def get_all_scores(db: AsyncSession = Depends(get_db)):
    try:
        score_service = ScoreService(db)
        scores = await score_service.get_all_scores()
        result = [ScoreSchema.model_validate(score) for score in scores]
        return JSONResponse(content={"data": jsonable_encoder(result)}, status_code=200)
    except Exception as e:
        return await handle_exception(e)
    
@router.get("/avg/{student_id}")
async def get_avg_score(student_id: int, db: AsyncSession = Depends(get_db)):
    try:
        if student_id is None:
            raise HTTPException(status_code=400, detail="Student ID is required")
        score_service = ScoreService(db)
        avg_score = await score_service.get_student_avg_score(student_id)
        if avg_score is None:
            raise HTTPException(status_code=404, detail="No scores found for this student")
        return JSONResponse(content={"data": avg_score}, status_code=200)
    except Exception as e:
        return await handle_exception(e)


    
@router.post("/add")
async def add_score(score_data: ScoreSchema, db: AsyncSession = Depends(get_db)):
    try:
        if score_data is None:
            raise HTTPException(status_code=400, detail="Score data is required")
        score_service = ScoreService(db)
        score = await score_service.add_score(score_data)
        if not score:
            raise HTTPException(status_code=500, detail="Failed to add score")
        validate_score = ScoreSchema.model_validate(score)
        return JSONResponse(content={"message": "Score added successfully", "data": jsonable_encoder(validate_score)}, status_code=201)
    except Exception as e:
        return await handle_exception(e)

@router.delete("/remove/{score_id}")
async def remove_score(score_id: int, db: AsyncSession = Depends(get_db)):
    try:
        if score_id is None:
            raise HTTPException(status_code=400, detail="Score ID is required")
        score_service = ScoreService(db)
        score = await score_service.remove_score(score_id)
        if not score:
            raise HTTPException(status_code=404, detail="Score not found")
        return JSONResponse(content={"message": "Score removed successfully"}, status_code=200)
    except Exception as e:
        return await handle_exception(e)
    
@router.put("/update/{score_id}")
async def update_score(score_id: int, score_data: ScoreSchema, db: AsyncSession = Depends(get_db)):
    try:
        if score_id is None:
            raise HTTPException(status_code=400, detail="Score ID is required")
        score_service = ScoreService(db)
        score = await score_service.update_score(score_id, score_data)
        if not score:
            raise HTTPException(status_code=404, detail="Score not found")
        validate_score = ScoreSchema.model_validate(score)
        return JSONResponse(content={"message": "Score updated successfully", "data": jsonable_encoder(validate_score)}, status_code=200)
    except Exception as e:
        return await handle_exception(e)
    
@router.get("/top/{limit}")
async def get_top_scores(limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        score_service = ScoreService(db)
        scores = await score_service.get_top_scores(limit)
        if scores is None:
            raise HTTPException(status_code=404, detail="No scores found")
        result = [ScoreSchema.model_validate(score) for score in scores]
        return JSONResponse(content={"data": jsonable_encoder(result)}, status_code=200)
    except Exception as e:
        return await handle_exception(e)
    
@router.get("/avg_all")
async def calculate_all_avg_scores(db: AsyncSession = Depends(get_db)):
    try:
        score_service = ScoreService(db)
        avg_scores = await score_service.calculate_all_avg_scores()
        if avg_scores is None:
            raise HTTPException(status_code=404, detail="No scores found")
        result = [StudentScoreSchema.model_validate(score) for score in avg_scores]
        return JSONResponse(content={"data": jsonable_encoder(result)}, status_code=200)
    except Exception as e:
        return await handle_exception(e)
