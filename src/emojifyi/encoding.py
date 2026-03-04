"""Emoji encoding engine — compute 8 encoding representations for any character.

Pure Python, zero dependencies. Works with single emojis, ZWJ sequences,
keycap sequences, flags, and any Unicode character.
"""

from __future__ import annotations

from typing import NamedTuple


class EncodingResult(NamedTuple):
    """All 8 encoding representations for a character."""

    codepoint: str
    utf8_bytes: str
    utf16_surrogates: str
    html_entity: str
    css_content: str
    python_literal: str
    javascript_literal: str
    java_literal: str


def char_to_codepoint(character: str) -> str:
    """Convert a character (possibly multi-codepoint) to 'U+XXXX' notation.

    >>> char_to_codepoint("😀")
    'U+1F600'
    >>> char_to_codepoint("👩\u200d💻")
    'U+1F469 U+200D U+1F4BB'
    """
    return " ".join(f"U+{ord(c):04X}" for c in character)


def encode_utf8(character: str) -> str:
    """UTF-8 byte representation.

    >>> encode_utf8("😀")
    '0xF0 0x9F 0x98 0x80'
    """
    return " ".join(f"0x{b:02X}" for b in character.encode("utf-8"))


def encode_utf16(character: str) -> str:
    """UTF-16 surrogate pair representation.

    >>> encode_utf16("😀")
    '0xD83D 0xDE00'
    """
    encoded = character.encode("utf-16-le")
    return " ".join(f"0x{encoded[i + 1]:02X}{encoded[i]:02X}" for i in range(0, len(encoded), 2))


def encode_html(codepoint: str) -> str:
    r"""HTML entity representation.

    >>> encode_html("U+1F600")
    '&#x1F600;'
    >>> encode_html("U+1F469 U+200D U+1F4BB")
    '&#x1F469;&#x200D;&#x1F4BB;'
    """
    cps = codepoint.split()
    return "".join(f"&#x{cp.replace('U+', '')};" for cp in cps)


def encode_css(codepoint: str) -> str:
    r"""CSS content property value.

    >>> encode_css("U+1F600")
    '\\1F600'
    """
    cps = codepoint.split()
    return "".join(f"\\{cp.replace('U+', '')}" for cp in cps)


def encode_python(codepoint: str) -> str:
    r"""Python string literal.

    >>> encode_python("U+1F600")
    '\\U0001F600'
    """
    cps = codepoint.split()
    return "".join(f"\\U{cp.replace('U+', '').zfill(8)}" for cp in cps)


def encode_javascript(codepoint: str) -> str:
    r"""JavaScript string literal.

    >>> encode_javascript("U+1F600")
    '\\u{1F600}'
    """
    cps = codepoint.split()
    return "".join(f"\\u{{{cp.replace('U+', '')}}}" for cp in cps)


def encode_java(character: str) -> str:
    r"""Java string literal with surrogate pairs.

    >>> encode_java("😀")
    '\\uD83D\\uDE00'
    """
    encoded = character.encode("utf-16-le")
    parts = []
    for i in range(0, len(encoded), 2):
        code_unit = encoded[i] | (encoded[i + 1] << 8)
        parts.append(f"\\u{code_unit:04X}")
    return "".join(parts)


def encode(character: str) -> EncodingResult:
    """Compute all 8 encoding representations for a character.

    Works with any Unicode character: single emojis, ZWJ sequences,
    flags, keycaps, or plain text characters.

    >>> result = encode("😀")
    >>> result.codepoint
    'U+1F600'
    >>> result.utf8_bytes
    '0xF0 0x9F 0x98 0x80'
    >>> result.html_entity
    '&#x1F600;'
    """
    codepoint = char_to_codepoint(character)
    return EncodingResult(
        codepoint=codepoint,
        utf8_bytes=encode_utf8(character),
        utf16_surrogates=encode_utf16(character),
        html_entity=encode_html(codepoint),
        css_content=encode_css(codepoint),
        python_literal=encode_python(codepoint),
        javascript_literal=encode_javascript(codepoint),
        java_literal=encode_java(character),
    )
