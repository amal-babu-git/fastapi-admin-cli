import typer
import subprocess
from fastapi_admin.utils import docker_utils

app = typer.Typer(help="Container operations")


@app.callback(invoke_without_command=True)
def main(container_name: str = "fastapi-app"):
    """Launch a shell inside the application's Docker container"""
    typer.echo(f"Checking for Docker container: {container_name}")

    if not docker_utils.is_container_running(container_name):
        typer.echo(
            f"Error: No running Docker container named '{container_name}' found.")
        typer.echo("Make sure your Docker container is running.")
        typer.echo(f"You can try: docker ps --filter name={container_name}")
        raise typer.Exit(code=1)

    typer.echo(f"Launching shell in container '{container_name}'...")
    try:
        subprocess.run(f"docker exec -it {container_name} bash", shell=True)

    except subprocess.CalledProcessError as e:
        typer.echo(f"Error launching shell: {e}")
        typer.echo(
            "Try: python manage.py shell your_container_name (default: fastapi-app)"
        )
        typer.echo("Or: docker exec -it your_container_name bash")
        raise typer.Exit(code=1)
