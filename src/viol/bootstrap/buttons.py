from __future__ import annotations

from typing import Literal

from viol.core import AttrMultiDict, Element, EventHandler

__all__ = ["Button"]

C = Literal[
    "primary",
    "secondary",
    "success",
    "danger",
    "warning",
    "info",
    "light",
    "dark",
    "link",
]


class Button(Element):
    """A Bootstrap button."""

    def __init__(
        self,
        text: str,
        color: C | None = "primary",
        size: Literal["sm", "md", "lg"] | None = None,
        disabled: bool = False,
        active: bool = False,
        type: Literal["button", "submit", "reset"] = "button",
        tag: Literal["button", "a", "input"] | None = "button",
        href: str | None = None,
        outline: bool = False,
        attrs: AttrMultiDict = None,
        events: list[EventHandler] | EventHandler | None = None,
        id: str | None = None,
        hyperscript: str | None = None,
    ):
        super().__init__(
            "a" if href else tag,
            children=text if tag != "input" else None,
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
        )
        if tag == "input":
            self.attrs["value"] = text
        if href:
            self.attrs["href"] = href
            self.attrs["role"] = "button"
        else:
            self.attrs["type"] = type
        self.attrs["class"] = ["btn"]
        if color:
            if outline:
                self.attrs["class"].append(f"btn-outline-{color}")
            else:
                self.attrs["class"].append(f"btn-{color}")
        if size and size != "md":
            self.attrs["class"].append(f"btn-{size}")
        if disabled:
            if href or tag == "a":
                self.attrs["aria-disabled"] = "true"
                self.attrs["tabindex"] = "-1"
                self.attrs.class_.append("disabled")
            else:
                self.attrs["disabled"] = True
        # active
        if active:
            self.attrs["class"].append("active")
            self.attrs["aria-current"] = "page"
