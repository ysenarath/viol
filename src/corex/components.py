"""
Pre-built components for corex.

This module provides common component types that extend the base Component class.
"""

from __future__ import annotations

from typing import Optional

from .component import Component


class TextComponent(Component):
    """
    A component for displaying text.
    """

    def __init__(self, text: str, tag: str = "p", id: Optional[str] = None, **kwargs):
        """
        Initialize a TextComponent.

        Args:
            text: The text to display.
            tag: The HTML tag to use (default: "p").
            id: Optional unique identifier for the component.
            **kwargs: Additional attributes to set on the component.
        """
        super().__init__(id=id, **kwargs)
        self.text = text
        self.tag = tag

    def render(self) -> str:
        """
        Render this component to HTML.

        Returns:
            The HTML representation of this component.
        """
        attrs = " ".join([f'{k}="{v}"' for k, v in self.attributes.items()])
        attrs = f" {attrs}" if attrs else ""

        return f'<{self.tag} id="{self.id}"{attrs}>{self.text}</{self.tag}>'


class ButtonComponent(Component):
    """
    A component for creating buttons that can trigger actions.
    """

    def __init__(
        self,
        text: str,
        action: str,
        component_id: str,
        id: Optional[str] = None,
        **kwargs,
    ):
        """
        Initialize a ButtonComponent.

        Args:
            text: The text to display on the button.
            action: The name of the action to trigger.
            component_id: The ID of the component to perform the action on.
            id: Optional unique identifier for the component.
            **kwargs: Additional attributes to set on the component.
        """
        super().__init__(id=id, **kwargs)
        self.text = text
        self.action = action
        self.target_component_id = component_id

    def render(self) -> str:
        """
        Render this component to HTML.

        Returns:
            The HTML representation of this component.
        """
        attrs = " ".join([f'{k}="{v}"' for k, v in self.attributes.items()])
        attrs = f" {attrs}" if attrs else ""

        # Use HTMX to trigger the component action
        htmx_attrs = f"""
            hx-post="/components/{self.id}/action/{self.action}"
            hx-trigger="click"
            hx-target="#{self.target_component_id}"
            hx-swap="outerHTML"
        """

        return f'<button id="{self.id}"{attrs} {htmx_attrs}>{self.text}</button>'


class ContainerComponent(Component):
    """
    A component for grouping other components with specific styling.
    """

    def __init__(self, tag: str = "div", id: Optional[str] = None, **kwargs):
        """
        Initialize a ContainerComponent.

        Args:
            tag: The HTML tag to use (default: "div").
            id: Optional unique identifier for the component.
            **kwargs: Additional attributes to set on the component.
        """
        super().__init__(id=id, **kwargs)
        self.tag = tag

    def render(self) -> str:
        """
        Render this component to HTML.

        Returns:
            The HTML representation of this component.
        """
        attrs = " ".join([f'{k}="{v}"' for k, v in self.attributes.items()])
        attrs = f" {attrs}" if attrs else ""

        children_html = "".join([child.render() for child in self.children])

        return f'<{self.tag} id="{self.id}"{attrs}>{children_html}</{self.tag}>'


class InputComponent(Component):
    """
    A component for creating input fields.
    """

    def __init__(
        self,
        name: str,
        input_type: str = "text",
        value: str = "",
        placeholder: str = "",
        id: Optional[str] = None,
        **kwargs,
    ):
        """
        Initialize an InputComponent.

        Args:
            name: The name of the input field.
            input_type: The type of input (default: "text").
            value: The initial value of the input.
            placeholder: The placeholder text for the input.
            id: Optional unique identifier for the component.
            **kwargs: Additional attributes to set on the component.
        """
        super().__init__(id=id, **kwargs)
        self.name = name
        self.input_type = input_type
        self.value = value
        self.placeholder = placeholder

    def render(self) -> str:
        """
        Render this component to HTML.

        Returns:
            The HTML representation of this component.
        """
        attrs = " ".join([f'{k}="{v}"' for k, v in self.attributes.items()])
        attrs = f" {attrs}" if attrs else ""

        return f'''
            <input 
                id="{self.id}" 
                name="{self.name}" 
                type="{self.input_type}" 
                value="{self.value}" 
                placeholder="{self.placeholder}"
                {attrs}
            >
        '''


class FormComponent(Component):
    """
    A component for creating forms with inputs.
    """

    def __init__(
        self,
        action: str,
        component_id: str,
        method: str = "post",
        id: Optional[str] = None,
        **kwargs,
    ):
        """
        Initialize a FormComponent.

        Args:
            action: The name of the action to trigger on submit.
            component_id: The ID of the component to perform the action on.
            method: The HTTP method to use (default: "post").
            id: Optional unique identifier for the component.
            **kwargs: Additional attributes to set on the component.
        """
        super().__init__(id=id, **kwargs)
        self.action_name = action
        self.target_component_id = component_id
        self.method = method

    def render(self) -> str:
        """
        Render this component to HTML.

        Returns:
            The HTML representation of this component.
        """
        attrs = " ".join([f'{k}="{v}"' for k, v in self.attributes.items()])
        attrs = f" {attrs}" if attrs else ""

        # Use HTMX to handle form submission
        htmx_attrs = f"""
            hx-post="/components/{self.target_component_id}/action/{self.action_name}"
            hx-trigger="submit"
            hx-target="#{self.target_component_id}"
            hx-swap="outerHTML"
        """

        children_html = "".join([child.render() for child in self.children])

        return f'''
            <form id="{self.id}" method="{self.method}" {attrs} {htmx_attrs}>
                {children_html}
            </form>
        '''


class CardComponent(Component):
    """
    A component for creating card-like UI elements.
    """

    def __init__(self, title: Optional[str] = None, id: Optional[str] = None, **kwargs):
        """
        Initialize a CardComponent.

        Args:
            title: Optional title for the card.
            id: Optional unique identifier for the component.
            **kwargs: Additional attributes to set on the component.
        """
        super().__init__(id=id, **kwargs)
        self.title = title

        # Default styling for cards
        self.attributes.setdefault(
            "style",
            """
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 16px;
            margin: 8px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        """,
        )

    def render(self) -> str:
        """
        Render this component to HTML.

        Returns:
            The HTML representation of this component.
        """
        attrs = " ".join([f'{k}="{v}"' for k, v in self.attributes.items()])
        attrs = f" {attrs}" if attrs else ""

        title_html = f"<h3>{self.title}</h3>" if self.title else ""
        children_html = "".join([child.render() for child in self.children])

        return f'''
            <div id="{self.id}" {attrs}>
                {title_html}
                {children_html}
            </div>
        '''


class ListComponent(Component):
    """
    A component for creating lists of items.
    """

    def __init__(self, ordered: bool = False, id: Optional[str] = None, **kwargs):
        """
        Initialize a ListComponent.

        Args:
            ordered: Whether the list should be ordered (ol) or unordered (ul).
            id: Optional unique identifier for the component.
            **kwargs: Additional attributes to set on the component.
        """
        super().__init__(id=id, **kwargs)
        self.ordered = ordered

    def render(self) -> str:
        """
        Render this component to HTML.

        Returns:
            The HTML representation of this component.
        """
        attrs = " ".join([f'{k}="{v}"' for k, v in self.attributes.items()])
        attrs = f" {attrs}" if attrs else ""

        tag = "ol" if self.ordered else "ul"
        children_html = "".join(
            [f"<li>{child.render()}</li>" for child in self.children]
        )

        return f'<{tag} id="{self.id}"{attrs}>{children_html}</{tag}>'
