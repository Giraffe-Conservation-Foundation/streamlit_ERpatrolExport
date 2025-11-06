#!/bin/bash
# Linux/Mac Quick Start Script for Patrol Shapefile Downloader

echo "========================================"
echo "Patrol Shapefile Downloader Setup"
echo "========================================"
echo ""

# Check Python installation
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from python.org"
    exit 1
fi
python3 --version
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Install requirements
echo "Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo ""

# Test setup
echo "Testing setup..."
python test_setup.py
echo ""

# Ask to run app
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
read -p "Do you want to run the app now? (y/n): " run_app
if [ "$run_app" = "y" ] || [ "$run_app" = "Y" ]; then
    echo ""
    echo "Starting Streamlit app..."
    echo "Press Ctrl+C to stop the server"
    echo ""
    streamlit run app.py
else
    echo ""
    echo "To run the app later, use:"
    echo "  source venv/bin/activate"
    echo "  streamlit run app.py"
    echo ""
fi
