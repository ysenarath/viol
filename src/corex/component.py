"""
Component module for corex.

This module defines the Component class, which is the basic building block for corex applications.
Components can contain other components and can be replaced based on UI actions.
"""

from __future__ import annotations

import uuid
from typing import List, Optional


class Component:
    """
    Base Component class for corex applications.

    A Component is the basic building block of a corex application. Components can contain
    other components and can be replaced based on UI actions.
    """

    def __init__(self, id: Optional[str] = None, **kwargs):
        """
        Initialize a Component.

        Args:
            id: Optional unique identifier for the component. If not provided, a UUID will be generated.
            **kwargs: Additional attributes to set on the component.
        """
        self.id = id or str(uuid.uuid4())
        self.children: List[Component] = []
        self.parent: Optional[Component] = None
        self.attributes = kwargs

    def add_child(self, component: Component) -> Component:
        """
        Add a child component to this component.

        Args:
            component: The component to add as a child.

        Returns:
            The added component for method chaining.
        """
        component.parent = self
        self.children.append(component)
        return component

    def add_children(self, *components: Component) -> Component:
        """
        Add multiple child components to this component.

        Args:
            *components: The components to add as children.

        Returns:
            Self for method chaining.
        """
        for component in components:
            self.add_child(component)
        return self

    def replace_with(self, component: Component) -> Component:
        """
        Replace this component with another component in the parent's children list.

        Args:
            component: The component to replace this component with.

        Returns:
            The new component that replaced this component.
        """
        if self.parent is None:
            raise ValueError("Cannot replace a component without a parent")

        index = self.parent.children.index(self)
        self.parent.children[index] = component
        component.parent = self.parent
        self.parent = None
        return component

    def find_by_id(self, id: str) -> Optional[Component]:
        """
        Find a component by its ID in this component's hierarchy.

        Args:
            id: The ID of the component to find.

        Returns:
            The component with the given ID, or None if not found.
        """
        if self.id == id:
            return self

        for child in self.children:
            found = child.find_by_id(id)
            if found:
                return found

        return None

    def render(self) -> str:
        """
        Render this component to HTML.

        This method should be overridden by subclasses to provide custom rendering.
        The base implementation renders a div with the component's ID and any children.

        Returns:
            The HTML representation of this component.
        """
        attrs = " ".join([f'{k}="{v}"' for k, v in self.attributes.items()])
        attrs = f" {attrs}" if attrs else ""

        children_html = "".join([child.render() for child in self.children])

        return f'<div id="{self.id}"{attrs}>{children_html}</div>'
