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
    
    if command -v fastapi-admin > /dev/null; then
        echo -e "${GREEN}FastAPI Admin CLI is already installed${NC}"
    else
        echo -e "${YELLOW}Installing FastAPI Admin CLI...${NC}"
        execute "pip install -e ." "continue"
        
        if ! command -v fastapi-admin > /dev/null; then
            echo -e "${RED}Failed to install FastAPI Admin CLI${NC}"
            exit 1
        fi
    fi
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
    
    # Test uv sync if uv is available
    if command -v uv > /dev/null; then
        execute "uv sync" "continue"
    else
        echo -e "${YELLOW}uv not found, skipping uv sync test${NC}"
        # Fall back to pip if uv is not available
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

# Create a test app
create_app() {
    section "Creating Test App"
    
    # Create an app
    execute "fastapi-admin startapp users"
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
    
    # Create virtual environment 
    execute "python -m venv venv" "continue"
    
    # Activate virtual environment (platform-dependent)
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        execute "source venv/Scripts/activate" "continue"
    else
        execute "source venv/bin/activate" "continue"
    fi
    
    # Copy environment variables
    execute "cp env.txt .env" "continue"
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
    create_app
    test_shell
    test_local_dev
    
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
