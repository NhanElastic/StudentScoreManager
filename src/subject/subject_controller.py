from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from subject.subject_service import SubjectService
from subject.subject_schema import SubjectSchema
from database.database import get_db

router = APIRouter(
    prefix="/api/subjects",
    tags=["subjects"],
    responses={404: {"description": "Not found"}},
)

@router.get("/list")
async def get_subjects(db: AsyncSession = Depends(get_db)):
    try:
        subject_service = SubjectService(db)
        subjects = await subject_service.get_subjects()
        return [SubjectSchema.model_validate(subject) for subject in subjects]
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
        return {"message": "Subject added successfully", "subject": SubjectSchema.model_validate(subject)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.delete("/remove/{subject_id}")
async def remove_subject(subject_id: int, db: AsyncSession = Depends(get_db)):
    try:
        subject_service = SubjectService(db)
        subject = await subject_service.remove_subject(subject_id)
        if subject:
            return {"message": "Subject removed successfully"}
        raise HTTPException(status_code=404, detail="Subject not found")
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
        if subject:
            return {"message": "Subject updated successfully", "subject": SubjectSchema.model_validate(subject)}
        raise HTTPException(status_code=404, detail="Subject not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
