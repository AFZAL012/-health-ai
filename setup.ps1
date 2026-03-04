# Setup script for Medical Diagnosis Enhancement System (Windows PowerShell)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Medical Diagnosis Enhancement Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed. Please install Python 3.11 or higher." -ForegroundColor Red
    exit 1
}

# Check Node.js
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js is not installed. Please install Node.js 18 or higher." -ForegroundColor Red
    exit 1
}

# Check Docker
try {
    $dockerVersion = docker --version
    Write-Host "✓ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not installed. Please install Docker Desktop." -ForegroundColor Red
    exit 1
}

# Check Docker Compose
try {
    $composeVersion = docker-compose --version
    Write-Host "✓ Docker Compose found: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose is not installed. Please install Docker Compose." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "All prerequisites met!" -ForegroundColor Green
Write-Host ""

# Setup environment file
if (-not (Test-Path .env)) {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "✓ .env file created. Please edit it with your configuration." -ForegroundColor Green
} else {
    Write-Host "✓ .env file already exists." -ForegroundColor Green
}

# Start Docker services
Write-Host ""
Write-Host "Starting Docker services (PostgreSQL and Redis)..." -ForegroundColor Yellow
docker-compose up -d

Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host "✓ Docker services started" -ForegroundColor Green

# Setup backend
Write-Host ""
Write-Host "Setting up backend..." -ForegroundColor Yellow
Set-Location backend

if (-not (Test-Path venv)) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
}

Write-Host "Activating virtual environment and installing dependencies..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host "Installing Python packages..." -ForegroundColor Yellow
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host "Downloading spaCy model..." -ForegroundColor Yellow
python -m spacy download en_core_web_sm

Write-Host "✓ Backend setup complete" -ForegroundColor Green

Set-Location ..

# Setup frontend
Write-Host ""
Write-Host "Setting up frontend..." -ForegroundColor Yellow
Set-Location frontend

if (-not (Test-Path node_modules)) {
    Write-Host "Installing Node.js packages..." -ForegroundColor Yellow
    npm install
    Write-Host "✓ Frontend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✓ Node.js packages already installed" -ForegroundColor Green
}

Set-Location ..

# Create necessary directories
Write-Host ""
Write-Host "Creating necessary directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path logs | Out-Null
New-Item -ItemType Directory -Force -Path reports | Out-Null
Write-Host "✓ Directories created" -ForegroundColor Green

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Setup Complete! 🎉" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env file with your configuration"
Write-Host "2. Start the backend:"
Write-Host "   cd backend"
Write-Host "   .\venv\Scripts\Activate.ps1"
Write-Host "   python app.py"
Write-Host ""
Write-Host "3. In a new terminal, start the frontend:"
Write-Host "   cd frontend"
Write-Host "   npm run dev"
Write-Host ""
Write-Host "4. Access the application:"
Write-Host "   Backend: http://localhost:5000"
Write-Host "   Frontend: http://localhost:5173"
Write-Host ""
Write-Host "For more information, see README.md"
