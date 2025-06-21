PYTHON ?= python3.11
PIP := $(PYTHON) -m pip

.PHONY: install run help

## Show available make targets
help:
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies using conda and pip
	conda env create -f environment.yml || echo "Environment may already exist, skipping..."
	@$(PYTHON) -m ensurepip --upgrade
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt

run: ## Run the main application
	@$(PYTHON) main.py
