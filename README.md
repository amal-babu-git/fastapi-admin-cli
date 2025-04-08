# FastAPI Admin CLI

A Django-inspired CLI tool for managing FastAPI applications with a modular structure.

## Installation

```bash
pip install fastapi-admin
```

## Usage

### Create a new project

```bash
fastapi-admin startproject myproject
```

### Create a new app within a project

```bash
cd myproject
fastapi-admin startapp myapp
```

### Run the development server

```bash
cd myproject
fastapi-admin runserver
# Or use the manage.py wrapper
python manage.py runserver
```

### Launch a shell in the Docker container

```bash
cd myproject
fastapi-admin shell
# Or use the manage.py wrapper
python manage.py shell
```

## Project Structure

The generated project follows a modular structure:

```
myproject/
├── main.py
├── manage.py
├── myapp/
│   ├── __init__.py
│   ├── models.py
│   ├── schemas.py
│   ├── routes.py
│   ├── services.py
│   └── admin.py
└── ...
```

Each app follows a modular structure with:
- models.py (SQLAlchemy models)
- schemas.py (Pydantic schemas)
- routes.py (FastAPI routes)
- services.py (Business logic)
- admin.py (Admin interface configuration)
