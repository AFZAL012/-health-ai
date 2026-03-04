#!/bin/bash
# Setup script for Medical Diagnosis Enhancement System

set -e

echo "=========================================="
echo "Medical Diagnosis Enhancement Setup"
echo "=========================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi
echo "✓ Python 3 found: $(python3 --version)"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi
echo "✓ Node.js found: $(node --version)"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker."
    exit 1
fi
echo "✓ Docker found: $(docker --version)"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose."
    exit 1
fi
echo "✓ Docker Compose found: $(docker-compose --version)"

echo ""
echo "All prerequisites met!"
echo ""

# Setup environment file
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created. Please edit it with your configuration."
else
    echo "✓ .env file already exists."
fi

# Start Docker services
echo ""
echo "Starting Docker services (PostgreSQL and Redis)..."
docker-compose up -d

echo "Waiting for services to be ready..."
sleep 5

# Check if services are healthy
if docker-compose ps | grep -q "healthy"; then
    echo "✓ Docker services are running and healthy"
else
    echo "⚠ Docker services started but may not be fully ready yet"
fi

# Setup backend
echo ""
echo "Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo "Activating virtual environment and installing dependencies..."
source venv/bin/activate

echo "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Downloading spaCy model..."
python -m spacy download en_core_web_sm

echo "✓ Backend setup complete"

cd ..

# Setup frontend
echo ""
echo "Setting up frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node.js packages..."
    npm install
    echo "✓ Frontend dependencies installed"
else
    echo "✓ Node.js packages already installed"
fi

cd ..

# Create necessary directories
echo ""
echo "Creating necessary directories..."
mkdir -p backend/logs
mkdir -p backend/reports
echo "✓ Directories created"

echo ""
echo "=========================================="
echo "Setup Complete! 🎉"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Start the backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python app.py"
echo ""
echo "3. In a new terminal, start the frontend:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4. Access the application:"
echo "   Backend: http://localhost:5000"
echo "   Frontend: http://localhost:5173"
echo ""
echo "For more information, see README.md"
