import typer
import asyncio
import sys
from typing import Optional
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(
    help="Superuser management operations",
    short_help="Superuser operations"
)
console = Console()


@app.callback(invoke_without_command=True)
def main(
    email: str = typer.Argument(..., help="Email of the superuser"),
    password: str = typer.Argument(..., help="Password for the superuser"),
    first_name: Optional[str] = typer.Option(
        None, help="First name of the superuser"),
    last_name: Optional[str] = typer.Option(
        None, help="Last name of the superuser")
):
    """
    Create a superuser for the admin panel.

    Example:
        $ fastapi-admin createsuperuser admin@example.com password123
        $ fastapi-admin createsuperuser admin@example.com password123 --first-name Admin --last-name User
    """
    console.print(Panel(
        f"Creating superuser with email: [bold blue]{email}[/]",
        border_style="blue"
    ))

    try:
        # We need to execute inside the container where the database is accessible
        _create_superuser_in_container(email, password, first_name, last_name)

        console.print(Panel(
            f"[bold green]✓ Superuser {email} created successfully![/]",
            border_style="green"
        ))
    except Exception as e:
        console.print(Panel(
            f"[bold red]Error creating superuser:[/]\n{str(e)}",
            title="Error",
            border_style="red"
        ))
        raise typer.Exit(code=1)


def _create_superuser_in_container(email: str, password: str, first_name: Optional[str], last_name: Optional[str]):
    """Execute superuser creation inside the Docker container"""
    import subprocess

    # Build the command with proper arguments
    command = f"python -c \"from app.core.commands import create_superuser; import asyncio; asyncio.run(create_superuser('{email}', '{password}'"

    # Add optional arguments if provided
    if first_name:
        command += f", first_name='{first_name}'"
    if last_name:
        command += f", last_name='{last_name}'"

    command += "));\""

    # Execute the command in the container
    try:
        result = subprocess.run(
            ["docker-compose", "-f", "docker/compose/docker-compose.yml",
                "run", "--rm", "api", "sh", "-c", command],
            check=True,
            capture_output=True,
            text=True
        )

        # Check for any output messages
        if result.stdout:
            console.print(result.stdout)

    except subprocess.CalledProcessError as e:
        console.print(Panel(
            f"[bold red]Failed to create superuser:[/]\n\n"
            f"[bold white]STDOUT:[/]\n{e.stdout if e.stdout else 'No output'}\n\n"
            f"[bold white]STDERR:[/]\n{e.stderr if e.stderr else 'No output'}",
            title="Error Details",
            border_style="red"
        ))
        raise Exception(f"Failed to create superuser: {e.stderr}")

    # Return success
    return True
