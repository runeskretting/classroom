#!/bin/bash
# Python Classroom - Quick Start Script

echo "🐍 Python Classroom - Starting Application"
echo "========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade requirements
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Create necessary directories
echo "Ensuring data directories exist..."
mkdir -p data/submissions/module1
mkdir -p data/submissions/module2
mkdir -p data/submissions/module3

# Start the application
echo ""
echo "========================================="
echo "✓ Setup complete!"
echo "Starting Flask application..."
echo "Access the app at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo "========================================="
echo ""

python app.py
