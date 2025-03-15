from __future__ import annotations

from typing_extensions import Literal

from viol.core import Element, RenderableType, VoidElement


class Base(VoidElement):
    def __init__(
        self,
        href: str,
        target: Literal["_blank", "_self", "_parent", "_top"] = "_self",
    ):
        super().__init__("base", attrs={"href": href, "target": target})


class Title(Element):
    def __init__(self, title: str):
        super().__init__("title", children=title)


class Meta(VoidElement):
    def __init__(
        self,
        charset: str | None = None,
        content: str | None = None,
        http_equiv: str | None = None,
        name: str | None = None,
    ):
        super().__init__(
            "meta",
            attrs={
                "charset": charset,
                "content": content,
                "http-equiv": http_equiv,
                "name": name,
            },
        )


class Head(Element):
    def __init__(
        self,
        children: RenderableType | list[RenderableType] = None,
        title: str | Title = "Untitled",
    ):
        title = title if isinstance(title, Title) else Title(title)
        super().__init__("head", children=[title, children])
