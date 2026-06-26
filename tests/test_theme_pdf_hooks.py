"""Tests for theme apply_pdf_html_hooks convention."""

import pytest
from sphinx.errors import ExtensionError

from .utils import build_and_capture_stdout


def test_theme_pdf_hook_runs(sphinx_build, capsys):
    result = build_and_capture_stdout(sphinx_build, capsys, srcdir="with_theme_pdf_hook")

    assert result.pdf_exists()
    assert not result.has_warnings("ERROR:")
    assert result.outdir is not None
    index_html = (result.outdir / "index.html").read_text(encoding="utf-8")
    assert 'id="theme-pdf-hook-applied"' in index_html


def test_theme_pdf_hook_returns_none_raises(sphinx_build):
    with pytest.raises(ExtensionError, match="apply_pdf_html_hooks returned None"):
        sphinx_build(
            srcdir="with_theme_pdf_hook",
            confoverrides={"simplepdf_theme": "stub_theme_returns_none"},
        ).build()
