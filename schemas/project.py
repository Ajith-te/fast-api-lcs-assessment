from pydantic import BaseModel
from typing import List, Optional
from schemas.user import UserResponse

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    assigned_users: List[int] = []

class ProjectUpdate(ProjectBase):
    assigned_users: List[int] = []

class ProjectResponse(ProjectBase):
    id: int
    created_by: int
    assigned_users: List[UserResponse] = []

    class Config:
        from_attributes = True
