import os
import shutil
import typer

def create_directory(path):
    """Create a directory if it doesn't exist"""
    if os.path.exists(path):
        typer.echo(f"Directory {path} already exists.")
        confirm = typer.confirm("Do you want to overwrite it?", default=False)
        if not confirm:
            typer.echo("Operation cancelled.")
            raise typer.Exit(code=1)
        shutil.rmtree(path)
    
    try:
        os.makedirs(path)
        return True
    except Exception as e:
        typer.echo(f"Error creating directory {path}: {str(e)}")
        raise typer.Exit(code=1)

def is_fastapi_project():
    """Check if the current directory is a FastAPI project"""
    return os.path.exists("manage.py") or os.path.exists("main.py")

def write_file(path, content):
    """Write content to a file"""
    try:
        with open(path, 'w') as file:
            file.write(content)
        return True
    except Exception as e:
        typer.echo(f"Error writing to file {path}: {str(e)}")
        raise typer.Exit(code=1)

def make_executable(path):
    """Make a file executable"""
    try:
        mode = os.stat(path).st_mode
        os.chmod(path, mode | 0o111)  # Add executable bit
        return True
    except Exception as e:
        typer.echo(f"Warning: Could not make {path} executable: {str(e)}")
        return False
