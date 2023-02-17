install:
	poetry shell
	poetry build
	poetry install

test:
	poetry run pytest --cov=hint_cli
