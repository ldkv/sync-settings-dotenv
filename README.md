![tests](https://github.com/ldkv/sync-settings-dotenv/actions/workflows/tests.yml/badge.svg?branch=main)
![lint](https://github.com/ldkv/sync-settings-dotenv/actions/workflows/linter.yml/badge.svg?branch=main)

# sync-settings-dotenv

A Python CLI to sync configs from code to dotenv file.

Currently only supports BaseSettings model from [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/).

## Prerequisites

- [uv](https://docs.astral.sh/uv/) installed

## Installation

The tool can be installed using [uv tool](https://docs.astral.sh/uv/guides/tools/):

```bash
uv tool install sync-settings-dotenv
```

After installation, it will be available as `sync-dotenv` command in your terminal.

## Usage

For details on usage, run:

```bash
sync-dotenv --help
```

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
