from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from student.student_service import StudentService
from database.database import get_db
from student.student_schema import StudentSchema
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(
    prefix="/api/students",
    tags=["students"],
    responses={404: {"description": "Not found"}},
)

# Centralized exception handler
async def handle_exception(e: Exception):
    if isinstance(e, SQLAlchemyError):
        return JSONResponse(content={"message": "Database error", "error": str(e)}, status_code=500)
    return JSONResponse(content={"message": "An unexpected error occurred", "error": str(e)}, status_code=500)

@router.get("/list")
async def get_students(db: AsyncSession = Depends(get_db)):
    try:
        student_service = StudentService(db)
        students = await student_service.get_all_students()
        return [StudentSchema.model_validate(student) for student in students]
    except Exception as e:
        return await handle_exception(e)

@router.post("/add")
async def add_student(student_data: StudentSchema, db: AsyncSession = Depends(get_db)):
    try:
        student_service = StudentService(db)
        student = await student_service.add_student(
            student_id=student_data.student_id,
            name=student_data.name,
            birthdate=student_data.birthdate,
            class_=student_data.class_
        )
        return {"message": "Student added successfully"}
    except Exception as e:
        return await handle_exception(e)

@router.delete("/remove/{student_id}")
async def remove_student(student_id: int, db: AsyncSession = Depends(get_db)):
    try:
        student_service = StudentService(db)
        student = await student_service.remove_student(student_id)
        if student:
            return {"message": "Student removed successfully"}
        raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        return await handle_exception(e)

@router.put("/update/")
async def update_student(student_data: StudentSchema, db: AsyncSession = Depends(get_db)):
    try:
        student_service = StudentService(db)
        student = await student_service.update_student(
            student_id=student_data.student_id,
            name=student_data.name,
            birthdate=student_data.birthdate,
            class_=student_data.class_
        )
        if student:
            return {"message": "Student updated successfully"}
        raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        return await handle_exception(e)

@router.get("/student/{student_id}")
async def get_student_by_id(student_id: int, db: AsyncSession = Depends(get_db)):
    try:
        student_service = StudentService(db)
        student = await student_service.repo.get_by_id(student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return StudentSchema.model_validate(student)
    except Exception as e:
        return await handle_exception(e)
