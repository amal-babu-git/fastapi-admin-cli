#!/usr/bin/env bash

# Test script for FastAPI Admin CLI commands
# This script exercises all the commands available in the CLI

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper function for section headers
section() {
    echo -e "\n${BLUE}======================================${NC}"
    echo -e "${BLUE}== $1${NC}"
    echo -e "${BLUE}======================================${NC}\n"
}

# Helper function for command execution with error handling
execute() {
    echo -e "${YELLOW}Executing:${NC} $1"
    if eval $1; then
        echo -e "${GREEN}✓ Command succeeded${NC}"
        return 0
    else
        echo -e "${RED}✗ Command failed with exit code $?${NC}"
        if [ "$2" != "continue" ]; then
            echo -e "${RED}Exiting script due to error${NC}"
            exit 1
        else
            echo -e "${YELLOW}Continuing despite error...${NC}"
            return 1
        fi
    fi
}

# Check if FastAPI Admin CLI is installed
check_installation() {
    section "Checking FastAPI Admin CLI Installation"

    echo -e "${YELLOW}Installing FastAPI Admin CLI...${NC}"
    execute "pip install -e ."
}

# Create a test project
create_project() {
    section "Creating Test Project"
    
    # Define project name
    PROJECT_NAME="testproject"
    
    # Remove existing test project if it exists
    if [ -d "$PROJECT_NAME" ]; then
        echo -e "${YELLOW}Removing existing test project...${NC}"
        execute "rm -rf $PROJECT_NAME" "continue"
    fi
    
    # Create new project
    execute "fastapi-admin startproject $PROJECT_NAME"
    
    # Check if project was created
    if [ ! -d "$PROJECT_NAME" ]; then
        echo -e "${RED}Project directory not found!${NC}"
        exit 1
    fi
    
    # Change to project directory
    cd "$PROJECT_NAME" || exit 1
    echo -e "${GREEN}Changed to directory: $(pwd)${NC}"
    
    # Examine project structure
    execute "ls -la" "continue"
}

# Docker build command
test_docker_build() {
    section "Testing Docker Build Command"
    
    # Docker build
    execute "fastapi-admin docker build" "continue"
}

# Docker run command
test_docker_run() {
    section "Testing Docker Run Command"
    
    # Docker run
    execute "fastapi-admin docker run" "continue"
}

# Test UV sync for dependencies
test_uv_sync() {
    section "Testing UV Sync for Dependencies"
    
    # Test uv virtual environment creation if uv is available
    if command -v uv > /dev/null; then
        execute "uv venv .venv" "continue"
        
        # Activate virtual environment (platform-dependent)
        if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
            execute "source .venv/Scripts/activate" "continue"
        else
            execute "source .venv/bin/activate" "continue"
        fi
        
        execute "uv sync" "continue"
    else
        echo -e "${YELLOW}uv not found, skipping uv venv and sync test${NC}"
        # Fall back to pip and standard venv if uv is not available
        execute "python -m venv .venv" "continue"
        
        # Activate virtual environment (platform-dependent)
        if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
            execute "source .venv/Scripts/activate" "continue"
        else
            execute "source .venv/bin/activate" "continue"
        fi
        
        execute "pip install -e ." "continue"
    fi
}

# Test database makemigrations
test_makemigrations() {
    section "Testing Database Makemigrations"
    
    # Make migrations
    execute "fastapi-admin db makemigrations -m 'initial migration'" "continue"
}

# Test database migrate
test_migrate() {
    section "Testing Database Migrate"
    
    # Apply migrations
    execute "fastapi-admin db migrate" "continue"
}

# Test creating a superuser
test_superuser() {
    section "Testing Superuser Creation"
    
    # Create a superuser (this may fail in automated testing if the container is not running, hence "continue")
    execute "fastapi-admin createsuperuser test@example.com password123" "continue"
    
    echo -e "${YELLOW}Note: Superuser creation requires a running container with database access${NC}"
    echo -e "${YELLOW}If these commands failed, ensure containers are running properly${NC}"
}

# Create a test app
create_app() {
    section "Creating Test App"
    
    # Create an app
    execute "fastapi-admin startapp users"
    
    # Examine app structure
    execute "ls -la app/users" "continue"
}

# Test shell access (non-blocking)
test_shell() {
    section "Testing Shell Access"
    
    echo -e "${YELLOW}Note: Shell access test is skipped in automated testing${NC}"
    echo -e "${YELLOW}To test manually, run: fastapi-admin shell${NC}"
    
    # In a real test, you might want to send commands to the shell
    # but for this test script, we'll skip actual execution since it's interactive
}

# Test local development setup
test_local_dev() {
    section "Testing Local Development Setup"
    
    # Copy environment variables
    execute "cp env.txt .env" "continue"
}

# Test typical development workflow
test_development_workflow() {
    section "Testing Typical Development Workflow"
    
    echo -e "${YELLOW}Demonstrating typical development workflow...${NC}"
    
    # Create second app for the workflow example
    execute "fastapi-admin startapp products" "continue"
    
    echo -e "${GREEN}✓ Typical development workflow commands executed${NC}"
}

# Cleanup function
cleanup() {
    section "Cleaning Up"
    
    # Change back to original directory
    execute "cd .." "continue"
    
    echo -e "${GREEN}Tests completed. Check above output for any errors.${NC}"
}

# Main test flow
main() {
    section "Starting FastAPI Admin CLI Test Suite"
    
    # Record start time
    start_time=$(date +%s)
    
    # Original directory
    orig_dir=$(pwd)
    
    # Run test functions in the requested order
    check_installation
    create_project
    test_docker_build
    test_docker_run
    test_uv_sync
    test_makemigrations
    test_migrate
    test_superuser
    create_app
    test_shell
    test_local_dev
    test_development_workflow
    
    # Return to original directory and cleanup
    cd "$orig_dir"
    cleanup
    
    # Calculate execution time
    end_time=$(date +%s)
    execution_time=$((end_time - start_time))
    echo -e "${GREEN}All tests completed in ${execution_time} seconds${NC}"
}

# Run the main function
main
