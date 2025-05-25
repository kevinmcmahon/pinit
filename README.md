# pinit

AI-powered Pinboard bookmark manager using Claude to automatically extract metadata from web pages.

## Features

- Automatically extracts title, description, and tags from web pages
- Configurable AI model (defaults to Claude Sonnet 4.0)
- Rich terminal output with progress indicators
- Dry-run mode for testing
- JSON output for scripting

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd pinit

# Install with uv
uv pip install -e .
```

## Configuration

Create a `.env` file with your Pinboard API token:

```bash
PINBOARD_API_TOKEN=your_username:your_token
```

Optionally set the AI model:

```bash
PINIT_MODEL=claude-opus-4-0  # defaults to claude-sonnet-4-0
```

## Usage

```bash
# Add a bookmark
pinit add https://example.com

# Add with options
pinit add https://example.com --private --toread

# Use a different model
pinit add https://example.com --model claude-opus-4-0

# Preview without saving
pinit add https://example.com --dry-run

# Show configuration
pinit config
```

## Development

```bash
# Setup development environment
make dev

# Run linting and type checking
make check

# Auto-format code
make format
```

## License

MIT
