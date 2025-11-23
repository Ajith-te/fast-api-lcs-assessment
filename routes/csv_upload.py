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
    Background task handler that processes a CSV file.

    This function is intended to be executed as a BackgroundTasks job. It
    delegates CSV parsing and database insertion to services.csv_processor.process_csv_file.

    Args:
        file_path (str): Full path to the uploaded CSV file on disk.
        db (Session): SQLAlchemy session instance for database operations.

    Returns:
        None
    """
    process_csv_file(file_path, db)


@router.post("/csv", dependencies=[Depends(require_admin)])
async def upload_csv(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload endpoint for CSV files. Saves the uploaded CSV to the local uploads
    directory and schedules background processing.

    Validations:
    - Only accepts files with content_type "text/csv" or "application/vnd.ms-excel".

    Behavior:
    - Ensures the uploads directory exists.
    - Persists the uploaded file to disk.
    - Adds a background task to process the CSV (inserts valid rows, writes invalid rows to *_errors.csv).

    Args:
        background_tasks (BackgroundTasks): FastAPI BackgroundTasks instance for scheduling work.
        file (UploadFile): Uploaded file object from the client.
        db (Session): SQLAlchemy session injected via dependency.

    Raises:
        HTTPException: 400 if the uploaded file is not a CSV.

    Returns:
        dict: A confirmation message that processing will run in the background.
    """
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
    """
    Returns the most recent error CSV produced by processing uploads.

    Looks for files in the uploads directory that end with "_errors.csv". If none
    are found, returns a JSON message indicating no error CSVs are available.
    Otherwise returns a FileResponse for the latest error CSV (by creation time).

    Args:
        None

    Returns:
        FileResponse or dict: FileResponse for the newest *_errors.csv, or a dict message if none exist.
    """
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

