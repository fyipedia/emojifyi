"""HTTP API client for emojifyi.com REST endpoints.

Requires the ``api`` extra: ``pip install emojifyi[api]``

Usage::

    from emojifyi.api import EmojiFYI

    with EmojiFYI() as api:
        items = api.list_categories()
        detail = api.get_category("example-slug")
        results = api.search("query")
"""

from __future__ import annotations

from typing import Any

import httpx


class EmojiFYI:
    """API client for the emojifyi.com REST API.

    Provides typed access to all emojifyi.com endpoints including
    list, detail, and search operations.

    Args:
        base_url: API base URL. Defaults to ``https://emojifyi.com``.
        timeout: Request timeout in seconds. Defaults to ``10.0``.
    """

    def __init__(
        self,
        base_url: str = "https://emojifyi.com",
        timeout: float = 10.0,
    ) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def _get(self, path: str, **params: Any) -> dict[str, Any]:
        resp = self._client.get(
            path,
            params={k: v for k, v in params.items() if v is not None},
        )
        resp.raise_for_status()
        result: dict[str, Any] = resp.json()
        return result

    # -- Endpoints -----------------------------------------------------------

    def list_categories(self, **params: Any) -> dict[str, Any]:
        """List all categories."""
        return self._get("/api/v1/categories/", **params)

    def get_category(self, slug: str) -> dict[str, Any]:
        """Get category by slug."""
        return self._get(f"/api/v1/categories/" + slug + "/")

    def list_emojis(self, **params: Any) -> dict[str, Any]:
        """List all emojis."""
        return self._get("/api/v1/emojis/", **params)

    def get_emoji(self, slug: str) -> dict[str, Any]:
        """Get emoji by slug."""
        return self._get(f"/api/v1/emojis/" + slug + "/")

    def list_faqs(self, **params: Any) -> dict[str, Any]:
        """List all faqs."""
        return self._get("/api/v1/faqs/", **params)

    def get_faq(self, slug: str) -> dict[str, Any]:
        """Get faq by slug."""
        return self._get(f"/api/v1/faqs/" + slug + "/")

    def list_glossary(self, **params: Any) -> dict[str, Any]:
        """List all glossary."""
        return self._get("/api/v1/glossary/", **params)

    def get_term(self, slug: str) -> dict[str, Any]:
        """Get term by slug."""
        return self._get(f"/api/v1/glossary/" + slug + "/")

    def list_stories(self, **params: Any) -> dict[str, Any]:
        """List all stories."""
        return self._get("/api/v1/stories/", **params)

    def get_story(self, slug: str) -> dict[str, Any]:
        """Get story by slug."""
        return self._get(f"/api/v1/stories/" + slug + "/")

    def search(self, query: str, **params: Any) -> dict[str, Any]:
        """Search across all content."""
        return self._get(f"/api/v1/search/", q=query, **params)

    # -- Lifecycle -----------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self) -> EmojiFYI:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
