#!/bin/bash

# Deployment script for chatbot application
# Usage: ./deploy.sh [tag]
# Example: ./deploy.sh v1.0.0

set -e  # Exit on any error

# Configuration
DOCKER_USERNAME="your-dockerhub-username"  # Replace with your Docker Hub username
IMAGE_NAME="chatbot-app"
DEFAULT_TAG="latest"

# Get tag from argument or use default
TAG=${1:-$DEFAULT_TAG}
FULL_IMAGE_NAME="$DOCKER_USERNAME/$IMAGE_NAME:$TAG"

echo "🚀 Starting deployment process for $FULL_IMAGE_NAME"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check required tools
echo "🔍 Checking required tools..."
if ! command_exists docker; then
    echo "❌ Docker is not installed"
    exit 1
fi

if ! command_exists npm; then
    echo "❌ npm is not installed"
    exit 1
fi

echo "✅ All required tools are available"

# Build frontend
echo "🏗️  Building frontend..."
cd frontend
npm ci
npm run build
cd ..

# Build Docker image
echo "🐳 Building Docker image..."
docker build -t $FULL_IMAGE_NAME .

# Test the image locally (optional)
echo "🧪 Testing image locally..."
docker run --rm -d --name test-container -p 8001:8000 $FULL_IMAGE_NAME
sleep 10

# Test health check
if curl -f http://localhost:8001/api/health >/dev/null 2>&1; then
    echo "✅ Health check passed"
else
    echo "⚠️  Health check failed, but continuing with deployment"
fi

# Stop test container
docker stop test-container

# Push to Docker Hub
echo "📤 Pushing to Docker Hub..."
docker push $FULL_IMAGE_NAME

echo "✅ Deployment completed successfully!"
echo "📋 Image pushed: $FULL_IMAGE_NAME"
echo ""
echo "🖥️  To deploy on VPS, run:"
echo "   ssh your-server"
echo "   docker pull $FULL_IMAGE_NAME"
echo "   docker-compose down"
echo "   docker-compose up -d"
