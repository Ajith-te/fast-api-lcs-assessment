from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime, func

from database import Base


# User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="User")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
        
    # Many-to-Many. A user can be assigned to multiple projects,
    # The 'project_user_association' table stores these links.
    assigned_projects = relationship("Project",secondary="project_user_association",back_populates="assigned_users")
    # One-to-Many. A user can have multiple tasks assigned to them
    tasks = relationship("Task", back_populates="assigned_user")
