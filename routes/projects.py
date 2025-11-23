from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.project import Project
from models.user import User
from models.association import project_user_association
from schemas.project import (ProjectCreate, ProjectResponse, ProjectUpdate)
from core.dependencies import get_current_user, require_admin


router = APIRouter(prefix="/projects", tags=["Projects"])

# Create new project
@router.post("/", response_model=ProjectResponse)
def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    project = Project(
        name=data.name,
        description=data.description,
        created_by=current_user.id
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    if data.assigned_users:
        for user_id in data.assigned_users:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                project.assigned_users.append(user)

        db.commit()
        db.refresh(project)

    return project


# View all projects
@router.get("/", response_model=list[ProjectResponse])
def get_projects(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "Admin":
        return db.query(Project).offset(skip).limit(limit).all()

    return current_user.assigned_projects[skip : skip + limit]


# View project by ID
@router.get("/{project_id}", response_model=ProjectResponse)
def get_project_by_id(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Fetch project from DB
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if current_user.role == "Admin":
        return project

    if project not in current_user.assigned_projects:
        raise HTTPException(
            status_code=403, detail="You are not allowed to view this project"
        )

    return project


# Update project by ID
@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.name = data.name
    project.description = data.description

    # Update assigned users
    project.assigned_users = []
    if data.assigned_users:
        for user_id in data.assigned_users:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                project.assigned_users.append(user)

    db.commit()
    db.refresh(project)
    return project


# Delete project by ID
@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}

