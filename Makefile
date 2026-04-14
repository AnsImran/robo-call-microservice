.PHONY: install run test lint format docker clean

install:
	pip install -e ".[dev]"

run:
	python main.py

test:
	pytest -v

lint:
	ruff check src tests

format:
	ruff format src tests

typecheck:
	mypy src

docker:
	docker build -t robo-call-service .

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache **/__pycache__
