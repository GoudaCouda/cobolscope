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
    aspx: bool = False,
) -> str:
    """
    Generate an interactive, standalone HTML documentation portal (index.html) or SharePoint ASPX page (portal.aspx).

    Args:
        manifest_or_path: Manifest dictionary, or path to manifest.json or directory containing manifest.json.
        output_path: Optional destination file path to write index.html or portal.aspx.
        title: Optional custom portal title.
        aspx: Whether to output as an ASP.NET / SharePoint compatible .aspx page.

    Returns:
        Rendered HTML/ASPX portal string.
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
                output_path = p / ("portal.aspx" if aspx else "index.html")
        else:
            if not p.exists():
                raise FileNotFoundError(f"Manifest file not found: {p}")
            manifest = json.loads(p.read_text(encoding="utf-8"))
            if not output_path:
                output_path = p.parent / ("portal.aspx" if aspx else "index.html")

    if not title:
        src_dir = manifest.get("batch_summary", {}).get("source_directory")
        title = Path(src_dir).name if src_dir else "COBOL Documentation Portal"

    is_aspx = aspx or (output_path is not None and str(output_path).lower().endswith(".aspx"))

    env = get_portal_jinja_env()
    template = env.get_template("portal.html.j2")
    content = template.render(
        manifest=manifest,
        title=title,
        aspx=is_aspx,
    )

    if output_path:
        out = Path(output_path).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")

        # When generating index.html, automatically generate companion portal.aspx for SharePoint
        if out.name.lower() == "index.html" and not aspx:
            aspx_path = out.parent / "portal.aspx"
            aspx_content = template.render(
                manifest=manifest,
                title=title,
                aspx=True,
            )
            aspx_path.write_text(aspx_content, encoding="utf-8")

    return content
