"""Smoke tests for the static homepage (index.html).

Verifies required sections exist and internal anchor links are consistent.
"""
import pathlib
import re
from html.parser import HTMLParser

import pytest

ROOT = pathlib.Path(__file__).parent.parent.parent
HTML_FILE = ROOT / "index.html"
CSS_FILE = ROOT / "styles.css"


class _AnchorCollector(HTMLParser):
    """Collects all id attributes and href="#..." links in an HTML document."""

    def __init__(self):
        super().__init__()
        self.ids: set[str] = set()
        self.anchor_hrefs: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if "id" in attrs_dict:
            self.ids.add(attrs_dict["id"])
        if tag == "a" and "href" in attrs_dict:
            href = attrs_dict["href"]
            if href.startswith("#") and href != "#":
                self.anchor_hrefs.append(href[1:])


@pytest.fixture(scope="module")
def html_source() -> str:
    return HTML_FILE.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def parsed(html_source) -> _AnchorCollector:
    collector = _AnchorCollector()
    collector.feed(html_source)
    return collector


@pytest.mark.smoke
class TestHomepageStructure:
    def test_html_file_exists(self):
        assert HTML_FILE.exists(), "index.html must exist"

    def test_css_file_exists(self):
        assert CSS_FILE.exists(), "styles.css must exist"

    def test_required_sections_present(self, html_source):
        required_ids = ["about", "features", "contact"]
        for section_id in required_ids:
            assert f'id="{section_id}"' in html_source, (
                f"Section #{section_id} missing from index.html"
            )

    def test_internal_anchor_links_resolve(self, parsed):
        """Every #anchor href must point to an existing id in the document."""
        broken = [href for href in parsed.anchor_hrefs if href not in parsed.ids]
        assert not broken, f"Broken internal anchor links: {broken}"

    def test_page_has_title(self, html_source):
        assert "<title>" in html_source and "</title>" in html_source

    def test_css_linked(self, html_source):
        assert 'href="styles.css"' in html_source
