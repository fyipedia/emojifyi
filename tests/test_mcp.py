"""Tests for emojifyi.mcp_server -- MCP tools."""

from __future__ import annotations

from emojifyi.mcp_server import (
    emoji_by_category,
    emoji_by_char,
    emoji_categories,
    emoji_encode,
    emoji_lookup,
    emoji_search,
)


class TestMCPEmojiLookup:
    def test_lookup_by_slug(self) -> None:
        result = emoji_lookup("grinning-face")
        assert "grinning face" in result.lower()
        assert "U+1F600" in result
        assert "smileys-and-emotion" in result

    def test_lookup_not_found(self) -> None:
        result = emoji_lookup("nonexistent-slug-xyz")
        assert "not found" in result.lower()


class TestMCPEmojiByChar:
    def test_by_character(self) -> None:
        result = emoji_by_char("\U0001f600")
        assert "grinning face" in result.lower()
        assert "U+1F600" in result

    def test_by_character_not_found(self) -> None:
        result = emoji_by_char("X")
        assert "not found" in result.lower()


class TestMCPEmojiSearch:
    def test_search_results(self) -> None:
        result = emoji_search("heart")
        assert "heart" in result.lower()
        assert "Search" in result
        assert "|" in result  # markdown table

    def test_search_no_results(self) -> None:
        result = emoji_search("xyznonexistent123")
        assert "No emojis found" in result

    def test_search_with_limit(self) -> None:
        result = emoji_search("face", limit=3)
        # Count table rows (excluding header)
        lines = [line for line in result.strip().split("\n") if line.startswith("|")]
        # Header + separator + data rows
        data_rows = len(lines) - 2
        assert data_rows <= 3


class TestMCPEmojiEncode:
    def test_encode_emoji(self) -> None:
        result = emoji_encode("\U0001f600")
        assert "U+1F600" in result
        assert "UTF-8" in result
        assert "HTML Entity" in result
        assert "CSS Content" in result
        assert "Python" in result
        assert "JavaScript" in result
        assert "Java" in result


class TestMCPEmojiCategories:
    def test_categories(self) -> None:
        result = emoji_categories()
        assert "Emoji Categories" in result
        assert "Smileys" in result
        assert "|" in result  # markdown table


class TestMCPEmojiByCategory:
    def test_browse_category(self) -> None:
        result = emoji_by_category("smileys-and-emotion")
        assert "smileys-and-emotion" in result
        assert "|" in result

    def test_browse_invalid_category(self) -> None:
        result = emoji_by_category("nonexistent-category")
        assert "No emojis found" in result
