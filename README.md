![tests](https://github.com/ldkv/sync-settings-dotenv/actions/workflows/tests.yml/badge.svg?branch=main)
![lint](https://github.com/ldkv/sync-settings-dotenv/actions/workflows/linter.yml/badge.svg?branch=main)

# sync-settings-dotenv

A Python CLI to sync configs between dotenv files and Python settings module.

It allows to define your application settings in a Python module and use it as a source of truth, instead of maintaining both the settings module and multiple dotenv files manually.

Currently only supports BaseSettings model from [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/).

## Prerequisites

- [uv](https://docs.astral.sh/uv/) installed

## Installation

The tool can be installed using [uv tool](https://docs.astral.sh/uv/guides/tools/):

```bash
uv tool install sync-settings-dotenv
```

After installation, it will be available as `sync-settings-dotenv` command in your terminal.

## Usage

For details on usage, run:

```bash
sync-settings-dotenv --help
```

### Generate a .env.example from Python settings file

To generate a `.env.example` file from a Python settings file, run:

```bash
sync-settings-dotenv path.to.settings.Module path/to/.env.example --exact
```

This command will create a `.env.example` file with all environment variables defined in the specified settings module, using their default values.

A backup of the previous version will be created as `.env.example.backup.timestamp` if the file already exists.

### Sync from Python settings file to .env file

```bash
sync-settings-dotenv path.to.settings.Module /path/to/.env
```

This command will generate or update the existing `.env` file with default values from the specified settings module. If the `.env` file already exists, it will only add missing variables without overwriting existing ones.

To overwrite existing values in the `.env` file, use the `--overwrite-values` flag:

```bash
sync-settings-dotenv path.to.settings.Module /path/to/.env --overwrite-values
```

### Sync from .env.example file to .env file

It is also possible to sync from an existing `.env.example` file to a `.env` file:

```bash
sync-settings-dotenv /path/to/.env.example /path/to/.env
```

It works the same way as syncing from a Python settings file.

## Known limitations

This approach only works with `BaseSettings` models from `pydantic-settings`.

The tool will execute the module to import the settings class, so any side effects in the module will be triggered.

It is assumed that the settings class can be instantiated without any required parameters other than those provided inside the module itself or via environment variables. Otherwise it will raise an error during execution.

## Update and Uninstallation

To upgrade to the latest version, run:

```bash
uv tool upgrade sync-settings-dotenv
```

To uninstall the tool (noooo), run:

```bash
uv tool uninstall sync-settings-dotenv
```

## Development

To set up the development environment, run:

```bash
make dev-setup
```

To verify all development checks:

```bash
make check-all
```

To install the tool in editable mode:

```bash
make local-install
```

Take a look at the [`Makefile`](./Makefile) for more commands to help with development and testing.
