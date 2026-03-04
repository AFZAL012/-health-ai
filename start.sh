#!/bin/bash

echo "========================================"
echo "AI Health Symptom Analyzer - Quick Start"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Download spaCy model
echo "Downloading spaCy language model..."
python -m spacy download en_core_web_sm
echo ""

# Check if model exists
if [ ! -f "models/model.pkl" ]; then
    echo "Training ML model..."
    python train_model.py
    echo ""
fi

# Start the application
echo "Starting Flask application..."
echo ""
echo "Application will be available at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""
python app.py
