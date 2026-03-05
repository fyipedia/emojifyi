# emojifyi

[![PyPI](https://img.shields.io/pypi/v/emojifyi)](https://pypi.org/project/emojifyi/)
[![Python](https://img.shields.io/pypi/pyversions/emojifyi)](https://pypi.org/project/emojifyi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Pure Python emoji toolkit for developers. Encode any emoji into 8 representations, look up metadata for 3,781 emojis, search and browse by category -- all with zero dependencies. Includes a CLI, MCP server for AI assistants, and an API client for [emojifyi.com](https://emojifyi.com/).

> Browse all emojis at [emojifyi.com](https://emojifyi.com/) -- [search emojis](https://emojifyi.com/search/), [browse categories](https://emojifyi.com/category/), [emoji encoding tools](https://emojifyi.com/tools/unicode-lookup/), [emoji collections](https://emojifyi.com/collection/)

<p align="center">
  <img src="demo.gif" alt="emojifyi CLI demo" width="800">
</p>

## Table of Contents

- [Install](#install)
- [Quick Start](#quick-start)
- [Advanced Usage](#advanced-usage)
- [CLI](#cli)
- [MCP Server](#mcp-server)
- [API Client](#api-client)
- [API Reference](#api-reference)
  - [Encoding](#encoding)
  - [Lookup and Search](#lookup-and-search)
  - [Browse](#browse)
- [Data Types](#data-types)
- [Features](#features)
- [Learn More About Emoji](#learn-more-about-emoji)
- [FYIPedia Developer Tools](#fyipedia-developer-tools)
- [License](#license)

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

## Learn More About Emoji

- **Browse**: [Emoji Browser](https://emojifyi.com/) · [Search Emojis](https://emojifyi.com/search/) · [Categories](https://emojifyi.com/category/)
- **Tools**: [Unicode Lookup](https://emojifyi.com/tools/unicode-lookup/) · [Encoding Tool](https://emojifyi.com/tools/encoding/)
- **Collections**: [Emoji Collections](https://emojifyi.com/collection/) · [Versions](https://emojifyi.com/versions/)
- **API**: [REST API Docs](https://emojifyi.com/developers/) · [OpenAPI Spec](https://emojifyi.com/api/openapi.json)

## FYIPedia Developer Tools

Part of the [FYIPedia](https://fyipedia.com) open-source developer tools ecosystem.

| Package | PyPI | npm | Description |
|---------|------|-----|-------------|
| colorfyi | [PyPI](https://pypi.org/project/colorfyi/) | [npm](https://www.npmjs.com/package/@fyipedia/colorfyi) | Color conversion, WCAG contrast, harmonies -- [colorfyi.com](https://colorfyi.com/) |
| **emojifyi** | [PyPI](https://pypi.org/project/emojifyi/) | [npm](https://www.npmjs.com/package/emojifyi) | Emoji encoding & metadata for 3,781 emojis -- [emojifyi.com](https://emojifyi.com/) |
| symbolfyi | [PyPI](https://pypi.org/project/symbolfyi/) | [npm](https://www.npmjs.com/package/symbolfyi) | Symbol encoding in 11 formats -- [symbolfyi.com](https://symbolfyi.com/) |
| unicodefyi | [PyPI](https://pypi.org/project/unicodefyi/) | [npm](https://www.npmjs.com/package/unicodefyi) | Unicode lookup with 17 encodings -- [unicodefyi.com](https://unicodefyi.com/) |
| fontfyi | [PyPI](https://pypi.org/project/fontfyi/) | [npm](https://www.npmjs.com/package/fontfyi) | Google Fonts metadata & CSS -- [fontfyi.com](https://fontfyi.com/) |
| distancefyi | [PyPI](https://pypi.org/project/distancefyi/) | [npm](https://www.npmjs.com/package/distancefyi) | Haversine distance & travel times -- [distancefyi.com](https://distancefyi.com/) |
| timefyi | [PyPI](https://pypi.org/project/timefyi/) | [npm](https://www.npmjs.com/package/timefyi) | Timezone ops & business hours -- [timefyi.com](https://timefyi.com/) |
| namefyi | [PyPI](https://pypi.org/project/namefyi/) | [npm](https://www.npmjs.com/package/namefyi) | Korean romanization & Five Elements -- [namefyi.com](https://namefyi.com/) |
| unitfyi | [PyPI](https://pypi.org/project/unitfyi/) | [npm](https://www.npmjs.com/package/unitfyi) | Unit conversion, 220 units -- [unitfyi.com](https://unitfyi.com/) |
| holidayfyi | [PyPI](https://pypi.org/project/holidayfyi/) | [npm](https://www.npmjs.com/package/holidayfyi) | Holiday dates & Easter calculation -- [holidayfyi.com](https://holidayfyi.com/) |
| cocktailfyi | [PyPI](https://pypi.org/project/cocktailfyi/) | -- | Cocktail ABV, calories, flavor -- [cocktailfyi.com](https://cocktailfyi.com/) |
| fyipedia | [PyPI](https://pypi.org/project/fyipedia/) | -- | Unified CLI: `fyi color info FF6B35` -- [fyipedia.com](https://fyipedia.com/) |
| fyipedia-mcp | [PyPI](https://pypi.org/project/fyipedia-mcp/) | -- | Unified MCP hub for AI assistants -- [fyipedia.com](https://fyipedia.com/) |

## License

MIT
