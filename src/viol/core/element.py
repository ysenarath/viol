from __future__ import annotations

from html import escape

from viol.core.attributes import AttrMultiDict
from viol.core.base import Component, RenderableType, render
from viol.core.events import EventHandler, EventHandlerList

__all__ = [
    "Element",
    "VoidElement",
]


class Element(Component):
    def __init__(
        self,
        tag: str,
        children: RenderableType | list[RenderableType] | None = None,
        attrs: AttrMultiDict = None,
        id: str | None = None,
        events: list[EventHandler] | EventHandler | None = None,
        _: str | None = None,
    ):
        super().__init__()
        self.tag = tag
        self.children = children
        self.attrs = AttrMultiDict(attrs)
        if id:
            self.attrs.id = id
        if _:
            self.attrs._ = _
        self.events = EventHandlerList(self, events)

    def render(self) -> str:
        children = render(self.children)
        tag = escape(self.tag)
        attrs = self.attrs.to_string()
        if self.events:
            event = self.events[0].to_string()
            other_events = render(self.events[1:])
            return f"<{tag} {attrs} {event}>{children}</{tag}>{other_events}"
        return f"<{tag} {attrs}>{children}</{tag}>"


class VoidElement(Element):
    def __init__(
        self,
        tag: str,
        attrs: AttrMultiDict = None,
        id: str | None = None,
        events: list[EventHandler] | EventHandler | None = None,
        _: str | None = None,
    ):
        super().__init__(tag=tag, children=None, attrs=attrs, id=id, events=events, _=_)

    def render(self) -> str:
        tag = escape(self.tag)
        attrs = self.attrs.to_string()
        if self.events:
            event = self.events[0].to_string()
            other_events = render(self.events[1:])
            return f"<{tag} {attrs} {event} />{other_events}"
        return f"<{tag} {attrs} />"
