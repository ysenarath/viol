from __future__ import annotations

from viol.core import AttrList, Element, Event, RenderableType

__all__ = [
    "H1",
    "H2",
    "H3",
    "H4",
    "H5",
    "H6",
    "Header",
]


class Header(Element):
    def __init__(
        self,
        children: RenderableType | list[RenderableType] | None = None,
        level: int = 1,
        attrs: AttrList = None,
        id: str | None = None,
        events: list[Event] | Event | None = None,
        _: str | None = None,
    ):
        super().__init__(
            tag=f"h{level}",
            children=children,
            attrs=attrs,
            id=id,
            events=events,
            _=_,
        )


class HeaderBuilder:
    def __init__(self, level: int):
        self.level = level

    def __call__(
        self,
        children: RenderableType | list[RenderableType] | None = None,
        attrs: AttrList = None,
        id: str | None = None,
        events: list[Event] | Event | None = None,
        _: str | None = None,
    ) -> Header:
        return Header(
            children=children,
            level=self.level,
            attrs=attrs,
            id=id,
            events=events,
            _=_,
        )


H1 = HeaderBuilder(1)
H2 = HeaderBuilder(2)
H3 = HeaderBuilder(3)
H4 = HeaderBuilder(4)
H5 = HeaderBuilder(5)
H6 = HeaderBuilder(6)
