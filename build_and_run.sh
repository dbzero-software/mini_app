#!/bin/bash

# Build and Run Script for Mini App
# This script builds the Docker image and runs the Mini App container

set -e

# Configuration
IMAGE_NAME="mini_app"
CONTAINER_NAME="mini_app_container"
PORT=8080

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show help
show_help() {
    echo "Mini App Build and Run Script"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -b, --build    Build the Docker image only"
    echo "  -r, --run      Run the container only (assumes image exists)"
    echo "  -s, --stop     Stop and remove the running container"
    echo "  -l, --logs     Show container logs"
    echo "  -c, --clean    Remove container and image"
    echo ""
    echo "Default behavior (no options): Build image and run container"
    echo ""
    exit 0
}

# Function to check if DBZero package exists locally
check_dbzero_package() {
    if [ ! -f "packages/dbzeroce-0.0.1-cp311-cp311-linux_x86_64.whl" ]; then
        print_error "DBZero package not found in packages/ directory!"
        print_error "Please copy the DBZero wheel file:"
        print_error "  cp ../selltime/packages/dbzeroce-0.0.1-cp311-cp311-linux_x86_64.whl packages/"
        exit 1
    fi
    print_success "DBZero package found in packages/ directory"
}

# Function to build the Docker image
build_image() {
    print_status "Building Mini App Docker image..."
    
    # Check if DBZero package exists
    check_dbzero_package
    
    if docker build -t $IMAGE_NAME .; then
        print_success "Docker image '$IMAGE_NAME' built successfully"
    else
        print_error "Failed to build Docker image"
        exit 1
    fi
}

# Function to stop and remove existing container
stop_container() {
    if docker ps -a | grep -q $CONTAINER_NAME; then
        print_status "Stopping and removing existing container..."
        docker stop $CONTAINER_NAME 2>/dev/null || true
        docker rm $CONTAINER_NAME 2>/dev/null || true
        print_success "Container stopped and removed"
    fi
}

# Function to run the container
run_container() {
    print_status "Starting Mini App container..."
    
    # Stop existing container if running
    stop_container
    
    # Check if image exists
    if ! docker images | grep -q $IMAGE_NAME; then
        print_error "Docker image '$IMAGE_NAME' not found. Please build it first."
        exit 1
    fi
    
    # Run the container
    if docker run -d \
        --name $CONTAINER_NAME \
        -p $PORT:8080 \
        $IMAGE_NAME; then
        print_success "Container '$CONTAINER_NAME' started successfully"
        print_success "Mini App is running at: http://localhost:$PORT"
        print_success "API Documentation: http://localhost:$PORT/docs"
        print_success "Health Check: http://localhost:$PORT/healthcheck"
        
        # Wait a moment and check if container is still running
        sleep 3
        if docker ps | grep -q $CONTAINER_NAME; then
            print_success "Container is running healthy"
        else
            print_error "Container failed to start properly"
            print_error "Check logs with: $0 --logs"
            exit 1
        fi
    else
        print_error "Failed to start container"
        exit 1
    fi
}

# Function to show logs
show_logs() {
    if docker ps -a | grep -q $CONTAINER_NAME; then
        print_status "Showing container logs..."
        docker logs -f $CONTAINER_NAME
    else
        print_error "Container '$CONTAINER_NAME' not found"
        exit 1
    fi
}

# Function to clean up
clean_up() {
    print_status "Cleaning up Mini App resources..."
    
    # Stop and remove container
    stop_container
    
    # Remove image
    if docker images | grep -q $IMAGE_NAME; then
        print_status "Removing Docker image..."
        docker rmi $IMAGE_NAME
        print_success "Docker image removed"
    fi
    
    # Remove volume
    if docker volume ls | grep -q mini_app_data; then
        print_status "Removing data volume..."
        docker volume rm mini_app_data 2>/dev/null || true
        print_success "Data volume removed"
    fi
    
    print_success "Cleanup completed"
}

# Parse command line arguments
case "${1:-}" in
    -h|--help)
        show_help
        ;;
    -b|--build)
        build_image
        ;;
    -r|--run)
        run_container
        ;;
    -s|--stop)
        stop_container
        ;;
    -l|--logs)
        show_logs
        ;;
    -c|--clean)
        clean_up
        ;;
    "")
        # Default behavior: build and run
        print_status "Building and running Mini App..."
        build_image
        run_container
        ;;
    *)
        print_error "Unknown option: $1"
        echo "Use -h or --help for usage information"
        exit 1
        ;;
esac
