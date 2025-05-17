from __future__ import annotations

from typing import Literal

from viol.core import AttrMultiDict, Element, EventHandler, RenderableType


class ListGroup(Element):
    """A Bootstrap list group."""

    def __init__(
        self,
        items: list[RenderableType],
        numbered: bool = False,
        horizontal: bool = False,
        horizontal_style: Literal["sm", "md", "lg", "xl", "xxl"] | None = None,
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
        self.attrs["class"] = ["list-group"]
        if numbered:
            self.attrs["class"].append("list-group-numbered")
        if horizontal:
            if horizontal_style:
                self.attrs["class"].append(f"list-group-horizontal-{horizontal_style}")
            else:
                self.attrs["class"].append("list-group-horizontal")

        for item in items:
            self.add_child(ListGroupItem(item))


class ListGroupItem(Element):
    """An item in a Bootstrap list group."""

    def __init__(
        self,
        content: RenderableType,
        active: bool = False,
        disabled: bool = False,
        color: Literal[
            "primary",
            "secondary",
            "success",
            "danger",
            "warning",
            "info",
            "light",
            "dark",
        ]
        | None = None,
        attrs: AttrMultiDict = None,
        events: list[EventHandler] | EventHandler | None = None,
        id: str | None = None,
        hyperscript: str | None = None,
    ):
        super().__init__(
            "li",
            children=content,
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
        )
        self.attrs["class"] = ["list-group-item"]
        if active:
            self.attrs["class"].append("active")
        if disabled:
            self.attrs["class"].append("disabled")
        if color:
            self.attrs["class"].append(f"list-group-item-{color}")
