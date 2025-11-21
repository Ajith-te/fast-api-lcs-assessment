import os
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from core.dependencies import require_admin
from services.csv_processor import process_csv_file
from fastapi.responses import FileResponse

router = APIRouter(prefix="/upload", tags=["CSV Upload"])


def background_csv_handler(file_path: str, db: Session):
    """
    Runs in background: processes CSV, inserts valid rows, 
    writes invalid rows to *_errors.csv inside uploads folder.
    """
    process_csv_file(file_path, db)


@router.post("/csv", dependencies=[Depends(require_admin)])
async def upload_csv(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Accept only CSV
    if file.content_type not in ["text/csv", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=400, detail="Invalid file format. Only CSV allowed.")

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    background_tasks.add_task(background_csv_handler, file_path, db)
    return {"message": "CSV uploaded. Processing in background."}




@router.get("/errors", dependencies=[Depends(require_admin)])
def download_error_csv():
    upload_dir = "uploads"

    # Get all *_errors.csv files
    error_files = []
    for f in os.listdir(upload_dir):
        if f.endswith("_errors.csv") and isinstance(f, str):
            error_files.append(f)

    if not error_files:
        return {"message": "No error CSV found"}

    # Ensure each item is a plain string (not list)
    error_files = [f for f in error_files if isinstance(f, str)]

    # Sort newest first
    latest_error_file = sorted(
        error_files,
        key=lambda x: os.path.getctime(os.path.join(upload_dir, x)),
        reverse=True
    )[0]

    file_path = os.path.join(upload_dir, latest_error_file)

    return FileResponse(
        file_path,
        media_type="text/csv",
        filename=latest_error_file
    )

