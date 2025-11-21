# FastAPI Developer Assessment

A complete FastAPI backend demonstrating:

- User authentication (JWT)
- Role-based authorization (Admin / User)
- CRUD operations for Projects & Tasks
- CSV upload and background processing
- Error CSV generation and download API
- PostgreSQL integration using SQLAlchemy ORM

---

## 🚀 Features

### ✔ 1. Authentication & Authorization
- User registration with hashed passwords (bcrypt)
- JWT-based login
- Admin has full access
- Users only access assigned projects and tasks

### ✔ 2. Project Module (CRUD)
- Fields: id, name, description, created_by
- Many-to-many relation: Projects ↔ Users
- Admin: full CRUD
- User: only view assigned projects

### ✔ 3. Task Module (CRUD)
- Fields: id, project_id, title, description, status, assigned_to
- Admin: full CRUD
- User: can manage only their assigned tasks

### ✔ 4. CSV Upload & Background Processing
- Admin uploads a CSV containing multiple tasks
- CSV file saved to `/uploads`
- Background task processes rows:
  - Valid rows → inserted into DB
  - Invalid rows → written to `<filename>_errors.csv`
- Download latest error file from:
  `GET /upload/errors`

### ✔ 5. PostgreSQL + SQLAlchemy ORM
- Connected using `.env` configuration
- Automatic table creation on startup

---

## 📁 Project Structure

```
fast_api_assessment/
│── main.py
│── database.py
│── core/
│     ├── security.py
│     └── dependencies.py
│     └── logs.py
│── models/
│     ├── user.py
│     ├── project.py
│     ├── task.py
│     └── association.py
│── schemas/
│     ├── user.py
│     ├── project.py
│     ├── task.py
│     └── auth.py
│── routes/
│     ├── auth.py
│     ├── users.py
│     ├── projects.py
│     ├── tasks.py
│     └── csv_upload.py
│── services/
│     └── csv_processor.py
uploads/ (auto-created)
.env
requirements.txt
```

---

## 🔧 Environment Setup

### Install Dependencies
```
pip install -r requirements.txt
```

### Create `.env`
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/fastapi_db
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
```

---

## ▶️ Run the Application

```
uvicorn app.main:app --reload
```

### API Docs:
- Swagger: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

## 🧪 Testing CSV Upload

### Endpoint:
```
POST /upload/csv
```

### Example CSV:
```
project_id,title,description,status,assigned_to
1,Login Task,Implement JWT,Pending,2
1,Invalid Task ID,Invalid entry,Pending,999
```

### Download Error CSV:
```
GET /upload/errors
```

---

## 🏁 Conclusion
This project demonstrates clean implementation of:
- FastAPI architecture
- SQLAlchemy ORM
- Authentication & authorization
- Background task processing
- File handling
- Error handling

