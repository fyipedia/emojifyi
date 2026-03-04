"""Command-line interface for emojifyi.

Requires the ``cli`` extra: ``pip install emojifyi[cli]``

Usage::

    emojifyi lookup grinning-face     # Emoji info by slug
    emojifyi char "smile"             # Look up by character
    emojifyi search heart             # Search emojis
    emojifyi encode "smile"           # All 8 encodings
    emojifyi categories               # List categories
    emojifyi browse smileys-and-emotion  # Emojis in a category
"""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    name="emojifyi",
    help=(
        "Pure Python emoji toolkit -- encoding, lookup, search, "
        "3,781 emojis from Unicode Emoji 16.0."
    ),
    no_args_is_help=True,
)
console = Console()


@app.command()
def lookup(
    slug: str = typer.Argument(help="Emoji slug (e.g. grinning-face)"),
) -> None:
    """Look up emoji metadata by slug."""
    from emojifyi import get_emoji

    info = get_emoji(slug)
    if info is None:
        console.print(f"[red]Emoji not found:[/red] {slug}")
        raise typer.Exit(code=1)

    table = Table(title=f"{info.character} {info.cldr_name}")
    table.add_column("Property", style="cyan", no_wrap=True)
    table.add_column("Value")

    table.add_row("Character", info.character)
    table.add_row("CLDR Name", info.cldr_name)
    table.add_row("Slug", info.slug)
    table.add_row("Codepoint", info.codepoint)
    table.add_row("Category", info.category)
    table.add_row("Subcategory", info.subcategory)
    table.add_row("Emoji Version", info.emoji_version)
    table.add_row("Unicode Version", info.unicode_version)
    table.add_row("Added Year", str(info.added_year))
    table.add_row("Type", info.emoji_type)
    table.add_row("ZWJ", "Yes" if info.is_zwj else "No")
    table.add_row("Skin Tones", "Yes" if info.has_skin_tones else "No")

    console.print(table)


@app.command()
def char(
    character: str = typer.Argument(help="Emoji character to look up"),
) -> None:
    """Look up emoji metadata by character."""
    from emojifyi import get_emoji_by_char

    info = get_emoji_by_char(character)
    if info is None:
        console.print(f"[red]Emoji not found for character:[/red] {character}")
        raise typer.Exit(code=1)

    table = Table(title=f"{info.character} {info.cldr_name}")
    table.add_column("Property", style="cyan", no_wrap=True)
    table.add_column("Value")

    table.add_row("Character", info.character)
    table.add_row("CLDR Name", info.cldr_name)
    table.add_row("Slug", info.slug)
    table.add_row("Codepoint", info.codepoint)
    table.add_row("Category", info.category)
    table.add_row("Subcategory", info.subcategory)
    table.add_row("Emoji Version", info.emoji_version)
    table.add_row("Type", info.emoji_type)

    console.print(table)


@app.command()
def search(
    query: str = typer.Argument(help="Search query (e.g. heart, fire, face)"),
    limit: int = typer.Option(20, "--limit", "-n", help="Maximum results"),
) -> None:
    """Search emojis by name."""
    from emojifyi import search as _search

    results = _search(query, limit=limit)
    if not results:
        console.print(f"[yellow]No emojis found for:[/yellow] {query}")
        raise typer.Exit(code=0)

    table = Table(title=f"Search: {query} ({len(results)} results)")
    table.add_column("Emoji", justify="center")
    table.add_column("Name")
    table.add_column("Slug", style="dim")
    table.add_column("Category", style="dim")

    for emoji in results:
        table.add_row(emoji.character, emoji.cldr_name, emoji.slug, emoji.category)

    console.print(table)


@app.command()
def encode(
    character: str = typer.Argument(help="Emoji character to encode"),
) -> None:
    """Show all 8 encoding representations for an emoji."""
    from emojifyi import encode as _encode

    result = _encode(character)

    table = Table(title=f"Encodings for {character}")
    table.add_column("Encoding", style="cyan", no_wrap=True)
    table.add_column("Value")

    table.add_row("Codepoint", result.codepoint)
    table.add_row("UTF-8", result.utf8_bytes)
    table.add_row("UTF-16", result.utf16_surrogates)
    table.add_row("HTML Entity", result.html_entity)
    table.add_row("CSS Content", result.css_content)
    table.add_row("Python", result.python_literal)
    table.add_row("JavaScript", result.javascript_literal)
    table.add_row("Java", result.java_literal)

    console.print(table)


@app.command()
def categories() -> None:
    """List all 10 emoji categories."""
    from emojifyi import categories as _categories

    cats = _categories()

    table = Table(title="Emoji Categories")
    table.add_column("Icon", justify="center")
    table.add_column("Name")
    table.add_column("Slug", style="dim")

    for cat in cats:
        table.add_row(cat.icon, cat.name, cat.slug)

    console.print(table)


@app.command()
def browse(
    category_slug: str = typer.Argument(help="Category slug (e.g. smileys-and-emotion)"),
    limit: int = typer.Option(50, "--limit", "-n", help="Maximum emojis to show"),
) -> None:
    """Browse emojis in a category."""
    from emojifyi import by_category

    emojis = by_category(category_slug)
    if not emojis:
        console.print(f"[yellow]No emojis found in category:[/yellow] {category_slug}")
        raise typer.Exit(code=0)

    shown = emojis[:limit]
    table = Table(title=f"Category: {category_slug} ({len(emojis)} total)")
    table.add_column("Emoji", justify="center")
    table.add_column("Name")
    table.add_column("Version", style="dim")

    for emoji in shown:
        table.add_row(emoji.character, emoji.cldr_name, emoji.emoji_version)

    console.print(table)
    if len(emojis) > limit:
        console.print(f"[dim]... and {len(emojis) - limit} more. Use --limit to show more.[/dim]")


@app.command()
def stats() -> None:
    """Show emoji dataset statistics."""
    from emojifyi import categories as _categories
    from emojifyi import emoji_count, subcategories

    total = emoji_count()
    cats = _categories()
    subs = subcategories()

    table = Table(title="Emoji Dataset Statistics")
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", justify="right")

    table.add_row("Total Emojis", str(total))
    table.add_row("Categories", str(len(cats)))
    table.add_row("Subcategories", str(len(subs)))

    console.print(table)
