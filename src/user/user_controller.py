from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from user.user_service import UserService
from user.user_schema import CreateUserReq
from database.database import get_db
from guard.guard_service import RoleGuard

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

async def handle_exception(e: Exception):
    if isinstance(e, HTTPException):
        return JSONResponse(content={"message": e.detail}, status_code=e.status_code)
    elif isinstance(e, SQLAlchemyError):
        return JSONResponse(content={"message": "Database error", "error": str(e)}, status_code=500)
    else:
        return JSONResponse(content={"message": "An unexpected error occurred", "error": str(e)}, status_code=500)
    
@router.post("/register", dependencies=[RoleGuard(["admin"])])
async def register_user(user_data: CreateUserReq, db: AsyncSession = Depends(get_db)):
    try:
        user_service = UserService(db)
        user = await user_service.create_user(user_data)
        if not user:
            raise HTTPException(status_code=500, detail="Failed to register user")
        return JSONResponse(content={"message": "User registered successfully", "username": user.username }, status_code=201)
    except Exception as e:
        return await handle_exception(e)