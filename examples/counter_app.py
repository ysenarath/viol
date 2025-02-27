"""
A simple counter app example using corex.

This example demonstrates how to create a counter application using corex components.
"""

import sys
import os

# Add the parent directory to the path so we can import corex
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.corex import (
    Component,
    create_app,
    TextComponent,
    ButtonComponent,
    ContainerComponent,
)


class CounterComponent(Component):
    """A component representing a counter with increment and decrement buttons."""

    def __init__(self, count: int = 0, id: str = None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.count = count

        # Create a container with centered content
        container = ContainerComponent(
            style="display: flex; flex-direction: column; align-items: center; margin: 50px auto; max-width: 400px;"
        )

        # Create a title
        title = TextComponent(
            text="Counter Example", tag="h1", style="margin-bottom: 20px;"
        )

        # Create the count display
        count_display = TextComponent(
            text=str(self.count), tag="div", style="font-size: 72px; margin: 20px 0;"
        )

        # Create a container for the buttons
        button_container = ContainerComponent(style="display: flex; gap: 10px;")

        # Create decrement button
        decrement_button = ButtonComponent(
            text="-",
            action="decrement",
            component_id=self.id,
            style="padding: 10px 20px; font-size: 24px; cursor: pointer; background-color: #f44336; color: white; border: none; border-radius: 4px;",
        )

        # Create increment button
        increment_button = ButtonComponent(
            text="+",
            action="increment",
            component_id=self.id,
            style="padding: 10px 20px; font-size: 24px; cursor: pointer; background-color: #4CAF50; color: white; border: none; border-radius: 4px;",
        )

        # Create reset button
        reset_button = ButtonComponent(
            text="Reset",
            action="reset",
            component_id=self.id,
            style="padding: 10px 20px; margin-top: 20px; cursor: pointer; background-color: #2196F3; color: white; border: none; border-radius: 4px;",
        )

        # Add buttons to the button container
        button_container.add_children(decrement_button, increment_button)

        # Add all components to the container
        container.add_children(title, count_display, button_container, reset_button)

        # Add the container to this component
        self.add_child(container)

    def increment(self):
        """Return a new counter with incremented count."""
        return CounterComponent(self.count + 1, id=self.id)

    def decrement(self):
        """Return a new counter with decremented count."""
        return CounterComponent(max(0, self.count - 1), id=self.id)

    def reset(self):
        """Return a new counter with count reset to 0."""
        return CounterComponent(0, id=self.id)


def create_counter_app():
    """Create and configure the counter app."""
    app = create_app(__name__)

    # Create the root component
    counter = CounterComponent(id="counter")

    # Set the root component
    app.set_root_component(counter)

    # Register action handlers
    app.register_component_action("counter", "increment", lambda c, d: c.increment())
    app.register_component_action("counter", "decrement", lambda c, d: c.decrement())
    app.register_component_action("counter", "reset", lambda c, d: c.reset())

    return app


if __name__ == "__main__":
    app = create_counter_app()
    app.run(debug=True)
