from __future__ import annotations

from viol.core import Element

__all__ = [
    "Style",
]


class Style(Element):
    def __init__(self, children: str):
        super().__init__("style", children=children)
