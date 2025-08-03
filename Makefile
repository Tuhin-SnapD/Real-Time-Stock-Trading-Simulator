.PHONY: help install run test clean lint format docs

help: ## Show this help message
	@echo "Real-Time Stock Trading Simulator - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install pytest pytest-cov black flake8 mypy

run: ## Run the application
	python app.py

run-dev: ## Run the application in development mode
	FLASK_DEBUG=True python app.py

test: ## Run tests
	python -m pytest tests/ -v

test-coverage: ## Run tests with coverage report
	python -m pytest tests/ --cov=src --cov-report=html --cov-report=term

lint: ## Run linting checks
	flake8 src/ tests/ app.py
	mypy src/ app.py

format: ## Format code with black
	black src/ tests/ app.py

clean: ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf .pytest_cache/

docs: ## Generate documentation
	@echo "Documentation generation not yet implemented"

docker-build: ## Build Docker image
	docker build -t trading-simulator .

docker-run: ## Run Docker container
	docker run -p 5000:5000 trading-simulator

docker-clean: ## Clean Docker images
	docker rmi trading-simulator

setup: install-dev ## Complete setup for development
	@echo "Setup complete! Run 'make run-dev' to start the application." 