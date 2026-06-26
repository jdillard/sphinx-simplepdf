"""Theme stub whose apply_pdf_html_hooks returns None (should raise)."""

from os import path

from bs4 import BeautifulSoup


def get_scss_sources_path():
    return path.join(path.abspath(path.dirname(__file__)), "static", "styles", "sources")


def apply_pdf_html_hooks(soup: BeautifulSoup, app):
    return None


def setup(app):
    app.add_html_theme("stub_theme_returns_none", path.abspath(path.dirname(__file__)))
    return {"parallel_read_safe": True, "parallel_write_safe": True}
