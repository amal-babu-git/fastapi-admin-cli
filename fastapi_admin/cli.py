import typer
from fastapi_admin.commands import project, app, server, container

cli_app = typer.Typer(help="FastAPI Admin CLI tool for managing FastAPI applications")

# Register commands
cli_app.add_typer(project.app, name="startproject")
cli_app.add_typer(app.app, name="startapp")
cli_app.add_typer(server.app, name="runserver")
cli_app.add_typer(container.app, name="shell")

def cli():
    """Entry point for the CLI tool"""
    cli_app()

if __name__ == "__main__":
    cli()
