from pydantic import BaseModel
from typing import Optional
from schemas.user import UserResponse

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "Pending"

class TaskCreate(TaskBase):
    project_id: int
    assigned_to: int

class TaskUpdate(TaskBase):
    assigned_to: Optional[int] = None

class TaskResponse(TaskBase):
    id: int
    project_id: int
    assigned_to: int

    class Config:
        from_attributes = True
