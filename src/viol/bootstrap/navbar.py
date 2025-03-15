from __future__ import annotations

from viol.core import AttrList, Event, RenderableType
from viol.html import A, Button, Div, Form, Li, Nav, Span, Ul


class Navbar(Nav):
    """Bootstrap navbar component that provides responsive navigation header."""

    def __init__(
        self,
        children: RenderableType | list[RenderableType] | None = None,
        expand: str = "lg",  # sm|md|lg|xl|xxl
        theme: str = "light",  # light|dark
        bg: str = "body-tertiary",
        container: str = "fluid",  # fluid|sm|md|lg|xl|xxl or None
        placement: str | None = None,  # fixed-top|fixed-bottom|sticky-top|sticky-bottom
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
            container_div = Div(
                children=children,
                attrs={"class": [f"container-{container}"]},
            )
            self.children = [container_div]
        else:
            self.children = (
                children
                if isinstance(children, list)
                else [children]
                if children
                else []
            )


class NavbarBrand(A):
    """Navbar brand/logo component."""

    def __init__(
        self,
        children: RenderableType | list[RenderableType] | None = None,
        href: str = "#",
        attrs: AttrList = None,
        id: str | None = None,
        events: list[Event] | Event | None = None,
        _: str | None = None,
    ):
        super().__init__(
            children=children,
            href=href,
            attrs=attrs,
            id=id,
            events=events,
            _=_,
        )
        self.attrs["class"] = ["navbar-brand"]


class NavbarToggler(Button):
    """Navbar toggler button for collapsing navigation on mobile."""

    def __init__(
        self,
        target: str,
        attrs: AttrList = None,
        id: str | None = None,
        events: list[Event] | Event | None = None,
        _: str | None = None,
    ):
        super().__init__(
            children=[Span(attrs={"class": "navbar-toggler-icon"})],
            attrs=attrs,
            id=id,
            events=events,
            _=_,
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


class NavbarCollapse(Div):
    """Collapsible navbar content container."""

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
        self.attrs["class"] = ["collapse", "navbar-collapse"]


class NavbarNav(Ul):
    """Navigation list container for navbar items."""

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
        self.attrs["class"] = ["navbar-nav", "me-auto", "mb-2", "mb-lg-0"]


class NavItem(Li):
    """Individual navigation item container."""

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
        self.attrs["class"] = ["nav-item"]


class NavLink(A):
    """Navigation link within navbar."""

    def __init__(
        self,
        children: RenderableType | list[RenderableType] | None = None,
        href: str = "#",
        active: bool = False,
        disabled: bool = False,
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
            href=href,
        )
        classes = ["nav-link"]
        if active:
            classes.append("active")
            self.attrs["aria-current"] = "page"
        if disabled:
            classes.append("disabled")
            self.attrs["aria-disabled"] = "true"
        self.attrs["class"] = classes


class NavbarText(Span):
    """Text content within navbar."""

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
        self.attrs["class"] = ["navbar-text"]


class NavbarForm(Form):
    """Form within navbar, typically used for search."""

    def __init__(
        self,
        children: RenderableType | list[RenderableType] | None = None,
        role: str = "search",
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
        self.attrs.update({"class": "d-flex", "role": role})
