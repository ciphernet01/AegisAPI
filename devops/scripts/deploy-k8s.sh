#!/bin/bash
# Deploy to Kubernetes cluster

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"
K8S_DIR="$PROJECT_ROOT/devops/kubernetes"

# Configuration
ENVIRONMENT=${1:-staging}
NAMESPACE=aegis
REGISTRY_URL=${ECR_REGISTRY:-localhost}

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
print_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

main() {
    print_info "Deploying to Kubernetes ($ENVIRONMENT)"
    
    # Check kubectl
    if ! command -v kubectl &> /dev/null; then
        print_error "kubectl is not installed"
        exit 1
    fi
    
    # Check cluster connection
    if ! kubectl cluster-info > /dev/null 2>&1; then
        print_error "Cannot connect to Kubernetes cluster"
        exit 1
    fi
    
    print_info "Connected to cluster: $(kubectl config current-context)"
    
    # Create namespace if not exists
    kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
    print_info "Namespace '$NAMESPACE' ensured"
    
    # Apply configurations
    print_info "Applying Kubernetes manifests..."
    kubectl apply -f "$K8S_DIR/deployment.yaml"
    kubectl apply -f "$K8S_DIR/cronjobs.yaml"
    kubectl apply -f "$K8S_DIR/policies.yaml"
    
    # Wait for deployments
    print_info "Waiting for deployments to be ready..."
    kubectl rollout status deployment/frontend -n $NAMESPACE --timeout=5m
    kubectl rollout status deployment/backend -n $NAMESPACE --timeout=5m
    
    print_info "Deployment successful!"
    print_info "Check status with: kubectl get all -n $NAMESPACE"
}

main
