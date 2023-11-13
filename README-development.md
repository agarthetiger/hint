# Development

This project used [Poetry](https://python-poetry.org/) to manage the project, dependencies, versioning and releasing. This was awesome, bbut it meant the tab-completion wasn't working which is not something I want to give up.

Therefore, this project is back to using setuptools to build and package.

Note that even if it wasn't, it's recommended to use setuptools instead of adding shebangs to the file to execute when using click. See https://click.palletsprojects.com/en/8.1.x/setuptools/#setuptools-integration

## Executing the local code instead of the installed version

```bash
# Run all the following commands from the project (root) folder.

# One-time initial setup
make setup

# This activates the virtual environment, installs the project in editable mode and all dev dependencies.
make install

hint --version # Run the local built version of hint and print the version. Useful to confirm you are running the code and not the version installed onto your development machine.

# Run the tests
make test
```

## Testing

`make test` will run the unit tests for this project with coverage.

## Versioning

The version number is configured in `setup.py` and has to be updated manually prior to any release.

## Release process

### Publish to pypi-testorg

Not yet implemented.

### Publish to pypi.org

Ensure the version in `setup.py` has been bumped appropriately, then manually trigger the `Release workflow` GitHub Action. This needs updating as it's configured for poetry still.
