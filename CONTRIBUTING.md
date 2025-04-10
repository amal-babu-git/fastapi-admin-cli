# Contributing to FastAPI Admin CLI

First off, thank you for considering contributing to FastAPI Admin CLI! It's people like you that make this tool better for everyone. This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Introduction](#introduction)
- [Project Structure](#project-structure)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Adding New Commands](#adding-new-commands)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Code of Conduct](#code-of-conduct)

## Introduction

FastAPI Admin CLI is a Django-inspired command-line tool for managing FastAPI applications with a modular structure. It helps developers quickly scaffold and manage FastAPI projects with a clean, organized architecture.

The project aims to simplify common tasks in FastAPI development, such as:
- Creating new projects with a well-structured template
- Adding modular apps within a project
- Managing Docker containers
- Handling database migrations
- Providing easy access to shell and admin operations

## Project Structure

Here's an overview of the project's structure:

```
fastapi-admin-cli/
├── fastapi_admin/              # Main package directory
│   ├── __init__.py             # Package initialization with version
│   ├── cli.py                  # Main CLI entry point
│   ├── commands/               # CLI commands implementation
│   │   ├── __init__.py         # Package initialization
│   │   ├── app.py              # App creation command
│   │   ├── container.py        # Container shell access
│   │   ├── docker.py           # Docker management commands
│   │   ├── migrations.py       # Database migration commands
│   │   ├── project.py          # Project creation command
│   │   └── superuser.py        # Superuser management
│   └── utils/                  # Utility functions
│       ├── __init__.py         # Package initialization
│       ├── docker_utils.py     # Docker-related utilities
│       ├── file_utils.py       # File operation utilities
│       └── template_utils.py   # Template handling utilities
├── pyproject.toml              # Project metadata and dependencies
├── README.md                   # Project documentation
├── record_demo.sh              # Demo recording script
└── test_commands.sh            # Test script for CLI commands
```

### Key Components:

1. **cli.py**: The main entry point for the CLI tool. It registers all the command groups.

2. **commands/**: Each file in this directory implements a specific command group:
   - `project.py`: Creates new FastAPI projects
   - `app.py`: Creates new apps within a project
   - `docker.py`: Manages Docker containers
   - `migrations.py`: Handles database migrations
   - `container.py`: Provides shell access to containers
   - `superuser.py`: Manages superuser creation

3. **utils/**: Contains utility functions used across the project:
   - `template_utils.py`: Handles fetching and processing templates
   - `file_utils.py`: Provides file system operations
   - `docker_utils.py`: Contains Docker-related utilities

## Development Setup

### Fork and Clone the Repository

1. Fork the repository on GitHub
2. Clone your fork locally:
```bash
git clone https://github.com/YOUR_USERNAME/fastapi-admin-cli.git
cd fastapi-admin-cli
```

3. Add the original repository as upstream:
```bash
git remote add upstream https://github.com/amal-babu-git/fastapi-admin-cli.git
```

### Setting Up Development Environment

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the package in development mode:
```bash
pip install -e .
```

3. Install additional development dependencies:
```bash
pip install pytest black isort mypy
```

## Development Workflow

1. Create a branch for your feature or bugfix:
```bash
git checkout -b feature-or-fix-name
```

2. Make your changes and commit them:
```bash
git add .
git commit -m "Description of your changes"
```

3. Keep your branch updated with the upstream:
```bash
git fetch upstream
git rebase upstream/main
```

4. Push your changes to your fork:
```bash
git push origin feature-or-fix-name
```

5. Open a pull request on GitHub

## Adding New Commands

To add a new command to the CLI:

1. Create a new file in the `fastapi_admin/commands/` directory, e.g., `mycommand.py`.
2. Implement your command using `typer` (see existing commands for examples).
3. Register your command in `cli.py` by adding:
```python
from fastapi_admin.commands import mycommand
cli_app.add_typer(mycommand.app, name="mycommand")
```

Example command structure:
```python
import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(help="My new command description")
console = Console()

@app.callback(invoke_without_command=True)
def main(param: str):
    """Main command implementation"""
    console.print(Panel(f"Executing command with {param}"))
    # Command implementation here
```

## Testing

You can test your changes using the `test_commands.sh` script:

```bash
./test_commands.sh
```

If you're adding new commands or features, consider adding tests for them to this script.

For interactive testing, use:

```bash
fastapi-admin your-command --your-parameters
```

## Documentation

When adding new features, please update the documentation:

1. Add your command to the command table in README.md
2. Document your command's usage with examples
3. If your command adds significant functionality, consider adding a section to README.md

## Pull Request Process

1. Ensure your code passes all tests and linting checks
2. Update the documentation if needed
3. Make sure your PR title and description clearly describe the changes
4. Link any related issues in your PR description
5. Be responsive to feedback and be willing to make requested changes

## Style Guidelines

This project follows these style guidelines:

1. Use [Black](https://black.readthedocs.io/) for code formatting
2. Use [isort](https://pycqa.github.io/isort/) for import sorting
3. Follow PEP 8 style guidelines
4. Write clear docstrings for functions and classes
5. Use type hints where appropriate

Before submitting a PR, format your code:

```bash
black fastapi_admin
isort fastapi_admin
```

<!-- ## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

--- -->

Thank you for contributing to FastAPI Admin CLI! Your efforts help make this tool better for everyone.
