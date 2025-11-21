from fastapi import FastAPI
from database import Base, engine

from routes.auth import router as auth_router
from routes.projects import router as project_router
from routes.tasks import router as task_router
from routes.csv_upload import router as csv_router
from routes.users import router as users_router

app = FastAPI(
    title="FastAPI Assessment",
    description="User Auth, Projects, Tasks, CSV Upload",
    version="1.0.0"
)

#Routers
app.include_router(auth_router)
app.include_router(project_router)
app.include_router(task_router)
app.include_router(csv_router)
app.include_router(users_router)


@app.get("/")
def Home():
    return {"message": "FastAPI backend running successfully!"}
