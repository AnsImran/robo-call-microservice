.PHONY: install run test lint format typecheck docker diagrams clean

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

diagrams:
	python scripts/render_diagrams.py

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache **/__pycache__
