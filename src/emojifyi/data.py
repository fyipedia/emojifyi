"""Emoji data bundle — 3,781 emojis from Unicode Emoji 16.0.

Loads emoji metadata from bundled JSON files. Data is lazy-loaded
on first access and cached in module-level variables.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, NamedTuple

_DATA_DIR = Path(__file__).parent / "_data"

# JSON row type alias
_Row = dict[str, Any]

# Lazy-loaded caches
_emojis: list[_Row] | None = None
_categories: list[_Row] | None = None
_subcategories: list[_Row] | None = None
_by_slug: dict[str, _Row] | None = None
_by_char: dict[str, _Row] | None = None


class EmojiInfo(NamedTuple):
    """Core emoji metadata."""

    codepoint: str
    character: str
    slug: str
    cldr_name: str
    category: str
    subcategory: str
    emoji_version: str
    unicode_version: str
    added_year: int
    emoji_type: str
    is_zwj: bool
    has_skin_tones: bool


class Category(NamedTuple):
    """Emoji category."""

    name: str
    slug: str
    icon: str
    order: int


class Subcategory(NamedTuple):
    """Emoji subcategory."""

    name: str
    slug: str
    category_slug: str
    order: int


def _load_emojis() -> list[_Row]:
    global _emojis
    if _emojis is None:
        with open(_DATA_DIR / "emojis.json", encoding="utf-8") as f:
            _emojis = json.load(f)
    return _emojis


def _load_categories() -> list[_Row]:
    global _categories
    if _categories is None:
        with open(_DATA_DIR / "categories.json", encoding="utf-8") as f:
            _categories = json.load(f)
    return _categories


def _load_subcategories() -> list[_Row]:
    global _subcategories
    if _subcategories is None:
        with open(_DATA_DIR / "subcategories.json", encoding="utf-8") as f:
            _subcategories = json.load(f)
    return _subcategories


def _build_slug_index() -> dict[str, _Row]:
    global _by_slug
    if _by_slug is None:
        _by_slug = {e["slug"]: e for e in _load_emojis()}
    return _by_slug


def _build_char_index() -> dict[str, _Row]:
    global _by_char
    if _by_char is None:
        _by_char = {e["character"]: e for e in _load_emojis()}
    return _by_char


def _to_emoji_info(raw: _Row) -> EmojiInfo:
    return EmojiInfo(
        codepoint=raw["codepoint"],
        character=raw["character"],
        slug=raw["slug"],
        cldr_name=raw["cldr_name"],
        category=raw["category_slug"],
        subcategory=raw["subcategory_slug"],
        emoji_version=raw["emoji_version"],
        unicode_version=raw["unicode_version"],
        added_year=raw["added_year"],
        emoji_type=raw["emoji_type"],
        is_zwj=raw["is_zwj"],
        has_skin_tones=raw["has_skin_tones"],
    )


def get_emoji(slug: str) -> EmojiInfo | None:
    """Look up an emoji by slug.

    >>> info = get_emoji("grinning-face")
    >>> info.character if info else None
    '😀'
    """
    raw = _build_slug_index().get(slug)
    return _to_emoji_info(raw) if raw else None


def get_emoji_by_char(character: str) -> EmojiInfo | None:
    """Look up an emoji by its character.

    >>> info = get_emoji_by_char("😀")
    >>> info.slug if info else None
    'grinning-face'
    """
    raw = _build_char_index().get(character)
    return _to_emoji_info(raw) if raw else None


def search(query: str, limit: int = 20) -> list[EmojiInfo]:
    """Search emojis by name (case-insensitive substring match).

    >>> results = search("grin")
    >>> len(results) > 0
    True
    """
    if limit <= 0:
        return []
    q = query.lower()
    results: list[EmojiInfo] = []
    for raw in _load_emojis():
        name: str = raw["cldr_name"]
        if q in name.lower():
            results.append(_to_emoji_info(raw))
            if len(results) >= limit:
                break
    return results


def all_emojis() -> list[EmojiInfo]:
    """Return all 3,781 emojis."""
    return [_to_emoji_info(raw) for raw in _load_emojis()]


def by_category(category_slug: str) -> list[EmojiInfo]:
    """Return all emojis in a category.

    >>> faces = by_category("smileys-and-emotion")
    >>> len(faces) > 0
    True
    """
    return [_to_emoji_info(raw) for raw in _load_emojis() if raw["category_slug"] == category_slug]


def by_version(version: str) -> list[EmojiInfo]:
    """Return all emojis added in a specific emoji version.

    >>> new = by_version("16.0")
    >>> all(e.emoji_version == "16.0" for e in new)
    True
    """
    return [_to_emoji_info(raw) for raw in _load_emojis() if raw["emoji_version"] == version]


def categories() -> list[Category]:
    """Return all 10 emoji categories."""
    return [
        Category(
            name=c["name"],
            slug=c["slug"],
            icon=c["icon"],
            order=c["order"],
        )
        for c in _load_categories()
    ]


def subcategories(category_slug: str | None = None) -> list[Subcategory]:
    """Return subcategories, optionally filtered by parent category."""
    result = []
    for sc in _load_subcategories():
        if category_slug and sc["category_slug"] != category_slug:
            continue
        result.append(
            Subcategory(
                name=sc["name"],
                slug=sc["slug"],
                category_slug=sc["category_slug"],
                order=sc["order"],
            )
        )
    return result


def emoji_count() -> int:
    """Total number of emojis in the dataset."""
    return len(_load_emojis())
