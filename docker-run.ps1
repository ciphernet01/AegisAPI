# Docker Build and Run Script for Zombie API Platform (Windows)

param(
    [Parameter(Mandatory=$false)]
    [string]$Environment = "dev",
    [switch]$Detach,
    [switch]$Logs,
    [switch]$Stop,
    [switch]$Down
)

$DOCKER_COMPOSE_FILE = "docker-compose.$Environment.yml"
$COMPOSE_PATH = "devops\docker"
$DOCKER_COMPOSE_PATH = "$COMPOSE_PATH\$DOCKER_COMPOSE_FILE"

Write-Host "🚀 Zombie API Platform - Docker Manager (Windows)" -ForegroundColor Cyan
Write-Host "Environment: $Environment" -ForegroundColor Yellow

# Check if compose file exists
if (-not (Test-Path $DOCKER_COMPOSE_PATH)) {
    Write-Host "❌ Error: $DOCKER_COMPOSE_FILE not found in $COMPOSE_PATH" -ForegroundColor Red
    exit 1
}

Push-Location $COMPOSE_PATH

try {
    if ($Stop) {
        Write-Host "⛔ Stopping services..." -ForegroundColor Yellow
        docker-compose -f $DOCKER_COMPOSE_FILE stop
        exit 0
    }

    if ($Down) {
        Write-Host "🗑️  Removing all services and volumes..." -ForegroundColor Yellow
        docker-compose -f $DOCKER_COMPOSE_FILE down -v
        Write-Host "✅ All services removed" -ForegroundColor Green
        exit 0
    }

    if ($Logs) {
        Write-Host "📋 Showing logs..." -ForegroundColor Yellow
        docker-compose -f $DOCKER_COMPOSE_FILE logs -f
        exit 0
    }

    switch ($Environment) {
        "dev" {
            Write-Host "📦 Development Mode: SQLite database, hot-reload enabled" -ForegroundColor Cyan
            if ($Detach) {
                docker-compose -f $DOCKER_COMPOSE_FILE up --build -d
                Write-Host "✅ Services started in background" -ForegroundColor Green
                Write-Host "Frontend: http://localhost:3000" -ForegroundColor Green
                Write-Host "Backend: http://localhost:5000" -ForegroundColor Green
                Write-Host "Logs: docker-compose -f $DOCKER_COMPOSE_FILE logs -f" -ForegroundColor Blue
            } else {
                docker-compose -f $DOCKER_COMPOSE_FILE up --build
            }
        }

        "prod" {
            Write-Host "📦 Production Mode: PostgreSQL + Redis" -ForegroundColor Cyan
            if (-not (Test-Path "..\..\..\.env")) {
                Write-Host "❌ Error: .env file not found" -ForegroundColor Red
                Write-Host "Copy .env.example to .env and fill in required values" -ForegroundColor Yellow
                exit 1
            }
            docker-compose -f $DOCKER_COMPOSE_FILE up --build -d
            Write-Host "✅ Services started in background" -ForegroundColor Green
            Write-Host "Frontend: http://localhost:3000" -ForegroundColor Green
            Write-Host "Backend: http://localhost:8000" -ForegroundColor Green
        }

        default {
            Write-Host "❌ Invalid environment: $Environment" -ForegroundColor Red
            Write-Host "Usage: .\docker-run.ps1 -Environment [dev|prod] [-Detach] [-Logs] [-Stop] [-Down]" -ForegroundColor Yellow
            exit 1
        }
    }

    Write-Host "✅ Operation completed" -ForegroundColor Green

} finally {
    Pop-Location
}
