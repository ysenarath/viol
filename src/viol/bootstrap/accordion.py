from __future__ import annotations

from viol.core import AttrMultiDict, Element, EventHandler, RenderableType


class ValueErrorMessages:
    VALUE_MUST_NOT_BE_NONE = "{key} must not be None"


def must(key: str, value: str | None) -> str:
    if value is None:
        raise ValueError(ValueErrorMessages.VALUE_MUST_NOT_BE_NONE.format(key=key))
    return value


class Accordion(Element):
    def __init__(
        self,
        children: list[AccordionItem] | None = None,
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
            id=must("id", id),
            hyperscript=hyperscript,
        )
        self.attrs["class"] = "accordion"


class AccordionItem(Element):
    def __init__(
        self,
        children: RenderableType | list[RenderableType] | None = None,
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
        self.attrs["class"] = "accordion-item"


class AccordionHeader(Element):
    def __init__(
        self,
        children: RenderableType | list[RenderableType] | None = None,
        level: int = 2,
        attrs: AttrMultiDict = None,
        events: list[EventHandler] | EventHandler | None = None,
        id: str | None = None,
        hyperscript: str | None = None,
    ):
        super().__init__(
            f"h{level}",
            children=children,
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
        )
        self.attrs["class"] = "accordion-header"


class AccordionButton(Element):
    def __init__(
        self,
        children: RenderableType | list[RenderableType] | None = None,
        attrs: AttrMultiDict = None,
        events: list[EventHandler] | EventHandler | None = None,
        id: str | None = None,
        hyperscript: str | None = None,
    ):
        super().__init__(
            "button",
            children=children,
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
        )
        self.attrs["class"] = "accordion-button collapsed"
        self.attrs["type"] = "button"
        self.attrs["data-bs-toggle"] = "collapse"
        # id of the collapse element
        self.attrs["data-bs-target"] = (
            "#{{ctx.parent.parent.component.children[-1].attrs.id}}"
        )
        self.attrs["aria-expanded"] = "false"
        # id of the collapse element
        self.attrs["aria-controls"] = (
            "{{ctx.parent.parent.component.children[-1].attrs.id}}"
        )


class AccordionCollapse(Element):
    def __init__(
        self,
        children: RenderableType | list[RenderableType] | None = None,
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
            id=must("id", id),
            hyperscript=hyperscript,
        )
        self.attrs["class"] = "accordion-collapse collapse"
        self.attrs["data-bs-parent"] = "#{{ctx.parent.parent.component.attrs.id}}"


class AccordionBody(Element):
    def __init__(
        self,
        children: RenderableType | list[RenderableType] | None = None,
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
        self.attrs["class"] = "accordion-body"
