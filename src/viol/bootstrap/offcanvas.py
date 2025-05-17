from __future__ import annotations

from typing import Literal

from src.viol.bootstrap.close_button import CloseButton
from viol.core import AttrMultiDict, Element, EventHandler, RenderableType


class Offcanvas(Element):
    """A Bootstrap offcanvas."""

    def __init__(
        self,
        title: RenderableType,
        body: RenderableType,
        placement: Literal["start", "end", "top", "bottom"] = "start",
        scroll: bool = False,
        backdrop: bool | Literal["static"] = True,
        keyboard: bool = True,
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
        self.attrs["class"] = ["offcanvas", f"offcanvas-{placement}"]
        self.attrs["tabindex"] = "-1"
        self.attrs["aria-labelledby"] = f"{id}Label" if id else None
        if scroll:
            self.attrs["data-bs-scroll"] = "true"
        if backdrop is True:
            self.attrs["data-bs-backdrop"] = "true"
        elif backdrop == "static":
            self.attrs["data-bs-backdrop"] = "static"
        if not keyboard:
            self.attrs["data-bs-keyboard"] = "false"

        header = OffcanvasHeader(title=title, offcanvas_id=id)
        body_element = OffcanvasBody(body)
        self.children.append(header)
        self.children.append(body_element)


class OffcanvasHeader(Element):
    """The header for a Bootstrap offcanvas."""

    def __init__(
        self,
        title: RenderableType,
        offcanvas_id: str | None = None,
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
        self.attrs["class"] = ["offcanvas-header"]
        title_element = Element(
            "h5",
            attrs={
                "class": ["offcanvas-title"],
                "id": f"{offcanvas_id}Label" if offcanvas_id else None,
            },
            children=title,
        )
        close_button = CloseButton(
            attrs={"data-bs-dismiss": "offcanvas", "aria-label": "Close"}
        )
        self.children.append(title_element)
        self.children.append(close_button)


class OffcanvasBody(Element):
    """The body for a Bootstrap offcanvas."""

    def __init__(
        self,
        content: RenderableType,
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
        self.attrs["class"] = ["offcanvas-body"]
