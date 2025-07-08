#!/bin/bash
echo "Setting up Pagila MCP with Google GenAI..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start PostgreSQL with Docker
echo "Starting PostgreSQL database..."
docker compose up -d

echo "Setup complete!"
echo "To run the application:"
echo "1. source venv/bin/activate"
echo "2. python main.py"