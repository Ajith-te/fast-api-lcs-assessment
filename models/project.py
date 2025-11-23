from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime, func

from database import Base


# Project model
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Many-to-many. A project can have multiple assigned users,
    # and a user can be part of multiple projects.
    assigned_users = relationship(
        "User",
        secondary="project_user_association",
        back_populates="assigned_projects"
    )

    # One-to-many. A project contains multiple tasks,
    # but each task belongs to only one project.
    tasks = relationship("Task", back_populates="project")
