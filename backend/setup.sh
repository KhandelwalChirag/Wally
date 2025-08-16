#!/bin/bash

# Create a virtual environment using uv
uv venv

# Activate the virtual environment
source .venv/bin/activate

# Install the packages using uv
uv pip install -r requirements.txt

echo "Setup complete. You can now run the application with 'sh run.sh'"