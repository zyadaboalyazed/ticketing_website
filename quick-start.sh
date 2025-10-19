#!/bin/bash

# Quick Start Script for Ticketing System
# This script sets up the development environment

set -e

echo "🎫 Ticketing System - Quick Start Setup"
echo "======================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Setup backend environment
echo "📝 Setting up backend environment..."
if [ ! -f "backend/.env" ]; then
    cp backend/.env.example backend/.env
    # Generate a random secret key
    if command -v openssl &> /dev/null; then
        SECRET_KEY=$(openssl rand -hex 32)
        sed -i.bak "s/your-secret-key-change-this-in-production/$SECRET_KEY/" backend/.env
        rm backend/.env.bak
        echo "   ✅ Generated secure SECRET_KEY"
    else
        echo "   ⚠️  Please set a secure SECRET_KEY in backend/.env"
    fi
else
    echo "   ✅ Backend .env already exists"
fi

# Setup frontend environment
echo "📝 Setting up frontend environment..."
if [ ! -f "frontend/.env" ]; then
    cp frontend/.env.example frontend/.env
    echo "   ✅ Created frontend .env"
else
    echo "   ✅ Frontend .env already exists"
fi

echo ""
echo "🐳 Starting Docker containers..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check service status
echo ""
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Access the application:"
echo "   Frontend:   http://localhost"
echo "   Backend:    http://localhost:8000"
echo "   API Docs:   http://localhost:8000/docs"
echo ""
echo "📚 Next steps:"
echo "   1. Open http://localhost in your browser"
echo "   2. Register a new account (select your role)"
echo "   3. Start creating tickets!"
echo ""
echo "🛠️  Useful commands:"
echo "   View logs:       docker-compose logs -f"
echo "   Stop services:   docker-compose stop"
echo "   Start services:  docker-compose start"
echo "   Clean up:        docker-compose down -v"
echo ""
