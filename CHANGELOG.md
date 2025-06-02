# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.3] - 2025-06-02

### Added

- Interactive configuration setup with `pinit config --init` command
- User configuration file support at `~/.pinit/config` with secure permissions (600)
- Automatic creation of ~/.pinit directory when needed

### Changed

- Configuration loading priority order clarified: system env vars (highest), local .env, user config (lowest)
- Enhanced `pinit config` command to show configuration file status with checkmarks
- Improved error messages when PINBOARD_API_TOKEN is not found
- Updated documentation to reflect new configuration system

### Fixed

- Configuration loading now properly respects priority order with override behavior

## [0.2.2] - 2025-05-31

### Changed

- Updated PyPI package name to `smartpin` for initial publication
- Repository renamed to `smartpin` to match PyPI package name
- CLI command remains `pinit` for ease of use

## [0.2.1] - 2025-05-30

### Added

- Python 3.13 support in CI/CD pipeline
- Comprehensive CLI help documentation with usage examples for all commands
- Detailed configuration instructions in main command help text
- Examples for each CLI option showing common usage patterns

### Changed

- Enhanced help text for `pinit`, `add`, and `config` commands
- Improved CI workflow formatting and structure
- Minor code formatting improvements

## [0.2.0] - 2025-05-30

### Added

- Local content fetching with httpx and BeautifulSoup for more reliable page parsing
- Improved error handling for HTTP network failures
- Comprehensive development tooling (linting, type checking, formatting)
- Apache 2.0 license
- GitHub Actions workflow for CI/CD

### Changed

- Default model specification now uses full `anthropic/claude-sonnet-4-0` identifier for consistency with LLM library conventions
- Replaced LLM-based web fetching with direct HTTP client implementation
- Modernized type hints throughout the codebase

### Fixed

- More robust content extraction from web pages
- Better handling of pages with complex JavaScript or dynamic content

## [0.1.0] - 2025-05-30

### Added

- Initial release
- AI-powered bookmark metadata extraction using Claude Sonnet
- Support for multiple LLM providers (Claude, GPT-4, Gemini, etc.)
- Rich terminal UI with progress indicators
- Dry-run mode for previewing extractions
- JSON output format for automation
- Private and "to read" bookmark flags
- Flexible configuration via environment variables
- Modular architecture with clean separation of concerns
