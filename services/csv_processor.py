import csv

from sqlalchemy.orm import Session
from models.task import Task
from models.project import Project
from models.user import User
from core.logger import logger


def process_csv_file(file_path: str, db: Session):
    """
    Processes the uploaded CSV file:
    - Inserts valid rows into the 'tasks' table
    - Creates an *_errors.csv file containing invalid rows
    """
    logger.info(f"Starting CSV processing: {file_path}")


    error_rows = []
    error_file_path = file_path.replace(".csv", "_errors.csv")

   
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                required = ["project_id", "title", "description", "status", "assigned_to"]
                if any(field not in row or not row[field] for field in required):
                    raise ValueError("Missing required fields")
               
                project_id = int(row["project_id"])
                user_id = int(row["assigned_to"])
               
                project = db.query(Project).filter(Project.id == project_id).first()
                if not project:
                    raise ValueError(f"Invalid project_id {project_id}")


                user = db.query(User).filter(User.id == user_id).first()
                if not user:
                    raise ValueError(f"Invalid assigned_to {user_id}")
                
                if user not in project.assigned_users:
                    raise ValueError(
                        f"User {user_id} not assigned to project {project_id}"
                    )
                
                task = Task(
                    project_id=project_id,
                    title=row["title"],
                    description=row["description"],
                    status=row["status"],
                    assigned_to=user_id
                )

                db.add(task)

                logger.info(f"Inserted task: {row['title']}")

            except Exception as e:
                row["error"] = str(e)
                error_rows.append(row)
                logger.warning(f"Invalid row: {row} – Error: {e}")


        db.commit()
    
    # Save error rows to file
    if error_rows:
        with open(error_file_path, "w", newline="") as ef:
            writer = csv.DictWriter(ef, fieldnames=error_rows[0].keys())
            writer.writeheader()
            writer.writerows(error_rows)
     
        logger.info(f"Error CSV created: {error_file_path}")

    logger.info(f"Finished CSV processing: {file_path}")
    return error_file_path if error_rows else None