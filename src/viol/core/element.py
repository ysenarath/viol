"""
HTML Element Module
=================

Purpose
-------
This module provides classes for representing HTML elements in the Viol library,
including both standard elements with closing tags and void elements without
closing tags.

Core Functionality
-----------------
- Element class for standard HTML elements with closing tags
- VoidElement class for HTML elements without closing tags (e.g., <img>, <br>)
- HTML rendering with proper escaping
- Support for attributes, children, and events

Dependencies
-----------
- html.escape: For proper HTML escaping
- viol.core.attributes: For HTML attribute management
- viol.core.base: For component system
- viol.core.events: For event handling

Usage Examples
-------------
>>> from viol.core.element import Element, VoidElement
>>>
>>> # Create a standard element
>>> div = Element("div", "Hello, World!", id="greeting")
>>> div.render()  # '<div id="greeting">Hello, World!</div>'
>>>
>>> # Create a void element
>>> img = VoidElement("img", attrs={"src": "image.jpg", "alt": "An image"})
>>> img.render()  # '<img src="image.jpg" alt="An image" />'

Edge Cases
---------
- Elements with no children render with empty content
- Elements with no attributes still include a space after the tag name
- Events are rendered as attributes and may include additional elements

Version History
--------------
1.0.0 - Initial stable release
"""

from __future__ import annotations

from html import escape

from viol.core.attributes import AttrMultiDict
from viol.core.base import Component, RenderableType, render
from viol.core.events import EventHandler, EventHandlerList

__all__ = [
    "Element",
    "VoidElement",
]


class Element(Component):
    """
    A standard HTML element with a closing tag.

    This class represents an HTML element with a tag name, attributes,
    children, and events. It renders to HTML with proper escaping.

    Parameters
    ----------
    tag : str
        The HTML tag name (e.g., "div", "span").
    children : RenderableType or list[RenderableType] or None, optional
        The element's children, which can be other components, strings, or None.
    attrs : AttrMultiDict, optional
        The element's attributes.
    events : list[EventHandler] or EventHandler or None, optional
        The element's event handlers.
    id : str, optional
        The element's ID attribute. If provided, it will be added to attrs.
    hyperscript : str, optional
        The element's hyperscript attribute. If provided, it will be added to attrs.

    Attributes
    ----------
    tag : str
        The HTML tag name.
    children : RenderableType or list[RenderableType] or None
        The element's children.
    attrs : AttrMultiDict
        The element's attributes.
    events : EventHandlerList
        The element's event handlers.

    Examples
    --------
    >>> div = Element("div", "Hello, World!", id="greeting")
    >>> div.render()  # '<div id="greeting">Hello, World!</div>'
    >>>
    >>> # With children and attributes
    >>> ul = Element("ul", [
    ...     Element("li", "Item 1"),
    ...     Element("li", "Item 2"),
    ... ], attrs={"class": "list"})
    >>> ul.render()  # '<ul class="list"><li>Item 1</li> <li>Item 2</li></ul>'
    """

    def __init__(
        self,
        tag: str,
        children: RenderableType | list[RenderableType] | None = None,
        attrs: AttrMultiDict = None,
        events: list[EventHandler] | EventHandler | None = None,
        id: str | None = None,
        hyperscript: str | None = None,
    ):
        """
        Initialize an HTML element.

        Parameters
        ----------
        tag : str
            The HTML tag name (e.g., "div", "span").
        children : RenderableType or list[RenderableType] or None, optional
            The element's children, which can be other components, strings, or None.
        attrs : AttrMultiDict, optional
            The element's attributes.
        events : list[EventHandler] or EventHandler or None, optional
            The element's event handlers.
        id : str, optional
            The element's ID attribute. If provided, it will be added to attrs.
        hyperscript : str, optional
            The element's hyperscript attribute. If provided, it will be added to attrs.
        """
        super().__init__()
        self.tag = tag
        self.children = children
        self.attrs = AttrMultiDict(attrs)
        if id:
            self.attrs.id = id
        if hyperscript:
            self.attrs._ = hyperscript
        self.events = EventHandlerList(self, events)

    def render(self) -> str:
        """
        Render the element to HTML.

        Returns
        -------
        str
            The HTML representation of the element.
        """
        children = render(self.children)
        tag = escape(self.tag)
        attrs = self.attrs.to_string()
        if self.events:
            event = self.events[0].to_string()
            other_events = render(self.events[1:])
            return f"<{tag} {attrs} {event}>{children}</{tag}>{other_events}"
        return f"<{tag} {attrs}>{children}</{tag}>"


class VoidElement(Element):
    """
    An HTML element without a closing tag.

    This class represents an HTML void element (e.g., <img>, <br>)
    with a tag name, attributes, and events. It renders to HTML with
    proper escaping and a self-closing tag.

    Parameters
    ----------
    tag : str
        The HTML tag name (e.g., "img", "br").
    attrs : AttrMultiDict, optional
        The element's attributes.
    events : list[EventHandler] or EventHandler or None, optional
        The element's event handlers.
    id : str, optional
        The element's ID attribute. If provided, it will be added to attrs.
    hyperscript : str, optional
        The element's hyperscript attribute. If provided, it will be added to attrs.

    Examples
    --------
    >>> img = VoidElement("img", attrs={"src": "image.jpg", "alt": "An image"})
    >>> img.render()  # '<img src="image.jpg" alt="An image" />'
    >>>
    >>> # With ID and events
    >>> input = VoidElement("input", id="name", attrs={"type": "text"})
    >>> input.render()  # '<input id="name" type="text" />'
    """

    def __init__(
        self,
        tag: str,
        attrs: AttrMultiDict = None,
        events: list[EventHandler] | EventHandler | None = None,
        id: str | None = None,
        hyperscript: str | None = None,
    ):
        """
        Initialize an HTML void element.

        Parameters
        ----------
        tag : str
            The HTML tag name (e.g., "img", "br").
        attrs : AttrMultiDict, optional
            The element's attributes.
        events : list[EventHandler] or EventHandler or None, optional
            The element's event handlers.
        id : str, optional
            The element's ID attribute. If provided, it will be added to attrs.
        hyperscript : str, optional
            The element's hyperscript attribute. If provided, it will be added to attrs.
        """
        super().__init__(
            tag=tag,
            children=None,
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
        )

    def render(self) -> str:
        """
        Render the void element to HTML.

        Returns
        -------
        str
            The HTML representation of the void element.
        """
        tag = escape(self.tag)
        attrs = self.attrs.to_string()
        if self.events:
            event = self.events[0].to_string()
            other_events = render(self.events[1:])
            return f"<{tag} {attrs} {event} />{other_events}"
        return f"<{tag} {attrs} />"
