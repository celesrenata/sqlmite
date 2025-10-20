# Makefile for SQLite to PostgreSQL Bridge

# Default target
.PHONY: help
help:
	@echo "SQLite to PostgreSQL Bridge Makefile"
	@echo "Available commands:"
	@echo "  make test-suite        - Run complete test suite"
	@echo "  make test-active     - Run active tests only"
	@echo "  make test-unit       - Run unit tests only"
	@echo "  make reset-db         - Reset test database"
	@echo "  make cli-test         - Test CLI functionality"
	@echo "  make build            - Build the package"
	@echo "  make clean            - Clean build artifacts"
	@echo "  make install          - Install the package"
	@echo "  make docs            - Generate documentation"

# Test suite targets
.PHONY: test-suite
test-suite:
	@echo "Running complete test suite..."
	python scripts/test_suite_runner.py

.PHONY: test-active
test-active:
	@echo "Running active tests..."
	python scripts/active_test_suite.py

.PHONY: test-unit
test-unit:
	@echo "Running unit tests..."
	pytest -v

.PHONY: reset-db
reset-db:
	@echo "Resetting test database..."
	python scripts/reset_test_database.py

# CLI test target
.PHONY: cli-test
cli-test:
	@echo "Testing CLI functionality..."
	@echo "Testing basic CLI help:"
	sqlite-postgres-bridge --help
	@echo "Testing CLI with parameters (placeholder):"
	@echo "sqlite-postgres-bridge --sqlite-db test.db --postgres-url \"postgresql://celes:PSCh4ng3me!@10.1.1.12:5432/testdb\""

# Build targets
.PHONY: build
build:
	@echo "Building package..."
	python setup.py sdist bdist_wheel

.PHONY: clean
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/ dist/ *.egg-info/

.PHONY: install
install:
	@echo "Installing package..."
	pip install -e .

.PHONY: docs
docs:
	@echo "Generating documentation..."
	@echo "Documentation generation not implemented yet"

# Default target
.PHONY: default
default: help
