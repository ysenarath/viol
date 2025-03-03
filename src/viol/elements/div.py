from __future__ import annotations

from viol.core import AttrList, Element, Event, R

__all__ = ["Div"]


class Div(Element, prefix="div-"):
    def __init__(
        self,
        children: R | list[R] | None = None,
        attrs: AttrList = None,
        id: str | None = None,
        events: list[Event] | Event | None = None,
        _: str | None = None,
    ):
        super().__init__(
            tag="div",
            children=children,
            attrs=attrs,
            id=id,
            events=events,
            _=_,
        )
