"""Test project for theme apply_pdf_html_hooks."""

project = "ThemePdfHookTest"
extensions = ["sphinx_simplepdf"]
master_doc = "index"
exclude_patterns = ["_build"]

simplepdf_theme = "stub_theme_with_pdf_hook"
simplepdf_theme_options = {"notoc": True}
