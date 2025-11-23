from sqlalchemy import Column, Date, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime, func

from database import Base


# Task model
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="Pending")
    assigned_to = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # One-to-Many A project has many tasks.
    project = relationship("Project", back_populates="tasks")
    # One-to-Many A user can have many tasks assigned.
    assigned_user = relationship("User", back_populates="tasks")
