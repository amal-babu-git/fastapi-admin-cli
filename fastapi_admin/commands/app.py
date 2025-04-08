import os
import typer
from fastapi_admin.utils import file_utils, template_utils

app = typer.Typer(help="Create a new app within a FastAPI project")

@app.callback(invoke_without_command=True)
def main(app_name: str):
    """Create a new app module within an existing project"""
    # Check if we're inside a FastAPI project
    if not file_utils.is_fastapi_project():
        typer.echo("Error: Not inside a FastAPI project. Run this command from the project root.")
        raise typer.Exit(code=1)
    
    typer.echo(f"Creating app: {app_name}")
    
    # Create app directory
    app_dir = os.path.join(os.getcwd(), app_name)
    file_utils.create_directory(app_dir)
    
    # Fetch app template
    template_utils.fetch_app_template(app_dir, app_name)
    
    typer.echo(f"App {app_name} created successfully!")
    typer.echo(f"Remember to add '{app_name}' to your main.py to include its routes")
