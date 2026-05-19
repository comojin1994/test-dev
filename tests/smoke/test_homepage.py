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
JS_FILE = ROOT / "scripts.js"


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


@pytest.fixture(scope="module")
def css_source() -> str:
    return CSS_FILE.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def js_source() -> str:
    return JS_FILE.read_text(encoding="utf-8")


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

    def test_footer_year_span_exists(self, html_source):
        assert 'id="footer-year"' in html_source, (
            "<span id=\"footer-year\"> must exist for JS to populate current year"
        )

    def test_scripts_js_linked(self, html_source):
        assert 'src="scripts.js"' in html_source, (
            "scripts.js must be linked from index.html"
        )

    def test_scripts_js_file_exists(self):
        assert JS_FILE.exists(), "scripts.js must exist at project root"

    def test_footer_has_fallback_year(self, html_source):
        match = re.search(
            r'<span id="footer-year">\s*(\b20\d{2}\b)\s*</span>',
            html_source,
        )
        assert match, (
            "Footer year span must contain a 4-digit fallback year (e.g. 2026)"
        )

    def test_back_to_top_button_present(self, html_source):
        assert 'id="back-to-top"' in html_source, (
            "<button id=\"back-to-top\"> must exist in index.html"
        )

    def test_back_to_top_has_aria_label(self, html_source):
        assert 'aria-label="맨 위로 이동"' in html_source, (
            "Back-to-top button must expose Korean aria-label for a11y"
        )

    def test_back_to_top_styles_defined(self, css_source):
        assert "#back-to-top" in css_source, (
            "styles.css must define #back-to-top rules"
        )
        assert ".is-visible" in css_source, (
            "styles.css must define .is-visible toggle rule"
        )

    def test_back_to_top_script_logic(self, js_source):
        assert "back-to-top" in js_source, (
            "scripts.js must reference back-to-top element"
        )
        assert "scrollTo" in js_source, (
            "scripts.js must call window.scrollTo for smooth scroll"
        )

    def test_viewport_meta_present(self, html_source):
        assert '<meta name="viewport"' in html_source, (
            "Responsive viewport meta tag must be present in <head>"
        )

    def test_nav_links_match_section_ids(self, html_source, parsed):
        import re
        block = re.search(
            r'<ul class="nav-links">(.*?)</ul>', html_source, re.S
        )
        assert block, "<ul class=\"nav-links\"> block not found"
        hrefs = re.findall(r'href="#([^"]+)"', block.group(1))
        assert hrefs, "nav-links must contain at least one anchor href"
        missing = [h for h in hrefs if h not in parsed.ids]
        assert not missing, (
            f"Nav links point to missing section ids: {missing}"
        )

    def test_scripts_loaded_with_defer(self, html_source):
        assert '<script defer src="scripts.js"></script>' in html_source, (
            "scripts.js must be loaded with defer attribute"
        )

    def test_css_design_tokens_defined(self, css_source):
        assert '--color-primary:' in css_source, (
            "styles.css must define --color-primary design token"
        )
        assert '--color-bg:' in css_source, (
            "styles.css must define --color-bg design token"
        )
