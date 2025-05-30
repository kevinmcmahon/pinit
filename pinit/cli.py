# ABOUTME: CLI interface for pinit using Click framework
# ABOUTME: Handles command-line parsing and user interaction

import os
import sys
from pathlib import Path

import click
import httpx
import pinboard
from dotenv import load_dotenv
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel

from .extractor import PinboardBookmarkExtractor
from .pinboard_client import add_bookmark

console = Console()


def load_config() -> None:
    """Load configuration from environment variables."""
    # Try to load from local .env first
    if Path(".env").exists():
        load_dotenv()
    else:
        # Try user's home directory
        home_env = Path.home() / ".pinit" / ".env"
        if home_env.exists():
            load_dotenv(home_env)

    # Finally, load system environment
    load_dotenv()


def get_api_token() -> str | None:
    """Get Pinboard API token from environment."""
    token = os.getenv("PINBOARD_API_TOKEN")
    if not token:
        console.print("[red]Error:[/red] PINBOARD_API_TOKEN not found in environment")
        console.print("\nPlease set your Pinboard API token:")
        console.print("  export PINBOARD_API_TOKEN=your_username:your_token")
        console.print("\nOr create a .env file with:")
        console.print("  PINBOARD_API_TOKEN=your_username:your_token")
    return token


@click.group()
@click.version_option()
def cli() -> None:
    """Pinit - AI-powered Pinboard bookmark manager.

    Automatically extracts metadata from web pages using AI to create
    organized bookmarks for your Pinboard account.

    Configuration:
      Set PINBOARD_API_TOKEN environment variable or create a .env file
      Optional: Set PINIT_MODEL to use a different AI model

    Examples:
      pinit add https://example.com
      pinit add https://example.com --dry-run
      pinit config
    """
    load_config()


@cli.command()
@click.argument("url")
@click.option("--dry-run", is_flag=True, help="Extract metadata without saving")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON")
@click.option("--private", is_flag=True, help="Make bookmark private")
@click.option("--toread", is_flag=True, help="Mark as 'to read'")
@click.option(
    "--model",
    default=None,
    help="LLM model to use (default: anthropic/claude-sonnet-4-0)",
    envvar="PINIT_MODEL",
)
def add(
    url: str,
    dry_run: bool,
    output_json: bool,
    private: bool,
    toread: bool,
    model: str | None,
) -> None:
    """Add a URL to Pinboard with AI-extracted metadata.

    The AI will analyze the webpage content and extract:
    - Title: The main content title (not just the HTML title)
    - Description: A 1-2 sentence summary
    - Tags: 3-8 relevant tags for organization

    Options:
      --dry-run     Preview extraction without saving to Pinboard
      --json        Output raw JSON instead of formatted display
      --private     Mark bookmark as private (default: public)
      --toread      Mark bookmark as "to read"
      --model       Specify AI model (default: anthropic/claude-sonnet-4-0)

    Examples:
      pinit add https://example.com
      pinit add https://example.com --dry-run
      pinit add https://example.com --private --toread
      pinit add https://example.com --model gpt-4 --json
    """
    try:
        # Use model from option/env or default
        model_name = model or "anthropic/claude-sonnet-4-0"

        # Extract bookmark data
        with console.status(f"[yellow]Analyzing webpage with {model_name}...[/yellow]"):
            extractor = PinboardBookmarkExtractor(model_name=model_name)
            bookmark = extractor.extract_bookmark(url)

        if output_json:
            console.print(JSON.from_data(bookmark))
        else:
            # Display formatted output
            panel = Panel.fit(
                f"[bold]Title:[/bold] {bookmark['title']}\n"
                f"[bold]URL:[/bold] {bookmark['url']}\n"
                f"[bold]Description:[/bold] {bookmark.get('description', 'N/A')}\n"
                f"[bold]Tags:[/bold] {', '.join(bookmark.get('tags', []))}",
                title="[green]Extracted Bookmark[/green]",
                border_style="green",
            )
            console.print(panel)

        if dry_run:
            console.print("\n[yellow]Dry run mode - bookmark not saved[/yellow]")
            return

        # Get API token
        api_token = get_api_token()
        if not api_token:
            sys.exit(1)

        # Save to Pinboard
        with console.status("[yellow]Saving to Pinboard...[/yellow]"):
            pb = pinboard.Pinboard(api_token)
            # Apply private and toread flags
            result = add_bookmark(
                pb=pb,
                url=bookmark["url"],
                title=bookmark["title"],
                description=bookmark.get("description", ""),
                tags=bookmark.get("tags", []),
                shared=not private,  # private flag inverts shared
                toread=toread,
            )

        if result:
            console.print("\n[green]✓ Bookmark saved successfully![/green]")
        else:
            console.print("\n[red]✗ Failed to save bookmark[/red]")
            sys.exit(1)

    except httpx.HTTPError as e:
        console.print(f"[red]Error fetching webpage:[/red] {e}")
        sys.exit(1)
    except ValueError as e:
        console.print(f"[red]Error extracting bookmark data:[/red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")
        sys.exit(1)


@cli.command()
def config() -> None:
    """Show configuration information.

    Displays:
    - Current API token status
    - Active AI model configuration
    - Location of configuration files

    Configuration files are loaded in priority order:
    1. Local .env file (in current directory)
    2. User config at ~/.pinit/.env
    3. System environment variables
    """
    console.print("[bold]Pinit Configuration[/bold]\n")

    api_token = os.getenv("PINBOARD_API_TOKEN")
    if api_token:
        # Mask the token for security
        username = api_token.split(":")[0] if ":" in api_token else "unknown"
        console.print(f"[green]✓[/green] API Token configured for user: {username}")
    else:
        console.print("[red]✗[/red] API Token not configured")

    # Show model configuration
    model = os.getenv("PINIT_MODEL", "anthropic/claude-sonnet-4-0")
    console.print(f"\n[bold]Model:[/bold] {model}")
    if os.getenv("PINIT_MODEL"):
        console.print("  [dim](set via PINIT_MODEL environment variable)[/dim]")
    else:
        console.print("  [dim](using default)[/dim]")

    # Check for config files
    local_env = Path(".env")
    home_env = Path.home() / ".pinit" / ".env"

    console.print("\n[bold]Configuration files:[/bold]")
    if local_env.exists():
        console.print(f"  - Local: {local_env.absolute()}")
    if home_env.exists():
        console.print(f"  - Home: {home_env.absolute()}")

    if not local_env.exists() and not home_env.exists():
        console.print("  [dim]No configuration files found[/dim]")


def main() -> None:
    """Entry point for the CLI."""
    cli()
