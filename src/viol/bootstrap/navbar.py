from __future__ import annotations

from viol import html
from viol.core import AttrMultiDict, Element, EventHandler, RenderableType

__all__ = [
    "NavItem",
    "NavLink",
    "Navbar",
    "NavbarBrand",
    "NavbarCollapse",
    "NavbarForm",
    "NavbarNav",
    "NavbarText",
    "NavbarToggler",
]


class Navbar(Element):
    """Bootstrap navbar component that provides responsive navigation header."""

    def __init__(
        self,
        children: RenderableType | list[RenderableType] | None = None,
        expand: str = "lg",  # sm|md|lg|xl|xxl
        theme: str = "light",  # light|dark
        bg: str = "body-tertiary",
        container: str | None = None,  # fluid|sm|md|lg|xl|xxl or None
        placement: str | None = None,  # fixed-top|fixed-bottom|sticky-top|sticky-bottom
        attrs: AttrMultiDict = None,
        events: list[EventHandler] | EventHandler | None = None,
        id: str | None = None,
        hyperscript: str | None = None,
    ):
        super().__init__(
            "nav",
            children=children,
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
        )
        # Add theme class
        if theme == "dark":
            self.attrs["data-bs-theme"] = "dark"
        # Base navbar class
        classes = ["navbar"]
        # Add expand class if specified
        if expand:
            classes.append(f"navbar-expand-{expand}")
        # Add background class
        if bg:
            classes.append(f"bg-{bg}")
        # Add placement class if specified
        if placement:
            classes.append(placement)
        self.attrs.class_ = classes
        # Wrap children in container if specified
        if container:
            container_div = html.div(
                children=children,
                attrs={"class": [f"container-{container}"]},
            )
            self.children = [container_div]
        else:
            self.children = html.div(
                children=children,
                attrs={"class": ["container"]},
            )


class NavbarBrand(Element):
    """Navbar brand/logo component."""

    def __init__(
        self,
        children: RenderableType | list[RenderableType] | None = None,
        href: str = "#",
        attrs: AttrMultiDict = None,
        events: list[EventHandler] | EventHandler | None = None,
        id: str | None = None,
        hyperscript: str | None = None,
    ):
        super().__init__(
            "a",
            children=children,
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
        )
        self.attrs["href"] = href
        self.attrs["class"] = ["navbar-brand"]


class NavbarToggler(Element):
    """Navbar toggler button for collapsing navigation on mobile."""

    def __init__(
        self,
        target: str,
        attrs: AttrMultiDict = None,
        events: list[EventHandler] | EventHandler | None = None,
        id: str | None = None,
        hyperscript: str | None = None,
    ):
        super().__init__(
            "button",
            children=[html.span(attrs={"class": "navbar-toggler-icon"})],
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
        )
        self.attrs.update(
            {
                "class": ["navbar-toggler"],
                "type": "button",
                "data-bs-toggle": "collapse",
                "data-bs-target": f"#{target}",
                "aria-controls": target,
                "aria-expanded": "false",
                "aria-label": "Toggle navigation",
            }
        )


class NavbarCollapse(Element):
    """Collapsible navbar content container."""

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
        self.attrs["class"] = ["collapse", "navbar-collapse"]


class NavbarNav(Element):
    """Navigation list container for navbar items."""

    def __init__(
        self,
        children: RenderableType | list[RenderableType] | None = None,
        attrs: AttrMultiDict = None,
        events: list[EventHandler] | EventHandler | None = None,
        id: str | None = None,
        hyperscript: str | None = None,
    ):
        super().__init__(
            "ul",
            children=children,
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
        )
        self.attrs["class"] = ["navbar-nav", "me-auto", "mb-2", "mb-lg-0"]


class NavItem(Element):
    """Individual navigation item container."""

    def __init__(
        self,
        children: RenderableType | list[RenderableType] | None = None,
        attrs: AttrMultiDict = None,
        events: list[EventHandler] | EventHandler | None = None,
        id: str | None = None,
        hyperscript: str | None = None,
    ):
        super().__init__(
            "li",
            children=children,
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
        )
        self.attrs["class"] = ["nav-item"]


class NavLink(Element):
    """Navigation link within navbar."""

    def __init__(
        self,
        children: RenderableType | list[RenderableType] | None = None,
        href: str = "#",
        active: bool = False,
        disabled: bool = False,
        attrs: AttrMultiDict = None,
        events: list[EventHandler] | EventHandler | None = None,
        id: str | None = None,
        hyperscript: str | None = None,
    ):
        super().__init__(
            "a",
            children=children,
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
        )
        self.attrs["href"] = href
        classes = ["nav-link"]
        if active:
            classes.append("active")
            self.attrs["aria-current"] = "page"
        if disabled:
            classes.append("disabled")
            self.attrs["aria-disabled"] = "true"
        self.attrs["class"] = classes


class NavbarText(Element):
    """Text content within navbar."""

    def __init__(
        self,
        children: RenderableType | list[RenderableType] | None = None,
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
        self.attrs["class"] = ["navbar-text"]


class NavbarForm(Element):
    """Form within navbar, typically used for search."""

    def __init__(
        self,
        children: RenderableType | list[RenderableType] | None = None,
        role: str = "search",
        attrs: AttrMultiDict = None,
        events: list[EventHandler] | EventHandler | None = None,
        id: str | None = None,
        hyperscript: str | None = None,
    ):
        super().__init__(
            "form",
            children=children,
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
        )
        self.attrs.update({"class": "d-flex", "role": role})
