"""
App module for corex.

This module defines the CorexApp class, which is a Flask application that can serve
corex components.
"""

from __future__ import annotations

from typing import Dict, Optional, Callable, Any

from flask import Flask, request, render_template_string, Response, jsonify

from .component import Component


class CorexApp(Flask):
    """
    A Flask application that can serve corex components.

    This class extends Flask to provide functionality for serving corex components
    and handling component updates via HTMX.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize a CorexApp.

        Args:
            *args: Additional arguments to pass to Flask.
            **kwargs: Additional arguments to pass to Flask.
        """
        super().__init__(*args, **kwargs)
        self.root_component: Optional[Component] = None
        self.component_actions: Dict[str, Dict[str, Callable]] = {}

        # Register the default routes
        self.add_url_rule("/", "index", self._index)
        self.add_url_rule(
            "/components/<component_id>/action/<action_name>/",
            "component_action",
            self._component_action,
            methods=["POST", "GET"],
        )

    def set_root_component(self, component: Component) -> None:
        """
        Set the root component for this application.

        Args:
            component: The component to set as the root component.
        """
        self.root_component = component

    def register_component_action(
        self,
        component_id: str,
        action_name: str,
        action_handler: Callable[[Component, Any], Component],
    ) -> None:
        """
        Register an action handler for a component.

        Args:
            component_id: The ID of the component to register the action for.
            action_name: The name of the action.
            action_handler: A function that takes a component and action data and returns a new component.
        """
        if component_id not in self.component_actions:
            self.component_actions[component_id] = {}

        self.component_actions[component_id][action_name] = action_handler

    def _index(self) -> str:
        """
        Render the index page with the root component.

        Returns:
            The rendered HTML for the index page.
        """
        if self.root_component is None:
            return "No root component set"

        return self._render_page(self.root_component)

    def _component_action(self, component_id: str, action_name: str) -> Response:
        """
        Handle a component action.

        Args:
            component_id: The ID of the component to perform the action on.
            action_name: The name of the action to perform.

        Returns:
            A response containing the rendered HTML for the updated component.
        """
        if self.root_component is None:
            return jsonify({"error": "No root component set"}), 400

        component = self.root_component.find_by_id(component_id)
        if component is None:
            return jsonify(
                {"error": f"Component with ID {component_id} not found"}
            ), 404

        if (
            component_id not in self.component_actions
            or action_name not in self.component_actions[component_id]
        ):
            return jsonify(
                {
                    "error": f"Action {action_name} not registered for component {component_id}"
                }
            ), 404

        action_data = request.json or {}
        action_handler = self.component_actions[component_id][action_name]

        try:
            new_component = action_handler(component, action_data)

            # If the action handler returns a component, replace the current component with it
            if new_component is not component:
                component.replace_with(new_component)
                component = new_component

            # Return just the HTML for the updated component
            return Response(component.render(), mimetype="text/html")
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def _render_page(self, root_component: Component) -> str:
        """
        Render a full HTML page with the given root component.

        Args:
            root_component: The root component to render.

        Returns:
            The rendered HTML page.
        """
        # Basic HTML template with HTMX included
        template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Corex App</title>
            <script src="https://unpkg.com/htmx.org@1.9.6"></script>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                    line-height: 1.5;
                    margin: 0;
                    padding: 0;
                }
            </style>
        </head>
        <body>
            {{ component_html|safe }}
        </body>
        </html>
        """

        return render_template_string(template, component_html=root_component.render())


def create_app(import_name: str, **kwargs) -> CorexApp:
    """
    Create a new CorexApp.

    Args:
        import_name: The name of the package or module that this app belongs to.
        **kwargs: Additional arguments to pass to CorexApp.

    Returns:
        A new CorexApp instance.
    """
    return CorexApp(import_name, **kwargs)
