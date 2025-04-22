from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from student.student_service import StudentService
from database.database import get_db
from student.student_schema import StudentSchema
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from fastapi.encoders import jsonable_encoder

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
        if students.get("status") == "error":
            raise HTTPException(status_code=500, detail=students.get("message"))
        if not students.get("data"):
            raise HTTPException(status_code=404, detail="No students found")
        lst: List[StudentSchema] = [StudentSchema.model_validate(student) for student in students.get("data", [])]
        return JSONResponse(content={"data" : jsonable_encoder(lst)}, status_code=200)
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
        if student.get("status") == "error":
            raise HTTPException(status_code=500, detail=student.get("message"))
        if not student.get("data"):
            raise HTTPException(status_code=400, detail="Failed to add student")
        validate_student = StudentSchema.model_validate(student.get("data"))
        return JSONResponse(content={"message": "Student added successfully", "data": jsonable_encoder(validate_student)}, status_code=201)
    except Exception as e:
        return await handle_exception(e)

@router.delete("/remove/{student_id}")
async def remove_student(student_id: int, db: AsyncSession = Depends(get_db)):
    try:
        student_service = StudentService(db)
        student = await student_service.remove_student(student_id)
        if student.get("status") == "error":
            raise HTTPException(status_code=500, detail=student.get("message"))
        elif student.get("status") == "success":
            return JSONResponse(content={"message": student.get("message")}, status_code=200)
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
        if student.get("status") == "error":
            raise HTTPException(status_code=500, detail=student.get("message"))
        elif student.get("status") == "success":
            validate_student = StudentSchema.model_validate(student.get("data"))
            return JSONResponse(content={"message": "Student updated successfully", "data": jsonable_encoder(validate_student)}, status_code=200)
        raise HTTPException(status_code=404, detail="Student not found")

    except Exception as e:
        return await handle_exception(e)

@router.get("/get_by_id/{student_id}")
async def get_student_by_id(student_id: int, db: AsyncSession = Depends(get_db)):
    try:
        student_service = StudentService(db)
        if student_id is None:
            raise HTTPException(status_code=400, detail="Student ID is required")
        
        student = await student_service.repo.get_by_id(student_id)
        if student.get("status") == "error":
            raise HTTPException(status_code=500, detail=student.get("message"))
        if not student.get("data"):
            raise HTTPException(status_code=404, detail="Student not found")
        student = student.get("data")
        validate_student = StudentSchema.model_validate(student)
        return JSONResponse(content={"message": "Student found", "data": jsonable_encoder(validate_student)}, status_code=200)
    
    except Exception as e:
        return await handle_exception(e)
