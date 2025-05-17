"""
Viol Layout Module
================

Purpose
-------
The layout module provides components and utilities for structuring web applications
built with Viol. It includes a basic layout template and Flask integration for
serving static assets and rendering templates.

Core Functionality
-----------------
- Flask application initialization with Viol integration
- Basic layout component for structuring HTML pages
- Template rendering with Jinja2
- Static asset management

Dependencies
-----------
- flask: For web application framework and Blueprint functionality
- jinja2: For template rendering
- viol.core: For Component base class and rendering utilities

Usage Examples
-------------
>>> from flask import Flask
>>> from viol.layout import init_app, BasicLayout
>>> from viol.html import div, p
>>>
>>> # Initialize a Flask application with Viol
>>> app = Flask(__name__)
>>> init_app(app)
>>>
>>> # Create a basic layout with content
>>> content = div([
...     p("Hello, World!")
... ])
>>> layout = BasicLayout(
...     body=content,
...     title="My Viol App"
... )
>>>
>>> # Render the layout to HTML
>>> html = layout.render()

Edge Cases
---------
- Custom static folders and URL paths can be specified during initialization
- Extra head and body content can be injected into the layout
- Template rendering uses Flask's url_for function for generating URLs

Version History
--------------
1.0.0 - Initial stable release with basic layout and Flask integration
"""

from __future__ import annotations

from pathlib import Path

from flask import Blueprint, Flask, url_for
from jinja2 import Environment, FileSystemLoader

from viol.core import Component
from viol.core.base import render

__all__ = [
    "BasicLayout",
    "init_app",
]

mdir = Path(__file__).parent


def init_app(
    app: Flask,
    static_folder: str | Path | None = None,
    static_url_path: str | None = None,
) -> None:
    """
    Initialize a Flask application with Viol integration.

    This function registers a Flask Blueprint that provides access to Viol's static
    assets (CSS, JavaScript) and templates. It should be called during your Flask
    application setup.

    Parameters
    ----------
    app : Flask
        The Flask application instance to initialize with Viol.
    static_folder : str | Path | None, optional
        Custom path to the static files folder. If None, defaults to the 'static'
        directory within the Viol package.
    static_url_path : str | None, optional
        Custom URL path for serving static files. If None, defaults to '/viol/static'.

    Returns
    -------
    None

    Examples
    --------
    >>> from flask import Flask
    >>> from viol.layout import init_app
    >>>
    >>> app = Flask(__name__)
    >>> init_app(app)
    >>>
    >>> # With custom static folder and URL path
    >>> init_app(app, static_folder="custom_static", static_url_path="/assets")
    """
    layout = Blueprint(
        "viol",
        __name__,
        static_folder=static_folder or mdir / "static",
        static_url_path=static_url_path or "/viol/static",
    )
    app.register_blueprint(layout)


class BasicLayout(Component):
    """
    A basic HTML page layout component.

    This component provides a standard HTML page structure with customizable
    title, body content, and optional extra content for the head and body
    sections. It uses a Jinja2 template to render the final HTML.

    The layout includes Bootstrap CSS and JavaScript, as well as HTMX and
    Hyperscript for enhanced interactivity.

    Parameters
    ----------
    body : str, optional
        The main content of the page. Can be a string, Element, or any renderable
        object. Defaults to an empty string.
    title : str, optional
        The page title. Defaults to "Viol".
    extra_head_content : str | None, optional
        Additional content to include in the HTML head section, such as meta tags,
        stylesheets, or scripts. Defaults to None.
    extra_body_content : str | None, optional
        Additional content to include at the end of the HTML body section, such as
        scripts or hidden elements. Defaults to None.

    Attributes
    ----------
    env : jinja2.Environment
        The Jinja2 environment used for template rendering.
    template : jinja2.Template
        The loaded template for the layout.
    title : str
        The page title.
    extra_head_content : str | None
        Additional content for the head section.
    body : str
        The main content of the page.
    extra_body_content : str | None
        Additional content for the end of the body section.

    Examples
    --------
    >>> from viol.layout import BasicLayout
    >>> from viol.html import div, h1, p
    >>>
    >>> # Create page content
    >>> content = div([
    ...     h1("Welcome to Viol"),
    ...     p("This is a simple page created with Viol.")
    ... ])
    >>>
    >>> # Create a layout with the content
    >>> layout = BasicLayout(
    ...     body=content,
    ...     title="My First Viol Page",
    ...     extra_head_content='<meta name="description" content="A Viol example">'
    ... )
    >>>
    >>> # Render the layout to HTML
    >>> html = layout.render()
    """

    def __init__(
        self,
        body: str = "",
        title: str = "Viol",
        extra_head_content: str | None = None,
        extra_body_content: str | None = None,
    ) -> None:
        self.env = Environment(loader=FileSystemLoader(mdir / "templates"))
        self.template = self.env.get_template("index.html")
        self.title = title
        self.extra_head_content = extra_head_content
        self.body = body
        self.extra_body_content = extra_body_content

    def render(self) -> str:
        """
        Render the layout to HTML.

        This method renders the layout template with the provided content and
        configuration. It automatically renders any nested components in the
        body and extra content sections.

        Returns
        -------
        str
            The complete HTML document as a string.
        """
        self.ctx["title"] = self.title
        self.ctx["extra_head_content"] = render(self.extra_head_content)
        self.ctx["body"] = render(self.body)
        self.ctx["extra_body_content"] = render(self.extra_body_content)
        return self.template.render(url_for=url_for, **self.ctx)
