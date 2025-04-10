#!/usr/bin/env bash

# Demo Script for FastAPI Admin CLI
# This script simulates commands being typed slowly for a demonstration

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Timing settings
TYPE_SPEED=0.1
PAUSE_SHORT=2
PAUSE_MEDIUM=4
PAUSE_LONG=6

# Helper function for slow typing simulation
slow_type() {
    text="$1"
    echo -n "$ "
    for (( i=0; i<${#text}; i++ )); do
        echo -n "${text:$i:1}"
        sleep $TYPE_SPEED
    done
    echo ""
    sleep $PAUSE_SHORT
    eval "$text"
    sleep $PAUSE_MEDIUM
}

# Helper function for section headers
section() {
    echo -e "\n${BLUE}======================================${NC}"
    echo -e "${BLUE}== $1${NC}"
    echo -e "${BLUE}======================================${NC}\n"
    sleep $PAUSE_SHORT
}

# Clear terminal and show welcome message
clear_and_welcome() {
    clear
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                                                          ║"
    echo "║           FastAPI Admin CLI Demonstration                ║"
    echo "║                                                          ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    sleep $PAUSE_MEDIUM
    
    echo -e "${YELLOW}This demonstration will show how to use FastAPI Admin CLI to:${NC}"
    echo -e " ${GREEN}•${NC} Install the package"
    echo -e " ${GREEN}•${NC} Create a new project"
    echo -e " ${GREEN}•${NC} Create apps within the project"
    echo -e " ${GREEN}•${NC} Use Docker integration"
    echo -e " ${GREEN}•${NC} Set up database migrations"
    echo -e " ${GREEN}•${NC} Configure local development"
    sleep $PAUSE_LONG
}

# Demo steps
demo_installation() {
    section "Installation"
    
    echo -e "Let's start by installing FastAPI Admin CLI using pip:"
    sleep $PAUSE_SHORT
    
    slow_type "pip install fastapi-admin-cli"
    
    echo -e "${GREEN}✓${NC} FastAPI Admin CLI has been installed successfully!"
    sleep $PAUSE_MEDIUM
}

demo_create_project() {
    section "Creating a New Project"
    
    echo -e "Now, let's create a new FastAPI project:"
    sleep $PAUSE_SHORT
    
    # Define project name
    PROJECT_NAME="demoproject"
    
    # Remove existing project if it exists
    if [ -d "$PROJECT_NAME" ]; then
        echo -e "${YELLOW}Removing existing project for demo...${NC}"
        rm -rf "$PROJECT_NAME"
    fi
    
    slow_type "fastapi-admin startproject $PROJECT_NAME"
    
    echo -e "${GREEN}✓${NC} Project created successfully!"
    
    echo -e "\nExploring the project structure:"
    slow_type "ls -la $PROJECT_NAME"
    
    echo -e "\nLet's navigate to the project directory:"
    slow_type "cd $PROJECT_NAME"
}

demo_docker_setup() {
    section "Docker Integration"
    
    echo -e "FastAPI Admin CLI includes Docker integration for easy deployment."
    echo -e "Let's build the Docker container:"
    sleep $PAUSE_SHORT
    
    slow_type "fastapi-admin docker build"
    
    echo -e "\nNow, let's run the container:"
    slow_type "fastapi-admin docker run"
    
    echo -e "${GREEN}✓${NC} Docker container is now running!"
    sleep $PAUSE_SHORT
}

demo_database_migrations() {
    section "Database Migrations"
    
    echo -e "FastAPI Admin CLI provides easy database management with Alembic."
    echo -e "Let's create our initial migration:"
    sleep $PAUSE_SHORT
    
    slow_type "fastapi-admin db makemigrations -m 'initial migration'"
    
    echo -e "\nNow, let's apply the migration:"
    slow_type "fastapi-admin db migrate"
    
    echo -e "${GREEN}✓${NC} Database is now set up with initial migration!"
    sleep $PAUSE_SHORT
}

demo_superuser() {
    section "Creating a Superuser"
    
    echo -e "FastAPI Admin CLI allows you to create a superuser for the admin panel."
    echo -e "Let's create a superuser with email and password:"
    sleep $PAUSE_SHORT
    
    slow_type "fastapi-admin createsuperuser admin@example.com securepassword123"
    
    echo -e "${GREEN}✓${NC} Superuser created successfully!"
    sleep $PAUSE_SHORT
    
    echo -e "\nYou can also add more details like first name and last name:"
    slow_type "fastapi-admin createsuperuser admin2@example.com password123 --first-name Admin --last-name User"
    
    echo -e "${GREEN}✓${NC} Second superuser created with additional details!"
    sleep $PAUSE_SHORT
    
    echo -e "\nThis user can now access the admin interface at '/admin' with these credentials."
    sleep $PAUSE_MEDIUM
}

demo_create_app() {
    section "Creating a New App"
    
    echo -e "Now, let's create a new app module within our project:"
    sleep $PAUSE_SHORT
    
    slow_type "fastapi-admin startapp users"
    
    echo -e "${GREEN}✓${NC} The users app has been created!"
    sleep $PAUSE_SHORT
    
    echo -e "\nExploring the app structure:"
    slow_type "ls -la app/users"
}

demo_local_development() {
    section "Local Development Setup"
    
    echo -e "For local development without Docker, let's set up a virtual environment using uv:"
    sleep $PAUSE_SHORT
    
    slow_type "uv venv .venv"
    
    echo -e "\nActivate the virtual environment:"
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        slow_type "source .venv/Scripts/activate"
    else
        slow_type "source .venv/bin/activate"
    fi
    
    echo -e "\nSet up the environment variables:"
    slow_type "cp env.txt .env"
    
    echo -e "\nInstall dependencies using uv sync:"
    slow_type "uv sync"
    
    echo -e "${GREEN}✓${NC} Local development environment is set up with uv!"
    sleep $PAUSE_SHORT
}

demo_workflow() {
    section "Typical Development Workflow"
    
    echo -e "A typical development workflow with FastAPI Admin CLI looks like this:"
    sleep $PAUSE_SHORT
    
    echo -e "${YELLOW}1. Create a project${NC}"
    echo -e "   $ fastapi-admin startproject myproject"
    
    echo -e "\n${YELLOW}2. Navigate to the project${NC}"
    echo -e "   $ cd myproject"
    
    echo -e "\n${YELLOW}3. Set up Docker containers${NC}"
    echo -e "   $ fastapi-admin docker build"
    echo -e "   $ fastapi-admin docker run"
    
    echo -e "\n${YELLOW}4. Create apps for different features${NC}"
    echo -e "   $ fastapi-admin startapp users"
    echo -e "   $ fastapi-admin startapp products"
    
    echo -e "\n${YELLOW}5. Create and apply database migrations${NC}"
    echo -e "   $ fastapi-admin db makemigrations"
    echo -e "   $ fastapi-admin db migrate"
    
    echo -e "\n${YELLOW}6. Create a superuser for the admin panel${NC}"
    echo -e "   $ fastapi-admin createsuperuser admin@example.com password123"
    
    echo -e "\n${YELLOW}7. Access shell for database operations${NC}"
    echo -e "   $ fastapi-admin shell"
    
    sleep $PAUSE_LONG
}

# Main demo flow
main_demo() {
    # Welcome message
    clear_and_welcome
    
    # Run demo sections
    demo_installation
    demo_create_project
    demo_docker_setup
    demo_database_migrations
    demo_superuser
    demo_create_app
    demo_local_development
    demo_workflow
    
    # Return to original directory
    if [ -n "$PROJECT_NAME" ] && [ -d "$PROJECT_NAME" ]; then
        slow_type "cd .."
    fi
    
    # Completion message
    section "Demo Completed"
    echo -e "${GREEN}You've now seen how to use FastAPI Admin CLI!${NC}"
    echo -e "Check out the documentation for more details:"
    echo -e "${CYAN}https://github.com/amal-babu-git/fastapi-admin-cli${NC}"
    sleep $PAUSE_LONG
}

# Run the demo
main_demo
