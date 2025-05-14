from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from student.student_service import StudentService
from database.database import get_db
from student.student_schema import StudentSchema
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/api/students",
    tags=["students"],
    responses={404: {"description": "Not found"}},
)

async def handle_exception(e: Exception):
    if isinstance(e, HTTPException):
        return JSONResponse(content={"message": e.detail}, status_code=e.status_code)
    elif isinstance(e, SQLAlchemyError):
        return JSONResponse(content={"message": "Database error", "error": str(e)}, status_code=500)
    else:
        return JSONResponse(content={"message": "An unexpected error occurred", "error": str(e)}, status_code=500)
    
@router.get("/list")
async def get_students(db: AsyncSession = Depends(get_db)):
    try:
        student_service = StudentService(db)
        students = await student_service.get_all_students()
        if students is None:
            raise HTTPException(status_code=404, detail="No students found")
        return JSONResponse(content={"data": jsonable_encoder(students)}, status_code=200)
    except Exception as e:
        return await handle_exception(e)


@router.post("/add")
async def add_student(student_data: StudentSchema, db: AsyncSession = Depends(get_db)):
    try:
        student_service = StudentService(db)
        student = await student_service.add_student(student_data)
        if not student:
            raise HTTPException(status_code=500, detail="Failed to add student")
        validate_student = StudentSchema.model_validate(student)
        print(validate_student)
        return JSONResponse(content={"message": "Student added successfully", "data": jsonable_encoder(validate_student)}, status_code=201)
    except Exception as e:
        return await handle_exception(e)

@router.delete("/remove/{student_id}")
async def remove_student(student_id: int, db: AsyncSession = Depends(get_db)):
    try:
        student_service = StudentService(db)
        if student_id is None:
            raise HTTPException(status_code=400, detail="Student ID is required")
        
        student = await student_service.remove_student(student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return JSONResponse(content={"message": "Student removed successfully"}, status_code=200)

    except Exception as e:
        return await handle_exception(e)

@router.put("/update/{student_id}")
async def update_student(student_id: int, student_data: StudentSchema, db: AsyncSession = Depends(get_db)):
    try:
        student_service = StudentService(db)
        if student_id is None:
            raise HTTPException(status_code=400, detail="Student ID is required")
        
        student = await student_service.update_student(student_id, student_data)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        validate_student = StudentSchema.model_validate(student)
        return JSONResponse(content={"message": "Student updated successfully", "data": jsonable_encoder(validate_student)}, status_code=200)

    except Exception as e:
        return await handle_exception(e)
    
@router.get("/get_by_id/{student_id}")
async def get_student_by_id(student_id: int, db: AsyncSession = Depends(get_db)):
    try:
        student_service = StudentService(db)
        if student_id is None:
            raise HTTPException(status_code=400, detail="Student ID is required")
        
        student = await student_service.get_student_by_id(student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        validate_student = StudentSchema.model_validate(student)
        return JSONResponse(content={"data": jsonable_encoder(validate_student)}, status_code=200)

    except Exception as e:
        return await handle_exception(e)
