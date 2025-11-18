#!make

SHELL := /bin/bash

.PHONY: help env

.DEFAULT_GOAL := help

help: ## show help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% 0-9a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)


# Function to export environment variables from a file
define export_env
	@echo "--- Exporting: $(1)"
	$(eval include $(1))
    $(eval export)
endef


##@ Dependency Management
env: ## Export environment variables from .env
	$(call export_env, .env)

install-uv: ## Install uv if not found
	@if ! uv -V ; then \
        echo "uv not found, installing..."; \
        curl -LsSf https://astral.sh/uv/install.sh | sh; \
		source $(HOME)/.cargo/env ; \
    else \
        echo "uv is already installed. Skipped."; \
    fi

dev-setup: install-uv ## Install all dependencies including dev, extras
	@uv venv --clear
	@uv sync

activate-venv: ## Activate the virtual environment
	. $(UV_PROJECT_ENVIRONMENT)/bin/activate && exec $$SHELL

dependencies-check: ## Check the dependencies are up to date
	uv lock --check

tree: ## Show the project dependency tree with outdated packages and sizes
	uv tree --outdated --show-sizes


##@ Code Quality
format-check: ## Verify code formatting
	uv run ruff format --check .

format: ## Format code
	uv run ruff format .

lint-check: ## Verify code linting
	uv run ruff check .

lint-fix: ## Apply linting fixes to codebase - use with caution
	uv run ruff check --fix .

type-check: ## Run the type checker
	uv run pyrefly check

code-quality: format-check lint-check type-check ## Run the linters and static type checker


##@ Testing
test: ## Run the tests in local environment
	uv run pytest .

check-all: dependencies-check code-quality test ## Run all checks and tests


##@ Release
build: ## Build the package
	uv build --clear

publish: env build ## Publish the package to PyPI
	uv publish

local-install: ## Install current version locally for testing
	uv tool install .

gh-release: ## Release a new version using gh CLI
	gh release create $(version) --generate-notes --target main


%:
	@true
