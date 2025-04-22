from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from subject.subject_service import SubjectService
from subject.subject_schema import SubjectSchema
from database.database import get_db
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
router = APIRouter(
    prefix="/api/subjects",
    tags=["subjects"],
    responses={404: {"description": "Not found"}},
)

@router.get("/list")
async def get_subjects(db: AsyncSession = Depends(get_db)):
    try:
        subject_service = SubjectService(db)
        subjects = await subject_service.get_all_subjects()
        if subjects.get("status") == "error":
            raise HTTPException(status_code=500, detail=subjects.get("message"))
        subjects_list = [SubjectSchema.model_validate(subject) for subject in subjects.get("data", [])]
        return JSONResponse(content={"data": jsonable_encoder(subjects_list)}, status_code=200)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.post("/add")
async def add_subject(subject_data: SubjectSchema, db: AsyncSession = Depends(get_db)):
    try:
        subject_service = SubjectService(db)
        subject = await subject_service.add_subject(
            subject_id=subject_data.subject_id,
            name=subject_data.name,
            amount=subject_data.amount
        )
        if subject.get("status") == "error":
            raise HTTPException(status_code=500, detail=subject.get("message"))
        return JSONResponse(content={"message": "Subject added successfully", "data": jsonable_encoder(subject)}, status_code=201)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.delete("/remove/{subject_id}")
async def remove_subject(subject_id: int, db: AsyncSession = Depends(get_db)):
    try:
        if subject_id is None:
            raise HTTPException(status_code=400, detail="Subject ID is required")
        subject_service = SubjectService(db)
        subject = await subject_service.remove_subject(subject_id)
        if subject.get("status") == "error":
            raise HTTPException(status_code=500, detail=subject.get("message"))
        return JSONResponse(content={"message": subject.get("message")}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.put("/update/")
async def update_subject(subject_data: SubjectSchema, db: AsyncSession = Depends(get_db)):
    try:
        subject_service = SubjectService(db)
        subject = await subject_service.update(
            subject_id=subject_data.subject_id,
            name=subject_data.name,
            amount=subject_data.amount
        )
        if subject.get("status") == "error":
            raise HTTPException(status_code=500, detail=subject.get("message"))
        validate_subject = SubjectSchema.model_validate(subject.get("data"))
        return JSONResponse(content={"message": "Subject updated successfully", "data": jsonable_encoder(validate_subject)}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
