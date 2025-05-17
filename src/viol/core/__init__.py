"""
Viol Core Module
===============

Purpose
-------
The core module provides the fundamental building blocks for the Viol library,
including components, elements, attributes, and event handling.

Core Functionality
-----------------
- Component system for building reusable UI elements
- HTML element representation and rendering
- Attribute management with special handling for HTML attributes
- Event handling for HTMX integration

Dependencies
-----------
- multidict: For case-insensitive multi-dictionaries
- jinja2: For template rendering
- typing_extensions: For advanced type annotations

Usage Examples
-------------
>>> from viol.core import Element, render
>>>
>>> # Create a simple element
>>> div = Element("div", "Hello, World!")
>>>
>>> # Render the element to HTML
>>> html = render(div)  # <div>Hello, World!</div>

Edge Cases
---------
- Nested components are automatically rendered recursively
- None values are rendered as empty strings
- Special handling for class attributes as lists or space-separated strings

Version History
--------------
1.0.0 - Initial stable release
"""

from viol.core.attributes import AttrMultiDict
from viol.core.base import Component, RenderableType, render
from viol.core.element import Element, VoidElement
from viol.core.events import EventHandler, EventHandlerList

__all__ = [
    "AttrMultiDict",
    "Component",
    "Element",
    "EventHandler",
    "EventHandlerList",
    "RenderableType",
    "VoidElement",
    "render",
]
