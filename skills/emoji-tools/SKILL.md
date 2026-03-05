---
name: emoji-tools
description: Look up emoji metadata, encode emojis into 8 formats (UTF-8, HTML, CSS, JS, Java), search 3,953 emojis from Unicode Emoji 16.0.
---

# Emoji Tools

Emoji lookup, encoding, and search powered by [emojifyi](https://emojifyi.com/) -- a pure Python emoji toolkit with bundled data for all 3,953 Unicode Emoji 16.0 characters.

## Setup

Install the MCP server:

```bash
pip install "emojifyi[mcp]"
```

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

## Available Tools

| Tool | Description |
|------|-------------|
| `emoji_lookup` | Get emoji metadata by slug or character |
| `emoji_search` | Search emojis by name or keyword |
| `emoji_encode` | Encode any emoji into 8 formats (UTF-8, UTF-16, HTML, CSS, Python, JS, Java) |
| `emoji_categories` | List all 10 emoji categories |
| `emoji_by_category` | Browse emojis in a specific category |
| `emoji_stats` | Dataset statistics (total count, categories, subcategories) |

## When to Use

- Finding the right emoji for a message or UI element
- Getting emoji codepoints or HTML entities for web development
- Encoding emojis for different programming languages
- Browsing emoji categories or searching by keyword
- Looking up emoji metadata (version, type, ZWJ status)

## Demo

![EmojiFYI CLI Demo](https://raw.githubusercontent.com/fyipedia/emojifyi/main/demo.gif)

## Links

- [Emoji Browser](https://emojifyi.com/emojis/)
- [Emoji Search](https://emojifyi.com/search/)
- [API Documentation](https://emojifyi.com/developers/)
- [PyPI Package](https://pypi.org/project/emojifyi/)
