.PHONY: help setup start-services stop-services backend-install frontend-install test clean

help:
	@echo "Medical Diagnosis Enhancement System - Make Commands"
	@echo ""
	@echo "Setup Commands:"
	@echo "  make setup              - Complete project setup"
	@echo "  make backend-install    - Install backend dependencies"
	@echo "  make frontend-install   - Install frontend dependencies"
	@echo ""
	@echo "Service Commands:"
	@echo "  make start-services     - Start Docker services (PostgreSQL, Redis)"
	@echo "  make stop-services      - Stop Docker services"
	@echo "  make restart-services   - Restart Docker services"
	@echo ""
	@echo "Development Commands:"
	@echo "  make backend-dev        - Run backend development server"
	@echo "  make frontend-dev       - Run frontend development server"
	@echo ""
	@echo "Testing Commands:"
	@echo "  make test               - Run all tests"
	@echo "  make test-backend       - Run backend tests"
	@echo "  make test-frontend      - Run frontend tests"
	@echo "  make coverage           - Generate coverage reports"
	@echo ""
	@echo "Code Quality Commands:"
	@echo "  make lint               - Lint all code"
	@echo "  make format             - Format all code"
	@echo ""
	@echo "Cleanup Commands:"
	@echo "  make clean              - Remove generated files"
	@echo "  make clean-all          - Remove all generated files and dependencies"

setup:
	@echo "Setting up project..."
	@if [ ! -f .env ]; then cp .env.example .env; fi
	@make start-services
	@make backend-install
	@make frontend-install
	@echo "Setup complete!"

backend-install:
	@echo "Installing backend dependencies..."
	cd backend && python -m venv venv && \
		. venv/bin/activate && \
		pip install --upgrade pip && \
		pip install -r requirements.txt && \
		python -m spacy download en_core_web_sm

frontend-install:
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

start-services:
	@echo "Starting Docker services..."
	docker-compose up -d
	@echo "Waiting for services to be ready..."
	@sleep 5

stop-services:
	@echo "Stopping Docker services..."
	docker-compose down

restart-services:
	@echo "Restarting Docker services..."
	docker-compose restart

backend-dev:
	@echo "Starting backend development server..."
	cd backend && . venv/bin/activate && python app.py

frontend-dev:
	@echo "Starting frontend development server..."
	cd frontend && npm run dev

test:
	@make test-backend
	@make test-frontend

test-backend:
	@echo "Running backend tests..."
	cd backend && . venv/bin/activate && pytest

test-frontend:
	@echo "Running frontend tests..."
	cd frontend && npm test

coverage:
	@echo "Generating coverage reports..."
	cd backend && . venv/bin/activate && pytest --cov-report=html
	cd frontend && npm run test:coverage

lint:
	@echo "Linting backend..."
	cd backend && . venv/bin/activate && flake8 .
	@echo "Linting frontend..."
	cd frontend && npm run lint

format:
	@echo "Formatting backend..."
	cd backend && . venv/bin/activate && black .
	@echo "Formatting frontend..."
	cd frontend && npm run format

clean:
	@echo "Cleaning generated files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -delete 2>/dev/null || true
	rm -rf backend/logs/* 2>/dev/null || true
	rm -rf reports/* 2>/dev/null || true

clean-all: clean
	@echo "Removing all dependencies..."
	rm -rf backend/venv
	rm -rf frontend/node_modules
	rm -rf frontend/dist
	docker-compose down -v
