from fastapi import APIRouter, Depends
from subject.subject_service import SubjectService
from subject.subject_schema import SubjectSchema
from database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

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
        print(e)
        return JSONResponse(content={"message": "An error occurred", "error": str(e)})
    
@router.post("/add")
async def add_subject(subject_data: SubjectSchema, db: AsyncSession = Depends(get_db)):
    try:
        subject_service = SubjectService(db)
        subject = await subject_service.add_subject(
            subject_id=subject_data.subject_id,
            name=subject_data.name,
            amount=subject_data.amount
        )
        return JSONResponse(content={"message": "Subject added successfully"})
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "An error occurred", "error": str(e)})
    
@router.delete("/remove/{subject_id}")
async def remove_subject(subject_id: int, db: AsyncSession = Depends(get_db)):
    try:
        subject_service = SubjectService(db)
        subject = await subject_service.remove_subject(subject_id)
        if subject:
            return JSONResponse(content={"message": "Subject removed successfully"})
        return JSONResponse(content={"message": "Subject not found"})
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "An error occurred", "error": str(e)})
    
@router.put("/update/")
async def update_subject(subject_data: SubjectSchema, db: AsyncSession = Depends(get_db)):
    try:
        subject_service = SubjectService(db)
        subject = await subject_service.update(
            subject_id=subject_data.subject_id,
            name=subject_data.name,
            amount=subject_data.amount
        )
        return JSONResponse(content={"message": "Subject updated successfully"})
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "An error occurred", "error": str(e)})
