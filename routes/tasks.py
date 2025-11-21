from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.task import Task
from models.project import Project
from models.user import User
from schemas.task import TaskCreate, TaskUpdate, TaskResponse
from core.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, dependencies=[Depends(require_admin)])
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == data.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project does not exist")

    task = Task(
        title=data.title,
        description=data.description,
        status=data.status,
        project_id=data.project_id,
        assigned_to=data.assigned_to
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "Admin":
        return db.query(Task).offset(skip).limit(limit).all()
    
    # User → only tasks assigned to them
    return db.query(Task).filter(Task.assigned_to == current_user.id)\
        .offset(skip).limit(limit).all()
  

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # User can only update own tasks
    if current_user.role != "Admin" and task.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    # Users can edit only SOME fields
    task.title = data.title
    task.description = data.description
    task.status = data.status

    # Prevent users from reassigning tasks
    if current_user.role == "Admin" and data.assigned_to:
        task.assigned_to = data.assigned_to

    db.commit()
    db.refresh(task)
    return task




@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if current_user.role != "Admin" and task.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}
