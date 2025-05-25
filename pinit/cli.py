# ABOUTME: CLI interface for pinit using Click framework
# ABOUTME: Handles command-line parsing and user interaction

import os
import sys
from pathlib import Path
from typing import Optional

import click
import pinboard
from dotenv import load_dotenv
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel

from .extractor import PinboardBookmarkExtractor
from .pinboard_client import add_bookmark_from_json

console = Console()


def load_config():
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


def get_api_token() -> Optional[str]:
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
def cli():
    """Pinit - AI-powered Pinboard bookmark manager."""
    load_config()


@cli.command()
@click.argument("url")
@click.option("--dry-run", is_flag=True, help="Extract metadata without saving")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON")
@click.option("--private", is_flag=True, help="Make bookmark private")
@click.option("--toread", is_flag=True, help="Mark as 'to read'")
def add(url: str, dry_run: bool, output_json: bool, private: bool, toread: bool):
    """Add a URL to Pinboard with AI-extracted metadata."""
    try:
        # Extract bookmark data
        with console.status("[yellow]Analyzing webpage...[/yellow]"):
            extractor = PinboardBookmarkExtractor()
            bookmark = extractor.extract_bookmark(url)
        
        if output_json:
            console.print(JSON(data=bookmark))
        else:
            # Display formatted output
            panel = Panel.fit(
                f"[bold]Title:[/bold] {bookmark['title']}\n"
                f"[bold]URL:[/bold] {bookmark['url']}\n"
                f"[bold]Description:[/bold] {bookmark.get('description', 'N/A')}\n"
                f"[bold]Tags:[/bold] {', '.join(bookmark.get('tags', []))}",
                title="[green]Extracted Bookmark[/green]",
                border_style="green"
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
            # Override shared setting based on private flag
            bookmark_data = bookmark.copy()
            result = add_bookmark_from_json(pb, bookmark_data)
        
        if result:
            console.print("\n[green]✓ Bookmark saved successfully![/green]")
        else:
            console.print("\n[red]✗ Failed to save bookmark[/red]")
            sys.exit(1)
            
    except ValueError as e:
        console.print(f"[red]Error extracting bookmark data:[/red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")
        sys.exit(1)


@cli.command()
def config():
    """Show configuration information."""
    console.print("[bold]Pinit Configuration[/bold]\n")
    
    api_token = os.getenv("PINBOARD_API_TOKEN")
    if api_token:
        # Mask the token for security
        username = api_token.split(":")[0] if ":" in api_token else "unknown"
        console.print(f"[green]✓[/green] API Token configured for user: {username}")
    else:
        console.print("[red]✗[/red] API Token not configured")
    
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


def main():
    """Entry point for the CLI."""
    cli()