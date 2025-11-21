# Database Schema Documentation

## Users Table
| Column         | Type     | Description                     |
|----------------|----------|---------------------------------|
| id             | Integer  | Primary key                     |
| name           | String   | User's name                     |
| email          | String   | Unique email                    |
| password_hash  | String   | Bcrypt hashed password          |
| role           | String   | "Admin" or "User"               |

## Projects Table
| Column       | Type     | Description                     |
|--------------|----------|---------------------------------|
| id           | Integer  | Primary key                     |
| name         | String   | Project name                    |
| description  | Text     | Project description             |
| created_by   | Integer  | FK → users.id                   |

## Project ↔ User Association Table  
(Many-to-Many relationship)
| Column       | Type     | Description                     |
|--------------|----------|---------------------------------|
| project_id   | Integer  | FK → projects.id                |
| user_id      | Integer  | FK → users.id                   |

## Tasks Table
| Column        | Type     | Description                     |
|---------------|----------|---------------------------------|
| id            | Integer  | Primary key                     |
| project_id    | Integer  | FK → projects.id                |
| title         | String   | Task title                      |
| description   | Text     | Task details                    |
| status        | String   | Pending / In Progress / Done    |
| assigned_to   | Integer  | FK → users.id                   |
