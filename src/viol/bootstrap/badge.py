from __future__ import annotations

from viol.core import AttrMultiDict, Element, EventHandler, RenderableType

__all__ = ["Badge"]


class Badge(Element):
    """Bootstrap badge component that provides a small count or labeling information."""

    def __init__(
        self,
        children: RenderableType | list[RenderableType] | None = None,
        bg_color: str = "primary",
        attrs: AttrMultiDict = None,
        events: list[EventHandler] | EventHandler | None = None,
        id: str | None = None,
        hyperscript: str | None = None,
    ):
        super().__init__(
            "span",
            children=children,
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
        )
        if "badge" not in self.attrs.class_:
            self.attrs.class_.append("badge")
        if not any(c.startswith("text-bg-") for c in self.attrs.class_):
            self.attrs.class_.append(f"text-bg-{bg_color}")
