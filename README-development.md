# Development

This project uses [Poetry](https://python-poetry.org/) to manage the project, dependencies, versioning and releasing.  

# Testing

`poetry run pytest --cov=hint_cli` will run the unit tests for this project with coverage.

# Updating dependencies

`poetry show --latest` shows the currently configured dependencies plus whether there are later versions available.
`poetry update` will update all dependencies to the latest version possible based on the version constraints in pyproject.toml.
`poetry add click@~8.0.0` will add or update click to use v8.0.0
`poetry add click@latest` will update click to the latest available version. Note you need to be explicit about adding `--dev` to add or update dev dependencies.

# Versioning

The version number is configured in pyproject.toml and has to be updated manually prior to any release.

# Release process

Releasing is done from my local machine. As an infrequently updated hobby project, the time to configure a release pipeline is not top of my priorities. 


