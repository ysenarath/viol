from __future__ import annotations

from typing import Literal

from viol.core import AttrMultiDict, Element, EventHandler, RenderableType


class Progress(Element):
    """A Bootstrap progress bar."""

    def __init__(
        self,
        value_now: int,
        value_min: int = 0,
        value_max: int = 100,
        height: str | None = None,
        striped: bool = False,
        animated: bool = False,
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
        label: RenderableType | None = None,
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
        self.attrs["class"] = ["progress"]
        self.attrs["role"] = "progressbar"
        self.attrs["aria-valuenow"] = str(value_now)
        self.attrs["aria-valuemin"] = str(value_min)
        self.attrs["aria-valuemax"] = str(value_max)

        bar = Element("div", attrs={"class": ["progress-bar"]})
        bar.attrs["style"] = f"width: {value_now}%"
        if color:
            bar.attrs["class"].append(f"bg-{color}")
        if striped:
            bar.attrs["class"].append("progress-bar-striped")
        if animated:
            bar.attrs["class"].append("progress-bar-animated")
        if label:
            bar.children.append(label)
        if height:
            self.attrs["style"] = f"height: {height}"

        self.children.append(bar)
