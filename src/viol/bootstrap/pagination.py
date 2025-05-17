from __future__ import annotations

from typing import Literal

from viol.core import AttrMultiDict, Element, EventHandler, RenderableType


class Pagination(Element):
    """A Bootstrap pagination component."""

    def __init__(
        self,
        items: list[RenderableType],
        size: Literal["sm", "lg"] | None = None,
        alignment: Literal["start", "center", "end"] | None = None,
        attrs: AttrMultiDict = None,
        events: list[EventHandler] | EventHandler | None = None,
        id: str | None = None,
        hyperscript: str | None = None,
    ):
        super().__init__(
            "nav",
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
        )
        self.attrs["aria-label"] = "Page navigation"
        ol = Element("ul", attrs={"class": ["pagination"]})

        if size:
            ol.attrs["class"].append(f"pagination-{size}")
        if alignment == "start":
            ol.attrs["class"].append("justify-content-start")
        elif alignment == "center":
            ol.attrs["class"].append("justify-content-center")
        elif alignment == "end":
            ol.attrs["class"].append("justify-content-end")

        for item in items:
            ol.children.append(PaginationItem(item))
        self.children.append(ol)


class PaginationItem(Element):
    """An item in a Bootstrap pagination."""

    def __init__(
        self,
        content: RenderableType,
        active: bool = False,
        disabled: bool = False,
        attrs: AttrMultiDict = None,
        events: list[EventHandler] | EventHandler | None = None,
        id: str | None = None,
        hyperscript: str | None = None,
    ):
        super().__init__(
            "li",
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
        )
        self.attrs["class"] = ["page-item"]
        link = Element("a", attrs={"class": ["page-link"]}, children=content)
        if active:
            self.attrs["class"].append("active")
            link.attrs["aria-current"] = "page"
        if disabled:
            self.attrs["class"].append("disabled")
        self.children.append(link)
