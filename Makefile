.PHONY: help build up down logs clean test dev-backend dev-frontend

# Default target
help:
	@echo "Available commands:"
	@echo "  build     - Build all Docker images"
	@echo "  up        - Start all services"
	@echo "  down      - Stop all services"
	@echo "  logs      - View logs from all services"
	@echo "  clean     - Remove all containers and volumes"
	@echo "  test      - Run tests for both backend and frontend"
	@echo "  dev-backend  - Start backend in development mode"
	@echo "  dev-frontend - Start frontend in development mode"

# Build all Docker images
build:
	docker-compose build

# Start all services
up:
	docker-compose up -d

# Stop all services
down:
	docker-compose down

# View logs
logs:
	docker-compose logs -f

# Clean up containers and volumes
clean:
	docker-compose down -v --remove-orphans
	docker system prune -f

# Run tests
test:
	@echo "Running backend tests..."
	cd backend && python -m pytest
	@echo "Running frontend tests..."
	cd frontend && npm test

# Development mode - Backend
dev-backend:
	@echo "Starting backend in development mode..."
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Development mode - Frontend
dev-frontend:
	@echo "Starting frontend in development mode..."
	cd frontend && npm run dev

# Install dependencies
install-backend:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt

install-frontend:
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

# Setup development environment
setup: install-backend install-frontend
	@echo "Development environment setup complete!"

# Health check
health:
	@echo "Checking service health..."
	curl -f http://localhost:8000/health || echo "Backend not responding"
	curl -f http://localhost:3000/health || echo "Frontend not responding"

# Database operations
db-migrate:
	@echo "Running database migrations..."
	cd backend && alembic upgrade head

db-reset:
	@echo "Resetting database..."
	docker-compose down -v
	docker-compose up -d postgres
	sleep 5
	docker-compose up -d backend

# Production build
prod-build:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

prod-up:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d 