#!/bin/bash
echo "🚀 Starting Synthetic Data AI Agent with File Upload..."
echo "📦 Building Docker container..."
docker-compose build --no-cache

echo "🏃 Running container..."
docker-compose up -d

echo "✅ Agent is running!"
echo "🌐 Open your browser to: http://localhost:8080"
echo ""
echo "🆕 NEW FEATURES:"
echo "  📁 File upload support (CSV, Excel, PDF)"
echo "  🧠 Pattern learning from your data"
echo "  📊 Statistical analysis"
echo "  🎯 Realistic synthetic data generation"
echo ""
echo "To stop: docker-compose down"
echo "To view logs: docker-compose logs -f"
