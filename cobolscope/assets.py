"""
cobolscope.assets
~~~~~~~~~~~~~~~~

Static asset management, vendoring, and dual-mode bundling for CobolScope documentation.
Supports air-gapped zero-dependency inlining (single-file mode) and shared relative asset
directories (batch portal mode).
"""

from __future__ import annotations

import enum
import shutil
from pathlib import Path
from typing import Dict, Optional, Union


class AssetMode(str, enum.Enum):
    """Asset distribution strategy for generated HTML documents."""
    AUTO = "auto"
    INLINE = "inline"
    EXTERNAL = "external"

    @classmethod
    def from_str(cls, value: Optional[Union[str, AssetMode]]) -> AssetMode:
        if isinstance(value, AssetMode):
            return value
        if not value:
            return cls.AUTO
        val = str(value).lower().strip()
        for member in cls:
            if member.value == val:
                return member
        return cls.AUTO


def get_assets_dir() -> Path:
    """Returns the absolute path to the packaged static assets directory."""
    pkg_assets = Path(__file__).resolve().parent / "templates" / "assets"
    if pkg_assets.exists():
        return pkg_assets
    # Fallback to dev workspace
    dev_assets = Path(__file__).resolve().parent.parent / "cobolscope" / "templates" / "assets"
    return dev_assets


def get_bundled_css() -> str:
    """Loads and returns the combined CSS bundle for inlining."""
    css_file = get_assets_dir() / "cobolscope-viewer.css"
    if css_file.exists():
        return css_file.read_text(encoding="utf-8")
    return ""


def get_bundled_js(monolithic: bool = True) -> str:
    """Loads and returns the combined JavaScript bundle for inlining."""
    assets_dir = get_assets_dir()
    js_file = assets_dir / ("cobolscope-viewer.bundle.js" if monolithic else "cobolscope-viewer.js")
    if js_file.exists():
        return js_file.read_text(encoding="utf-8")
    return ""


def copy_static_assets(destination_dir: Union[str, Path]) -> Dict[str, Path]:
    """
    Copies pre-bundled CSS and JS assets into the destination directory.
    Typically called during batch documentation generation to populate `site/assets/`.

    Returns:
        Dict mapping asset name to the destination Path.
    """
    dest = Path(destination_dir).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    src_dir = get_assets_dir()

    copied: Dict[str, Path] = {}
    files_to_copy = [
        "cobolscope-viewer.bundle.js",
        "cobolscope-viewer.css",
        "cobolscope-viewer.js",
        "vendor.bundle.js",
    ]

    for fname in files_to_copy:
        src = src_dir / fname
        if src.exists():
            target = dest / fname
            shutil.copy2(src, target)
            copied[fname] = target

    return copied


def resolve_asset_mode(
    mode: Optional[Union[str, AssetMode]] = None,
    is_batch: bool = False,
    output_path: Optional[Union[str, Path]] = None,
) -> AssetMode:
    """
    Resolves the effective asset mode.
    - AUTO defaults to INLINE for single-file mode (maximizing portability).
    - AUTO defaults to EXTERNAL for batch mode (sharing assets across programs).
    - Explicit INLINE or EXTERNAL overrides defaults.
    """
    resolved = AssetMode.from_str(mode)
    if resolved == AssetMode.AUTO:
        if is_batch:
            return AssetMode.EXTERNAL
        return AssetMode.INLINE
    return resolved
