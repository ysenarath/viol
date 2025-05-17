"""
HTML Attribute Management Module
===============================

Purpose
-------
This module provides classes for managing HTML attributes in a case-insensitive way,
with special handling for certain attributes like 'class' and HTMX attributes.

Core Functionality
-----------------
- Case-insensitive attribute dictionary
- Special handling for class attributes (as lists)
- Property descriptors for common attributes
- Support for HTMX method attributes
- HTML attribute string rendering with proper escaping

Dependencies
-----------
- multidict: For case-insensitive multi-dictionaries
- html.escape: For proper HTML attribute escaping
- typing_extensions: For advanced type annotations

Usage Examples
-------------
>>> from viol.core.attributes import AttrMultiDict
>>>
>>> # Create attributes
>>> attrs = AttrMultiDict(id="my-element", class="btn btn-primary")
>>>
>>> # Access attributes
>>> attrs["id"]  # "my-element"
>>> attrs.id     # "my-element" (property access)
>>> attrs.class_ # ["btn", "btn-primary"] (as list)
>>>
>>> # Render to HTML attribute string
>>> attrs.to_string()  # 'id="my-element" class="btn btn-primary"'

Edge Cases
---------
- Class attributes can be provided as space-separated strings or lists
- HTMX method attributes (get, post, etc.) have special handling
- Case-insensitive keys but preserves original case for rendering

Version History
--------------
1.0.0 - Initial stable release
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, MutableMapping
from html import escape
from typing import Any, ClassVar, Generic, TypeVar, overload

from multidict import CIMultiDict
from typing_extensions import Literal

from viol.core.base import render

__all__ = [
    "AttrMultiDict",
]

T = TypeVar("T")


class AttrsProperty(Generic[T]):
    """
    Descriptor for HTML attribute properties with special handling.

    This descriptor provides property-like access to attributes in AttrMultiDict,
    with special handling for certain attributes like HTTP methods and rules.

    Parameters
    ----------
    prefix : str, optional
        Prefix to apply to the attribute name (e.g., "hx-").
    name : str, optional
        Explicit name for the attribute. If not provided,
        the property name with prefix will be used.

    Attributes
    ----------
    methods : set of str
        Class variable containing the set of supported HTTP methods.
    prefix : str
        Prefix applied to the attribute name.
    name : str
        The attribute name.

    Examples
    --------
    >>> class MyAttrs(AttrMultiDict):
    ...     id = AttrsProperty[str]()
    ...     method = AttrsProperty[str]("hx-")
    """
    methods: ClassVar[set[str]] = {"get", "post", "put", "patch", "delete"}

    def __init__(self, prefix: str = "", name: str | None = None):
        """
        Initialize an attribute property.

        Parameters
        ----------
        prefix : str, optional
            Prefix to apply to the attribute name (e.g., "hx-").
        name : str, optional
            Explicit name for the attribute. If not provided,
            the property name with prefix will be used.
        """
        self.prefix = prefix
        self.name = name

    def __set_name__(self, owner: Any, name: str, /) -> None:
        """
        Set the descriptor name when it's assigned to a class.
        
        Parameters
        ----------
        owner : type
            The class that owns this descriptor.
        name : str
            The name of the attribute this descriptor is assigned to.
        """
        if self.name:
            return
        self.name = f"{self.prefix}{name}"

    def __get__(self, instance: AttrMultiDict | None, owner: Any = None) -> T:
        """
        Get the attribute value from the instance.

        Special handling for method and rule attributes with prefixes.

        Parameters
        ----------
        instance : AttrMultiDict or None
            The AttrMultiDict instance.
        owner : type, optional
            The class that owns this descriptor.

        Returns
        -------
        T
            The attribute value.

        Raises
        ------
        KeyError
            If the attribute doesn't exist in the instance.
        """
        if instance is None:
            return self
        if self.name == f"{self.prefix}method":
            for method in self.methods:
                if instance.get(f"{self.prefix}{method}"):
                    return method
        if self.name == f"{self.prefix}rule":
            for method in self.methods:
                rule = instance.get(f"{self.prefix}{method}")
                if rule:
                    return rule
        return instance[self.name]

    def __set__(self, instance: AttrMultiDict | None, value: T) -> None:
        """
        Set the attribute value on the instance.

        Special handling for method and rule attributes with prefixes.

        Parameters
        ----------
        instance : AttrMultiDict or None
            The AttrMultiDict instance.
        value : T
            The value to set.

        Raises
        ------
        AttributeError
            If instance is None.
        """
        if instance is None:
            msg = f"{self.name} must be set on an Event instance"
            raise AttributeError(msg)
        if self.name == f"{self.prefix}method":
            # find current method
            current_method = None
            for method in self.methods:
                current_method = f"{self.prefix}{method}"
                if current_method in instance:
                    break
            # get and delete the current rule
            current_rule = instance[current_method]
            del instance[current_method]
            # set the new method
            instance[f"{self.prefix}{value}"] = current_rule
        elif self.name == f"{self.prefix}rule":
            # find current method
            current_method = None
            for method in self.methods:
                current_method = f"{self.prefix}{method}"
                if current_method in instance:
                    break
            # set the new rule for the current method
            instance[current_method] = value
        else:
            instance[self.name] = value


class AttrMultiDict(MutableMapping[str, T]):
    """
    A case-insensitive dictionary for HTML attributes with special handling.

    This class provides a dictionary-like interface for HTML attributes with
    special handling for certain attributes like 'class' and support for
    property-like access to common attributes.

    Attributes
    ----------
    id : AttrsProperty[str]
        Property for the 'id' attribute.
    _ : AttrsProperty[str]
        Property for the hyperscript ('_') attribute.
    class_ : AttrsProperty[list[str]]
        Property for the 'class' attribute (as a list of strings).
    style : AttrsProperty[str]
        Property for the 'style' attribute.

    Examples
    --------
    >>> # Create attributes
    >>> attrs = AttrMultiDict(id="my-element", class="btn btn-primary")
    >>>
    >>> # Dictionary-like access
    >>> attrs["id"] = "new-id"
    >>>
    >>> # Property access
    >>> attrs.id = "new-id"
    >>> attrs.class_ = ["btn", "btn-secondary"]
    >>>
    >>> # Render to HTML
    >>> html_attrs = attrs.to_string()  # 'id="new-id" class="btn btn-secondary"'
    """
    id = AttrsProperty[str]()
    _ = AttrsProperty[str]()
    class_ = AttrsProperty[list[str]](name="class")
    style = AttrsProperty[str]()

    def __init__(self, *args: Mapping[str, T] | None, **kwargs: T):
        """
        Initialize an attribute dictionary.

        Parameters
        ----------
        *args : Mapping[str, T] or None
            Optional mapping to initialize from.
        **kwargs : T
            Optional keyword arguments to initialize from.

        Raises
        ------
        TypeError
            If more than one positional argument is provided.
        """
        if args:
            if len(args) > 1:
                msg = "at most one mapping is allowed"
                raise TypeError(msg)
            if args[0] is None:
                args = {}
        self._data = CIMultiDict()
        self.update(dict(*args, **kwargs))

    @overload
    def __getitem__(self, key: Literal["class"]) -> list[str]: ...

    def __getitem__(self, key: str) -> T:
        """
        Get an attribute value.

        Special handling for 'class' attribute to ensure it's always a list.

        Parameters
        ----------
        key : str
            The attribute name.

        Returns
        -------
        T
            The attribute value.

        Raises
        ------
        KeyError
            If the attribute doesn't exist.
        """
        if key == "class" and key not in self._data:
            self._data[key] = []
        return self._data[key]

    def _validate_class(self, value: T) -> list[str]:
        """
        Validate and normalize a class attribute value.

        Converts string class values to lists of class names.

        Parameters
        ----------
        value : T
            The class value to validate.

        Returns
        -------
        list of str
            A list of class names.
        """
        if isinstance(value, str):
            value = set(value.strip().split())
        return list(value)

    def __setitem__(self, key: str, value: T) -> None:
        """
        Set an attribute value.

        Special handling for 'class' attribute to ensure it's always a list.

        Parameters
        ----------
        key : str
            The attribute name.
        value : T
            The attribute value.
        """
        if key == "class":
            self._data[key] = self._validate_class(value)
        else:
            self._data[key] = value

    def __delitem__(self, key: str) -> None:
        """
        Delete an attribute.

        Parameters
        ----------
        key : str
            The attribute name.

        Raises
        ------
        KeyError
            If the attribute doesn't exist.
        """
        del self._data[key]

    def __iter__(self) -> Iterable[str]:
        """
        Iterate over attribute names.

        Returns
        -------
        Iterable[str]
            An iterator over attribute names.
        """
        return iter(self._data)

    def __len__(self) -> int:
        """
        Get the number of attributes.

        Returns
        -------
        int
            The number of attributes.
        """
        return len(self._data)

    def to_string(self) -> str:
        """
        Render attributes to an HTML attribute string.

        Returns
        -------
        str
            A string of HTML attributes in the format 'key="value"'.

        Raises
        ------
        ValueError
            If an attribute value cannot be rendered.
        """
        items = []
        for k, v in self.items():
            try:
                v = render(v)  # noqa: PLW2901
            except Exception as e:
                msg = f"unable to render value '{v}' for attribute '{k}' due to {type(e).__name__}({e})"
                raise ValueError(msg) from None
            items.append(f'{escape(k)}="{escape(v)}"')
        return " ".join(items)

    def __repr__(self) -> str:
        """
        Get a string representation of the attributes.

        Returns
        -------
        str
            The HTML attribute string.
        """
        return self.to_string()
