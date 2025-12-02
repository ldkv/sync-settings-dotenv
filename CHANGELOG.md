# Changelog

## Guidelines

https://keepachangelog.com/en/1.0.0/

**Added** for new features.\
**Changed** for changes in existing functionality.\
**Deprecated** for soon-to-be removed features.\
**Removed** for now removed features.\
**Fixed** for any bug fixes.\
**Security** in case of vulnerabilities.

## [Unreleased]

### Changed

- Move version info to `__init__.py`

### Fixed

- Process secret fields of `pydantic-settings` properly

## [0.2.1] - 2025-11-20

### Added

- CLI option to show version
- Known limitations section in README

### Fixed

- No longer overwrite with identical keys/values

## [0.2.0] - 2025-11-18

### Added

- Support sync between dotenv files
- Resolve required fields without default values
- Allow to generate without header comment

### Changed

- Rename CLI command to `sync-settings-dotenv` instead of `sync-dotenv` to avoid confusion
- Generate backups any time the target file is modified
- Update README with more detailed usage instructions
- Minor refactoring of utility functions

## [0.1.0] - 2025-11-18

### Added

- Github actions to automate publishing to PyPI as Trusted Publisher

## [0.0.2] - 2025-11-18

### Added

- Project management with `uv`
- Linter & unit tests CI pipeline with GitHub Actions
- `pyproject.toml` configuration file
- Linting with `ruff`
- Type checking with `pyrefly`
- `Makefile` for common tasks
- CLI command to sync settings to dotenv file
- Compatibility with `pydantic-settings` BaseSettings models
