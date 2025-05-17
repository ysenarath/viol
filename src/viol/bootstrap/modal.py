from __future__ import annotations

from typing import Literal

from src.viol.bootstrap.close_button import CloseButton
from viol.core import AttrMultiDict, Element, EventHandler, RenderableType


class Modal(Element):
    """A Bootstrap modal."""

    def __init__(
        self,
        title: RenderableType,
        body: RenderableType,
        footer: RenderableType | None = None,
        size: Literal["sm", "lg", "xl"] | None = None,
        scrollable: bool = False,
        centered: bool = False,
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
        self.attrs["class"] = ["modal", "fade"]
        self.attrs["tabindex"] = "-1"
        self.attrs["aria-hidden"] = "true"

        dialog_attrs = AttrMultiDict({"class": ["modal-dialog"]})
        if size:
            dialog_attrs["class"].append(f"modal-dialog-{size}")
        if scrollable:
            dialog_attrs["class"].append("modal-dialog-scrollable")
        if centered:
            dialog_attrs["class"].append("modal-dialog-centered")

        modal_dialog = ModalDialog(
            title=title, body=body, footer=footer, attrs=dialog_attrs
        )
        self.children.append(modal_dialog)


class ModalDialog(Element):
    """The dialog for a Bootstrap modal."""

    def __init__(
        self,
        title: RenderableType,
        body: RenderableType,
        footer: RenderableType | None = None,
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
        self.attrs["class"] = ["modal-dialog"]
        content = ModalContent(title=title, body=body, footer=footer)
        self.children.append(content)


class ModalContent(Element):
    """The content for a Bootstrap modal."""

    def __init__(
        self,
        title: RenderableType,
        body: RenderableType,
        footer: RenderableType | None = None,
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
        self.attrs["class"] = ["modal-content"]
        header = ModalHeader(title)
        body_element = ModalBody(body)
        self.children.append(header)
        self.children.append(body_element)
        if footer:
            self.children.append(ModalFooter(footer))


class ModalHeader(Element):
    """The header for a Bootstrap modal."""

    def __init__(
        self,
        title: RenderableType,
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
        self.attrs["class"] = ["modal-header"]
        title_element = Element("h5", attrs={"class": ["modal-title"]}, children=title)
        close_button = CloseButton(
            attrs={"data-bs-dismiss": "modal", "aria-label": "Close"}
        )
        self.children.append(title_element)
        self.children.append(close_button)


class ModalBody(Element):
    """The body for a Bootstrap modal."""

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
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
        )
        self.attrs["class"] = ["modal-body"]


class ModalFooter(Element):
    """The footer for a Bootstrap modal."""

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
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
        )
        self.attrs["class"] = ["modal-footer"]
