# 📚 pinit

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)

> AI-powered Pinboard bookmark manager that automatically extracts metadata from web pages

**pinit** intelligently analyzes web pages and creates perfectly organized bookmarks for your Pinboard account. Just provide a URL, and AI will extract the title, generate a concise description, and suggest relevant tags - no manual data entry required! 🤖✨

## ✨ Features

- 🤖 **Automatic metadata extraction** - AI analyzes pages to extract title, description, and relevant tags
- 🎯 **Smart tagging** - AI suggests contextually appropriate tags for better organization
- 🔄 **Flexible AI models** - Supports Claude, GPT-4, Gemini, and other LLM providers
- 💻 **Rich terminal UI** - Beautiful output with progress indicators and formatted results
- 🧪 **Dry-run mode** - Preview extractions without saving to Pinboard
- 📊 **JSON output** - Machine-readable format for scripting and automation
- 🔒 **Privacy controls** - Mark bookmarks as private or "to read" as needed

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/kevinmcmahon/pinit.git
cd pinit

# Install with uv (recommended)
uv pip install -e .

# Or install all dependencies
uv sync
```

### Configuration

**1. Get your Pinboard API token:**

Visit [https://pinboard.in/settings/password](https://pinboard.in/settings/password) to find your API token.

**2. Set up environment variables:**

```bash
# Required: Pinboard authentication
export PINBOARD_API_TOKEN=your_username:your_token

# Required: AI provider API key (choose one based on your model)
export ANTHROPIC_API_KEY=your_key  # For Claude models
# OR
export OPENAI_API_KEY=your_key     # For GPT models
# OR see LLM docs for other providers
```

**3. Optional: Create a `.env` file for persistent configuration:**

```bash
# Create in project directory or ~/.pinit/.env
PINBOARD_API_TOKEN=your_username:your_token

# Choose your AI provider (set the appropriate key)
ANTHROPIC_API_KEY=your_anthropic_api_key  # For Claude models
# OPENAI_API_KEY=your_openai_api_key     # For GPT models

# Optional: specify model (defaults to anthropic/claude-sonnet-4-0)
PINIT_MODEL=gpt-4  # or claude-opus-4-0, gpt-3.5-turbo, etc.
```

### Basic Usage

```bash
# Add a bookmark with AI analysis
pinit add https://example.com

# Preview extraction without saving
pinit add https://example.com --dry-run

# Add private bookmark marked as "to read"
pinit add https://example.com --private --toread

# Get JSON output for scripting
pinit add https://example.com --json
```

## 📖 Usage Examples

### Standard Bookmark Addition

```bash
$ pinit add https://example.com/ai-software-development
```

**Output:**
```
┌─ Extracted Bookmark ─────────────────────────────────┐
│ Title: How to Build Better Software with AI          │
│ URL: https://example.com/ai-software-development      │
│ Description: A comprehensive guide exploring how     │
│ artificial intelligence can enhance software         │
│ development workflows and code quality.              │
│ Tags: ai, software-development, programming, guide   │
└───────────────────────────────────────────────────────┘

✓ Bookmark saved successfully!
```

### Advanced Options

```bash
# Use a different AI model
pinit add https://example.com --model gpt-4

# Or use GPT-3.5 for faster/cheaper processing
pinit add https://example.com --model gpt-3.5-turbo

# Check your configuration
pinit config

# JSON output for automation
pinit add https://example.com --json | jq '.tags'
```

## 🔧 Configuration

### Environment Variables

Configuration is loaded in this priority order:

1. Local `.env` file (project directory)
2. User configuration `~/.pinit/.env`
3. System environment variables

### AI Model Configuration

The application uses the [LLM library](https://llm.datasette.io/) for flexible AI model integration:

- **Default model**: `anthropic/claude-sonnet-4-0` (can be changed via `PINIT_MODEL`)
- **Supported providers**: Anthropic Claude, OpenAI GPT, Google Gemini, and many others
- **Easy model switching**: Change models without code modifications
- **Required API keys** depend on your chosen provider:
  - `ANTHROPIC_API_KEY` for Claude models
  - `OPENAI_API_KEY` for GPT models
  - `GEMINI_API_KEY` for Google Gemini
  - See [LLM documentation](https://llm.datasette.io/en/stable/setup.html) for other providers

### Supported Models

| Provider | Popular Models | Environment Variable |
|----------|---------------|---------------------|
| OpenAI | gpt-4, gpt-4-turbo, gpt-3.5-turbo | OPENAI_API_KEY |
| Anthropic | claude-sonnet-4-0, claude-opus-4-0 | ANTHROPIC_API_KEY |
| Google | gemini-pro, gemini-ultra | GEMINI_API_KEY |
| Cohere | command, command-light | COHERE_API_KEY |
| Others | Various | See [LLM docs](https://llm.datasette.io/en/stable/other-models.html) |

Choose the model that best fits your needs:

- **Speed**: GPT-3.5-turbo, Claude Sonnet, Gemini Pro
- **Quality**: GPT-4, Claude Opus, Gemini Ultra
- **Cost**: GPT-3.5-turbo, Cohere Command-light

## 🛠️ Development

### Setup Development Environment

```bash
# Install development dependencies
make dev

# Run all quality checks
make check

# Individual commands
make lint      # Run Ruff linting
make typecheck # Run MyPy type checking
make format    # Auto-format code
make clean     # Remove cache files
```

### Architecture

**pinit** follows modern Python best practices with:

- **Type hints** throughout the codebase
- **Comprehensive error handling** with user-friendly messages
- **Clean separation of concerns** between CLI, AI processing, and API interactions
- **Rich terminal formatting** for beautiful output
- **Configurable AI models** via the LLM library abstraction

### Core Components

- **`PinboardBookmarkExtractor`** - Interfaces with AI models to analyze web pages
- **`pinboard_client`** - Wrapper functions for Pinboard API operations
- **`cli`** - Click-based command interface with Rich formatting
- **Jinja2 templates** - Customizable prompts for AI extraction

## 📦 Dependencies

- **CLI Framework**: `click` - Command-line interface creation
- **Terminal UI**: `rich` - Beautiful terminal formatting
- **AI Integration**: `llm` - Universal LLM library for multiple providers
- **API Client**: `pinboard` - Official Pinboard API client
- **Configuration**: `python-dotenv` - Environment variable management
- **Templating**: `jinja2` - Prompt template rendering

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Run quality checks (`make check`)
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with the excellent [LLM library](https://llm.datasette.io/) by Simon Willison
- Terminal UI enhanced by [Rich](https://github.com/Textualize/rich)
- Pinboard API by [Pinboard](https://pinboard.in/api/)

---
