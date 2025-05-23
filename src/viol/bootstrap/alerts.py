from __future__ import annotations

from typing_extensions import Literal

from viol.core import AttrMultiDict, Element, EventHandler, RenderableType

__all__ = [
    "Alert",
]

VariantType = Literal[
    "primary",
    "secondary",
    "success",
    "danger",
    "warning",
    "info",
    "light",
    "dark",
]


class CloseButton(Element):
    def __init__(
        self,
        attrs: AttrMultiDict = None,
        events: list[EventHandler] | EventHandler | None = None,
        id: str | None = None,
        hyperscript: str | None = None,
    ):
        super().__init__(
            "button",
            children=None,
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
        )
        self.attrs["type"] = "button"
        self.attrs["class"] = ["btn-close"]
        self.attrs["data-bs-dismiss"] = "alert"
        self.attrs["aria-label"] = "Close"


class Alert(Element):
    def __init__(
        self,
        children: RenderableType = None,
        variant: VariantType = "primary",
        dismissible: bool = True,
        attrs: AttrMultiDict = None,
        events: list[EventHandler] | EventHandler | None = None,
        id: str | None = None,
        hyperscript: str | None = None,
    ):
        if dismissible:
            children = [children, CloseButton()]
        super().__init__(
            "div",
            children=children,
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
        )
        self.attrs["role"] = "alert"
        self.attrs["class"] = ["alert", f"alert-{variant}"]
        if dismissible:
            self.attrs["class"] += ["alert-dismissible", "fade", "show"]
