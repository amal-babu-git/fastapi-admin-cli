import typer
import os
import requests
from typing import Optional
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(
    help="Superuser management operations",
    short_help="Superuser operations"
)
console = Console()

SCRIPT_URL = "https://raw.githubusercontent.com/amal-babu-git/fastapi-admin-cli-template/refs/heads/main/scripts/create_superuser.py"


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

    # Path to the script that should exist in the project
    script_dir = os.path.join(os.getcwd(), "scripts")
    script_path = os.path.join(script_dir, "create_superuser.py")

    # Create scripts directory if it doesn't exist
    if not os.path.exists(script_dir):
        console.print(f"[yellow]Creating scripts directory: {script_dir}[/]")
        os.makedirs(script_dir)

    # Check if the script exists, if not download it
    if not os.path.exists(script_path):
        console.print(
            "[yellow]create_superuser.py script not found, downloading it...[/]")

        try:
            response = requests.get(SCRIPT_URL)
            response.raise_for_status()  # Raise an exception for HTTP errors

            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(response.text)

            console.print(
                f"[green]✓ Script downloaded successfully to {script_path}\n")
        except Exception as e:
            console.print(
                f"[bold red]Failed to download the script:[/] {str(e)}")
            raise Exception(
                f"Failed to download create_superuser.py: {str(e)}")

    # Support both docker-compose and docker compose syntax
    docker_cmd = "docker-compose"
    try:
        subprocess.run(["docker-compose", "--version"],
                       check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        docker_cmd = "docker compose"

    # Build command arguments
    command_args = ["python", "scripts/create_superuser.py", email, password]
    if first_name:
        command_args.extend(["--first-name", first_name])
    if last_name:
        command_args.extend(["--last-name", last_name])

    command = " ".join(command_args)

    console.print(f"[dim]Executing: {command}[/dim]")

    try:
        # Run the script in the container
        result = subprocess.run(
            f"{docker_cmd} -f docker/compose/docker-compose.yml exec api {command}",
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )

        # Check for specific output messages
        if result.stdout:
            # Check for already exists message
            if "already exists" in result.stdout:
                console.print(Panel(
                    f"[bold yellow]User {email} already exists[/]",
                    border_style="yellow"
                ))
            # Check for update to superuser message
            elif "Updated user" in result.stdout and "to superuser status" in result.stdout:
                console.print(Panel(
                    f"[bold green]✓ User {email} updated to superuser status![/]",
                    border_style="green"
                ))
            # Success message
            elif "created successfully" in result.stdout:
                console.print(Panel(
                    f"[bold green]✓ Superuser {email} created successfully![/]",
                    border_style="green"
                ))
            # Any other output
            else:
                console.print(result.stdout)

    except subprocess.CalledProcessError as e:
        # Handle environment variable warnings
        if hasattr(e, 'stderr') and e.stderr and "variable is not set. Defaulting to a blank string" in e.stderr:
            console.print(Panel(
                "\n".join([
                    "[bold yellow]Warning: Environment variables not set[/]",
                    "",
                    "Some environment variables are missing in your .env file.",
                    "This may cause issues with your application but the superuser creation might still work.",
                    "",
                    "Create a .env file with the required variables:",
                    "[dim]cp env.txt .env[/dim]"
                ]),
                title="Environment Warning",
                border_style="yellow"
            ))

        # Handle case where container might not be running
        if hasattr(e, 'stderr') and e.stderr and ("not running" in e.stderr or "No such container" in e.stderr):
            console.print(Panel(
                "\n".join([
                    "[bold red]Container not running[/]",
                    "",
                    "The API container doesn't appear to be running.",
                    "Please start your containers first:",
                    "[dim]fastapi-admin docker run[/dim]"
                ]),
                title="Container Error",
                border_style="red"
            ))

        # Handle database connection errors
        if hasattr(e, 'stdout') and "Error creating superuser" in e.stdout:
            error_msg = e.stdout.split("Error creating superuser: ")[1].strip()
            console.print(Panel(
                f"[bold red]Database error:[/]\n{error_msg}",
                title="Database Error",
                border_style="red"
            ))

        console.print(Panel(
            f"[bold red]Failed to create superuser:[/]\n\n"
            f"[bold white]STDOUT:[/]\n{e.stdout if hasattr(e, 'stdout') and e.stdout else 'No output'}\n\n"
            f"[bold white]STDERR:[/]\n{e.stderr if hasattr(e, 'stderr') and e.stderr else 'No output'}",
            title="Error Details",
            border_style="red"
        ))
        raise Exception("Failed to create superuser. See error details above.")

    # Return success
    return True
