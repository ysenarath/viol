from collections.abc import Iterator

from viol.bootstrap.navbar import (
    Navbar,
    NavbarBrand,
    NavbarCollapse,
    NavbarNav,
    NavbarToggler,
    NavItem,
    NavLink,
)

__all__ = [
    "simple_navbar",
]


def validate_each(items: list[dict]) -> Iterator[tuple[int, dict]]:
    """Validate each item in the list and yield valid items."""
    for i, item in enumerate(items):
        if isinstance(item, str):
            yield {"name": item}
        yield i, item


def simple_navbar(
    items: list[dict],
    id: str = "main-navbar",
    brand: str = "Bootstrap",
    brand_href: str = "/",
    target: str = "#main-content",
) -> Navbar:
    """Create a complex Bootstrap navbar with brand and toggler."""
    return Navbar(
        [
            NavbarBrand(brand, brand_href),
            NavbarToggler(target=id),
            NavbarCollapse(
                [
                    NavbarNav(
                        [
                            *[
                                NavItem(
                                    NavLink(
                                        item["name"],
                                        active=item.get("active", False),
                                        disabled=item.get("disabled", False),
                                        events=[
                                            {
                                                "method": "get",
                                                "rule": item["href"],
                                                "trigger": "click",
                                                "target": target,
                                            }
                                        ],
                                        id=f"navbar-link-{i}",
                                        hyperscript=f'on click remove .active from <#{id} a[id^="navbar-link-"]/> add .active',
                                    )
                                )
                                for i, item in validate_each(items)
                            ]
                        ],
                    )
                ]
            ),
        ],
        id=id,
    )
