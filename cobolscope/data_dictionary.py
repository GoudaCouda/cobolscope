"""
Backward-compatibility proxy for cobolscope.dictionary.
"""

from cobolscope.dictionary import (
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
