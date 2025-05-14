from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from auth.auth_service import AuthService
from auth.auth_schema import SignInSchema, RefreshTokenRequest
from database.database import get_db
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router.post("/signin")
async def sign_in(user_data: SignInSchema, db: AsyncSession = Depends(get_db)):
    try:
        auth_service = AuthService(db)
        token = await auth_service.sign_in(user_data)
        if not token:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return JSONResponse(content={"message": "Sign in successful", "data": jsonable_encoder(token)}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "An unexpected error occurred", "error": str(e)}, status_code=500)
    
@router.post("/refresh")
async def refresh_access_token(refresh_token: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    try:
        auth_service = AuthService(db)
        token = refresh_token.refresh_token
        if not token:
            raise HTTPException(status_code=400, detail="Refresh token is required")
        new_access_token = await auth_service.refresh_access_token(token)
        return JSONResponse(content={"message": "Access token refreshed successfully", "data": jsonable_encoder(new_access_token)}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "An unexpected error occurred", "error": str(e)}, status_code=500)