import os
import tempfile
import subprocess
import shutil
import typer
import re
from fastapi_admin.utils import file_utils

TEMPLATE_REPO = "https://github.com/amal-babu-git/fastapi-admin-cli-template"


def fetch_project_template(project_dir, project_name):
    """Fetch project template from GitHub"""
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            typer.echo("Fetching project template...")
            subprocess.run(
                ["git", "clone", TEMPLATE_REPO, temp_dir],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Copy project template
            project_template_dir = os.path.join(temp_dir, "project_template")
            if os.path.exists(project_template_dir):
                # Define replacements for template variables
                replacements = {
                    "PROJECT_NAME": project_name,
                    "project_name": project_name.lower(),  # For Python package name
                    # Default description
                    "project_description": f"FastAPI project {project_name}",
                }

                _copy_and_replace_template(
                    project_template_dir, project_dir, replacements)
                create_manage_py(project_dir, project_name)
            else:
                typer.echo(
                    "Error: Project template not found in the repository.")
                raise typer.Exit(code=1)
        except subprocess.CalledProcessError as e:
            typer.echo(f"Error: Failed to fetch template from {TEMPLATE_REPO}")
            typer.echo(
                f"Details: {e.stderr.decode() if e.stderr else 'Unknown error'}")
            raise typer.Exit(code=1)


def fetch_app_template(app_dir, app_name, template_vars=None):
    """Fetch app template from GitHub"""
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            typer.echo("Fetching app template...")
            subprocess.run(
                ["git", "clone", TEMPLATE_REPO, temp_dir],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Copy app template
            app_template_dir = os.path.join(temp_dir, "app_template")
            if os.path.exists(app_template_dir):
                # Create base replacements with app_name
                replacements = {"APP_NAME": app_name}

                # Add template variables if provided
                if template_vars:
                    replacements.update(template_vars)

                _copy_and_replace_template(
                    app_template_dir, app_dir, replacements)
            else:
                typer.echo("Error: App template not found in the repository.")
                raise typer.Exit(code=1)
        except subprocess.CalledProcessError as e:
            typer.echo(f"Error: Failed to fetch template from {TEMPLATE_REPO}")
            typer.echo(
                f"Details: {e.stderr.decode() if e.stderr else 'Unknown error'}")
            raise typer.Exit(code=1)


def _copy_and_replace_template(src_dir, dest_dir, replacements):
    """Copy template files and replace placeholders

        Args:
        src_dir: Source directory containing the template files
        dest_dir: Destination directory where the files will be copied
        replacements: Dictionary of placeholders and their replacements
    """
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isdir(src_path):
            _copy_and_replace_template(src_path, dest_path, replacements)
        else:
            # Replace placeholders in the file content
            with open(src_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()

            # Handle both {{ variable }} and {{{ variable }}} style placeholders
            for placeholder, value in replacements.items():
                content = content.replace(
                    f"{{{{{placeholder}}}}}", value)  # Handle {{var}}
                content = content.replace(
                    f"{{{{ {placeholder} }}}}", value)  # Handle {{ var }}
                # Handle ${variable} style placeholders
                content = content.replace(f"${{{placeholder}}}", value)

            with open(dest_path, 'w', encoding='utf-8') as file:
                file.write(content)


def create_manage_py(project_dir, project_name):
    """Create a manage.py file in the project directory"""
    manage_py_content = f'''#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # Add the current directory to the path
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    
    try:
        from fastapi_admin.cli import cli
    except ImportError:
        print("fastapi-admin package is not installed. Please install it with:")
        print("pip install fastapi-admin")
        sys.exit(1)
    
    cli()
'''

    manage_py_path = os.path.join(project_dir, "manage.py")
    file_utils.write_file(manage_py_path, manage_py_content)

    # Make manage.py executable
    file_utils.make_executable(manage_py_path)
