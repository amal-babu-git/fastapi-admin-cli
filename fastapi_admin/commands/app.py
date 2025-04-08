import os
import typer
from fastapi_admin.utils import file_utils, template_utils
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

app = typer.Typer(help="Create a new app within a FastAPI project")
console = Console()


@app.callback(invoke_without_command=True)
def main(app_name: str):
    """Create a new app module within an existing project"""
    # Check if we're inside a FastAPI project
    if not file_utils.is_fastapi_project():
        console.print(Panel(
            "[bold red]Error: Not inside a FastAPI project[/]\nRun this command from the project root.",
            border_style="red",
            title="Error"
        ))
        raise typer.Exit(code=1)

    # Show creation message
    console.print(Panel.fit(
        Text(f"Creating app: {app_name}", style="bold green"),
        title="FastAPI Admin CLI",
        border_style="blue"
    ))

    # Create app directory
    app_dir = os.path.join(os.getcwd(), app_name)
    file_utils.create_directory(app_dir)

    # Fetch app template
    template_utils.fetch_app_template(app_dir, app_name)

    # Success message with instructions
    console.print("\n[bold green]✨ App created successfully![/]")
    console.print(
        Panel(
            "\n".join([
                "[bold yellow]Next steps:[/]",
                "",
                f"[cyan]1.[/] [white]Add the following to your main.py:[/]",
                f"[dim green]from {app_name}.routes import router as {app_name}_router",
                f"app.include_router({app_name}_router)[/]",
                "",
                f"[cyan]2.[/] [white]Start implementing your endpoints in:[/]",
                f"[dim]{app_name}/routes.py[/]"
            ]),
            title="[bold]Getting Started[/]",
            border_style="green"
        )
    )
