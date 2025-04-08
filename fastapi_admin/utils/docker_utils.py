import subprocess
import typer

def is_container_running(container_name):
    """Check if a Docker container is running"""
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", f"name={container_name}", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            check=False
        )
        
        return container_name in result.stdout.strip()
    except FileNotFoundError:
        typer.echo("Docker command not found. Please ensure Docker is installed and in your PATH.")
        return False
    except Exception as e:
        typer.echo(f"Error checking Docker container: {str(e)}")
        return False
