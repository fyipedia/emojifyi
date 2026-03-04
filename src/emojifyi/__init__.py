"""emojifyi — Pure Python emoji toolkit for developers.

Encode any emoji into 8 representations (UTF-8, UTF-16, HTML, CSS,
Python, JavaScript, Java), look up emoji metadata, and search
3,781 emojis from Unicode Emoji 16.0.

Zero dependencies. Bundled emoji data.

Usage::

    from emojifyi import encode, get_emoji, search

    # Encode any emoji
    result = encode("😀")
    print(result.utf8_bytes)      # 0xF0 0x9F 0x98 0x80
    print(result.html_entity)     # &#x1F600;
    print(result.java_literal)    # \\uD83D\\uDE00

    # Look up emoji metadata
    info = get_emoji("grinning-face")
    print(info.character)         # 😀
    print(info.category)          # smileys-and-emotion

    # Search emojis
    results = search("heart")
    for emoji in results[:5]:
        print(f"{emoji.character} {emoji.cldr_name}")
"""

from emojifyi.data import (
    Category,
    EmojiInfo,
    Subcategory,
    all_emojis,
    by_category,
    by_version,
    categories,
    emoji_count,
    get_emoji,
    get_emoji_by_char,
    search,
    subcategories,
)
from emojifyi.encoding import (
    EncodingResult,
    char_to_codepoint,
    encode,
    encode_css,
    encode_html,
    encode_java,
    encode_javascript,
    encode_python,
    encode_utf8,
    encode_utf16,
)

__version__ = "0.2.0"

__all__ = [
    # Encoding types
    "EncodingResult",
    # Encoding functions
    "encode",
    "char_to_codepoint",
    "encode_utf8",
    "encode_utf16",
    "encode_html",
    "encode_css",
    "encode_python",
    "encode_javascript",
    "encode_java",
    # Data types
    "EmojiInfo",
    "Category",
    "Subcategory",
    # Lookup
    "get_emoji",
    "get_emoji_by_char",
    # Search & browse
    "search",
    "all_emojis",
    "by_category",
    "by_version",
    "categories",
    "subcategories",
    "emoji_count",
]
