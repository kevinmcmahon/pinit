# ABOUTME: Development task automation for pinit project
# ABOUTME: Provides convenient commands for linting, type checking, and formatting

.PHONY: help
help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install:  ## Install the package in development mode
	uv pip install -e .
	uv sync --dev

.PHONY: format
format:  ## Format code with ruff
	uv run ruff format pinit/
	uv run ruff check --fix pinit/

.PHONY: lint
lint:  ## Run linting checks with ruff
	uv run ruff check pinit/

.PHONY: typecheck
typecheck:  ## Run type checking with mypy
	uv run mypy pinit/

.PHONY: check
check: lint typecheck  ## Run all checks (lint + typecheck)

.PHONY: clean
clean:  ## Clean up cache and build files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

.PHONY: dev
dev: install  ## Setup development environment