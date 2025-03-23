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


def simple_navbar() -> Navbar:
    """Create a simple Bootstrap navbar with brand and toggler."""
    return Navbar(
        [
            NavbarBrand("Navbar", "/"),
            NavbarToggler(target="navbarNav"),
            NavbarCollapse(
                [
                    NavbarNav(
                        [
                            NavItem(NavLink("Home", "/home", active=True)),
                            NavItem(NavLink("Features", "/features")),
                            NavItem(NavLink("Pricing", "/pricing")),
                            NavItem(NavLink("Disabled", "/diabled", disabled=True)),
                        ]
                    )
                ]
            ),
        ],
        id="navbarNav",
    )
