from __future__ import annotations

from viol.core import AttrList, Element, Event, R


class Button(Element, prefix="btn-"):
    def __init__(
        self,
        children: R | list[R] | None = None,
        attrs: AttrList = None,
        id: str | None = None,
        events: list[Event] | Event | None = None,
        _: str | None = None,
    ):
        super().__init__(
            tag="button",
            children=children,
            attrs=attrs,
            id=id,
            events=events,
            _=_,
        )
