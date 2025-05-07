from __future__ import annotations

import re

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
        accordion_flush: bool = False,
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
        self.accordion_flush = accordion_flush

    @property
    def accordion_flush(self) -> bool:
        # use regex to check if accordion-flush is present
        return bool(re.search(r"\baccordion-flush\b", self.attrs["class"]))

    @accordion_flush.setter
    def accordion_flush(self, value: bool) -> None:
        if value:
            if "accordion-flush" in self.attrs["class"]:
                return
            self.attrs["class"] += " accordion-flush"
        elif "accordion-flush" in self.attrs["class"]:
            self.attrs["class"] = re.sub(
                r"\baccordion-flush\b", " ", self.attrs["class"]
            ).strip()


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
        # ctx.parent.paren.component is the AccordionItem
        # ctx.parent.parent.component.children[-1] is the AccordionCollapse
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
        always_open: bool = False,
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
        self.always_open = always_open

    @property
    def always_open(self) -> bool:
        return "data-bs-parent" in self.attrs

    @always_open.setter
    def always_open(self, value: bool) -> None:
        if value:
            self.attrs.pop("data-bs-parent", None)
        else:
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
