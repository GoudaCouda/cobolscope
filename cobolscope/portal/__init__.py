"""
CobolScope Documentation Portal Module.
Generates an interactive, standalone HTML portal for navigating call graphs,
data dictionaries, and program metrics across a batch directory.
"""

from cobolscope.portal.generator import generate_portal

__all__ = ["generate_portal"]
