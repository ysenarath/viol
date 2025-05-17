"""
Viol HTML Module
===============

Purpose
-------
The HTML module provides a comprehensive set of HTML element builders for creating
HTML documents in a Pythonic way. It exposes all standard HTML elements as callable
functions that create Element instances.

Core Functionality
-----------------
- Complete set of HTML element builders for all standard HTML elements
- Type-hinted attributes for each HTML element
- Consistent interface for creating HTML elements with children, attributes, and events
- Integration with the core Element system

Dependencies
-----------
- viol.core: For Element, EventHandler, and RenderableType classes
- typing: For type annotations and TypedDict

Usage Examples
-------------
>>> from viol.html import div, p, a, span
>>>
>>> # Create a simple div with a paragraph
>>> content = div([
...     p("This is a paragraph with a ", [
...         a("link", attrs={"href": "https://example.com"}),
...         " and some ",
...         span("styled text", attrs={"class": "highlight"})
...     ])
... ])
>>>
>>> # Render the content
>>> from viol.core import render
>>> html = render(content)

Edge Cases
---------
- Element names that conflict with Python keywords are suffixed with an underscore (e.g., 'del_')
- Void elements (like br, hr, img) don't require children but still accept them for API consistency
- HTML attributes are case-insensitive but are defined in lowercase for consistency

Version History
--------------
1.0.0 - Initial stable release with complete HTML5 element support
"""

from viol.html.elements import *


__all__ = [
    "a",
    "abbr",
    "address",
    "area",
    "article",
    "aside",
    "audio",
    "b",
    "base",
    "bdi",
    "bdo",
    "blockquote",
    "body",
    "br",
    "button",
    "canvas",
    "caption",
    "cite",
    "code",
    "col",
    "colgroup",
    "data",
    "datalist",
    "dd",
    "del_",
    "details",
    "dfn",
    "dialog",
    "div",
    "dl",
    "dt",
    "em",
    "embed",
    "fieldset",
    "figcaption",
    "figure",
    "footer",
    "form",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "head",
    "header",
    "hgroup",
    "hr",
    "html",
    "i",
    "iframe",
    "img",
    "input",
    "ins",
    "kbd",
    "label",
    "legend",
    "li",
    "link",
    "main",
    "map",
    "mark",
    "math",
    "menu",
    "meta",
    "meter",
    "nav",
    "noscript",
    "object",
    "ol",
    "optgroup",
    "option",
    "output",
    "p",
    "picture",
    "pre",
    "progress",
    "q",
    "rp",
    "rt",
    "ruby",
    "s",
    "samp",
    "script",
    "search",
    "section",
    "select",
    "slot",
    "small",
    "source",
    "span",
    "strong",
    "style",
    "sub",
    "summary",
    "sup",
    "svg",
    "table",
    "tbody",
    "td",
    "template",
    "textarea",
    "tfoot",
    "th",
    "thead",
    "time",
    "title",
    "tr",
    "track",
    "u",
    "ul",
    "var",
    "video",
    "wbr",
]
