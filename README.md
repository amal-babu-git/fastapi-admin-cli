# FastAPI Admin CLI

A Django-inspired CLI tool for managing FastAPI applications with a modular structure. This tool helps developers quickly scaffold and manage FastAPI projects with a clean, organized architecture.

[![PyPI version](https://badge.fury.io/py/fastapi-admin-cli.svg)](https://badge.fury.io/py/fastapi-admin-cli)
[![Python versions](https://img.shields.io/pypi/pyversions/fastapi-admin.svg)](https://pypi.org/project/fastapi-admin-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🚀 **Project Scaffolding**: Create well-structured FastAPI projects with a single command
- 📦 **App Management**: Generate modular apps within your project
- 🐳 **Docker Integration**: Built-in Docker support with commands for building and running containers
- 🔄 **Database Migrations**: Easy database migration commands using Alembic
- 🛠️ **Developer Tools**: Shell access to Docker containers and more

## Installation

Install the package from PyPI:

```bash
pip install fastapi-admin-cli
```

## Usage

### Create a New Project

```bash
fastapi-admin startproject myproject
cd myproject
```

This creates a new FastAPI project with the following structure:
- Docker configuration
- Database migration setup with Alembic
- Environment variable management
- Modular app structure

### Create a New App

```bash
# Make sure you're in the project directory
fastapi-admin startapp users
```

This creates a new app with the following files:
- `models.py`: SQLAlchemy models
- `schemas.py`: Pydantic schemas
- `routes.py`: FastAPI routes
- `services.py`: Business logic
- `admin.py`: Admin interface configuration

### Docker Operations

Build and run your application using Docker:

```bash
# Build Docker containers
fastapi-admin docker build

# Run Docker containers
fastapi-admin docker run
```

### Database Migrations

```bash
# Create new migrations
fastapi-admin db makemigrations -m "create users table"

# Apply migrations
fastapi-admin db migrate
```

### Database Administration

The CLI provides several commands for database management inside the container shell:

```bash
# Launch a shell in the container
fastapi-admin shell

# Inside the container, you can use Alembic directly:
alembic current          # Show current migration revision
alembic history          # Show migration history
alembic downgrade -1     # Downgrade to previous migration
alembic stamp head       # Mark the database as being at the 'head' revision
```

You can also run SQL queries directly using the SQLAlchemy admin panel included in the project.

### Authentication

The project includes a pre-configured authentication module implemented with the fastapi-users package:

- JWT authentication with access and refresh tokens
- User registration, email verification, and password reset

To use authentication in your routes:

```python
from app.auth.dependencies import current_active_user

@router.get("/protected-route")
def protected_route(user = Depends(current_active_user)):
    return {"message": f"Hello, {user.email}!"}
```

### ORM Integration

The project uses SQLModel for ORM operations, which combines the best of SQLAlchemy and Pydantic:

- Type-safe models that work as both Pydantic models and SQLAlchemy models
- Simplified query syntax while maintaining full SQLAlchemy power
- Automatic schema validation

Example model:

```python
from sqlmodel import Field, SQLModel
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
```

### Admin Panel

The project includes an SQLAlchemy admin panel for database management:

- Automatic CRUD interface for all your models
- Customizable admin views

To access the admin panel, navigate to `/admin` after starting your application.

## Project Structure

The generated project follows a modular structure inspired by Django:

```
myproject/
├── main.py                # Main application entry point
├── manage.py              # CLI wrapper script
├── docker/                # Docker configuration
│   └── compose/           # Docker Compose files
├── migrations/               # Database migrations
├── auth/                 # Example app
│   ├── __init__.py
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── routes.py          # FastAPI routes
│   ├── auth.py        # Business logic
│   └── admin.py           # Admin interface configuration
└── ...
```

## Environment Variables

The project template includes an `env.txt` file that should be copied to `.env` for local development. The CLI will attempt to do this automatically when running `docker build`.

## Using the Manage.py Wrapper

Each generated project includes a `manage.py` wrapper that provides the same functionality as the fastapi-admin CLI:

```bash
python manage.py startapp new_app
python manage.py docker build
python manage.py docker run
python manage.py db migrate
python manage.py shell
```

## Local Development

For local development without Docker:

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   # Or if you have uv installed
   uv sync
   ```

3. Copy environment variables:
   ```bash
   cp env.txt .env
   ```

## Troubleshooting

### Docker Issues

If you encounter issues with Docker containers:

1. Check if Docker is installed and running
2. Verify the container name with `docker ps`
3. Check Docker Compose configuration in `docker/compose/docker-compose.yml`

### Database Migration Issues

If you have problems with database migrations:

1. Ensure the database container is running
2. Check if Alembic is properly installed in the container
3. Verify your database connection settings
4. Try running migrations manually inside the container shell:
   ```bash
   fastapi-admin shell
   alembic upgrade head
   ```
5. Check Alembic logs for detailed error messages

## License

This project is licensed under the MIT License - see the LICENSE file for details.
