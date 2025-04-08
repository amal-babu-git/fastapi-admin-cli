import os
import typer
from fastapi_admin.utils import file_utils, template_utils
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

app = typer.Typer(help="Create a new FastAPI project")
console = Console()


@app.callback(invoke_without_command=True)
def main(project_name: str):
    """Create a new FastAPI project with modular structure"""
    console.print(Panel.fit(
        Text(f"Creating project: {project_name}", style="bold green"),
        title="FastAPI Admin CLI",
        border_style="blue"
    ))

    # Create project directory
    project_dir = os.path.join(os.getcwd(), project_name)
    file_utils.create_directory(project_dir)

    # Fetch project template
    template_utils.fetch_project_template(project_dir, project_name)

    console.print("\n[bold green]✨ Project created successfully![/]")
    console.print(
        Panel(
            "\n".join([
                "[bold yellow]Next steps (use python manage.py or fastapi-admin):[/]",
                "",
                f"[cyan]1.[/] [white]cd {project_name}[/]",
                f"[cyan]2.[/] [white]copy env.txt to .env[/]",
                f"[cyan]3.[/] [white]python manage.py build[/] [dim](building docker-container)[/]",
                f"[cyan]4.[/] [white]python manage.py run[/] [dim](running docker-container)[/]",
                "",
                f"[bold blue]Additional commands:[/]",
                f"[green]•[/] [white]python manage.py shell[/] [dim](launching shell in container)[/]",
                f"[green]•[/] [white]python manage.py makemigrations[/] [dim](create migrations)[/]",
                f"[green]•[/] [white]python manage.py migrate[/] [dim](run migrations)[/]",
                "",
                f"[bold blue]Note:[/] [italic]This template only supports dockerize development.[/]",
                f"[green]•[/] [white]Use docker-compose:[/] [dim]docker/compose/docker-compose.yml[/]",
                f"[green]•[/] [white]Database migrations use alembic within the container[/]",
            ]),
            title="[bold]Getting Started[/]",
            border_style="green"
        )
    )
