from __future__ import annotations

from viol.bootstrap.close_button import CloseButton
from viol.core import AttrMultiDict, Element, EventHandler, RenderableType


class Toast(Element):
    """A Bootstrap toast."""

    def __init__(
        self,
        header: RenderableType,
        body: RenderableType,
        animation: bool = True,
        autohide: bool = True,
        delay: int = 5000,
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
        self.attrs["class"] = ["toast"]
        self.attrs["role"] = "alert"
        self.attrs["aria-live"] = "assertive"
        self.attrs["aria-atomic"] = "true"
        if animation:
            self.attrs["data-bs-animation"] = "true"
        else:
            self.attrs["data-bs-animation"] = "false"
        if autohide:
            self.attrs["data-bs-autohide"] = "true"
        else:
            self.attrs["data-bs-autohide"] = "false"
        self.attrs["data-bs-delay"] = str(delay)

        self.children.append(ToastHeader(title=header))
        self.children.append(ToastBody(content=body))


class ToastHeader(Element):
    """The header for a Bootstrap toast."""

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
        self.attrs["class"] = ["toast-header"]
        self.children.append(title)
        self.children.append(
            CloseButton(attrs={"data-bs-dismiss": "toast", "aria-label": "Close"})
        )


class ToastBody(Element):
    """The body for a Bootstrap toast."""

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
        self.attrs["class"] = ["toast-body"]
