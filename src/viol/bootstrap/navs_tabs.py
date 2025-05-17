from __future__ import annotations

from typing import Literal

from viol.core import AttrMultiDict, Element, EventHandler, RenderableType


class Nav(Element):
    """A Bootstrap nav component."""

    def __init__(
        self,
        items: list[RenderableType],
        variant: Literal["tabs", "pills"] = "tabs",
        justified: bool = False,
        fill: bool = False,
        attrs: AttrMultiDict = None,
        events: list[EventHandler] | EventHandler | None = None,
        id: str | None = None,
        hyperscript: str | None = None,
    ):
        super().__init__(
            "ul",
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
        )
        self.attrs["class"] = ["nav", f"nav-{variant}"]
        if justified:
            self.attrs["class"].append("nav-justified")
        if fill:
            self.attrs["class"].append("nav-fill")

        for item in items:
            nav_item = NavItem(item)
            self.children.append(nav_item)


class NavItem(Element):
    """An item in a Bootstrap nav."""

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
        self.attrs["class"] = ["nav-item"]
        link = Element("a", attrs={"class": ["nav-link"]}, children=content)
        if active:
            link.attrs["class"].append("active")
            link.attrs["aria-current"] = "page"
        if disabled:
            link.attrs["class"].append("disabled")
            link.attrs["aria-disabled"] = "true"
        self.children.append(link)
