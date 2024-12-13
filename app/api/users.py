from fastapi import APIRouter, Depends, HTTPException, Request
from app.db.database import DB_CONNECT
from loguru import logger
from app.schema.users import UserRegisterRequest, UserLoginRequest

router = APIRouter()
db = DB_CONNECT()

@router.post("/register")
async def register(user: UserRegisterRequest):
    try:
        response = await db.save_user_info(user.name, user.email, user.password)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi đăng ký: {str(e)}")
    
@router.post("/login")
async def login(user: UserLoginRequest):
    try:
        response = await db.login_user(user.email, user.password)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi đăng ký: {str(e)}")
    
@router.get("/get-user")
async def getData(email):
    try:
        response = await db.get_data_user(email)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")
    
@router.post("/update_user")
async def updateData(user_Id, userInfo):
    try:
        response = await db.get_data_user(user_Id, userInfo)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")
    
