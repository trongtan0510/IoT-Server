from dotenv import load_dotenv
from fastapi import HTTPException
from loguru import logger
from pymongo import MongoClient
from datetime import datetime
import bcrypt
import os
from bson import ObjectId
from app.schema.users import UserModel

load_dotenv()
class DB_CONNECT:
    def __init__(self):
        self.uri = os.getenv("DATABASE_URL")
        self.client = MongoClient(self.uri)

        self.db = self.client["irrigation_db"]
        self.users_collection = self.db["users"]  

    async def save_user_info (self, name, email, password):
        try:
            existing_user = self.users_collection.find_one({"email": email})
            if existing_user:
                return {"status": "error", "message": "Email này đã được sử dụng."}
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user_data = {
                "name": name,
                "email": email,
                "password": hashed_password,
                "created_at": datetime.now()  
            }

            self.users_collection.insert_one(user_data)
            return {"status": "success", "message": "Thông tin người dùng đã được lưu."}

        except Exception as e:
            print(f"Lỗi khi lưu thông tin người dùng: {e}")
            return {"status": "error", "message": str(e)}

    async def login_user(self, email, password):
        try:
            user = self.users_collection.find_one({'email': email})
            if not user:
                return {"status": "error", "message": "Email không tồn tại."}
            if bcrypt.checkpw(password.encode('utf-8'), user['password']):
                return {"status": "success", "message": "Đăng nhập thành công."}
            else:
                return {"status": "error", "message": "Mật khẩu không chính xác."}
        except Exception as e:
            logger.error(f"Lỗi trong hàm login_user: {e}")
    
    async def get_data_user(self, email):
        try:
            user = self.users_collection.find_one({'email': email})

            if user:
                user_model = UserModel.from_mongo(user)
                return {"status": "success", "user": user_model}
            else:
                raise HTTPException(status_code=404, detail="Người dùng không tìm thấy.")
        except Exception as e:
            logger.error(f"Lỗi trong hàm get_data_user: {e}")
            raise HTTPException(status_code=500, detail="Đã xảy ra lỗi khi lấy thông tin người dùng.")
        
    async def update_data_user(self, user_id, user_info):
        try:
            updated_user = self.users_collection.find_one_and_update(
                {'_id': ObjectId(user_id)}, 
                {'$set': user_info.dict()},   
                return_document=True         
            )
            if updated_user:
                return {"status": "success", "message": "Thông tin đã được cập nhật.", "user": updated_user}
            else:
                raise HTTPException(status_code=404, detail="Người dùng không tìm thấy hoặc không có thay đổi.")
        except Exception as e:
            logger.error(f"Lỗi trong hàm get_data_user: {e}")
            raise HTTPException(status_code=500, detail="Đã xảy ra lỗi khi cập nhật thông tin người dùng.")
