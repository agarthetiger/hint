.ONESHELL:

.PHONY: install
install:
	$(info $(SHELL))
	pwd
	[ -d ".venv" ] && echo ".venv dir exists" || python3 -m venv --upgrade-deps ./.venv
	. ./.venv/bin/activate
	pip install --editable .
	pip install ."[tests]"

.PHONY: release
release:
	pip3 install .
	build

.PHONY: test
test:
	pytest

.PHONY: build
build:
	python3 -m build

.PHONY: clean
clean:
	rm -rf ./.venv
	rm -rf ./dist
	rm -rf ./hint*.egg-info
