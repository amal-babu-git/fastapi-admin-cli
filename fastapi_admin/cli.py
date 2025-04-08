import typer
from fastapi_admin.commands import project, app, container, migrations, docker

cli_app = typer.Typer(
    help="FastAPI Admin CLI tool for managing FastAPI applications")

# Register commands
cli_app.add_typer(project.app, name="startproject")
cli_app.add_typer(app.app, name="startapp")
cli_app.add_typer(container.app, name="shell")
# Access as: fastapi-admin db migrate
cli_app.add_typer(migrations.app, name="db")
# Access as: fastapi-admin docker build
cli_app.add_typer(docker.app, name="docker")


def cli():
    """Entry point for the CLI tool"""
    cli_app()


if __name__ == "__main__":
    cli()
