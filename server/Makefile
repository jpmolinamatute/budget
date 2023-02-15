SHELL := bash
.ONESHELL:

.PHONY: help clean activate_venv lint test run format typehint isort all

help:
	@echo "---------------HELP-----------------"
	@echo "To activate the virtual environment type 'make activate_venv'"
	@echo "To run pylint in the project type 'make lint'"
	@echo "To run mypy in the project type 'make typehint'"
	@echo "To run black in the project type 'make black'"
	@echo "To run test in the project type 'make test'"
	@echo "To run isort in the project type 'make isort'"
	@echo "------------------------------------"

clean:
	find . -type d -name __pycache__ -exec rm -rv {} +

activate_venv:
	poetry shell

lint:
	poetry run pylint --rcfile=/home/juanpa/Projects/budget/server/pyproject.toml src/

test:
	poetry run pytest

format:
	poetry run black --config=/home/juanpa/Projects/budget/server/pyproject.toml src/

typehint:
	poetry run mypy --config-file=/home/juanpa/Projects/budget/server/pyproject.toml src/

run:
	/home/juanpa/Projects/budget/server/main.py

isort:
	poetry run isort --settings-path=/home/juanpa/Projects/budget/server/pyproject.toml src/

all: format isort lint typehint
