from __future__ import annotations

from viol.core import AttrMultiDict, Element, EventHandler


class CloseButton(Element):
    """A Bootstrap close button."""

    def __init__(
        self,
        aria_label: str = "Close",
        white: bool = False,
        attrs: AttrMultiDict = None,
        events: list[EventHandler] | EventHandler | None = None,
        id: str | None = None,
        hyperscript: str | None = None,
    ):
        super().__init__(
            "button",
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
        )
        self.attrs["type"] = "button"
        self.attrs["class"] = ["btn-close"]
        self.attrs["aria-label"] = aria_label
        if white:
            self.attrs["class"].append("btn-close-white")
