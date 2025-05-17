from __future__ import annotations

from viol.core import AttrMultiDict, Element, EventHandler, RenderableType


class Card(Element):
    """A Bootstrap card."""

    def __init__(
        self,
        header: RenderableType | None = None,
        body: RenderableType | None = None,
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
        self.attrs["class"] = ["card"]

        if header:
            self.children.append(CardHeader(header))
        if body:
            self.children.append(CardBody(body))
        if footer:
            self.children.append(CardFooter(footer))


class CardHeader(Element):
    """A Bootstrap card header."""

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
        self.attrs["class"] = ["card-header"]


class CardBody(Element):
    """A Bootstrap card body."""

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
        self.attrs["class"] = ["card-body"]


class CardFooter(Element):
    """A Bootstrap card footer."""

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
        self.attrs["class"] = ["card-footer"]
