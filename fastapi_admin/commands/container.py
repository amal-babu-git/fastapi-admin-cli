import typer
import subprocess
from fastapi_admin.utils import docker_utils
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(
    help="Launch a shell inside a Docker container",
    short_help="Container shell access"
)
console = Console()


@app.callback(invoke_without_command=True)
def main(container_name: str = "fastapi-app"):
    """
    Launch a shell inside the application's Docker container

    Args:
        container_name: Name of the Docker container (default: fastapi-app)

    Example:
        $ fastapi-admin shell
        $ fastapi-admin shell --container-name my-container
    """
    console.print(Panel.fit(
        f"Checking for Docker container: [bold blue]{container_name}[/]",
        border_style="blue"
    ))

    if not docker_utils.is_container_running(container_name):
        console.print(Panel(
            "\n".join([
                f"[bold red]Error:[/] No running Docker container named '{container_name}' found.",
                "",
                "[yellow]Make sure your Docker container is running:[/]",
                f"• Check container status: [dim]docker ps --filter name={container_name}[/]",
                "• Start your container: [dim]docker-compose up -d[/]",
                f"• Try a different container name: [dim]fastapi-admin shell --container-name <name>[/]"
            ]),
            title="Container Not Found",
            border_style="red"
        ))
        raise typer.Exit(code=1)

    console.print(Panel(
        f"Launching shell in container '[bold blue]{container_name}[/]'...",
        border_style="green"
    ))

    try:
        subprocess.run(f"docker exec -it {container_name} bash", shell=True)
    except subprocess.CalledProcessError as e:
        console.print(Panel(
            "\n".join([
                f"[bold red]Error launching shell:[/] {str(e)}",
                "",
                "[yellow]Try one of the following:[/]",
                f"• [dim]python manage.py shell {container_name}[/]",
                f"• [dim]fastapi-admin shell --container-name {container_name}[/]",
                f"• [dim]docker exec -it {container_name} bash[/]"
            ]),
            title="Shell Error",
            border_style="red"
        ))
        raise typer.Exit(code=1)
