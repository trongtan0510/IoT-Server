from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from typing import Optional

class UserRegisterRequest(BaseModel):
    name: str = Field(..., min_length=1) 
    email: EmailStr 
    password: str = Field(..., min_length=6) 

class UserLoginRequest(BaseModel):
    email: EmailStr 
    password: str = Field(..., min_length=6) 




class UserModel(BaseModel):
    id: str  
    email: str
    name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    
    class Config:
        json_encoders = {
            ObjectId: lambda v: str(v)  
        }

    @classmethod
    def from_mongo(cls, user_data: dict):
        user_data['id'] = str(user_data['_id']) 
        user_data.pop('_id', None) 
        return cls(**user_data)

