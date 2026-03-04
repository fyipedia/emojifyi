"""Tests for emojifyi package."""

from __future__ import annotations

from emojifyi import (
    Category,
    EmojiInfo,
    EncodingResult,
    Subcategory,
    all_emojis,
    by_category,
    by_version,
    categories,
    char_to_codepoint,
    emoji_count,
    encode,
    encode_css,
    encode_html,
    encode_java,
    encode_javascript,
    encode_python,
    encode_utf8,
    encode_utf16,
    get_emoji,
    get_emoji_by_char,
    search,
    subcategories,
)


# =============================================================================
# Encoding — individual functions
# =============================================================================
class TestCharToCodepoint:
    def test_basic_emoji(self) -> None:
        assert char_to_codepoint("😀") == "U+1F600"

    def test_ascii(self) -> None:
        assert char_to_codepoint("A") == "U+0041"

    def test_zwj_sequence(self) -> None:
        # 👩‍💻 = U+1F469 U+200D U+1F4BB
        result = char_to_codepoint("👩\u200d💻")
        assert "U+1F469" in result
        assert "U+200D" in result
        assert "U+1F4BB" in result


class TestEncodeUTF8:
    def test_basic_emoji(self) -> None:
        assert encode_utf8("😀") == "0xF0 0x9F 0x98 0x80"

    def test_ascii(self) -> None:
        assert encode_utf8("A") == "0x41"


class TestEncodeUTF16:
    def test_surrogate_pair(self) -> None:
        assert encode_utf16("😀") == "0xD83D 0xDE00"

    def test_bmp_character(self) -> None:
        # ♠ = U+2660, no surrogate pair needed
        assert encode_utf16("♠") == "0x2660"


class TestEncodeHTML:
    def test_single_codepoint(self) -> None:
        assert encode_html("U+1F600") == "&#x1F600;"

    def test_multi_codepoint(self) -> None:
        assert encode_html("U+1F469 U+200D U+1F4BB") == "&#x1F469;&#x200D;&#x1F4BB;"


class TestEncodeCSS:
    def test_basic(self) -> None:
        assert encode_css("U+1F600") == "\\1F600"


class TestEncodePython:
    def test_basic(self) -> None:
        assert encode_python("U+1F600") == "\\U0001F600"

    def test_padding(self) -> None:
        # Should zero-pad to 8 characters
        assert encode_python("U+41") == "\\U00000041"


class TestEncodeJavaScript:
    def test_basic(self) -> None:
        assert encode_javascript("U+1F600") == "\\u{1F600}"


class TestEncodeJava:
    def test_surrogate_pair(self) -> None:
        assert encode_java("😀") == "\\uD83D\\uDE00"

    def test_bmp(self) -> None:
        assert encode_java("♠") == "\\u2660"


# =============================================================================
# Encoding — combined
# =============================================================================
class TestEncode:
    def test_returns_encoding_result(self) -> None:
        result = encode("😀")
        assert isinstance(result, EncodingResult)

    def test_all_fields(self) -> None:
        result = encode("😀")
        assert result.codepoint == "U+1F600"
        assert result.utf8_bytes == "0xF0 0x9F 0x98 0x80"
        assert result.utf16_surrogates == "0xD83D 0xDE00"
        assert result.html_entity == "&#x1F600;"
        assert result.css_content == "\\1F600"
        assert result.python_literal == "\\U0001F600"
        assert result.javascript_literal == "\\u{1F600}"
        assert result.java_literal == "\\uD83D\\uDE00"

    def test_zwj_sequence(self) -> None:
        # 👩‍💻 woman technologist
        result = encode("👩\u200d💻")
        assert "1F469" in result.codepoint
        assert "200D" in result.codepoint
        assert "&#x1F469;" in result.html_entity

    def test_flag_sequence(self) -> None:
        # 🇰🇷 = U+1F1F0 U+1F1F7
        result = encode("🇰🇷")
        assert "1F1F0" in result.codepoint
        assert "1F1F7" in result.codepoint


# =============================================================================
# Data — lookup
# =============================================================================
class TestGetEmoji:
    def test_by_slug(self) -> None:
        info = get_emoji("grinning-face")
        assert info is not None
        assert isinstance(info, EmojiInfo)
        assert info.character == "😀"
        assert info.codepoint == "U+1F600"
        assert info.category == "smileys-and-emotion"
        assert info.emoji_version == "1.0"

    def test_not_found(self) -> None:
        assert get_emoji("nonexistent-emoji-slug") is None

    def test_zwj_emoji(self) -> None:
        info = get_emoji("face-in-clouds")
        assert info is not None
        assert info.is_zwj is True
        assert info.emoji_type == "zwj"


class TestGetEmojiByChar:
    def test_by_character(self) -> None:
        info = get_emoji_by_char("😀")
        assert info is not None
        assert info.slug == "grinning-face"

    def test_not_found(self) -> None:
        assert get_emoji_by_char("X") is None


# =============================================================================
# Data — search
# =============================================================================
class TestSearch:
    def test_basic_search(self) -> None:
        results = search("grinning")
        assert len(results) > 0
        assert any(e.slug == "grinning-face" for e in results)

    def test_case_insensitive(self) -> None:
        results = search("HEART")
        assert len(results) > 0

    def test_limit(self) -> None:
        results = search("face", limit=5)
        assert len(results) <= 5

    def test_no_results(self) -> None:
        results = search("xyznonexistent")
        assert len(results) == 0


# =============================================================================
# Data — browse
# =============================================================================
class TestBrowse:
    def test_all_emojis(self) -> None:
        all_e = all_emojis()
        assert len(all_e) > 3000
        assert all(isinstance(e, EmojiInfo) for e in all_e[:10])

    def test_emoji_count(self) -> None:
        assert emoji_count() > 3000

    def test_by_category(self) -> None:
        smileys = by_category("smileys-and-emotion")
        assert len(smileys) > 0
        assert all(e.category == "smileys-and-emotion" for e in smileys)

    def test_by_version(self) -> None:
        v1 = by_version("1.0")
        assert len(v1) > 0
        assert all(e.emoji_version == "1.0" for e in v1)


# =============================================================================
# Data — categories
# =============================================================================
class TestCategories:
    def test_categories_count(self) -> None:
        cats = categories()
        assert len(cats) == 10
        assert all(isinstance(c, Category) for c in cats)

    def test_category_fields(self) -> None:
        cats = categories()
        smileys = next(c for c in cats if c.slug == "smileys-and-emotion")
        assert smileys.name == "Smileys & Emotion"
        assert smileys.icon == "😀"

    def test_subcategories_all(self) -> None:
        subs = subcategories()
        assert len(subs) == 100
        assert all(isinstance(s, Subcategory) for s in subs)

    def test_subcategories_filtered(self) -> None:
        subs = subcategories("smileys-and-emotion")
        assert len(subs) > 0
        assert all(s.category_slug == "smileys-and-emotion" for s in subs)


# =============================================================================
# Exports
# =============================================================================
class TestExports:
    def test_all_types(self) -> None:
        assert EncodingResult is not None
        assert EmojiInfo is not None
        assert Category is not None
        assert Subcategory is not None


# =============================================================================
# Edge cases
# =============================================================================
class TestEdgeCases:
    def test_search_limit_zero(self) -> None:
        results = search("heart", limit=0)
        assert len(results) == 0

    def test_search_empty_query(self) -> None:
        results = search("", limit=5)
        assert len(results) == 5  # matches everything

    def test_search_no_match(self) -> None:
        results = search("xyznonexistent123")
        assert len(results) == 0

    def test_get_emoji_none(self) -> None:
        assert get_emoji("this-does-not-exist-at-all") is None

    def test_get_emoji_by_char_none(self) -> None:
        assert get_emoji_by_char("X") is None

    def test_by_category_invalid(self) -> None:
        results = by_category("nonexistent-category")
        assert len(results) == 0

    def test_by_version_invalid(self) -> None:
        results = by_version("99.0")
        assert len(results) == 0

    def test_encode_ascii(self) -> None:
        result = encode("A")
        assert result.codepoint == "U+0041"
        assert result.html_entity == "&#x0041;"
