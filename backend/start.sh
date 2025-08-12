#!/bin/bash

# Backend startup script
echo "Starting Smart Cart Builder Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env file with your API keys before running the server"
    exit 1
fi

# Create user_data directory if it doesn't exist
mkdir -p user_data

# Start the server
echo "Starting FastAPI server..."
python main.py