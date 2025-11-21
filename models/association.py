from sqlalchemy import Table, Column, Integer, ForeignKey

from database import Base

project_user_association = Table(
    "project_user_association",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id")),
    Column("user_id", Integer, ForeignKey("users.id"))
)
