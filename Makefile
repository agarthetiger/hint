install:
	source .venv/bin/activate
	pip install --editable .

test:
	pytest
