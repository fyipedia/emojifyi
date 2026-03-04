"""HTTP API client for emojifyi.com REST endpoints.

Requires the ``api`` extra: ``pip install emojifyi[api]``

Usage::

    from emojifyi.api import EmojiFYI

    with EmojiFYI() as api:
        info = api.emoji("grinning-face")
        print(info["character"])  # grinning face

        results = api.search("heart")
        for r in results["results"]:
            print(r["character"], r["cldr_name"])
"""

from __future__ import annotations

from typing import Any

import httpx


class EmojiFYI:
    """API client for the emojifyi.com REST API.

    Args:
        base_url: API base URL. Defaults to ``https://emojifyi.com/api``.
        timeout: Request timeout in seconds. Defaults to ``10.0``.
    """

    def __init__(
        self,
        base_url: str = "https://emojifyi.com/api",
        timeout: float = 10.0,
    ) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    # -- HTTP helpers ----------------------------------------------------------

    def _get(self, path: str, **params: Any) -> dict[str, Any]:
        resp = self._client.get(path, params={k: v for k, v in params.items() if v is not None})
        resp.raise_for_status()
        result: dict[str, Any] = resp.json()
        return result

    # -- Endpoints -------------------------------------------------------------

    def emoji(self, slug: str) -> dict[str, Any]:
        """Get full emoji details by slug.

        Args:
            slug: Emoji slug (e.g. ``"grinning-face"``).

        Returns:
            Dict with character, cldr_name, codepoint, category, encoding, etc.
        """
        return self._get(f"/emoji/{slug}/")

    def search(self, query: str) -> dict[str, Any]:
        """Search emojis by name, keywords, character, or codepoint.

        Args:
            query: Search term (e.g. ``"heart"``, ``"fire"``).

        Returns:
            Dict with results list and query string.
        """
        return self._get("/search/", q=query)

    def autocomplete(self, query: str) -> dict[str, Any]:
        """Get fast autocomplete suggestions.

        Args:
            query: Partial search term (minimum 2 characters).

        Returns:
            Dict with suggestions list.
        """
        return self._get("/autocomplete/", q=query)

    def category(self, slug: str) -> dict[str, Any]:
        """Get all emojis in a category.

        Args:
            slug: Category slug (e.g. ``"smileys-and-emotion"``).

        Returns:
            Dict with category name, slug, icon, and emojis list.
        """
        return self._get(f"/category/{slug}/")

    def categories(self) -> dict[str, Any]:
        """List all emoji categories with counts.

        Returns:
            Dict with count and categories list.
        """
        return self._get("/categories/")

    def collections(self) -> dict[str, Any]:
        """List all curated emoji collections.

        Returns:
            Dict with count and collections list.
        """
        return self._get("/collections/")

    def collection(self, slug: str) -> dict[str, Any]:
        """Get a curated emoji collection with its emojis.

        Args:
            slug: Collection slug (e.g. ``"love-romance"``).

        Returns:
            Dict with collection details and emojis list.
        """
        return self._get(f"/collection/{slug}/")

    def types(self) -> dict[str, Any]:
        """List emoji types (basic, ZWJ, flag, keycap, skin tone) with counts.

        Returns:
            Dict with count and types list.
        """
        return self._get("/types/")

    def versions(self) -> dict[str, Any]:
        """List all emoji versions from 0.6 to 16.0.

        Returns:
            Dict with count and versions list.
        """
        return self._get("/versions/")

    def years(self) -> dict[str, Any]:
        """Get emoji timeline by year.

        Returns:
            Dict with count and years list.
        """
        return self._get("/years/")

    def similar(self, slug: str) -> dict[str, Any]:
        """Find emojis similar to the given emoji.

        Args:
            slug: Emoji slug (e.g. ``"grinning-face"``).

        Returns:
            Dict with emoji info and similar emojis list.
        """
        return self._get(f"/emoji/{slug}/similar/")

    def random(self) -> dict[str, Any]:
        """Get a random emoji.

        Returns:
            Dict with character, cldr_name, slug, codepoint, url.
        """
        return self._get("/random/")

    # -- Context manager -------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP connection."""
        self._client.close()

    def __enter__(self) -> EmojiFYI:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
