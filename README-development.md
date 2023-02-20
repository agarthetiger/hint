# Development

This project uses [Poetry](https://python-poetry.org/) to manage the project, dependencies, versioning and releasing.

Note that even if it wasn't, it's recommended to use setuptools instead of adding shebangs to the file to execute when using click. See https://click.palletsprojects.com/en/8.1.x/setuptools/#setuptools-integration

## Executing the local code instead of the installed version

```bash
pipx install poetry # Install poetry if it's not already present

# Run all the following commands from the project (root) folder.
make install # See Makefile for details

poetry run hint --version # Run the local built version of hint and print the version. Useful to confirm you are running the code and not the version installed onto your development machine.

# Run the tests
make test
```

## Testing

See the `test` target in the Makefile.

`poetry run pytest --cov=hint_cli` will run the unit tests for this project with coverage.

## Updating dependencies

`poetry show --latest` shows the currently configured dependencies plus whether there are later versions available.
`poetry update` will update all dependencies to the latest version possible based on the version constraints in pyproject.toml.
`poetry add click@~8.0.0` will add or update click to use v8.0.0
`poetry add click@latest` will update click to the latest available version. Note you need to be explicit about adding `--dev` to add or update dev dependencies.

## Versioning

The version number is configured in pyproject.toml and has to be updated manually prior to any release.

## Release process

### Publish to pypi-testorg

Ensure the version in `pyproject.toml` has been bumped appropriately, then manually trigger the `Release workflow` GitHub Action.

### Publish to pypi.org

Not yet implemented.
