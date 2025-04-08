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
                "[bold yellow]Next steps:[/]",
                "",
                f"[cyan]1.[/] [white]cd {project_name}[/]",
                f"[cyan]2.[/] [white]copy env.txt to .env[/]",
                f"[cyan]3.[/] [white]fastapi-admin docker build[/] [dim](or python manage.py docker build)[/]",
                f"[cyan]4.[/] [white]fastapi-admin docker run[/] [dim](or python manage.py docker run)[/]",
                "",
                f"[bold blue]Additional commands:[/]",
                f"[green]•[/] [white]fastapi-admin db makemigrations[/] [dim](create migrations)[/]",
                f"[green]•[/] [white]fastapi-admin db migrate[/] [dim](run migrations)[/]",
                f"[green]•[/] [white]fastapi-admin shell[/] [dim](launching shell in container)[/]",
                "",
                f"[bold blue]For local setup:[/]",
                f"[green]•[/] [white]Create virtual environment:[/] [dim]python -m venv venv[/]",
                f"[green]•[/] [white]Install dependencies:[/] [dim]pip install -r requirements.txt[/]",
                f"[green]•[/] [white]Or use uv:[/] [dim]uv sync[/]",
                "",
                f"[bold blue]Note:[/] [italic]Docker configuration available at:[/] [dim]docker/compose/docker-compose.yml[/]",
            ]),
            title="[bold]Getting Started[/]",
            border_style="green"
        )
    )
