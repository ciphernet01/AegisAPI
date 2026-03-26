#!/bin/bash

# Docker Build and Run Script for Zombie API Platform

set -e

ENVIRONMENT=${1:-dev}
DOCKER_COMPOSE_FILE="docker-compose.${ENVIRONMENT}.yml"

echo "🚀 Building and starting Zombie API Platform in ${ENVIRONMENT} mode..."

if [ ! -f "devops/docker/${DOCKER_COMPOSE_FILE}" ]; then
    echo "❌ Error: ${DOCKER_COMPOSE_FILE} not found in devops/docker/"
    exit 1
fi

cd devops/docker

case "${ENVIRONMENT}" in
    dev)
        echo "📦 Development Mode: SQLite database, hot-reload enabled"
        docker-compose -f "${DOCKER_COMPOSE_FILE}" up --build
        ;;
    prod)
        echo "📦 Production Mode: PostgreSQL + Redis"
        if [ ! -f "../../.env" ]; then
            echo "❌ Error: .env file not found. Copy .env.example to .env and fill in values."
            exit 1
        fi
        docker-compose -f "${DOCKER_COMPOSE_FILE}" up --build -d
        echo "✅ Services started in background"
        echo "📊 Check logs: docker-compose -f ${DOCKER_COMPOSE_FILE} logs -f"
        ;;
    *)
        echo "❌ Invalid environment: ${ENVIRONMENT}"
        echo "Usage: ./docker-run.sh [dev|prod]"
        exit 1
        ;;
esac
