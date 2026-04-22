"""Tests for the docs Sphinx configuration helpers."""

from __future__ import annotations

import importlib.util
import os
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CONF_PATH = REPO_ROOT / "docs" / "source" / "conf.py"


def _load_conf_module():
    """Load ``docs/source/conf.py`` without initializing autodoc."""

    spec = importlib.util.spec_from_file_location("evennia_docs_conf_test", CONF_PATH)
    module = importlib.util.module_from_spec(spec)
    original_noautodoc = os.environ.get("NOAUTODOC")
    os.environ["NOAUTODOC"] = "1"
    try:
        assert spec.loader is not None
        spec.loader.exec_module(module)
    finally:
        if original_noautodoc is None:
            os.environ.pop("NOAUTODOC", None)
        else:
            os.environ["NOAUTODOC"] = original_noautodoc
    return module


class TestDocsConf(unittest.TestCase):
    """Verify the fork-specific docs configuration behavior."""

    @classmethod
    def setUpClass(cls):
        """Load the docs configuration once for all tests."""

        cls.conf = _load_conf_module()

    def test_version_context_uses_single_latest_release(self):
        """The version sidebar should only expose the latest docs root."""

        context = {}

        self.conf.add_doc_versions_to_html_page_context(
            app=None,
            pagename="index",
            templatename="page.html",
            context=context,
            doctree=None,
        )

        self.assertEqual(
            context["versions"],
            [{"release": "latest", "label": "current", "url": "https://evennia.jakeuj.com/"}],
        )
        self.assertEqual(context["legacy_versions"], [])
        self.assertFalse(context["current_is_legacy"])

    def test_url_resolver_rewrites_existing_official_docs_links(self):
        """Known local docs pages should point to the custom domain."""

        source = [
            "[docs](https://www.evennia.com/docs/latest/Coding/Setting-up-PyCharm.html#requirements)"
        ]

        self.conf.url_resolver(app=None, docname="index", source=source)

        self.assertEqual(
            source[0],
            "[docs](https://evennia.jakeuj.com/Coding/Setting-up-PyCharm.html#requirements)",
        )

    def test_url_resolver_keeps_missing_official_docs_links_external(self):
        """Unknown docs pages should keep pointing at upstream."""

        source = ["[docs](https://www.evennia.com/docs/latest/Does-Not-Exist.html)"]

        self.conf.url_resolver(app=None, docname="index", source=source)

        self.assertEqual(
            source[0], "[docs](https://www.evennia.com/docs/latest/Does-Not-Exist.html)"
        )
