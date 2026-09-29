"""
Portal generator module for creating standalone HTML documentation portals.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional, Union
import jinja2


def get_portal_jinja_env() -> jinja2.Environment:
    """Returns a configured Jinja2 environment for portal rendering."""
    template_dir = Path(__file__).resolve().parent.parent / "templates"
    try:
        loader = jinja2.PackageLoader("cobolscope", "templates")
    except Exception:
        loader = jinja2.FileSystemLoader(str(template_dir))

    return jinja2.Environment(
        loader=loader,
        autoescape=jinja2.select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def generate_portal(
    manifest_or_path: Union[Dict[str, Any], str, Path],
    output_path: Optional[Union[str, Path]] = None,
    title: Optional[str] = None,
) -> str:
    """
    Generate an interactive, standalone HTML documentation portal (index.html).

    Args:
        manifest_or_path: Manifest dictionary, or path to manifest.json or directory containing manifest.json.
        output_path: Optional destination file path to write index.html.
        title: Optional custom portal title.

    Returns:
        Rendered HTML portal string.
    """
    if isinstance(manifest_or_path, dict):
        manifest = manifest_or_path
    else:
        p = Path(manifest_or_path).resolve()
        if p.is_dir():
            mf = p / "manifest.json"
            if not mf.exists():
                raise FileNotFoundError(f"Manifest not found in directory: {p}")
            manifest = json.loads(mf.read_text(encoding="utf-8"))
            if not output_path:
                output_path = p / "index.html"
        else:
            if not p.exists():
                raise FileNotFoundError(f"Manifest file not found: {p}")
            manifest = json.loads(p.read_text(encoding="utf-8"))
            if not output_path:
                output_path = p.parent / "index.html"

    if not title:
        src_dir = manifest.get("batch_summary", {}).get("source_directory")
        title = Path(src_dir).name if src_dir else "COBOL Documentation Portal"

    env = get_portal_jinja_env()
    template = env.get_template("portal.html.j2")
    content = template.render(
        manifest=manifest,
        title=title,
    )

    if output_path:
        out = Path(output_path).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")

    return content
