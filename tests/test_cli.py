"""Tests for emojifyi.cli -- command-line interface."""

from __future__ import annotations

from typer.testing import CliRunner

from emojifyi.cli import app

runner = CliRunner()


class TestCLILookup:
    def test_lookup_by_slug(self) -> None:
        result = runner.invoke(app, ["lookup", "grinning-face"])
        assert result.exit_code == 0
        assert "grinning face" in result.output.lower()

    def test_lookup_not_found(self) -> None:
        result = runner.invoke(app, ["lookup", "nonexistent-slug"])
        assert result.exit_code == 1
        assert "not found" in result.output.lower()


class TestCLIChar:
    def test_char_lookup(self) -> None:
        result = runner.invoke(app, ["char", "\U0001f600"])
        assert result.exit_code == 0
        assert "grinning" in result.output.lower()

    def test_char_not_found(self) -> None:
        result = runner.invoke(app, ["char", "X"])
        assert result.exit_code == 1
        assert "not found" in result.output.lower()


class TestCLISearch:
    def test_search_results(self) -> None:
        result = runner.invoke(app, ["search", "heart"])
        assert result.exit_code == 0
        assert "heart" in result.output.lower()

    def test_search_no_results(self) -> None:
        result = runner.invoke(app, ["search", "xyznonexistent123"])
        assert result.exit_code == 0
        assert "no emojis found" in result.output.lower()

    def test_search_with_limit(self) -> None:
        result = runner.invoke(app, ["search", "face", "--limit", "3"])
        assert result.exit_code == 0


class TestCLIEncode:
    def test_encode_emoji(self) -> None:
        result = runner.invoke(app, ["encode", "\U0001f600"])
        assert result.exit_code == 0
        assert "U+1F600" in result.output
        assert "UTF-8" in result.output
        assert "HTML" in result.output


class TestCLICategories:
    def test_categories(self) -> None:
        result = runner.invoke(app, ["categories"])
        assert result.exit_code == 0
        assert "Smileys" in result.output


class TestCLIBrowse:
    def test_browse_category(self) -> None:
        result = runner.invoke(app, ["browse", "smileys-and-emotion"])
        assert result.exit_code == 0
        assert "smileys-and-emotion" in result.output.lower()

    def test_browse_invalid_category(self) -> None:
        result = runner.invoke(app, ["browse", "nonexistent-category"])
        assert result.exit_code == 0
        assert "no emojis found" in result.output.lower()


class TestCLIStats:
    def test_stats(self) -> None:
        result = runner.invoke(app, ["stats"])
        assert result.exit_code == 0
        assert "Total" in result.output
        assert "Categories" in result.output


class TestCLINoArgs:
    def test_no_args_shows_help(self) -> None:
        result = runner.invoke(app, [])
        # Typer no_args_is_help=True returns exit code 0 or 2 depending on version
        assert result.exit_code in (0, 2)
        assert "Usage" in result.output or "emojifyi" in result.output.lower()
