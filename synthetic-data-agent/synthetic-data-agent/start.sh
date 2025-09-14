#!/bin/bash
echo "🚀 Starting Synthetic Data AI Agent..."
echo "📦 Building Docker container..."
docker-compose build

echo "🏃 Running container..."
docker-compose up -d

echo "✅ Agent is running!"
echo "🌐 Open your browser to: http://localhost:8080"
echo ""
echo "To stop the agent: docker-compose down"
echo "To view logs: docker-compose logs -f"
