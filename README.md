# Esagil

Esagil is an image processing library for JunoCam built on Python.

## Getting Started
### Dependent Libraries

If you have not installed `pipx` before, be sure to install it using the following commands.

```shell
pip install pipx
pipx ensurepath --global
```

Additionally, if you have not installed `poetry`, run the following command.

```shell
pipx install poetry
```

With `pipx` and `poetry` installed, run the following command to set up the project.

```shell
poetry install
```

## Development

Esagil is managed using `poetry` for dependencies, building, and publishing.

### Building

To build the project, run the following command.

```shell
poetry build
```

### Publishing

To publish a build, run the following command.

```shell
poetry publish
```

### Dependencies

#### View

To view the current dependencies that the project is using, run the following command.

```shell
poetry show --tree
```

#### Add

To add a new dependency, run the following command.

```shell
poetry add dependency
```

The `dependency` parameter can specify versions with dynamic constraints; you can view further details [here](https://python-poetry.org/docs/cli/#add).

### Versioning

To update the project version, run the following command.

```shell
poetry version [major|minor|patch|premajor|preminor|prepatch|prerelease|prerelease-next-phase]
```

You can view what each version type does [here](https://python-poetry.org/docs/cli/#version).