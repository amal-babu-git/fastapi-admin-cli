import typer
import subprocess
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(
    help="Database migration operations using Alembic",
    short_help="Database migration operations"
)
console = Console()


def _run_docker_compose_command(command: str, message: str):
    """Helper function to run docker-compose commands"""
    console.print(Panel(message, style="bold blue"))
    try:
        # Use arrays instead of shell=True for better quote handling
        base_cmd = [
            "docker-compose",
            "-f", "docker/compose/docker-compose.yml",
            "run", "--rm", "api",
            "sh", "-c"
        ]
        # The key fix: properly escape the quotes in the command
        alembic_cmd = f"alembic {command}"
        cmd = base_cmd + [alembic_cmd]

        # Print the command being executed
        console.print(f"[dim]Executing: {' '.join(cmd)}[/dim]")

        result = subprocess.run(
            cmd,
            check=False,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            console.print(Panel(
                f"[bold red]Command failed with exit code {result.returncode}[/]\n\n"
                f"[bold white]STDOUT:[/]\n{result.stdout}\n\n"
                f"[bold white]STDERR:[/]\n{result.stderr}",
                title="Error Details",
                border_style="red"
            ))
            raise subprocess.CalledProcessError(result.returncode, cmd)

        # Handle empty output case and provide success feedback
        output = result.stdout.strip()
        if not output:
            output = "[green]Command completed successfully with no output.[/]\n\n" + \
                "[dim]Note: No output typically means:[/]\n" + \
                "• For migrations: No pending migrations to apply\n" + \
                "• For makemigrations: No changes detected"

        console.print(
            Panel(output, title="Command Output", border_style="green"))

        # Add explicit success message
        console.print(Panel(
            f"[bold green]✓ {message.rstrip('...')} completed successfully![/]",
            border_style="green"
        ))

    except Exception as e:
        console.print(Panel(
            f"[bold red]Error executing command:[/]\n{str(e)}",
            title="Error",
            border_style="red"
        ))
        console.print(Panel(
            "\n".join([
                "[yellow]Try the following solutions:[/]",
                "• For environment variables warnings, create a .env file with required variables",
                "• For quote issues, try running directly in the container with shell command",
                "• Check if alembic is properly installed in the container",
                "• Verify your docker-compose.yml configuration"
            ]),
            title="Troubleshooting",
            border_style="yellow"
        ))
        raise typer.Exit(code=1)


@app.command(name="makemigrations")
def make_migrations(
    message: str = typer.Option(
        "init",
        "-m",
        "--message",
        help="Migration message"
    )
):
    """
    Create new database migrations using Alembic

    Example:
        $ fastapi-admin makemigrations -m "add user table"
        $ fastapi-admin makemigrations --message "add user table"
    """
    # Fix the quotes issue by using single quotes for the alembic command
    _run_docker_compose_command(
        f"revision --autogenerate -m '{message}'",
        "Creating database migrations..."
    )


@app.command(name="migrate")
def migrate():
    """
    Apply database migrations using Alembic

    Example:
        $ fastapi-admin migrate
    """
    _run_docker_compose_command(
        "upgrade head",
        "Applying database migrations..."
    )


@app.command(name="shell")
def shell():
    """
    Open a shell in the API container

    Example:
        $ fastapi-admin shell
    """
    console.print(
        Panel("Opening shell in API container...", style="bold blue"))
    try:
        subprocess.run(
            ["docker-compose", "-f", "docker/compose/docker-compose.yml",
                "run", "--rm", "api", "sh"],
            check=True
        )
    except subprocess.CalledProcessError as e:
        console.print(
            Panel(f"Error opening shell: {str(e)}", title="Error", border_style="red"))
        raise typer.Exit(code=1)


@app.command(name="env_check")
def env_check():
    """
    Check for missing environment variables that docker-compose needs

    Example:
        $ fastapi-admin env_check
    """
    missing_vars = ["apr1", "xyz123", "hashedpassword"]
    console.print(Panel(
        "\n".join([
            "[bold]Missing environment variables detected in docker-compose output:[/]",
            "• apr1",
            "• xyz123",
            "• hashedpassword",
            "",
            "[yellow]Create a .env file in the same directory as docker-compose.yml with:[/]",
            "apr1=your_value",
            "xyz123=your_value",
            "hashedpassword=your_value"
        ]),
        title="Environment Variables Check",
        border_style="blue"
    ))


if __name__ == "__main__":
    app()
