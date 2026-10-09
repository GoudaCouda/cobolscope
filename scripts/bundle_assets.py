"""
Build script to download and package CobolScope frontend assets.
Produces vendor.bundle.js, cobolscope-viewer.css, cobolscope-viewer.js,
and the monolithic cobolscope-viewer.bundle.js in cobolscope/templates/assets/.
"""

import os
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = REPO_ROOT / "cobolscope" / "templates" / "assets"
TEMPLATES_CG = REPO_ROOT / "cobolscope" / "templates" / "call_graph"

VENDOR_URLS = [
    ("cytoscape.min.js", "https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.28.1/cytoscape.min.js"),
    ("dagre.min.js", "https://cdn.jsdelivr.net/npm/dagre@0.8.5/dist/dagre.min.js"),
    ("cytoscape-dagre.min.js", "https://cdn.jsdelivr.net/npm/cytoscape-dagre@2.5.0/cytoscape-dagre.min.js"),
    ("elk.bundled.js", "https://cdn.jsdelivr.net/npm/elkjs@0.9.3/lib/elk.bundled.js"),
    ("cytoscape-elk.min.js", "https://cdn.jsdelivr.net/npm/cytoscape-elk@2.1.0/dist/cytoscape-elk.min.js"),
]

def main():
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Writing assets to: {ASSETS_DIR}")

    # 1. Download vendor scripts
    vendor_contents = []
    for filename, url in VENDOR_URLS:
        cache_file = ASSETS_DIR / filename
        if not cache_file.exists() or cache_file.stat().st_size == 0:
            print(f"Downloading {filename} from {url}...")
            req = urllib.request.Request(url, headers={"User-Agent": "CobolScope-Asset-Builder/1.0"})
            with urllib.request.urlopen(req) as resp:
                data = resp.read()
            cache_file.write_bytes(data)
            print(f"  Saved {filename} ({len(data)} bytes)")
        else:
            print(f"Using cached {filename} ({cache_file.stat().st_size} bytes)")
        vendor_contents.append(cache_file.read_text(encoding="utf-8"))

    # 2. Assemble vendor.bundle.js
    vendor_bundle = "\n;\n".join(vendor_contents)
    (ASSETS_DIR / "vendor.bundle.js").write_text(vendor_bundle, encoding="utf-8")
    print(f"Generated vendor.bundle.js ({len(vendor_bundle)} characters)")

    # 3. Assemble cobolscope-viewer.css
    css_files = [
        TEMPLATES_CG / "styles.css.j2",
        TEMPLATES_CG / "splitters.css.j2",
        TEMPLATES_CG / "inspector.css.j2",
        TEMPLATES_CG / "modals.css.j2",
        TEMPLATES_CG / "code_viewer.css.j2",
    ]
    css_parts = []
    # Base reset and root variables
    css_parts.append("""
:root {
  --bg-primary: #F4F6F8;
  --bg-surface: #FFFFFF;
  --surface-hover: #ECEFF2;
  --border-color: #D3D9E0;
  --border-subtle: #E8ECEF;
  --text-primary: #1A202C;
  --text-secondary: #4A5568;
  --text-muted: #718096;
  --primary: #0056B3;
  --primary-hover: #004494;
  --primary-light: #EBF3FC;
  --primary-border: #BCD7F5;
  --sidebar-width: 380px;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
}
""")
    for cf in css_files:
        if cf.exists():
            text = cf.read_text(encoding="utf-8")
            # Strip any jinja includes if present
            lines = [l for l in text.splitlines() if not l.strip().startswith("{% include")]
            css_parts.append("\n".join(lines))

    combined_css = "\n\n".join(css_parts)
    (ASSETS_DIR / "cobolscope-viewer.css").write_text(combined_css, encoding="utf-8")
    print(f"Generated cobolscope-viewer.css ({len(combined_css)} characters)")

    # 4. Assemble cobolscope-viewer.js
    js_parts = []
    js_parts.append("""
/**
 * CobolScope Interactive Call Graph Viewer Runtime Engine
 * Encapsulated client runtime for Cytoscape, ELK, Dagre, Inspector, and Code Viewer.
 */
(function(window, document) {
  'use strict';

  // Safe iframe detection (no cross-origin exceptions)
  try {
    if (window.self !== window.top) {
      document.documentElement.classList.add("in-portal-iframe");
    }
  } catch (e) {
    document.documentElement.classList.add("in-portal-iframe");
  }

  // Escape HTML helper (preserves quotes for code viewing parity)
  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }
  window.escapeHtml = escapeHtml;

  // Module-level shared variables accessible to all components
  let graphData = {};
  let cytoElements = [];
  let canonicalElements = [];
  let clonedElements = [];
  let initialEnableCloning = false;
  let layoutHeuristics = {};
  let initialEnginePreference = "cytoscape";
  let sourceCodeRaw = "";

  let currentEngine = "cytoscape";
  let selectedRoutineNode = null;
  let cy = null;
  let cyLevel3 = null;
  let cyContainer = null;
  let layoutSelect = null;
  let cytoLayoutGroup = null;

  // Pre-populate data from #cobolscope-data if already in DOM
  function populateDataIsland() {
    const dataEl = document.getElementById("cobolscope-data");
    if (!dataEl) return false;
    try {
      const payload = JSON.parse(dataEl.textContent);
      graphData = payload.graph || {};
      cytoElements = payload.cytoElements || [];
      canonicalElements = payload.canonicalElements || [];
      clonedElements = payload.clonedElements || [];
      initialEnableCloning = !!payload.initialEnableCloning;
      layoutHeuristics = payload.layoutHeuristics || {};
      initialEnginePreference = payload.initialEnginePreference || "cytoscape";
      sourceCodeRaw = payload.sourceCodeRaw || "";

      currentEngine = initialEnginePreference;
      selectedRoutineNode = null;
      cyContainer = document.getElementById("cy-container");
      layoutSelect = document.getElementById("layoutSelect");
      cytoLayoutGroup = document.getElementById("cytoLayoutGroup");

      // Expose to window for backward compatibility and debugging
      window.graphData = graphData;
      window.cytoElements = cytoElements;
      window.canonicalElements = canonicalElements;
      window.clonedElements = clonedElements;
      window.sourceCodeRaw = sourceCodeRaw;
      window.selectedRoutineNode = selectedRoutineNode;
      window.cyContainer = cyContainer;
      window.layoutSelect = layoutSelect;
      window.cytoLayoutGroup = cytoLayoutGroup;
      return true;
    } catch(e) {
      console.error("[CobolScope] Failed to parse JSON data island:", e);
      return false;
    }
  }

  // Populate data island immediately if elements exist
  populateDataIsland();
""")

    # Append client logic modules
    js_modules = [
        "diagnostics.js.j2",
        "cyto_call_graph.js.j2",
        "linear_card.js.j2",
        "inspector.js.j2",
        "linear_modal.js.j2",
        "level3_cfg.js.j2",
        "toolbar.js.j2",
        "code_viewer.js.j2",
    ]

    for jm in js_modules:
        p = TEMPLATES_CG / "js" / jm
        if p.exists():
            js_parts.append(f"\n/* --- {jm} --- */\n")
            js_parts.append(p.read_text(encoding="utf-8"))

    # Mount / Init Controller
    js_parts.append("""

  // -------------------------------------------------------------
  // CobolScope Global Controller & Auto-Init
  // -------------------------------------------------------------
  const CobolScope = {
    version: "0.1.0",
    isInitialized: false,

    init: function() {
      if (this.isInitialized) return;
      populateDataIsland();
      if (typeof bootstrapCallGraph === 'function') {
        bootstrapCallGraph();
      } else if (typeof initCytoscape === 'function') {
        initCytoscape();
      }
      this.isInitialized = true;
    }
  };

  window.CobolScope = CobolScope;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => CobolScope.init());
  } else {
    CobolScope.init();
  }

})(window, document);
""")

    viewer_js = "\n".join(js_parts)
    (ASSETS_DIR / "cobolscope-viewer.js").write_text(viewer_js, encoding="utf-8")
    print(f"Generated cobolscope-viewer.js ({len(viewer_js)} characters)")

    # 5. Assemble monolithic cobolscope-viewer.bundle.js
    monolithic = vendor_bundle + "\n\n;\n\n" + viewer_js
    (ASSETS_DIR / "cobolscope-viewer.bundle.js").write_text(monolithic, encoding="utf-8")
    print(f"Generated monolithic cobolscope-viewer.bundle.js ({len(monolithic)} characters)")

if __name__ == "__main__":
    main()
