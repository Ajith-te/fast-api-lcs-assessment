from pydantic import BaseModel
from typing import List, Optional
from schemas.user import UserResponse


# Base project schema
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None


# Create project schema
class ProjectCreate(ProjectBase):
    assigned_users: List[int] = []


# Update project schema
class ProjectUpdate(ProjectBase):
    assigned_users: List[int] = []


# Response project schema
class ProjectResponse(ProjectBase):
    id: int
    created_by: int
    assigned_users: List[UserResponse] = []

    class Config:
        from_attributes = True
