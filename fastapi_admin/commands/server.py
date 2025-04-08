import os
import typer
import subprocess
from fastapi_admin.utils import file_utils

app = typer.Typer(help="Run the development server")

@app.callback(invoke_without_command=True)
def main(host: str = "127.0.0.1", port: int = 8000, reload: bool = True):
    """Run development server using uvicorn"""
    # Check if we're inside a FastAPI project
    if not file_utils.is_fastapi_project():
        typer.echo("Error: Not inside a FastAPI project. Run this command from the project root.")
        raise typer.Exit(code=1)
    
    typer.echo(f"Starting development server at http://{host}:{port}")
    
    # Determine the app module to run
    app_module = "main:app"
    if not os.path.exists("main.py"):
        typer.echo("Error: main.py not found. Make sure you have a main.py file in your project.")
        raise typer.Exit(code=1)
    
    # Build the uvicorn command
    cmd = ["uvicorn", app_module, "--host", host, "--port", str(port)]
    if reload:
        cmd.append("--reload")
    
    try:
        # Run the server
        subprocess.run(cmd)
    except KeyboardInterrupt:
        typer.echo("\nDevelopment server stopped")
