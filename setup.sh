#!/bin/bash

# Ticketing System Setup Script

set -e

echo "================================"
echo "Ticketing System Setup"
echo "================================"
echo ""

# Check for required tools
check_requirements() {
    echo "Checking requirements..."
    
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker compose &> /dev/null; then
        echo "❌ Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    echo "✅ All requirements met!"
    echo ""
}

# Create .env files
create_env_files() {
    echo "Creating environment files..."
    
    # Backend .env
    if [ ! -f backend/.env ]; then
        cp backend/.env.example backend/.env
        echo "✅ Created backend/.env (please update with your settings)"
    else
        echo "⚠️  backend/.env already exists, skipping..."
    fi
    
    # Frontend .env
    if [ ! -f frontend/.env ]; then
        echo "REACT_APP_API_URL=http://localhost:8000" > frontend/.env
        echo "✅ Created frontend/.env"
    else
        echo "⚠️  frontend/.env already exists, skipping..."
    fi
    
    echo ""
}

# Build and start services
start_services() {
    echo "Building Docker images..."
    docker compose build
    
    echo ""
    echo "Starting services..."
    docker compose up -d
    
    echo ""
    echo "Waiting for services to be ready..."
    sleep 10
    
    echo ""
    echo "✅ Services are starting!"
}

# Show status
show_status() {
    echo ""
    echo "================================"
    echo "Service Status"
    echo "================================"
    docker compose ps
    
    echo ""
    echo "================================"
    echo "Access Information"
    echo "================================"
    echo "🌐 Frontend: http://localhost:3000"
    echo "🔧 Backend API: http://localhost:8000"
    echo "📚 API Documentation: http://localhost:8000/docs"
    echo "🗄️  Database: localhost:5432"
    echo "📮 Redis: localhost:6379"
    echo ""
    echo "To view logs: docker compose logs -f"
    echo "To stop services: docker compose down"
    echo ""
}

# Main
main() {
    check_requirements
    create_env_files
    start_services
    show_status
}

main
