.PHONY: install test test-core clean help

help:
	@echo "Available commands:"
	@echo "  install    - Install package in development mode"
	@echo "  test       - Run end-to-end tests (no database required)"
	@echo "  test-core  - Run core unit tests only"
	@echo "  test-all   - Run all unit tests (may fail without PostgreSQL)"
	@echo "  clean      - Clean up temporary files"

install:
	pip install -e .

test:
	python test_bridge_e2e.py

test-core:
	python -m pytest tests/test_query_translator.py tests/test_data_mapper.py -v

test-all:
	python -m pytest tests/ -v

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/
	rm -f test_bridge.db
