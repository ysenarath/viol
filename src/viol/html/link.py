from __future__ import annotations

from viol.core import VoidElement

__all__ = [
    "Link",
]


class Link(VoidElement):
    def __init__(
        self,
        href: str,
        rel: str,
        type: str | None = None,
        sizes: str | None = None,
        media: str | None = None,
        crossorigin: str | None = None,
        referrerpolicy: str | None = None,
        hreflang: str | None = None,
    ):
        super().__init__(
            "link",
            attrs={
                "href": href,
                "rel": rel,
                "type": type,
                "sizes": sizes,
                "media": media,
                "crossorigin": crossorigin,
                "referrerpolicy": referrerpolicy,
                "hreflang": hreflang,
            },
        )
