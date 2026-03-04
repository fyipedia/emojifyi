# emojifyi

[![PyPI](https://img.shields.io/pypi/v/emojifyi)](https://pypi.org/project/emojifyi/)
[![Python](https://img.shields.io/pypi/pyversions/emojifyi)](https://pypi.org/project/emojifyi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Pure Python emoji toolkit for developers. Encode any emoji into 8 representations, look up metadata for 3,781 emojis, search and browse by category — all with zero dependencies.

> Browse all emojis at [emojifyi.com](https://emojifyi.com/)

## Install

```bash
pip install emojifyi
```

## Quick Start

```python
from emojifyi import encode, get_emoji, search

# Encode any emoji into 8 representations
result = encode("😀")
print(result.codepoint)         # U+1F600
print(result.utf8_bytes)        # 0xF0 0x9F 0x98 0x80
print(result.html_entity)       # &#x1F600;
print(result.css_content)       # \1F600
print(result.python_literal)    # \U0001F600
print(result.java_literal)      # \uD83D\uDE00

# Look up emoji metadata
info = get_emoji("red-heart")
print(info.character)           # ❤️
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
info = get_emoji_by_char("🔥")
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

### Lookup & Search

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

- **`EncodingResult`** — 8-field NamedTuple: codepoint, utf8_bytes, utf16_surrogates, html_entity, css_content, python_literal, javascript_literal, java_literal
- **`EmojiInfo`** — 12-field NamedTuple: character, slug, cldr_name, codepoint, category, subcategory, emoji_version, unicode_version, added_year, emoji_type, is_zwj, has_skin_tones
- **`Category`** — 4-field NamedTuple: slug, name, icon, order
- **`Subcategory`** — 4-field NamedTuple: slug, name, category_slug, order

## Features

- **8 encoding types**: UTF-8 bytes, UTF-16 surrogates, HTML entity, CSS content, Python/JavaScript/Java literals, codepoint
- **3,781 emojis**: Full Unicode Emoji 16.0 dataset with metadata
- **10 categories, 100 subcategories**: Browse and filter
- **ZWJ support**: Multi-codepoint sequences, flags, keycaps, skin tones
- **Zero dependencies**: Pure Python, bundled JSON data
- **Type-safe**: Full type annotations, `py.typed` marker (PEP 561)

## Related Packages

| Package | Description |
|---------|-------------|
| [colorfyi](https://github.com/fyipedia/colorfyi) | Color conversion, contrast, harmonies, shades |
| [fontfyi](https://github.com/fyipedia/fontfyi) | Google Fonts metadata, CSS helpers, font pairings |
| [symbolfyi](https://github.com/fyipedia/symbolfyi) | Symbol & character encoding (11 formats) |
| [unicodefyi](https://github.com/fyipedia/unicodefyi) | Unicode character toolkit (17 encodings) |

## Links

- [Emoji Browser](https://emojifyi.com/) — Browse all emojis online
- [API Documentation](https://emojifyi.com/developers/) — REST API with free access
- [Source Code](https://github.com/fyipedia/emojifyi)

## License

MIT
