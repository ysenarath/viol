from __future__ import annotations

from typing_extensions import Literal

from viol.core import AttrList, Event, RenderableType
from viol.elements import Button, Div

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


class CloseButton(Button):
    def __init__(
        self,
        attrs: AttrList = None,
        id: str | None = None,
        events: list[Event] | Event | None = None,
        _: str | None = None,
    ):
        super().__init__(children=None, attrs=attrs, id=id, events=events, _=_)
        self.attrs["type"] = "button"
        self.attrs["class"] = "btn-close"
        self.attrs["data-bs-dismiss"] = "alert"
        self.attrs["aria-label"] = "Close"


class Alert(Div):
    def __init__(
        self,
        children: RenderableType = None,
        variant: VariantType = "primary",
        dismissible: bool = True,
        attrs: AttrList = None,
        id: str | None = None,
        events: list[Event] | Event | None = None,
        _: str | None = None,
    ):
        if dismissible:
            children = [children, CloseButton()]
        super().__init__(children=children, attrs=attrs, id=id, events=events, _=_)
        self.attrs["role"] = "alert"
        self.attrs["class"] = [
            "alert",
            f"alert-{variant}",
            ["alert-dismissible", "fade", "show"] if dismissible else [],
        ]
