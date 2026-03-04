# emojifyi

[![PyPI](https://img.shields.io/pypi/v/emojifyi)](https://pypi.org/project/emojifyi/)
[![Python](https://img.shields.io/pypi/pyversions/emojifyi)](https://pypi.org/project/emojifyi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Pure Python emoji toolkit for developers. Encode any emoji into 8 representations, look up metadata for 3,781 emojis, search and browse by category -- all with zero dependencies. Includes a CLI, MCP server for AI assistants, and an API client for [emojifyi.com](https://emojifyi.com/).

> Browse all emojis at [emojifyi.com](https://emojifyi.com/) -- [search emojis](https://emojifyi.com/search/), [browse categories](https://emojifyi.com/category/), [emoji encoding tools](https://emojifyi.com/tools/unicode-lookup/), [emoji collections](https://emojifyi.com/collection/)

## Install

```bash
pip install emojifyi            # Core library (zero dependencies)
pip install emojifyi[cli]       # + CLI (typer, rich)
pip install emojifyi[mcp]       # + MCP server for AI assistants
pip install emojifyi[api]       # + HTTP client for emojifyi.com API
pip install emojifyi[all]       # Everything
```

## Quick Start

```python
from emojifyi import encode, get_emoji, search

# Encode any emoji into 8 representations
result = encode("\U0001f600")
print(result.codepoint)         # U+1F600
print(result.utf8_bytes)        # 0xF0 0x9F 0x98 0x80
print(result.html_entity)       # &#x1F600;
print(result.css_content)       # \1F600
print(result.python_literal)    # \U0001F600
print(result.java_literal)      # \uD83D\uDE00

# Look up emoji metadata
info = get_emoji("red-heart")
print(info.character)           # Red heart emoji
print(info.category)            # smileys-and-emotion
print(info.emoji_version)       # 1.0

# Search emojis by name
for emoji in search("fire")[:5]:
    print(f"{emoji.character} {emoji.cldr_name}")
```

## Advanced Usage

```python
from emojifyi import (
    get_emoji_by_char, by_category, by_version,
    categories, subcategories, all_emojis, emoji_count,
)

# Look up by character
info = get_emoji_by_char("\U0001f525")
print(info.slug)  # fire

# Browse by category
animals = by_category("animals-and-nature")
print(len(animals))  # 151 emojis

# New emojis in a specific version
new = by_version("16.0")
print(len(new))  # Latest additions

# Category metadata
for cat in categories():
    print(f"{cat.icon} {cat.name} ({cat.slug})")

# Total count
print(emoji_count())  # 3781
```

## CLI

Requires the `cli` extra: `pip install emojifyi[cli]`

```bash
# Look up emoji by slug
emojifyi lookup grinning-face

# Look up by character
emojifyi char "\U0001f600"

# Search emojis
emojifyi search heart
emojifyi search fire --limit 5

# Show all 8 encodings
emojifyi encode "\U0001f600"

# List categories
emojifyi categories

# Browse a category
emojifyi browse smileys-and-emotion

# Dataset statistics
emojifyi stats
```

## MCP Server

Requires the `mcp` extra: `pip install emojifyi[mcp]`

Add to your `claude_desktop_config.json`:

```json
{
    "mcpServers": {
        "emojifyi": {
            "command": "python",
            "args": ["-m", "emojifyi.mcp_server"]
        }
    }
}
```

Available tools:

| Tool | Description |
|------|-------------|
| `emoji_lookup` | Look up emoji by slug or character |
| `emoji_search` | Search emojis by name |
| `emoji_encode` | Encode emoji into 8 representations |
| `emoji_categories` | List all 10 categories |
| `emoji_by_category` | Browse emojis in a category |
| `emoji_stats` | Dataset statistics |

## API Client

Requires the `api` extra: `pip install emojifyi[api]`

```python
from emojifyi.api import EmojiFYI

with EmojiFYI() as api:
    # Get emoji details
    info = api.emoji("grinning-face")
    print(info["character"])

    # Search emojis
    results = api.search("heart")
    for r in results["results"]:
        print(r["character"], r["cldr_name"])

    # List categories
    cats = api.categories()
    print(cats["count"])  # 10

    # Get random emoji
    lucky = api.random()
    print(lucky["character"], lucky["cldr_name"])
```

Full API documentation at [emojifyi.com/developers](https://emojifyi.com/developers/).

## API Reference

### Encoding

| Function | Description |
|----------|-------------|
| `encode(char) -> EncodingResult` | All 8 encodings at once |
| `char_to_codepoint(char) -> str` | Character to `U+XXXX` |
| `encode_utf8(char) -> str` | UTF-8 byte representation |
| `encode_utf16(char) -> str` | UTF-16 surrogates |
| `encode_html(codepoint) -> str` | HTML numeric entity |
| `encode_css(codepoint) -> str` | CSS content value |
| `encode_python(codepoint) -> str` | Python literal |
| `encode_javascript(codepoint) -> str` | JavaScript literal |
| `encode_java(char) -> str` | Java literal (with surrogates) |

### Lookup and Search

| Function | Description |
|----------|-------------|
| `get_emoji(slug) -> EmojiInfo \| None` | Look up by slug |
| `get_emoji_by_char(char) -> EmojiInfo \| None` | Look up by character |
| `search(query, limit=20) -> list[EmojiInfo]` | Case-insensitive name search |
| `all_emojis() -> list[EmojiInfo]` | All 3,781 emojis |
| `emoji_count() -> int` | Total emoji count |

### Browse

| Function | Description |
|----------|-------------|
| `by_category(slug) -> list[EmojiInfo]` | Filter by category |
| `by_version(version) -> list[EmojiInfo]` | Filter by emoji version |
| `categories() -> list[Category]` | All 10 categories |
| `subcategories(slug?) -> list[Subcategory]` | All or filtered subcategories |

## Data Types

- **`EncodingResult`** -- 8-field NamedTuple: codepoint, utf8_bytes, utf16_surrogates, html_entity, css_content, python_literal, javascript_literal, java_literal
- **`EmojiInfo`** -- 12-field NamedTuple: character, slug, cldr_name, codepoint, category, subcategory, emoji_version, unicode_version, added_year, emoji_type, is_zwj, has_skin_tones
- **`Category`** -- 4-field NamedTuple: slug, name, icon, order
- **`Subcategory`** -- 4-field NamedTuple: slug, name, category_slug, order

## Features

- **8 encoding types**: UTF-8 bytes, UTF-16 surrogates, HTML entity, CSS content, Python/JavaScript/Java literals, codepoint
- **3,781 emojis**: Full Unicode Emoji 16.0 dataset with metadata
- **10 categories, 100 subcategories**: Browse and filter
- **ZWJ support**: Multi-codepoint sequences, flags, keycaps, skin tones
- **Zero dependencies**: Core library is pure Python with bundled JSON data
- **CLI**: Rich terminal interface for emoji lookup, search, and encoding
- **MCP server**: AI assistant integration with 6 tools
- **API client**: HTTP client for emojifyi.com REST API
- **Type-safe**: Full type annotations, `py.typed` marker (PEP 561)

## FYIPedia Developer Tools

Part of the [FYIPedia](https://github.com/fyipedia) open-source developer tools ecosystem:

| Package | Description |
|---------|-------------|
| [colorfyi](https://colorfyi.com/) | Color conversion, WCAG contrast, harmonies, shades |
| [symbolfyi](https://symbolfyi.com/) | Symbol and character encoding (11 formats) |
| [unicodefyi](https://unicodefyi.com/) | Unicode character toolkit (17 encodings) |
| [fontfyi](https://fontfyi.com/) | Google Fonts metadata, CSS helpers, font pairings |
| [distancefyi](https://pypi.org/project/distancefyi/) | Haversine distance, bearing, travel times -- [distancefyi.com](https://distancefyi.com/) |
| [timefyi](https://pypi.org/project/timefyi/) | Timezone operations, time differences -- [timefyi.com](https://timefyi.com/) |
| [namefyi](https://pypi.org/project/namefyi/) | Korean romanization, Five Elements -- [namefyi.com](https://namefyi.com/) |
| [unitfyi](https://pypi.org/project/unitfyi/) | Unit conversion, 200 units, 20 categories -- [unitfyi.com](https://unitfyi.com/) |
| [holidayfyi](https://pypi.org/project/holidayfyi/) | Holiday dates, Easter calculation -- [holidayfyi.com](https://holidayfyi.com/) |

## Links

- [Emoji Browser](https://emojifyi.com/) -- Browse all 3,781 emojis online
- [Emoji Search](https://emojifyi.com/search/) -- Search emojis by name or keyword
- [Emoji Categories](https://emojifyi.com/category/) -- Browse emojis by category
- [Emoji Encoding Tools](https://emojifyi.com/tools/unicode-lookup/) -- Codepoint and encoding breakdown
- [Emoji Collections](https://emojifyi.com/collection/) -- Curated emoji collections
- [Emoji Versions](https://emojifyi.com/versions/) -- Unicode Emoji version history
- [API Documentation](https://emojifyi.com/developers/) -- REST API with free access
- [Source Code](https://github.com/fyipedia/emojifyi)

## License

MIT
