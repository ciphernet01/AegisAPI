#!/bin/bash
# Build and push Docker images to ECR

set -e

REGISTRY_URL=${ECR_REGISTRY:-localhost}
VERSION=${1:-latest}

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check Docker
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running"
    exit 1
fi

print_info "Building and pushing images (version: $VERSION)..."

# Build frontend
print_info "Building frontend image..."
docker build -t $REGISTRY_URL/aegis/frontend:$VERSION \
  -t $REGISTRY_URL/aegis/frontend:latest \
  -f devops/docker/Dockerfile.frontend \
  frontend/

# Build backend
print_info "Building backend image..."
docker build -t $REGISTRY_URL/aegis/backend:$VERSION \
  -t $REGISTRY_URL/aegis/backend:latest \
  -f devops/docker/Dockerfile.backend \
  backend/

print_info "Images built successfully"

# Push if registry is not localhost
if [ "$REGISTRY_URL" != "localhost" ]; then
    print_info "Pushing images to $REGISTRY_URL..."
    docker push $REGISTRY_URL/aegis/frontend:$VERSION
    docker push $REGISTRY_URL/aegis/frontend:latest
    docker push $REGISTRY_URL/aegis/backend:$VERSION
    docker push $REGISTRY_URL/aegis/backend:latest
    print_info "Images pushed successfully"
fi
