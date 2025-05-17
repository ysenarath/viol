from __future__ import annotations

from typing import Literal

from viol.core import AttrMultiDict, Element, EventHandler, RenderableType


class Carousel(Element):
    """A Bootstrap carousel."""

    def __init__(
        self,
        items: list[CarouselItem],
        controls: bool = True,
        indicators: bool = True,
        crossfade: bool = False,
        interval: int = 5000,  # Default interval of 5 seconds
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
        self.attrs["class"] = ["carousel", "slide"]
        self.attrs["data-bs-ride"] = "carousel"  # Enable auto-cycling
        self.attrs["data-bs-interval"] = interval

        if crossfade:
            self.attrs["class"].append("carousel-fade")

        if id:
            self.attrs["id"] = id

        inner = CarouselInner(items)
        self.children.append(inner)

        if indicators and id:
            indicators_element = CarouselIndicators(len(items), target=f"#{id}")
            self.children.append(indicators_element)

        if controls and id:
            control_prev = CarouselControl(direction="prev", target=f"#{id}")
            control_next = CarouselControl(direction="next", target=f"#{id}")
            self.children.append(control_prev)
            self.children.append(control_next)


class CarouselInner(Element):
    """Inner container for carousel items."""

    def __init__(self, items: list[CarouselItem], attrs: AttrMultiDict = None,
                 events: list[EventHandler] | EventHandler | None = None,
                 id: str | None = None,
                 hyperscript: str | None = None):
        super().__init__("div", attrs=attrs, events=events, id=id, hyperscript=hyperscript)
        self.attrs["class"] = ["carousel-inner"]
        for i, item in enumerate(items):
            item.attrs["class"].append("carousel-item")
            if i == 0:
                item.attrs["class"].append("active")
            self.children.append(item)


class CarouselItem(Element):
    """A single item in the carousel."""

    def __init__(self, content: RenderableType, attrs: AttrMultiDict = None,
                 events: list[EventHandler] | EventHandler | None = None,
                 id: str | None = None,
                 hyperscript: str | None = None):
        super().__init__("div", children=content, attrs=attrs, events=events, id=id, hyperscript=hyperscript)
        self.attrs["class"] = ["carousel-item"]


class CarouselControl(Element):
    """Control buttons for the carousel."""

    def __init__(self, direction: Literal["prev", "next"], target: str, attrs: AttrMultiDict = None,
                 events: list[EventHandler] | EventHandler | None = None,
                 id: str | None = None,
                 hyperscript: str | None = None):
        super().__init__("button", attrs=attrs, events=events, id=id, hyperscript=hyperscript)
        self.attrs["class"] = [f"carousel-control-{direction}"]
        self.attrs["type"] = "button"
        self.attrs["data-bs-target"] = target
        self.attrs["data-bs-slide"] = direction
        icon = Element("span", attrs={"class": f"carousel-control-{direction}-icon", "aria-hidden": "true"})
        visually_hidden = Element("span", attrs={"class": "visually-hidden"}, children=direction)
        self.children.append(icon)
        self.children.append(visually_hidden)


class CarouselIndicators(Element):
    """Indicators for the carousel."""

    def __init__(self, count: int, target: str, attrs: AttrMultiDict = None,
                 events: list[EventHandler] | EventHandler | None = None,
                 id: str | None = None,
                 hyperscript: str | None = None):
        super().__init__("div", attrs=attrs, events=events, id=id, hyperscript=hyperscript)
        ol = Element("ol", attrs={"class": ["carousel-indicators"]})
        for i in range(count):
            li = Element("button", attrs={
                "type": "button",
                "data-bs-target": target,
                "data-bs-slide-to": str(i),
                "aria-label": f"Slide {i+1}"
            })
            if i == 0:
                li.attrs["class"] = ["active"]
                li.attrs["aria-current"] = "true"
            ol.children.append(li)
        self.children.append(ol)
