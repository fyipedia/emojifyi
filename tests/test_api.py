"""Tests for emojifyi.api -- HTTP client for emojifyi.com."""

from __future__ import annotations

from emojifyi.api import EmojiFYI


class TestEmojiFYIClient:
    """Verify the client initializes and has all expected methods."""

    def test_init_default(self) -> None:
        client = EmojiFYI()
        assert str(client._client.base_url) == "https://emojifyi.com/api/"
        client.close()

    def test_init_custom_url(self) -> None:
        client = EmojiFYI(base_url="http://localhost:8006/api", timeout=5.0)
        assert "localhost" in str(client._client.base_url)
        client.close()

    def test_context_manager(self) -> None:
        with EmojiFYI() as client:
            assert client is not None

    def test_has_all_methods(self) -> None:
        client = EmojiFYI()
        methods = [
            "emoji",
            "search",
            "autocomplete",
            "category",
            "categories",
            "collections",
            "collection",
            "types",
            "versions",
            "years",
            "similar",
            "random",
        ]
        for method in methods:
            assert hasattr(client, method), f"Missing method: {method}"
            assert callable(getattr(client, method))
        client.close()
