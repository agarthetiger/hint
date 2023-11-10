# Development

This project used [Poetry](https://python-poetry.org/) to manage the project, dependencies, versioning and releasing. This was awesome, bbut it meant the tab-completion wasn't working which is not something I want to give up.

Therefore, this project is back to using setuptools to build and package.

Note that even if it wasn't, it's recommended to use setuptools instead of adding shebangs to the file to execute when using click. See https://click.palletsprojects.com/en/8.1.x/setuptools/#setuptools-integration

## Executing the local code instead of the installed version

```bash
# One-time initial setup
python3 -m venv .venv

# Run all the following commands from the project (root) folder.
make install # This activates the virtual environment and installs the project in editable mode.

hint --version # Run the local built version of hint and print the version. Useful to confirm you are running the code and not the version installed onto your development machine.

# Run the tests
make test
```

## Testing

See the `test` target in the Makefile.

`pytest` will run the unit tests for this project with coverage.

## Updating dependencies

`poetry show --latest` shows the currently configured dependencies plus whether there are later versions available.
`poetry update` will update all dependencies to the latest version possible based on the version constraints in pyproject.toml.
`poetry add click@~8.0.0` will add or update click to use v8.0.0
`poetry add click@latest` will update click to the latest available version. Note you need to be explicit about adding `--dev` to add or update dev dependencies.

## Versioning

The version number is configured in `setup.py` and has to be updated manually prior to any release.

## Release process

### Publish to pypi-testorg

Not yet implemented.

### Publish to pypi.org

Ensure the version in `setup.py` has been bumped appropriately, then manually trigger the `Release workflow` GitHub Action. This needs updating as it's configured for poetry still.
