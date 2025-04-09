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

    # Create a Python script with the exact implementation provided
    script = """
import asyncio
import uuid
import logging
from typing import Optional

try:
    # Try to import from the expected module structure
    from app.core.db import async_session_factory
    from app.auth.models import User
except ImportError:
    try:
        # Fall back to alternative module structures
        from app.database import async_session_factory
        from app.models import User
    except ImportError:
        print("ERROR: Could not import required modules. Check your project structure.")
        exit(1)

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_superuser(
    email: str, 
    password: str, 
    first_name: Optional[str] = None, 
    last_name: Optional[str] = None
) -> None:
    \"\"\"
    Create a superuser account for admin panel access.
    
    Args:
        email: Email address for the superuser
        password: Password for the superuser
        first_name: Optional first name
        last_name: Optional last name
    \"\"\"
    from fastapi_users.password import PasswordHelper
    password_helper = PasswordHelper()
    
    print(f"Creating superuser with email: {email}")
    
    async with async_session_factory() as session:
        try:
            # Try ORM approach first (SQLAlchemy models)
            from sqlalchemy import select
            
            # Check if user exists
            stmt = select(User).where(User.email == email)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            
            if user:
                print(f"User with email {email} already exists.")
                
                # Update to superuser if needed
                if not user.is_superuser:
                    user.is_superuser = True
                    user.is_verified = True
                    await session.commit()
                    print(f"Updated user {email} to superuser.")
                return
            
            # Hash the password
            hashed_password = password_helper.hash(password)
            
            # Create new superuser
            user_id = uuid.uuid4() if hasattr(User, 'id') and isinstance(getattr(User, 'id').type, uuid.UUID) else None
            
            user = User(
                id=user_id,
                email=email,
                hashed_password=hashed_password,
                is_active=True,
                is_superuser=True,
                is_verified=True
            )
            
            # Add optional fields if they exist on the model
            if hasattr(User, 'first_name') and first_name:
                user.first_name = first_name
            if hasattr(User, 'last_name') and last_name:
                user.last_name = last_name
                
            session.add(user)
            await session.commit()
            print(f"Superuser {email} created successfully!")
            
        except Exception as e:
            # Fall back to raw SQL if ORM approach fails
            print(f"ORM approach failed, trying with raw SQL: {str(e)}")
            
            try:
                # Check if user exists
                result = await session.execute("SELECT * FROM users WHERE email = :email", {"email": email})
                user = result.fetchone()
                
                if user:
                    print(f"User with email {email} already exists.")
                    
                    # Update to superuser if needed
                    if not getattr(user, 'is_superuser', False):
                        await session.execute(
                            "UPDATE users SET is_superuser = TRUE, is_verified = TRUE WHERE email = :email",
                            {"email": email}
                        )
                        await session.commit()
                        print(f"Updated user {email} to superuser.")
                    return
                
                # Hash the password
                hashed_password = password_helper.hash(password)
                
                # Create new superuser with UUID
                user_id = uuid.uuid4()
                
                # Insert the new user
                await session.execute(
                    \"\"\"
                    INSERT INTO users (
                        id, email, hashed_password, is_active, 
                        is_superuser, is_verified, first_name, last_name
                    ) VALUES (
                        :id, :email, :hashed_password, TRUE,
                        TRUE, TRUE, :first_name, :last_name
                    )
                    \"\"\",
                    {
                        "id": str(user_id),
                        "email": email,
                        "hashed_password": hashed_password,
                        "first_name": first_name,
                        "last_name": last_name
                    }
                )
                
                await session.commit()
                print(f"Superuser {email} created successfully!")
            except Exception as inner_e:
                print(f"Error creating superuser: {str(inner_e)}")
                raise

# Execute the async function with the provided parameters
if __name__ == "__main__":
    email = "{email}"
    password = "{password}"
    first_name = {repr(first_name)}
    last_name = {repr(last_name)}
    
    asyncio.run(create_superuser(email, password, first_name, last_name))
"""

    # Create a temporary file in the container
    temp_file = "/tmp/create_superuser.py"
    setup_cmd = f"cat > {temp_file} << 'EOF'\n{script}\nEOF"

    # Build the command to run the script
    run_cmd = f"python {temp_file}"

    # Full command: setup the script then run it
    full_cmd = f"{setup_cmd} && {run_cmd}"

    # Execute the command in the container
    try:
        # Support both docker-compose and docker compose syntax
        docker_cmd = "docker-compose"
        try:
            subprocess.run(["docker-compose", "--version"],
                           check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            docker_cmd = "docker compose"

        result = subprocess.run(
            f"{docker_cmd} -f docker/compose/docker-compose.yml run --rm api sh -c '{full_cmd}'",
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )

        # Check for any output messages
        if result.stdout:
            console.print(result.stdout)

    except subprocess.CalledProcessError as e:
        # Handle environment variable warnings
        if "variable is not set. Defaulting to a blank string" in e.stderr:
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

        console.print(Panel(
            f"[bold red]Failed to create superuser:[/]\n\n"
            f"[bold white]STDOUT:[/]\n{e.stdout if e.stdout else 'No output'}\n\n"
            f"[bold white]STDERR:[/]\n{e.stderr if e.stderr else 'No output'}",
            title="Error Details",
            border_style="red"
        ))
        raise Exception(
            f"Failed to create superuser. See error details above.")

    # Return success
    return True
