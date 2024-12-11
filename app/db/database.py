from dotenv import load_dotenv
from loguru import logger
from pymongo import MongoClient
from datetime import datetime
import bcrypt
import os

load_dotenv()
class DB_CONNECT:
    def __init__(self):
        self.uri = os.getenv("DATABASE_URL")
        self.client = MongoClient(self.uri)

        self.db = self.client["irrigation_db"]
        self.users_collection = self.db["users"]  

    async def save_user_info (self, name, email, password):
        """Hàm lưu thông tin người dùng vào MongoDB, kiểm tra email đã tồn tại chưa."""
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
                logger.warning(f"Email không tồn tại: {email}")
                return {"status": "error", "message": "Email không tồn tại."}

            if bcrypt.checkpw(password.encode('utf-8'), user['password']):
                logger.info("Đăng nhập thành công.")
                return {"status": "success", "message": "Đăng nhập thành công."}
            else:
                logger.warning("Mật khẩu không chính xác.")
                return {"status": "error", "message": "Mật khẩu không chính xác."}
        except Exception as e:
            logger.error(f"Lỗi trong hàm login_user: {e}")
            

  