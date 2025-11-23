from pydantic import BaseModel, EmailStr


# Base user schema
class UserBase(BaseModel):
    name: str
    email: EmailStr


# Request model for user registration
class UserCreate(UserBase):
    password: str


# Response model for user data
class UserResponse(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True
