"""
cobolscope.dictionary - Data Dictionary generator, type inference, and multi-format exporters.
"""

from .generator import (
    DataDictionaryGenerator,
    DictionaryRow,
    infer_logical_type,
    generate_data_dictionary,
)

__all__ = [
    "DataDictionaryGenerator",
    "DictionaryRow",
    "infer_logical_type",
    "generate_data_dictionary",
]
