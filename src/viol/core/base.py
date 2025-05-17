"""
Component System Base Module
===========================

Purpose
-------
This module provides the core component system for Viol, including the abstract
Component class, context management for rendering, and utility functions for
rendering components.

Core Functionality
-----------------
- Abstract Component base class for all UI components
- Context management for component rendering
- Linked list view for traversing parent-child relationships
- Utility functions for rendering components to HTML

Dependencies
-----------
- jinja2: For template rendering
- contextvars: For context management during rendering
- abc: For abstract base classes
- uuid: For generating unique component IDs

Usage Examples
-------------
>>> from viol.core.base import Component, render
>>>
>>> class MyComponent(Component):
>>>     def __init__(self, content):
>>>         super().__init__()
>>>         self.content = content
>>>
>>>     def render(self) -> str:
>>>         return f"<div>{self.content}</div>"
>>>
>>> # Create and render a component
>>> component = MyComponent("Hello, World!")
>>> html = render(component)  # "<div>Hello, World!</div>"

Edge Cases
---------
- None values are rendered as empty strings
- Iterables (lists, tuples) of components are joined with spaces
- Context is automatically managed during rendering
- String templates are rendered with Jinja2

Version History
--------------
1.0.0 - Initial stable release
"""

from __future__ import annotations

import abc
import functools
import uuid
import weakref
from collections import UserDict
from collections.abc import Iterable, Sequence
from contextvars import Context, ContextVar, copy_context
from typing import Any, TypeGuard, TypeVar, Union

from jinja2 import Template

__all__ = [
    "Component",
    "RenderableType",
    "render",
]

T = TypeVar("T")

render_ctx: ContextVar[ContextDict] = ContextVar("render_ctx", default=None)


class ListView(Sequence[T]):
    """
    A sequence view that traverses linked objects via an attribute.

    This class provides a sequence-like view of a chain of objects connected
    by a common attribute, such as parent-child relationships.

    Parameters
    ----------
    object : T
        The starting object for the list view.
    attr : str
        The attribute name to follow for traversal.

    Examples
    --------
    >>> obj = SomeObject()
    >>> obj.parent = ParentObject()
    >>> obj.parent.parent = GrandparentObject()
    >>> parents = ListView(obj, "parent")
    >>> len(parents)  # 2
    >>> list(parents)  # [ParentObject(), GrandparentObject()]
    """
    def __init__(self, object: T, attr: str):
        """
        Initialize a list view.

        Parameters
        ----------
        object : T
            The starting object for the list view.
        attr : str
            The attribute name to follow for traversal.
        """
        self.get_object = weakref.ref(object)
        self.attr = attr

    def __iter__(self) -> Iterable[T]:
        """
        Iterate through the linked objects.

        Yields
        ------
        T
            Each object in the chain, starting from the first linked object.
        """
        obj = self.get_object()
        while obj is not None:
            obj = getattr(obj, self.attr)
            yield obj

    def __len__(self) -> int:
        """
        Get the number of linked objects.

        Returns
        -------
        int
            The number of objects in the chain.
        """
        obj = self.get_object()
        count = 0
        while obj is not None:
            count += 1
            obj = getattr(obj, self.attr)
        return count

    def __getitem__(self, index: int) -> T:
        """
        Get an object at a specific position in the chain.

        Parameters
        ----------
        index : int
            The index of the object to retrieve.

        Returns
        -------
        T
            The object at the specified index.

        Raises
        ------
        IndexError
            If the index is out of range.
        """
        obj = self.get_object()
        for _ in range(index):
            if obj is None:
                msg = f"index {index} out of range for '{self.attr}'"
                raise IndexError(msg)
            obj = getattr(obj, self.attr)
        return obj


class ContextDict(UserDict[str, Any]):
    """
    A dictionary for component rendering context with parent-child relationships.

    This class extends UserDict to provide a context dictionary that can be
    linked to parent contexts, allowing for hierarchical context lookups.

    Attributes
    ----------
    parent : ContextDict or None
        The parent context dictionary, if any.
    component : Component or None
        The component associated with this context.
    parents : ListView[ContextDict]
        A list view of all parent contexts.

    Examples
    --------
    >>> ctx = ContextDict({"key": "value"})
    >>> parent_ctx = ContextDict({"parent_key": "parent_value"})
    >>> ctx.parent = parent_ctx
    >>> ctx["key"]  # "value"
    >>> ctx["parent_key"]  # "parent_value" (from parent)
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize a context dictionary.

        Parameters
        ----------
        *args
            Arguments to pass to UserDict.__init__.
        **kwargs
            Keyword arguments to pass to UserDict.__init__.
        """
        super().__init__(*args, **kwargs)
        self.parent: ContextDict | None = None
        self.component: Component | None = None

    @property
    def parents(self) -> ListView[ContextDict]:
        """
        Get a list view of all parent contexts.

        Returns
        -------
        ListView[ContextDict]
            A list view of all parent contexts.
        """
        return ListView(self, "parent")

    def __getitem__(self, key: str) -> Any:
        """
        Get an item from this context or a parent context.

        Parameters
        ----------
        key : str
            The key to look up.

        Returns
        -------
        Any
            The value associated with the key.

        Raises
        ------
        KeyError
            If the key is not found in this context or any parent context.
        """
        try:
            return super().__getitem__(key)
        except KeyError:
            if self.parent is not None:
                return self.parent[key]
            raise

    def __delitem__(self, key: str) -> None:
        """
        Delete an item from this context or a parent context.

        Parameters
        ----------
        key : str
            The key to delete.

        Raises
        ------
        KeyError
            If the key is not found in this context or any parent context.
        """
        try:
            super().__delitem__(key)
        except KeyError:
            if self.parent:
                del self.parent[key]
            raise

    def __iter__(self) -> Iterable[str]:
        """
        Iterate over all keys in this context and parent contexts.

        Returns
        -------
        Iterable[str]
            An iterator over all keys.
        """
        keys = set(super().__iter__())
        if self.parent:
            keys.update(self.parent.__iter__())
        return iter(keys)

    def __len__(self) -> int:
        """
        Get the number of unique keys in this context and parent contexts.

        Returns
        -------
        int
            The number of unique keys.
        """
        return len(set(self.keys()))


class Component(abc.ABC):
    """
    Abstract base class for all UI components.

    This class provides the foundation for all UI components in Viol,
    including context management and rendering.

    Attributes
    ----------
    uuid : str
        A unique identifier for the component.
    ctx : ContextDict
        The current rendering context.

    Examples
    --------
    >>> class MyComponent(Component):
    ...     def __init__(self, content):
    ...         super().__init__()
    ...         self.content = content
    ...
    ...     def render(self) -> str:
    ...         return f"<div>{self.content}</div>"
    """
    uuid: str

    def __new__(cls, *args, **kwargs):
        """
        Create a new component instance with a unique ID.

        Parameters
        ----------
        *args
            Arguments to pass to the constructor.
        **kwargs
            Keyword arguments to pass to the constructor.

        Returns
        -------
        Component
            A new component instance.
        """
        obj = super().__new__(cls)
        obj.uuid = uuid.uuid4().hex
        return obj

    @property
    def ctx(self) -> ContextDict:
        """
        Get the current rendering context.

        Returns
        -------
        ContextDict
            The current rendering context.
        """
        return render_ctx.get()

    @abc.abstractmethod
    def render(self) -> str:
        """
        Render the component to HTML.

        This method must be implemented by subclasses.

        Returns
        -------
        str
            The HTML representation of the component.
        """
        ...

    def render_with_context(self) -> str:
        """
        Render the component with a new context.

        This method sets up a new context for rendering the component,
        linking it to the parent context if one exists.

        Returns
        -------
        str
            The HTML representation of the component.
        """
        ctx = ContextDict()
        parent = render_ctx.get()
        ctx.parent = parent
        ctx.component = self
        token = render_ctx.set(ctx)
        try:
            return super().__getattribute__("render")()
        finally:
            if token:
                render_ctx.reset(token)

    def __getattribute__(self, name: str) -> Any:
        """
        Get an attribute from the component.

        Special handling for the 'render' attribute to ensure proper context management.

        Parameters
        ----------
        name : str
            The name of the attribute to get.

        Returns
        -------
        Any
            The attribute value.
        """
        attr = super().__getattribute__(name)
        if name == "render":
            # copy the current context
            ctx: Context = copy_context()
            return functools.partial(ctx.run, self.render_with_context)
        return attr


RenderableType = Union[
    Component,
    Iterable[Component],
    str,
    None,
]


def is_renderable(obj: Any) -> TypeGuard[RenderableType]:
    """
    Check if an object is renderable.

    Parameters
    ----------
    obj : Any
        The object to check.

    Returns
    -------
    bool
        True if the object is renderable, False otherwise.
    """
    if obj is None:
        # None is renderable as an empty string
        return True
    if isinstance(obj, (Component, str)):
        # Components and strings are renderable
        return True
    if isinstance(obj, Iterable) and not isinstance(obj, str):
        # All elements of an iterable must be renderable
        # Caution: iterators will be consumed
        return all(is_renderable(c) for c in obj)
    # Not renderable
    return False


def render(r: RenderableType) -> str:
    """
    Render an object to HTML.

    Parameters
    ----------
    r : RenderableType
        The object to render. Can be a Component, an iterable of Components,
        a string, or None.

    Returns
    -------
    str
        The HTML representation of the object.

    Examples
    --------
    >>> component = MyComponent("Hello, World!")
    >>> render(component)  # "<div>Hello, World!</div>"
    >>> render([component, component])  # "<div>Hello, World!</div> <div>Hello, World!</div>"
    >>> render(None)  # ""
    >>> render("Hello, {{ name }}")  # "Hello, World" (with context {"name": "World"})
    """
    # None
    if r is None:
        return ""
    if isinstance(r, Component):
        # components
        return r.render()
    if isinstance(r, Iterable) and not isinstance(r, str):
        # lists, tuples, sets, etc.
        return " ".join(render(c) for c in r)
    # template to render
    if isinstance(r, str):
        r: Template = Template(r)
    ctx = render_ctx.get()
    if ctx is None:
        return r.render()
    return r.render(ctx=ctx)
