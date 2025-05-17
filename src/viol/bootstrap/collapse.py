from __future__ import annotations

from viol.core import AttrMultiDict, Element, EventHandler, RenderableType


class Collapse(Element):
    """A Bootstrap collapse component."""

    def __init__(
        self,
        content: RenderableType,
        horizontal: bool = False,
        show: bool = False,
        attrs: AttrMultiDict = None,
        events: list[EventHandler] | EventHandler | None = None,
        id: str | None = None,
        hyperscript: str | None = None,
    ):
        super().__init__(
            "div",
            children=content,
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
        )
        self.attrs["class"] = ["collapse"]
        if horizontal:
            self.attrs["class"].append("collapse-horizontal")
        if show:
            self.attrs["class"].append("show")
