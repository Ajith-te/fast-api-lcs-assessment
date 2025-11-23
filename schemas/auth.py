from pydantic import BaseModel, EmailStr


# Request model for user registration
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# Response model for tokens
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
