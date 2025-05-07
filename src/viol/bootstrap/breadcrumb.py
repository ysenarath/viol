from __future__ import annotations

from viol import html
from viol.core import AttrMultiDict, Element, EventHandler

__all__ = ["Breadcrumb"]


def location_to_children(location: list[str | tuple[str, str]]) -> list[Element]:
    """Convert a list of locations to a list of HTML elements."""
    children: list[Element] = []
    for loc in location:
        if isinstance(loc, tuple):
            children.append(
                html.li(
                    html.a(
                        loc[0],
                        attrs={"href": loc[1]},
                    ),
                    attrs={
                        "class": "breadcrumb-item",
                    },
                )
            )
        else:
            children.append(
                html.li(
                    loc,
                    attrs={
                        "class": "breadcrumb-item",
                    },
                )
            )
    children[-1].attrs["aria-current"] = "page"
    children[-1].attrs.class_.append("active")
    return html.nav(
        html.ol(
            children,
            attrs={
                "class": "breadcrumb",
            },
        ),
        attrs={
            "aria-label": "breadcrumb",
        },
    )


class Breadcrumb(Element):
    def __init__(
        self,
        location: list[str | tuple[str, str]],
        attrs: AttrMultiDict = None,
        events: list[EventHandler] | EventHandler | None = None,
        id: str | None = None,
        hyperscript: str | None = None,
    ):
        super().__init__(
            "span",
            children=location_to_children(location),
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
        )
