# Corex

[![PyPI - Version](https://img.shields.io/pypi/v/corex.svg)](https://pypi.org/project/corex)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/corex.svg)](https://pypi.org/project/corex)

Corex is a Flask and HTMX-based app building platform. It provides a component-based architecture for building web applications, where "Component" is the basic unit. Components can contain other components and may get replaced on different actions on the UI.

---

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Concepts](#core-concepts)
  - [Components](#components)
  - [Actions](#actions)
- [Built-in Components](#built-in-components)
- [Creating Custom Components](#creating-custom-components)
- [Examples](#examples)
- [License](#license)

## Installation

```console
pip install corex
```

## Quick Start

Here's a simple example of creating a Corex application:

```python
from corex import create_app, TextComponent, ButtonComponent

# Create a Corex app
app = create_app(__name__)

# Create a root component
root = TextComponent("Hello, Corex!", tag="h1")

# Add a button that will replace the text when clicked
button = ButtonComponent("Click me!", action="change_text", component_id=root.id)
root.add_child(button)

# Set the root component
app.set_root_component(root)

# Register an action handler
def change_text_handler(component, data):
    return TextComponent("Text changed!", tag="h1", id=component.id)

app.register_component_action(root.id, "change_text", change_text_handler)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
```

## Core Concepts

### Components

Components are the basic building blocks of a Corex application. A component:

- Has a unique ID
- Can contain other components (hierarchical structure)
- Can be replaced based on UI actions
- Renders to HTML

The base `Component` class provides methods for:

- Adding child components
- Finding components by ID
- Replacing components
- Rendering to HTML

### Actions

Actions are events that can be triggered by user interactions (like clicking a button or submitting a form). When an action is triggered:

1. The client sends a request to the server
2. The server executes the registered action handler
3. The handler returns a new or modified component
4. The component is rendered and sent back to the client
5. The client updates the UI with the new component

## Built-in Components

Corex provides several built-in components:

- `TextComponent`: For displaying text
- `ButtonComponent`: For creating buttons that can trigger actions
- `ContainerComponent`: For grouping components with specific styling
- `InputComponent`: For creating input fields
- `FormComponent`: For creating forms with inputs
- `CardComponent`: For creating card-like UI elements
- `ListComponent`: For creating lists of items

## Creating Custom Components

You can create custom components by extending the base `Component` class:

```python
from corex import Component

class CounterComponent(Component):
    def __init__(self, count=0, id=None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.count = count
        
        # Create child components
        self.text = TextComponent(f"Count: {self.count}")
        self.button = ButtonComponent("Increment", action="increment", component_id=self.id)
        
        # Add child components
        self.add_children(self.text, self.button)
    
    def increment(self):
        """Return a new counter with incremented count."""
        return CounterComponent(self.count + 1, id=self.id)
```

## Examples

Check out the examples directory for more examples:

- [Todo App](examples/todo_app.py): A simple todo list application
- [Counter App](examples/counter_app.py): A basic counter with increment and decrement buttons
- [Form Validation](examples/form_validation.py): A registration form with client-side validation
- [Multi-page App](examples/multi_page_app.py): A multi-page application with navigation
- [Data-driven App](examples/data_driven_app.py): A product catalog with filtering and details view
- [Custom Components](examples/custom_components.py): Custom components with custom rendering (progress bars, ratings, accordions, tabs)

To run any of the examples, navigate to the project root directory and run:

```console
python examples/example_name.py
```

For instance:

```console
python examples/todo_app.py
```

This will start a local development server, and you can access the application at http://127.0.0.1:5000/.

Alternatively, you can use the examples runner script to select and run any example from a menu:

```console
python examples/run_examples.py
```

This will display a menu of all available examples, allowing you to select which one to run.

## Running Tests

Corex uses pytest for testing. To run the tests, you can use the following command:

```console
pytest tests/
```

Or if you're using hatch:

```console
hatch run test
```

To run tests with coverage:

```console
hatch run test-cov
```

## License

`corex` is distributed under the terms of the
[MIT](https://spdx.org/licenses/MIT.html) license.
