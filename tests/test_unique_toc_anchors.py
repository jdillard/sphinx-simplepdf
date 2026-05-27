"""Tests for unique section anchors in merged simplepdf HTML."""

from __future__ import annotations

from collections import Counter
import re
from unittest.mock import MagicMock

from bs4 import BeautifulSoup
from bs4.element import Tag
import pytest

import tests._weasyprint_mock  # noqa: F401  # must load before sphinx_simplepdf

from .utils import build_and_capture_stdout


def _collect_html_ids(html: str) -> list[str]:
    return re.findall(r'\bid="([^"]+)"', html)


def _sidebar_toc_hrefs(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    sidebar = soup.find("div", class_="sphinxsidebarwrapper")
    if not isinstance(sidebar, Tag):
        return []
    links = sidebar.find_all("a", class_="reference internal")
    return [link.get("href", "") for link in links if link.get("href")]


def _normalize_toc_href(href: str, root_doc: str = "index") -> str:
    return href.replace(f"{root_doc}.html", "")


@pytest.fixture(autouse=True)
def _mock_weasyprint(monkeypatch):
    """Allow simplepdf builds without native WeasyPrint libraries."""
    monkeypatch.setattr(
        "sphinx_simplepdf.builders.simplepdf.subprocess.check_output",
        lambda *args, **kwargs: "",
    )
    monkeypatch.setattr(
        "sphinx_simplepdf.builders.simplepdf.weasyprint.HTML",
        MagicMock(),
    )


def test_merged_html_has_no_duplicate_ids(sphinx_build, capsys):
    result = build_and_capture_stdout(
        sphinx_build,
        capsys,
        srcdir="with_duplicate_sections",
        confoverrides={"simplepdf_use_weasyprint_api": True},
    )

    html = result.html_content("index")
    ids = _collect_html_ids(html)
    duplicates = [id_ for id_, count in Counter(ids).items() if count > 1]

    assert duplicates == [], f"duplicate id attributes found: {duplicates}"


def test_sidebar_toc_hrefs_resolve_to_unique_anchors(sphinx_build, capsys):
    result = build_and_capture_stdout(
        sphinx_build,
        capsys,
        srcdir="with_duplicate_sections",
        confoverrides={"simplepdf_use_weasyprint_api": True},
    )

    html = result.html_content("index")
    ids = set(_collect_html_ids(html))

    toc_hrefs = [_normalize_toc_href(href) for href in _sidebar_toc_hrefs(html)]
    section_hrefs = [href for href in toc_hrefs if re.match(r"^#/[^#]+/#", href)]

    assert section_hrefs, "expected sidebar TOC section links"

    for href in section_hrefs:
        anchor = href[1:]  # strip leading '#'
        assert anchor in ids, f"TOC href {href!r} does not match any element id"
        assert html.count(f'id="{anchor}"') == 1, f"anchor {anchor!r} is not unique in HTML"
