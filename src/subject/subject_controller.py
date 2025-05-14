from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from subject.subject_service import SubjectService
from subject.subject_schema import SubjectSchema
from database.database import get_db
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError
from guard.guard_service import RoleGuard
ANYROLE = ["admin", "user"]

router = APIRouter(
    prefix="/api/subjects",
    tags=["subjects"],
    responses={404: {"description": "Not found"}},
)

async def handle_exception(e: Exception):
    if isinstance(e, HTTPException):
        return JSONResponse(content={"message": e.detail}, status_code=e.status_code)
    elif isinstance(e, SQLAlchemyError):
        return JSONResponse(content={"message": "Database error", "error": str(e)}, status_code=500)
    else:
        return JSONResponse(content={"message": "An unexpected error occurred", "error": str(e)}, status_code=500)

@router.get("/list", dependencies=[RoleGuard(ANYROLE)])
async def get_subjects(db: AsyncSession = Depends(get_db)):
    try:
        subject_service = SubjectService(db)
        subjects = await subject_service.get_all_subjects()
        if subjects is None:
            raise HTTPException(status_code=404, detail="No subjects found")
        return JSONResponse(content={"data": jsonable_encoder(subjects)}, status_code=200)
    except Exception as e:
        return await handle_exception(e)

@router.post("/add", dependencies=[RoleGuard(["admin"])])
async def add_subject(subject_data: SubjectSchema, db: AsyncSession = Depends(get_db)):
    try:
        subject_service = SubjectService(db)
        subject = await subject_service.add_subject(subject_data)
        if not subject:
            raise HTTPException(status_code=500, detail="Failed to add subject")
        validate_subject = SubjectSchema.model_validate(subject)
        return JSONResponse(content={"message": "Subject added successfully", "data": jsonable_encoder(validate_subject)}, status_code=201)
    except Exception as e:
        return await handle_exception(e)
    
@router.delete("/remove/{subject_id}", dependencies=[RoleGuard(["admin"])])
async def remove_subject(subject_id: int, db: AsyncSession = Depends(get_db)):
    try:
        subject_service = SubjectService(db)
        if subject_id is None:
            raise HTTPException(status_code=400, detail="Subject ID is required")
        
        subject = await subject_service.remove_subject(subject_id)
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")
        return JSONResponse(content={"message": "Subject removed successfully"}, status_code=200)
    except Exception as e:
        return await handle_exception(e)

@router.put("/update/{subject_id}", dependencies=[RoleGuard(["admin"])])
async def update_subject(subject_id: int, subject_data: SubjectSchema, db: AsyncSession = Depends(get_db)):
    try:
        subject_service = SubjectService(db)
        if subject_id is None:
            raise HTTPException(status_code=400, detail="Subject ID is required")
        
        subject = await subject_service.update(subject_id, subject_data)
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")
        validate_subject = SubjectSchema.model_validate(subject)
        return JSONResponse(content={"message": "Subject updated successfully", "data": jsonable_encoder(validate_subject)}, status_code=200)
    except Exception as e:
        return await handle_exception(e)
