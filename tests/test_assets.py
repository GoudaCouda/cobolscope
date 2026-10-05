"""
Test suite for CobolScope asset management, dual-mode bundling, and zero-CORS data islands.
Verifies air-gap offline readiness, CDN elimination, and file:// double-click compatibility.
"""

import json
import tempfile
import unittest
from pathlib import Path

from cobolscope.assets import (
    AssetMode,
    copy_static_assets,
    get_assets_dir,
    get_bundled_css,
    get_bundled_js,
    resolve_asset_mode,
)
from cobolscope.models import ParagraphNode, ProgramModel, SourceLocation
from cobolscope.graph import CallGraphGenerator, generate_call_graph


class TestAssetManagement(unittest.TestCase):
    """Verifies asset loading, mode resolution, and file copying."""

    def test_asset_mode_resolution(self):
        # Auto mode resolution
        self.assertEqual(resolve_asset_mode("auto", is_batch=False), AssetMode.INLINE)
        self.assertEqual(resolve_asset_mode("auto", is_batch=True), AssetMode.EXTERNAL)
        self.assertEqual(resolve_asset_mode(None, is_batch=False), AssetMode.INLINE)
        self.assertEqual(resolve_asset_mode(None, is_batch=True), AssetMode.EXTERNAL)

        # Explicit mode overrides
        self.assertEqual(resolve_asset_mode("inline", is_batch=True), AssetMode.INLINE)
        self.assertEqual(resolve_asset_mode("external", is_batch=False), AssetMode.EXTERNAL)
        self.assertEqual(resolve_asset_mode(AssetMode.INLINE, is_batch=True), AssetMode.INLINE)

    def test_bundled_assets_exist(self):
        assets_dir = get_assets_dir()
        self.assertTrue(assets_dir.exists())

        css = get_bundled_css()
        self.assertGreater(len(css), 1000)
        self.assertIn("--bg-primary", css)
        self.assertIn("workspace", css)

        js = get_bundled_js(monolithic=True)
        self.assertGreater(len(js), 100000)
        self.assertIn("CobolScope", js)
        self.assertIn("cytoscape", js)

    def test_copy_static_assets(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dest = Path(tmp_dir) / "assets"
            copied = copy_static_assets(dest)

            self.assertIn("cobolscope-viewer.bundle.js", copied)
            self.assertIn("cobolscope-viewer.css", copied)
            self.assertTrue(copied["cobolscope-viewer.bundle.js"].exists())
            self.assertTrue(copied["cobolscope-viewer.css"].exists())
            self.assertGreater(copied["cobolscope-viewer.bundle.js"].stat().st_size, 100000)
            self.assertGreater(copied["cobolscope-viewer.css"].stat().st_size, 1000)


class TestHtmlAssetEmbedding(unittest.TestCase):
    """Verifies call graph HTML rendering in inline vs external modes."""

    def setUp(self):
        p1 = ParagraphNode(
            name="1000-PROCESS",
            location=SourceLocation(start_line=10, end_line=20),
        )
        p2 = ParagraphNode(
            name="2000-CLEANUP",
            location=SourceLocation(start_line=25, end_line=35),
        )
        self.model = ProgramModel(
            program_id="TEST-ASSETS",
            paragraphs=[p1, p2],
            source_code="       IDENTIFICATION DIVISION.\n       PROGRAM-ID. TEST-ASSETS.\n",
        )

    def test_inline_mode_zero_cdn_and_self_contained(self):
        generator = CallGraphGenerator(self.model)
        html = generator.to_html(asset_mode="inline")

        # Zero external CDN links
        self.assertNotIn("https://cdnjs.cloudflare.com", html)
        self.assertNotIn("https://cdn.jsdelivr.net", html)

        # Embedded JSON data island
        self.assertIn('<script id="cobolscope-data" type="application/json">', html)
        self.assertIn("TEST-ASSETS", html)
        self.assertIn("1000-PROCESS", html)

        # Inlined JS runtime and CSS
        self.assertIn("CobolScope", html)
        self.assertIn("--bg-primary", html)

    def test_external_mode_relative_links(self):
        generator = CallGraphGenerator(self.model)
        html = generator.to_html(asset_mode="external", assets_rel_path="assets")

        # Zero external CDN links
        self.assertNotIn("https://cdnjs.cloudflare.com", html)
        self.assertNotIn("https://cdn.jsdelivr.net", html)

        # Relative links to local assets
        self.assertIn('href="assets/cobolscope-viewer.css"', html)
        self.assertIn('src="assets/cobolscope-viewer.bundle.js"', html)

        # Embedded JSON data island
        self.assertIn('<script id="cobolscope-data" type="application/json">', html)
        self.assertIn("TEST-ASSETS", html)

    def test_functional_api_asset_modes(self):
        # Default inline
        html_default = generate_call_graph(self.model, format="html")
        self.assertNotIn("https://cdnjs.cloudflare.com", html_default)
        self.assertIn('<script id="cobolscope-data" type="application/json">', html_default)

        # Explicit external
        html_ext = generate_call_graph(self.model, format="html", asset_mode="external")
        self.assertIn('src="assets/cobolscope-viewer.bundle.js"', html_ext)


if __name__ == "__main__":
    unittest.main()
