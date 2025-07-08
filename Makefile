
.PHONY: help setup build deploy clean logs test

help:
	@echo "Weather App - Local Development Commands"
	@echo "========================================"
	@echo ""
	@echo "Setup Commands:"
	@echo "  make setup          - Setup k3d cluster and dependencies"
	@echo "  make setup-hosts    - Add entries to /etc/hosts"
	@echo ""
	@echo "Development Commands:"
	@echo "  make build          - Build Docker images"
	@echo "  make deploy         - Deploy to k3d cluster"
	@echo "  make redeploy       - Rebuild and redeploy everything"
	@echo ""
	@echo "Testing Commands:"
	@echo "  make test           - Run all tests"
	@echo "  make test-backend   - Run backend tests only"
	@echo "  make test-frontend  - Run frontend tests only"
	@echo ""
	@echo "Utility Commands:"
	@echo "  make logs           - Show application logs"
	@echo "  make logs-backend   - Show backend logs only"
	@echo "  make logs-frontend  - Show frontend logs only"
	@echo "  make status         - Show cluster status"
	@echo "  make clean          - Clean up everything"
	@echo ""
	@echo "Access URLs:"
	@echo "  Frontend: http://weather.local:8080"
	@echo "  Backend:  http://api.weather.local:8080"

# Variables
CLUSTER_NAME := weather-cluster
REGISTRY_PORT := 5556
BACKEND_IMAGE := fierdakcap/weather-backend:latest
FRONTEND_IMAGE := fierdakcap/weather-frontend:latest

setup:
	@echo "Setting up k3d cluster..."
	@if ! k3d cluster list | grep -q $(CLUSTER_NAME); then \
	k3d cluster create $(CLUSTER_NAME) \
		--port "8080:80@loadbalancer" \
		--port "8443:443@loadbalancer" \
		--agents 2; \
	else \
		echo "⚠️  Cluster $(CLUSTER_NAME) already exists"; \
	fi
	@echo "⏳ Waiting for cluster to be ready..."
	@kubectl wait --for=condition=ready node --all --timeout=300s
	@echo "📦 Creating namespace and secrets..."
	@kubectl create namespace weather-app --dry-run=client -o yaml | kubectl apply -f -
	@kubectl create secret generic weather-secrets \
		--from-literal=OPENWEATHER_API_KEY=${OPENWEATHER_API_KEY:-demo_key} \
		--namespace=weather-app \
		--dry-run=client -o yaml | kubectl apply -f -
	@echo "✅ Setup complete!"
	@make setup-hosts

# Add entries to /etc/hosts
setup-hosts:
	@echo "📝 Adding entries to /etc/hosts..."
	@if ! grep -q "weather.local" /etc/hosts; then \
		echo "127.0.0.1 weather.local" | sudo tee -a /etc/hosts; \
	fi
	@if ! grep -q "api.weather.local" /etc/hosts; then \
		echo "127.0.0.1 api.weather.local" | sudo tee -a /etc/hosts; \
	fi
	@echo "✅ /etc/hosts updated"

# Build Docker images
build:
	@echo "🔨 Building Docker images..."
	@echo "Building backend..."
	@docker build -t $(BACKEND_IMAGE) ./backend
	@docker push $(BACKEND_IMAGE)
	@echo "Building frontend..."
	@docker build -t $(FRONTEND_IMAGE) ./frontend
	@docker push $(FRONTEND_IMAGE)
	@echo "✅ Images built and pushed to local registry"

# Deploy to k3d
deploy:
	@echo "📦 Deploying to k3d cluster..."
	@kubectl apply -f k8s/local/
	@echo "⏳ Waiting for deployments to be ready..."
	@kubectl wait --for=condition=available --timeout=300s deployment/weather-backend -n weather-app || true
	@kubectl wait --for=condition=available --timeout=300s deployment/weather-frontend -n weather-app || true
	@echo "✅ Deployment complete!"
	@make status

# Rebuild and redeploy everything
redeploy: build deploy

# Run all tests
test:
	@echo "🧪 Running all tests..."
	@make test-backend
	@make test-frontend

# Test backend
test-backend:
	@echo "🧪 Running backend tests..."
	@cd backend && python -m pytest tests/ -v

# Test frontend
test-frontend:
	@echo "🧪 Running frontend tests..."
	@cd frontend && npm test -- --coverage --watchAll=false

# Show application logs
logs:
	@echo "📋 Application Logs:"
	@echo "===================="
	@echo "Backend logs:"
	@kubectl logs deployment/weather-backend -n weather-app --tail=20 || true
	@echo ""
	@echo "Frontend logs:"
	@kubectl logs deployment/weather-frontend -n weather-app --tail=20 || true

# Show backend logs only
logs-backend:
	@kubectl logs -f deployment/weather-backend -n weather-app

# Show frontend logs only
logs-frontend:
	@kubectl logs -f deployment/weather-frontend -n weather-app

# Show cluster status
status:
	@echo "📊 Cluster Status:"
	@echo "=================="
	@echo "Nodes:"
	@kubectl get nodes
	@echo ""
	@echo "Pods:"
	@kubectl get pods -n weather-app
	@echo ""
	@echo "Services:"
	@kubectl get services -n weather-app
	@echo ""
	@echo "Ingress:"
	@kubectl get ingress -n weather-app
	@echo ""
	@echo "🌐 Access URLs:"
	@echo "   Frontend: http://weather.local:8080"
	@echo "   Backend:  http://api.weather.local:8080/docs"

# Port forward for direct access (alternative to ingress)
port-forward:
	@echo "🔗 Setting up port forwarding..."
	@echo "Frontend will be available at: http://localhost:3000"
	@echo "Backend will be available at: http://localhost:8000"
	@kubectl port-forward service/weather-frontend-service 3000:80 -n weather-app &
	@kubectl port-forward service/weather-backend-service 8000:8000 -n weather-app &
	@echo "✅ Port forwarding active. Press Ctrl+C to stop."

# Development mode (run locally without k8s)
dev:
	@echo "🚀 Starting development servers..."
	@echo "Starting backend..."
	@cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
	@echo "Starting frontend..."
	@cd frontend && npm start &
	@echo "✅ Development servers started"
	@echo "   Frontend: http://localhost:3000"
	@echo "   Backend:  http://localhost:8000/docs"

# Clean up everything
clean:
	@echo "🧹 Cleaning up..."
	@k3d cluster delete $(CLUSTER_NAME) || true
	@docker system prune -f || true
	@echo "✅ Cleanup complete!"

# Install dependencies
install-deps:
	@echo "📦 Installing dependencies..."
	@echo "Installing backend dependencies..."
	@cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	@cd frontend && npm install
	@echo "✅ Dependencies installed"

# Restart deployments
restart:
	@echo "🔄 Restarting deployments..."
	@kubectl rollout restart deployment/weather-backend -n weather-app
	@kubectl rollout restart deployment/weather-frontend -n weather-app
	@kubectl rollout status deployment/weather-backend -n weather-app
	@kubectl rollout status deployment/weather-frontend -n weather-app
	@echo "✅ Deployments restarted"