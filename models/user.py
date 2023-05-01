from pydantic import Field, EmailStr
from models.CustomBaseModels import CustomBaseModel

class User(CustomBaseModel):
  email: EmailStr = Field(default=None)
  hashed_password: str = Field(default=None, hidden=True)
  
class UserLogin(CustomBaseModel):
  email: EmailStr = Field(default=None)
  password: str = Field(default=None)