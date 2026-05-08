# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.1.0] - 2026-05-08

### Added
- New method for publishing functional block inputs and outputs.
- CLI support: the project can now be installed as a Python module in a virtual environment and used as a command-line utility.
- Logging handler to forward logs to an arbitrary UNIX socket for integration with logging collector tools.
- Expanded functional block library with new modules: `convert`, `events`, `iec61131`, `utils`.

### Changed
- Refactored project structure.
- Fixed OPC UA node value updates in the embedded server.
- Standardized log output using Python's built-in `logging` module.
- Updated CLI startup arguments.
- Updated project dependencies.

### Removed
- Functional block execution analytics.

## [1.0.0] - 2025-12-10

- Initial release.