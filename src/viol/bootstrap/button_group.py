from __future__ import annotations

from viol.core import AttrMultiDict, Element, EventHandler, RenderableType


class ButtonGroup(Element):
    def __init__(
        self,
        children: RenderableType | list[RenderableType] | None = None,
        aria_label: str | None = None,
        attrs: AttrMultiDict = None,
        events: list[EventHandler] | EventHandler | None = None,
        id: str | None = None,
        hyperscript: str | None = None,
    ):
        super().__init__(
            "div",
            children=children,
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
        )
        self.attrs["class"] = ["btn-group"]
        # role
        self.attrs["role"] = "group"
        # aria-label
        if aria_label:
            self.attrs["aria-label"] = aria_label
        # aria-labelledby
        if id:
            self.attrs["aria-labelledby"] = id
