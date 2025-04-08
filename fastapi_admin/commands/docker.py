import typer
import subprocess
import shutil
from rich.console import Console
from rich.panel import Panel
import os

app = typer.Typer(
    help="Docker container management operations",
    short_help="Docker operations"
)
console = Console()


@app.command(name="build")
def build():
    """
    Build Docker container using docker-compose

    Example:
        $ fastapi-admin docker build
    """
    console.print(Panel("Setting up environment...", style="bold blue"))
    if not os.path.exists('.env'):
        try:
            shutil.copy('env.txt', '.env')
            console.print(
                Panel("✓ Environment file copied", style="bold green"))
        except FileNotFoundError:
            console.print(Panel(
                "Warning: env.txt not found. Proceeding without environment file.",
                style="bold yellow"
            ))
    else:
        console.print(Panel("✓ Using existing .env file", style="bold green"))

    console.print(Panel("Building Docker container...", style="bold blue"))
    try:
        subprocess.run(
            "docker-compose -f docker/compose/docker-compose.yml build",
            shell=True,
            check=True
        )
        console.print(
            Panel("✓ Container built successfully", style="bold green"))
    except subprocess.CalledProcessError as e:
        console.print(Panel(
            f"[bold red]Build failed:[/]\n{str(e)}",
            title="Error",
            border_style="red"
        ))
        raise typer.Exit(code=1)


@app.command(name="run")
def run():
    """
    Run Docker container using docker-compose

    Example:
        $ fastapi-admin docker run
    """
    console.print(Panel("Starting Docker container...", style="bold blue"))
    try:
        subprocess.run(
            "docker-compose -f docker/compose/docker-compose.yml up -d",
            shell=True,
            check=True
        )
        console.print(Panel("✓ Container is now running", style="bold green"))
    except subprocess.CalledProcessError as e:
        console.print(Panel(
            f"[bold red]Failed to start container:[/]\n{str(e)}",
            title="Error",
            border_style="red"
        ))
        raise typer.Exit(code=1)
