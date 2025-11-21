# FastAPI Developer Assessment

This project implements a full FastAPI backend with:

- User authentication (JWT)
- Role-based authorization (Admin/User)
- CRUD operations for Projects and Tasks
- CSV upload + background processing
- Error CSV generation for invalid rows
- Alembic migrations for database schema
- PostgreSQL + SQLAlchemy ORM

## 🚀 Features Implemented

### 🔐 Authentication & Authorization
- User registration with bcrypt password hashing  
- JWT login  
- Admin → full access  
- User → limited to assigned projects/tasks  

### 📁 Projects Module
- Admin: Create, update, delete, list  
- Users: Only view assigned projects  
- Many-to-many relationship: Project ↔ User  

### 📝 Tasks Module
- Admin: Full CRUD  
- Users: Only manage tasks assigned to them  
- Task belongs to exactly one project  

### 📤 CSV Upload (Admin only)
- Upload CSV containing multiple tasks  
- Background task processes rows  
  - Valid → inserted to DB  
  - Invalid → exported to an `_errors.csv` file  
- API provided to download latest error CSV  

### 🛢 Database
- PostgreSQL  
- SQLAlchemy ORM  
- Alembic migrations

## 📦 Project Setup

### 1. Clone Repository
git clone https://github.com/Ajith-te/fast-api-lcs-assessment.git

### 2. Create Virtual Environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate (Windows)

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Configure .env
DATABASE_URL=postgresql://postgres:password@localhost:5432/fastapi_assessment
JWT_SECRET_KEY=your_jwt_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

### 5. Run Migrations
alembic upgrade head

### 6. Start Application
uvicorn app.main:app --reload

## 📚 API Documentation
Swagger UI → http://127.0.0.1:8000/docs  
Redoc UI → http://127.0.0.1:8000/redoc  

## 🔌 API Endpoints Summary
(Shortened for file — use your full API list in GitHub.)

- POST /auth/register  
- POST /auth/login  
- GET /users/me  
- GET /projects/  
- POST /tasks/  
- POST /upload/csv  
- GET /upload/errors  

## 🧪 CSV Format
project_id,title,description,status,assigned_to

## 🏁 Summary
Production-ready FastAPI backend following clean architecture, migrations, and background processing.
