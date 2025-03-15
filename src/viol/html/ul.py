from __future__ import annotations

from viol.core import AttrList, Element, Event, RenderableType

__all__ = [
    "Ul",
]


class Ul(Element):
    def __init__(
        self,
        children: RenderableType = None,
        attrs: AttrList = None,
        id: str | None = None,
        events: list[Event] | Event | None = None,
        _: str | None = None,
    ):
        super().__init__(
            tag="ul", children=children, attrs=attrs, id=id, events=events, _=_
        )
