"""Dependency-free validation of the static portfolio and public boundaries."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
HTML = (DIST / "index.html").read_text(encoding="utf-8")
SITE_URL = "https://4sy8zwp9hz-netizen.github.io/matthew-chung-portfolio/"


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.elements = []
        self.feed(HTML)

    def handle_starttag(self, tag, attributes):
        self.elements.append((tag, dict(attributes)))


class SiteChecks(unittest.TestCase):
    def setUp(self):
        self.elements = Page().elements

    def test_local_assets_and_anchors_resolve(self):
        ids = [a["id"] for _, a in self.elements if "id" in a]
        self.assertEqual(len(ids), len(set(ids)))
        for tag, attrs in self.elements:
            for attribute in ("href", "src"):
                value = attrs.get(attribute)
                if not value:
                    continue
                url = urlsplit(value)
                if url.scheme:
                    continue
                if url.path:
                    target = (DIST / unquote(url.path)).resolve()
                    self.assertTrue(target.is_relative_to(DIST.resolve()), value)
                    self.assertTrue(target.is_file(), value)
                elif url.fragment:
                    self.assertIn(url.fragment, ids, value)

    def test_external_destinations_are_public_and_expected(self):
        allowed = {
            "github.com", "4sy8zwp9hz-netizen.github.io", "www.linkedin.com",
            "engineering-workspace-demo.holykungfu.chatgpt.site",
            "small-group-demo.orange-rat-4119.chatgpt.site",
        }
        for tag, attrs in self.elements:
            if tag != "a":
                continue
            url = urlsplit(attrs["href"])
            if url.scheme == "mailto":
                self.assertEqual(url.path, "matthewvchung@gmail.com")
            elif url.scheme:
                self.assertEqual(url.scheme, "https")
                self.assertIn(url.hostname, allowed)
                self.assertEqual(attrs.get("target"), "_blank")
                self.assertIn("noopener", attrs.get("rel", ""))

    def test_accessible_structure(self):
        self.assertEqual(sum(tag == "h1" for tag, _ in self.elements), 1)
        self.assertEqual(sum(tag == "main" for tag, _ in self.elements), 1)
        self.assertIn(("html", {"lang": "en"}), self.elements)
        for tag, attrs in self.elements:
            if tag == "img":
                self.assertTrue(attrs.get("alt"))
                self.assertIn("width", attrs)
                self.assertIn("height", attrs)
        self.assertIn("Skip to content", HTML)

    def test_project_site_base_path_and_metadata(self):
        canonical = [a["href"] for tag, a in self.elements
                     if tag == "link" and a.get("rel") == "canonical"]
        metadata = {a["property"]: a["content"] for tag, a in self.elements
                    if tag == "meta" and "property" in a}
        self.assertEqual(canonical, [SITE_URL])
        self.assertEqual(metadata["og:url"], SITE_URL)
        self.assertEqual(metadata["og:image"], SITE_URL + "assets/linked-wafer-maps.png")
        self.assertFalse(any(tag == "base" for tag, _ in self.elements))
        for _, attrs in self.elements:
            for attribute in ("href", "src"):
                value = attrs.get(attribute, "")
                if value and not urlsplit(value).scheme:
                    self.assertTrue(urljoin(SITE_URL, value).startswith(SITE_URL), value)

    def test_utf8_and_no_source_configuration_in_public_artifact(self):
        for path in DIST.rglob("*"):
            if path.suffix in {".html", ".css", ".svg"}:
                text = path.read_text(encoding="utf-8")
                self.assertNotIn("\ufffd", text, str(path))
                self.assertFalse(any(ord(c) < 32 and c not in "\n\r\t" for c in text), str(path))
        self.assertFalse((DIST / ".git").exists())
        self.assertFalse((DIST / ".openai").exists())
        self.assertFalse((DIST / "CNAME").exists())

    def test_github_near_top_and_both_flagships_present(self):
        hero = HTML.split('class="capability-strip')[0]
        self.assertGreaterEqual(hero.count("https://github.com/"), 2)
        self.assertIn("Manufacturing<br> Yield Platform", HTML)
        self.assertIn("Manufacturing<br> Application Platform", HTML)
        self.assertIn("Supplier qualification, technical audits", HTML)

    def test_scope_and_measurement_labels(self):
        for phrase in (
            "November 4, 2026", "stored test-parameter values", "of inspection history",
            "app opens &amp; reloads", "Sept 11–Nov 6, 2026", "manual failover",
            "anonymized observed data", "Independent fictional-data demo",
            "Separate browser-only demo", "No live group data",
        ):
            self.assertIn(phrase, HTML)

    def test_no_runtime_integrations_or_sensitive_patterns(self):
        self.assertFalse(any(tag in {"script", "iframe", "form"} for tag, _ in self.elements))
        self.assertIn("connect-src 'none'", HTML)
        for path in DIST.rglob("*"):
            if path.suffix not in {".html", ".css", ".svg"}:
                continue
            content = path.read_text(encoding="utf-8")
            self.assertNotRegex(content, r"(?:10|192\.168|172\.(?:1[6-9]|2[0-9]|3[01]))\.\d+\.\d+")
            self.assertNotRegex(content, r"(?:ghp_|github_pat_|sk-proj-)[A-Za-z0-9_]+")
            self.assertNotIn("C:\\Users", content)
            self.assertNotIn("aoi_apps_portal_server", content)

    def test_svg_well_formed_and_css_braces_balanced(self):
        for path in (DIST / "assets").glob("*.svg"):
            ET.parse(path)
        css = (DIST / "styles.css").read_text(encoding="utf-8")
        self.assertEqual(css.count("{"), css.count("}"))
        self.assertIn("prefers-reduced-motion", css)
        self.assertNotRegex(css, r"url\(\s*['\"]?https?://")


if __name__ == "__main__":
    unittest.main(verbosity=2)
