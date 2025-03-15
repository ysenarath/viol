from viol.core import Element, RenderableType

__all__ = [
    "Html",
]


class Html(Element):
    def __init__(
        self,
        children: RenderableType | list[RenderableType] = None,
        lang: str = "en",
    ):
        super().__init__("html", children=children)
        self.attrs["lang"] = lang
