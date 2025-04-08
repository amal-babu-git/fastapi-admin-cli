import os
import typer
from fastapi_admin.utils import file_utils, template_utils

app = typer.Typer(help="Create a new FastAPI project")

@app.callback(invoke_without_command=True)
def main(project_name: str):
    """Create a new FastAPI project with modular structure"""
    typer.echo(f"Creating project: {project_name}")
    
    # Create project directory
    project_dir = os.path.join(os.getcwd(), project_name)
    file_utils.create_directory(project_dir)
    
    # Fetch project template
    template_utils.fetch_project_template(project_dir, project_name)
    
    typer.echo(f"Project {project_name} created successfully!")
    typer.echo(f"Run 'cd {project_name}' to navigate to your project")
    typer.echo(f"Use 'python manage.py runserver' to start the development server")
