from pydantic import BaseModel
from typing import Optional
from schemas.user import UserResponse


# Base task schema
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "Pending"


# Create task schema
class TaskCreate(TaskBase):
    project_id: int
    assigned_to: int


# Update task schema
class TaskUpdate(TaskBase):
    assigned_to: Optional[int] = None


# Response task schema
class TaskResponse(TaskBase):
    id: int
    project_id: int
    assigned_to: int

    class Config:
        from_attributes = True
