"""MCP server for emojifyi -- emoji tools for AI assistants.

Requires the ``mcp`` extra: ``pip install emojifyi[mcp]``

Run as a standalone server::

    python -m emojifyi.mcp_server

Or configure in ``claude_desktop_config.json``::

    {
        "mcpServers": {
            "emojifyi": {
                "command": "python",
                "args": ["-m", "emojifyi.mcp_server"]
            }
        }
    }
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("emojifyi")


@mcp.tool()
def emoji_lookup(slug: str) -> str:
    """Look up emoji metadata by slug.

    Returns emoji name, codepoint, category, version, and other metadata
    in a markdown table.

    Args:
        slug: Emoji slug (e.g. "grinning-face", "red-heart").
    """
    from emojifyi import get_emoji

    info = get_emoji(slug)
    if info is None:
        return f"Emoji not found: {slug}"

    return "\n".join(
        [
            f"## {info.character} {info.cldr_name}",
            "",
            "| Property | Value |",
            "|----------|-------|",
            f"| Character | {info.character} |",
            f"| CLDR Name | {info.cldr_name} |",
            f"| Slug | `{info.slug}` |",
            f"| Codepoint | `{info.codepoint}` |",
            f"| Category | {info.category} |",
            f"| Subcategory | {info.subcategory} |",
            f"| Emoji Version | {info.emoji_version} |",
            f"| Unicode Version | {info.unicode_version} |",
            f"| Added Year | {info.added_year} |",
            f"| Type | {info.emoji_type} |",
            f"| ZWJ | {'Yes' if info.is_zwj else 'No'} |",
            f"| Skin Tones | {'Yes' if info.has_skin_tones else 'No'} |",
        ]
    )


@mcp.tool()
def emoji_by_char(character: str) -> str:
    """Look up emoji metadata by character.

    Returns emoji name, codepoint, category, version, and other metadata
    in a markdown table.

    Args:
        character: Emoji character (e.g. the actual emoji glyph).
    """
    from emojifyi import get_emoji_by_char

    info = get_emoji_by_char(character)
    if info is None:
        return f"Emoji not found for character: {character}"

    return "\n".join(
        [
            f"## {info.character} {info.cldr_name}",
            "",
            "| Property | Value |",
            "|----------|-------|",
            f"| Character | {info.character} |",
            f"| CLDR Name | {info.cldr_name} |",
            f"| Slug | `{info.slug}` |",
            f"| Codepoint | `{info.codepoint}` |",
            f"| Category | {info.category} |",
            f"| Subcategory | {info.subcategory} |",
            f"| Emoji Version | {info.emoji_version} |",
            f"| Unicode Version | {info.unicode_version} |",
            f"| Added Year | {info.added_year} |",
            f"| Type | {info.emoji_type} |",
            f"| ZWJ | {'Yes' if info.is_zwj else 'No'} |",
            f"| Skin Tones | {'Yes' if info.has_skin_tones else 'No'} |",
        ]
    )


@mcp.tool()
def emoji_search(query: str, limit: int = 10) -> str:
    """Search emojis by name.

    Returns a list of matching emojis with their characters, names, and categories.

    Args:
        query: Search term (e.g. "heart", "fire", "face").
        limit: Maximum number of results (default 10).
    """
    from emojifyi import search

    results = search(query, limit=limit)
    if not results:
        return f"No emojis found for: {query}"

    lines = [
        f"## Search: {query} ({len(results)} results)",
        "",
        "| Emoji | Name | Category |",
        "|-------|------|----------|",
    ]
    for emoji in results:
        lines.append(f"| {emoji.character} | {emoji.cldr_name} | {emoji.category} |")

    return "\n".join(lines)


@mcp.tool()
def emoji_encode(character: str) -> str:
    """Encode an emoji into 8 different representations.

    Returns UTF-8 bytes, UTF-16 surrogates, HTML entity, CSS content value,
    Python/JavaScript/Java literals, and Unicode codepoint notation.

    Args:
        character: Emoji character to encode.
    """
    from emojifyi import encode

    result = encode(character)

    return "\n".join(
        [
            f"## Encodings for {character}",
            "",
            "| Encoding | Value |",
            "|----------|-------|",
            f"| Codepoint | `{result.codepoint}` |",
            f"| UTF-8 | `{result.utf8_bytes}` |",
            f"| UTF-16 | `{result.utf16_surrogates}` |",
            f"| HTML Entity | `{result.html_entity}` |",
            f"| CSS Content | `{result.css_content}` |",
            f"| Python | `{result.python_literal}` |",
            f"| JavaScript | `{result.javascript_literal}` |",
            f"| Java | `{result.java_literal}` |",
        ]
    )


@mcp.tool()
def emoji_categories() -> str:
    """List all 10 emoji categories with their icons.

    Returns the complete list of Unicode emoji categories.
    """
    from emojifyi import categories

    cats = categories()

    lines = [
        "## Emoji Categories",
        "",
        "| Icon | Name | Slug |",
        "|------|------|------|",
    ]
    for cat in cats:
        lines.append(f"| {cat.icon} | {cat.name} | `{cat.slug}` |")

    return "\n".join(lines)


@mcp.tool()
def emoji_by_category(category_slug: str, limit: int = 20) -> str:
    """Browse emojis in a specific category.

    Args:
        category_slug: Category slug (e.g. "smileys-and-emotion", "animals-and-nature").
        limit: Maximum number of emojis to return (default 20).
    """
    from emojifyi import by_category

    emojis = by_category(category_slug)
    if not emojis:
        return f"No emojis found in category: {category_slug}"

    shown = emojis[:limit]
    lines = [
        f"## Category: {category_slug} ({len(emojis)} emojis)",
        "",
        "| Emoji | Name | Version |",
        "|-------|------|---------|",
    ]
    for emoji in shown:
        lines.append(f"| {emoji.character} | {emoji.cldr_name} | {emoji.emoji_version} |")

    if len(emojis) > limit:
        lines.append(f"\n*... and {len(emojis) - limit} more*")

    return "\n".join(lines)


def main() -> None:
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
