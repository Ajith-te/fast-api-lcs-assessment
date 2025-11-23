from sqlalchemy import Table, Column, Integer, ForeignKey

from database import Base


# Association Table (Junction Table)
# This table connects Users and Projects in a Many-to-Many relationship.
# Each row links ONE user to ONE project.
project_user_association = Table(
    "project_user_association",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id")),
    Column("user_id", Integer, ForeignKey("users.id"))
)
