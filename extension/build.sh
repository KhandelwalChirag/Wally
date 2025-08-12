#!/bin/bash

# Frontend build script
echo "Building Smart Cart Builder Extension..."

# Install dependencies
echo "Installing dependencies..."
npm install

# Build the extension
echo "Building extension..."
npm run build

echo "Extension built successfully!"
echo "To load in Chrome:"
echo "1. Open Chrome and go to chrome://extensions/"
echo "2. Enable 'Developer mode'"
echo "3. Click 'Load unpacked' and select the 'extension' folder"