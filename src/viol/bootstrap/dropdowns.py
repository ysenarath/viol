from __future__ import annotations

from typing import Literal

from viol.core import AttrMultiDict, Element, EventHandler, RenderableType


class Dropdown(Element):
    """A Bootstrap dropdown."""

    def __init__(
        self,
        toggle: RenderableType,
        menu: list[RenderableType],
        direction: Literal["up", "down", "start", "end"] | None = None,
        attrs: AttrMultiDict = None,
        events: list[EventHandler] | EventHandler | None = None,
        id: str | None = None,
        hyperscript: str | None = None,
    ):
        super().__init__(
            "div",
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
        )
        self.attrs["class"] = ["dropdown"]
        if direction:
            self.attrs["class"].append(f"drop{direction}")

        toggle_element = DropdownToggle(toggle)
        menu_element = DropdownMenu(menu)
        self.children.append(toggle_element)
        self.children.append(menu_element)


class DropdownToggle(Element):
    """The toggle element for a Bootstrap dropdown."""

    def __init__(
        self,
        content: RenderableType,
        attrs: AttrMultiDict = None,
        events: list[EventHandler] | EventHandler | None = None,
        id: str | None = None,
        hyperscript: str | None = None,
    ):
        super().__init__(
            "button",
            children=content,
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
        )
        self.attrs["class"] = ["btn", "dropdown-toggle"]
        self.attrs["type"] = "button"
        self.attrs["data-bs-toggle"] = "dropdown"
        self.attrs["aria-expanded"] = "false"


class DropdownMenu(Element):
    """The menu for a Bootstrap dropdown."""

    def __init__(
        self,
        items: list[RenderableType],
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
        self.attrs["class"] = ["dropdown-menu"]
        for item in items:
            self.children.append(DropdownItem(item))


class DropdownItem(Element):
    """An item in a Bootstrap dropdown menu."""

    def __init__(
        self,
        content: RenderableType,
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
        item = Element("a", attrs={"class": ["dropdown-item"]}, children=content)
        self.children.append(item)
