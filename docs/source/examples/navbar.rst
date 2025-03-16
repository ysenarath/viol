Navbar Example
=============

This example demonstrates how to create a responsive Bootstrap navbar using viol's Bootstrap components.

Components Overview
----------------

First, import the necessary navbar components:

.. code-block:: python

    from viol.bootstrap.navbar import (
        Navbar,
        NavbarBrand,
        NavbarCollapse,
        NavbarNav,
        NavbarToggler,
        NavItem,
        NavLink,
    )

Creating a Simple Navbar
---------------------

The example shows how to create a responsive navbar with a brand, toggler, and navigation items:

.. code-block:: python

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

Component Breakdown
----------------

1. **Navbar**
    * The main container component
    * Takes an ID that matches the toggler's target

2. **NavbarBrand**
    * Creates the brand/logo area
    * Takes text and a URL

3. **NavbarToggler**
    * Creates the mobile menu toggle button
    * Links to the collapse section via target ID

4. **NavbarCollapse**
    * Collapsible container for navbar content
    * Toggles visibility on mobile devices

5. **NavbarNav**
    * Container for navigation items
    * Organizes links horizontally (desktop) or vertically (mobile)

6. **NavItem and NavLink**
    * NavItem: Wrapper for individual navigation elements
    * NavLink: The actual link with support for active and disabled states

Features
-------

1. **Responsive Design**
    * Automatically collapses on mobile devices
    * Toggler button appears on small screens

2. **State Management**
    * Support for active links
    * Support for disabled links

3. **Bootstrap Integration**
    * Uses Bootstrap's navbar classes
    * Follows Bootstrap's component structure

4. **Customization**
    * Links can be configured with different URLs
    * States can be controlled via parameters