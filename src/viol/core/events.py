"""
Event Handling Module
===================

Purpose
-------
This module provides classes for handling HTMX events in the Viol library,
allowing for interactive web components with client-side behavior.

Core Functionality
-----------------
- EventHandler class for defining HTMX event attributes
- EventHandlerList for managing collections of event handlers
- Automatic binding of events to elements
- Support for common HTMX attributes like trigger, target, and swap

Dependencies
-----------
- viol.core.attributes: For HTML attribute management
- viol.core.base: For component system
- viol.utils.collections: For validated lists
- re: For regular expression matching

Usage Examples
-------------
>>> from viol.core.events import EventHandler
>>> from viol.core.element import Element
>>>
>>> # Create an element with an event handler
>>> button = Element("button", "Click me", id="btn")
>>> event = EventHandler(
...     method="get",
...     rule="/api/data",
...     target="#result",
...     trigger="click",
... )
>>> button.events.append(event)
>>> button.render()  # '<button id="btn" hx-get="/api/data" hx-target="#result" hx-trigger="click">Click me</button>'

Edge Cases
---------
- Events without a trigger attribute are still valid
- Events are automatically bound to their parent element
- Multiple events on a single element are supported
- Event triggers can reference other elements with 'from:' syntax

Version History
--------------
1.0.0 - Initial stable release
"""

from __future__ import annotations

import copy
import re
import weakref
from typing import TYPE_CHECKING, Any

from viol.core.attributes import AttrMultiDict, AttrsProperty
from viol.core.base import Component
from viol.utils.collections import ValidatedList

__all__ = [
    "EventHandler",
    "EventHandlerList",
]

if TYPE_CHECKING:
    from viol.core.element import Element


class EventHandler(AttrMultiDict, Component):
    """
    A handler for HTMX events.

    This class represents an HTMX event handler with attributes for
    defining client-side behavior. It extends AttrMultiDict to provide
    attribute-like access to HTMX attributes.

    Parameters
    ----------
    rule : str, optional
        The URL or selector to use for the request.
    method : str, optional
        The HTTP method to use (get, post, put, patch, delete).
    trigger : str, optional
        The event that triggers the request.
    target : str, optional
        The target element to update with the response.
    swap : str, optional
        How to swap the response into the DOM.
    include : str, optional
        Additional elements to include in the request.
    sync : str, optional
        How to synchronize the request with other requests.
    confirm : str, optional
        A confirmation message to show before sending the request.
    vals : str, optional
        Additional values to include in the request.

    Attributes
    ----------
    method : str
        The HTTP method to use.
    rule : str
        The URL or selector to use for the request.
    trigger : str
        The event that triggers the request.
    target : str
        The target element to update with the response.
    swap : str
        How to swap the response into the DOM.
    include : str
        Additional elements to include in the request.
    sync : str
        How to synchronize the request with other requests.
    confirm : str
        A confirmation message to show before sending the request.
    vals : str
        Additional values to include in the request.

    Examples
    --------
    >>> event = EventHandler(
    ...     method="get",
    ...     rule="/api/data",
    ...     target="#result",
    ...     trigger="click",
    ... )
    >>> event.to_string()  # 'hx-get="/api/data" hx-target="#result" hx-trigger="click"'
    """

    method = AttrsProperty("hx-")
    rule = AttrsProperty("hx-")
    trigger = AttrsProperty("hx-")
    target = AttrsProperty("hx-")
    swap = AttrsProperty("hx-")
    include = AttrsProperty("hx-")
    sync = AttrsProperty("hx-")
    confirm = AttrsProperty("hx-")
    vals = AttrsProperty("hx-")

    def __init__(
        self,
        rule: str | None = None,
        method: str | None = None,
        trigger: str | None = None,
        target: str | None = None,
        swap: str | None = None,
        include: str | None = None,
        sync: str | None = None,
        confirm: str | None = None,
        vals: str | None = None,
    ):
        """
        Initialize an event handler.

        Parameters
        ----------
        rule : str, optional
            The URL or selector to use for the request.
        method : str, optional
            The HTTP method to use (get, post, put, patch, delete).
        trigger : str, optional
            The event that triggers the request.
        target : str, optional
            The target element to update with the response.
        swap : str, optional
            How to swap the response into the DOM.
        include : str, optional
            Additional elements to include in the request.
        sync : str, optional
            How to synchronize the request with other requests.
        confirm : str, optional
            A confirmation message to show before sending the request.
        vals : str, optional
            Additional values to include in the request.
        """
        attrs = [
            (k, v)
            for k, v in {
                f"hx-{method}": rule,
                "hx-trigger": trigger,
                "hx-target": target,
                "hx-swap": swap,
                "hx-include": include,
                "hx-sync": sync,
                "hx-confirm": confirm,
                "hx-vals": vals,
            }.items()
            if v
        ]
        super().__init__(attrs)

    def render(self) -> str:
        """
        Render the event handler to HTML.

        Returns
        -------
        str
            The HTML representation of the event handler.
        """
        return f"<div {self.to_string()}></div>"


class EventHandlerList(ValidatedList[EventHandler]):
    """
    A list of event handlers bound to an element.

    This class extends ValidatedList to provide a list of event handlers
    that are bound to a specific element. It automatically validates and
    modifies event handlers to ensure they are properly bound to the element.

    Parameters
    ----------
    bound : Element
        The element to bind the event handlers to.
    data : list[EventHandler] or EventHandler or None, optional
        Initial event handlers to add to the list.

    Attributes
    ----------
    bound : weakref.ref[Element]
        A weak reference to the bound element.

    Examples
    --------
    >>> element = Element("div", id="my-div")
    >>> events = EventHandlerList(element)
    >>> events.append(EventHandler(method="get", rule="/api/data"))
    >>> len(events)  # 1
    """

    def __init__(
        self, bound: Element, data: list[EventHandler] | EventHandler | None = None
    ):
        """
        Initialize an event handler list.

        Parameters
        ----------
        bound : Element
            The element to bind the event handlers to.
        data : list[EventHandler] or EventHandler or None, optional
            Initial event handlers to add to the list.
        """
        super().__init__()
        self.bound = weakref.ref(bound)
        if isinstance(data, EventHandler):
            data = [data]
        self.extend(data or [])

    class Match:
        """
        A helper class for matching and replacing text in regular expressions.

        This class is used to track whether a match was found and to provide
        a replacement string.

        Parameters
        ----------
        repl : str
            The replacement string.

        Attributes
        ----------
        found : bool
            Whether a match was found.
        repl : str
            The replacement string.
        """

        def __init__(self, repl: str):
            """
            Initialize a match helper.

            Parameters
            ----------
            repl : str
                The replacement string.
            """
            self.found = False
            self.repl = repl

        def __call__(self, event: re.Match[str]) -> str:
            """
            Called when a match is found.

            Parameters
            ----------
            event : re.Match[str]
                The match object.

            Returns
            -------
            str
                The replacement string.
            """
            self.found = True
            return self.repl

    def validate(self, value: Any) -> EventHandler:
        """
        Validate and modify an event handler.

        This method ensures that the event handler is properly bound to the
        element by modifying its trigger attribute if necessary.

        Parameters
        ----------
        value : Any
            The event handler to validate.

        Returns
        -------
        EventHandler
            The validated and modified event handler.
        """
        event = (
            copy.deepcopy(value)
            if isinstance(value, EventHandler)
            else EventHandler(**value)
        )
        # replace or add the trigger (directing to the bound element)
        try:
            event.trigger  # noqa: B018
        except Exception:
            return event
        match = self.Match(f"#{self.bound().attrs.id}")
        event.trigger = re.sub(r"(?<=from:)([#\w]+)", match, event.trigger)
        if not match.found:
            event.trigger = f"{event.trigger} from:{match.repl}"
        return event
