"""
Tests for the CorexApp class.
"""

import unittest
import sys
import os
import json

# Add the parent directory to the path so we can import corex
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.corex import Component, CorexApp, TextComponent, ButtonComponent


class TestCorexApp(unittest.TestCase):
    """Test cases for the CorexApp class."""

    def setUp(self):
        """Set up a test app and client for each test."""
        self.app = CorexApp(__name__)
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        # Create a simple root component
        self.root = TextComponent("Hello, Corex!", tag="h1", id="root")
        self.app.set_root_component(self.root)

    def test_index_route(self):
        """Test that the index route returns the rendered root component."""
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello, Corex!", response.data)
        self.assertIn(b'id="root"', response.data)

    def test_component_action(self):
        """Test that a component action can be triggered and handled."""
        # Add a button to the root component
        button = ButtonComponent(
            "Click me!", action="change_text", component_id="root", id="button"
        )
        self.root.add_child(button)

        # Register an action handler
        def change_text_handler(component, data):
            return TextComponent("Text changed!", tag="h1", id=component.id)

        self.app.register_component_action("root", "change_text", change_text_handler)

        # Trigger the action
        response = self.client.post(
            "/components/root/action/change_text",
            data=json.dumps({}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Text changed!", response.data)
        self.assertIn(b'id="root"', response.data)

    def test_component_action_with_data(self):
        """Test that a component action can be triggered with data."""

        # Register an action handler that uses data
        def update_text_handler(component, data):
            new_text = data.get("text", "No text provided")
            return TextComponent(new_text, tag="h1", id=component.id)

        self.app.register_component_action("root", "update_text", update_text_handler)

        # Trigger the action with data
        response = self.client.post(
            "/components/root/action/update_text",
            data=json.dumps({"text": "Updated text!"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Updated text!", response.data)

    def test_component_not_found(self):
        """Test that a 404 is returned when a component is not found."""
        response = self.client.post(
            "/components/nonexistent/action/test",
            data=json.dumps({}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)

    def test_action_not_found(self):
        """Test that a 404 is returned when an action is not found."""
        response = self.client.post(
            "/components/root/action/nonexistent",
            data=json.dumps({}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)

    def test_no_root_component(self):
        """Test that an error is returned when no root component is set."""
        app = CorexApp(__name__)
        app.config["TESTING"] = True
        client = app.test_client()

        response = client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No root component set", response.data)


if __name__ == "__main__":
    unittest.main()
