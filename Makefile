install:
	python3 -m venv .venv
	source .venv/bin/activate
	pip install --editable .
	pip install ."[tests]"

test:
	pytest

build:
	# Doesn't work from make
	python3 -m build
