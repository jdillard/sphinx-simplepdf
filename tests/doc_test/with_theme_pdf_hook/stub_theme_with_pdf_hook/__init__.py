"""External theme stub with apply_pdf_html_hooks for tests."""

from os import path

from bs4 import BeautifulSoup


def get_scss_sources_path():
    return path.join(path.abspath(path.dirname(__file__)), "static", "styles", "sources")


def apply_pdf_html_hooks(soup: BeautifulSoup, app) -> BeautifulSoup:
    body = soup.find("body")
    if body is not None:
        marker = soup.new_tag("div", id="theme-pdf-hook-applied")
        body.insert(0, marker)
    return soup


def setup(app):
    app.add_html_theme("stub_theme_with_pdf_hook", path.abspath(path.dirname(__file__)))
    return {"parallel_read_safe": True, "parallel_write_safe": True}
