import os
import typer
import re
import inflect
from fastapi_admin.utils import file_utils, template_utils
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

app = typer.Typer(help="Create a new app within a FastAPI project")
console = Console()
p = inflect.engine()  # For handling singular/plural conversions


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

    # Generate template variables based on app_name
    template_vars = generate_template_variables(app_name)

    # Ensure the "app" directory exists
    app_module_dir = os.path.join(os.getcwd(), "app")
    if not os.path.exists(app_module_dir):
        console.print(
            f"[yellow]Creating app module directory at: {app_module_dir}[/]")
        os.makedirs(app_module_dir)

        # Create __init__.py in the app module to make it a proper package
        init_file = os.path.join(app_module_dir, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write("# App module initialization")

    # Create app directory inside the app module
    app_dir = os.path.join(app_module_dir, app_name)
    file_utils.create_directory(app_dir)

    # Fetch app template with replacements
    template_utils.fetch_app_template(app_dir, app_name, template_vars)

    # Success message with instructions
    console.print("\n[bold green]✨ App created successfully![/]")
    console.print(
        Panel(
            "\n".join([
                "[bold yellow]Next steps:[/]",
                "",
                f"[cyan]1.[/] [white]Add the following to your main.py:[/]",
                f"[dim green]from app.{app_name}.routes import router as {app_name}_router",
                f"app.include_router({app_name}_router, prefix='/api/{app_name}', tags=['{app_name}'])[/]",
                "",
                f"[cyan]2.[/] [white]Start implementing your endpoints in:[/]",
                f"[dim]app/{app_name}/routes.py[/]"
            ]),
            title="[bold]Getting Started[/]",
            border_style="green"
        )
    )


def generate_template_variables(app_name):
    """Generate template variables based on app_name"""
    # Convert app_name to singular form if it's plural
    singular_name = p.singular_noun(app_name) or app_name

    # Generate model name (capitalized singular form)
    model_name = singular_name.title().replace('_', '')

    # Generate model name plural
    model_name_plural = p.plural(model_name)

    # Generate app_name_lowercase for route functions
    app_name_lowercase = singular_name.lower()

    # Generate table_name (typically underscore_separated and plural)
    table_name = p.plural(singular_name.lower()).replace('-', '_')

    # Generate model description
    model_description = f"Database model for {singular_name}"

    return {
        "app_name": app_name,
        "app_name_lowercase": app_name_lowercase,
        "model_name": model_name,
        "model_name_plural": model_name_plural,
        "table_name": table_name,
        "model_description": model_description
    }
