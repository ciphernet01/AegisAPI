#!/bin/bash
# Deployment script for local development using Docker Compose

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"
DEVOPS_DIR="$PROJECT_ROOT/devops"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker."
        exit 1
    fi
    print_info "Docker is running"
}

# Check if Docker Compose is installed
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install it."
        exit 1
    fi
    print_info "Docker Compose is installed"
}

# Create environment file if it doesn't exist
setup_env() {
    if [ ! -f "$DEVOPS_DIR/docker/.env" ]; then
        print_info "Creating .env file from .env.example"
        cat > "$DEVOPS_DIR/docker/.env" << EOF
DB_USER=aegisdb
DB_PASSWORD=changeme
DB_NAME=aegis_api
API_ENV=development
ALLOW_ORIGINS=http://localhost:3000
GRAFANA_PASSWORD=admin
EOF
        print_warn "Please update .env with secure credentials"
    fi
}

# Build images
build_images() {
    print_info "Building Docker images..."
    cd "$DEVOPS_DIR/docker"
    docker-compose build
    print_info "Images built successfully"
}

# Start services
start_services() {
    print_info "Starting services with Docker Compose..."
    cd "$DEVOPS_DIR/docker"
    docker-compose up -d
    print_info "Services started"
}

# Wait for services to be ready
wait_services() {
    print_info "Waiting for services to be ready..."
    
    # Wait for backend
    for i in {1..30}; do
        if docker-compose exec -T backend curl -f http://localhost:8000/health > /dev/null 2>&1; then
            print_info "Backend is ready"
            break
        fi
        echo "Waiting for backend... ($i/30)"
        sleep 2
    done
    
    # Wait for frontend
    for i in {1..30}; do
        if docker-compose exec -T frontend curl -f http://localhost:3000 > /dev/null 2>&1; then
            print_info "Frontend is ready"
            break
        fi
        echo "Waiting for frontend... ($i/30)"
        sleep 2
    done
}

# Display service URLs
print_urls() {
    echo ""
    echo "=========================================="
    print_info "Services are running at:"
    echo "=========================================="
    echo "Frontend Dashboard: http://localhost:3000"
    echo "Backend API:        http://localhost:8000"
    echo "Security Engine:    http://localhost:8001"
    echo "Prometheus:         http://localhost:9090"
    echo "Grafana:            http://localhost:3001 (admin/admin)"
    echo "PostgreSQL:         localhost:5432"
    echo "Redis:              localhost:6379"
    echo "=========================================="
    echo ""
}

# Main execution
main() {
    print_info "Starting AegisAPI local deployment..."
    
    check_docker
    check_docker_compose
    setup_env
    build_images
    start_services
    wait_services
    print_urls
    
    print_info "Deployment complete! Run 'docker-compose logs -f' to view logs"
}

# Run main function
main
