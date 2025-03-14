from __future__ import annotations

from viol.core import AttrList, Event, RenderableType
from viol.elements.button import Button
from viol.elements.div import Div
from viol.elements.header import Header


class ValueErrorMessages:
    VALUE_MUST_NOT_BE_NONE = "{key} must not be None"


def must(key: str, value: str | None) -> str:
    if value is None:
        raise ValueError(ValueErrorMessages.VALUE_MUST_NOT_BE_NONE.format(key=key))
    return value


class Accordion(Div):
    def __init__(
        self,
        children: list[AccordionItem] | None = None,
        attrs: AttrList = None,
        id: str | None = None,
        events: list[Event] | Event | None = None,
        _: str | None = None,
    ):
        super().__init__(
            children=children,
            attrs=attrs,
            id=must("id", id),
            events=events,
            _=_,
        )
        self.attrs["class"] = "accordion"


class AccordionItem(Div):
    def __init__(
        self,
        children: RenderableType | list[RenderableType] | None = None,
        attrs: AttrList = None,
        id: str | None = None,
        events: list[Event] | Event | None = None,
        _: str | None = None,
    ):
        super().__init__(
            children=children,
            attrs=attrs,
            id=id,
            events=events,
            _=_,
        )
        self.attrs["class"] = "accordion-item"


class AccordionHeader(Header):
    def __init__(
        self,
        children: RenderableType | list[RenderableType] | None = None,
        level: int = 2,
        attrs: AttrList = None,
        id: str | None = None,
        events: list[Event] | Event | None = None,
        _: str | None = None,
    ):
        super().__init__(
            children=children,
            level=level,
            attrs=attrs,
            id=id,
            events=events,
            _=_,
        )
        self.attrs["class"] = "accordion-header"


class AccordionButton(Button):
    def __init__(
        self,
        children: RenderableType | list[RenderableType] | None = None,
        attrs: AttrList = None,
        id: str | None = None,
        events: list[Event] | Event | None = None,
        _: str | None = None,
    ):
        super().__init__(
            children=children,
            attrs=attrs,
            id=id,
            events=events,
            _=_,
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


class AccordionCollapse(Div):
    def __init__(
        self,
        children: RenderableType | list[RenderableType] | None = None,
        attrs: AttrList = None,
        id: str | None = None,
        events: list[Event] | Event | None = None,
        _: str | None = None,
    ):
        super().__init__(
            children=children,
            attrs=attrs,
            id=must("id", id),
            events=events,
            _=_,
        )
        self.attrs["class"] = "accordion-collapse collapse"
        self.attrs["data-bs-parent"] = "#{{ctx.parent.parent.component.attrs.id}}"


class AccordionBody(Div):
    def __init__(
        self,
        children: RenderableType | list[RenderableType] | None = None,
        attrs: AttrList = None,
        id: str | None = None,
        events: list[Event] | Event | None = None,
        _: str | None = None,
    ):
        super().__init__(
            children=children,
            attrs=attrs,
            id=id,
            events=events,
            _=_,
        )
        self.attrs["class"] = "accordion-body"
