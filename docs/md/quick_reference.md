# Viol AI Quick Reference Guide

This guide is designed to help AI systems quickly understand the viol package and use it effectively in production-grade web app development.

## 1. Package Overview

Viol is a Python library for building web applications using a component-based approach. It provides a Pythonic way to create HTML elements and components, with built-in support for Bootstrap UI components and HTMX for interactivity.

### Core Philosophy

Viol's core philosophy is to enable developers to build web applications using Python's object-oriented paradigm rather than template languages. It treats UI components as first-class objects that can be composed, extended, and reused.

Key principles:
- **Component-based architecture**: Everything is a component that can be composed
- **Pythonic API**: Intuitive and type-safe interfaces for creating HTML elements
- **Seamless integration**: Works with Flask and other web frameworks
- **Progressive enhancement**: Built-in support for HTMX and Hyperscript for client-side interactivity

### Key Features

- Type-safe HTML element builders
- Bootstrap component library
- HTMX integration for interactive applications
- Flask integration for serving applications
- Attribute management with special handling for HTML attributes
- Event handling system

## 2. Architecture Overview

Viol is organized into several key modules, each with a specific responsibility:

```
viol/
├── core/           # Core component system and rendering
├── html/           # HTML element builders
├── bootstrap/      # Bootstrap UI components
├── utils/          # Utility functions and classes
├── static/         # Static assets (CSS, JS)
├── templates/      # HTML templates
└── layout.py       # Layout components and Flask integration
```

### Module Relationships Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    html     │     │  bootstrap  │     │   layout    │
│  elements   │────>│  components │────>│ application │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────────────────────────────────────────────┐
│                       core                           │
│  (Component, Element, Attributes, Events, Rendering) │
└─────────────────────────────────────────────────────┘
                           │
                           │
                           ▼
                    ┌─────────────┐
                    │    utils    │
                    └─────────────┘
```

### Component Hierarchy

```
Component (base class)
├── Element
│   └── VoidElement
├── EventHandler
└── Custom Components (e.g., Button, Card, etc.)
```

### Data Flow Diagram

```
┌───────────┐     ┌───────────┐     ┌───────────┐     ┌───────────┐
│  Python   │     │   Viol    │     │   HTML    │     │  Browser  │
│  Objects  │────>│ Components│────>│ Rendering │────>│  Display  │
└───────────┘     └───────────┘     └───────────┘     └───────────┘
                       │  ▲                                │
                       │  │                                │
                       ▼  │                                │
                  ┌───────────┐                           │
                  │   HTMX    │                           │
                  │  Events   │<──────────────────────────┘
                  └───────────┘
```

## 3. Key Components

### Core Module

The core module provides the fundamental building blocks for the Viol library.

#### Component

The base class for all Viol components. It provides the basic structure and rendering capabilities.

```python
from viol.core import Component

class MyComponent(Component):
    def __init__(self, content):
        self.content = content
        
    def render(self) -> str:
        return f"<div>{self.content}</div>"
```

#### Element

Represents a standard HTML element with a closing tag.

```python
from viol.core import Element

# Create a div with text content
div = Element("div", "Hello, World!", attrs={"class": "container"})

# Create a div with nested elements
div = Element("div", [
    Element("h1", "Title"),
    Element("p", "Paragraph")
], attrs={"class": "container"})
```

#### VoidElement

Represents an HTML element without a closing tag (e.g., `<img>`, `<br>`).

```python
from viol.core import VoidElement

# Create an image element
img = VoidElement("img", attrs={"src": "image.jpg", "alt": "An image"})
```

#### AttrMultiDict

Manages HTML attributes with special handling for class attributes and case-insensitivity.

```python
from viol.core import AttrMultiDict

# Create attributes
attrs = AttrMultiDict()
attrs["class"] = ["container", "mt-3"]
attrs["data-toggle"] = "modal"

# Access attributes
print(attrs["class"])  # ['container', 'mt-3']
print(attrs.to_string())  # 'class="container mt-3" data-toggle="modal"'
```

#### EventHandler

Handles HTMX events for interactive components.

```python
from viol.core import EventHandler, Element

# Create a button that loads content on click
button = Element("button", "Load Data")
event = EventHandler(
    method="get",
    rule="/api/data",
    target="#result",
    trigger="click"
)
button.events.append(event)
```

#### render

The core rendering function that converts components to HTML.

```python
from viol.core import render, Element

div = Element("div", "Hello, World!")
html = render(div)  # "<div>Hello, World!</div>"
```

### HTML Module

The HTML module provides builders for all standard HTML elements.

```python
from viol.html import div, p, a, span, ul, li

# Create a simple div with a paragraph
content = div([
    p("This is a paragraph with a ", [
        a("link", attrs={"href": "https://example.com"}),
        " and some ",
        span("styled text", attrs={"class": "highlight"})
    ])
])

# Create a list
list_content = ul([
    li("Item 1"),
    li("Item 2"),
    li("Item 3")
], attrs={"class": "list-group"})
```

### Bootstrap Module

The Bootstrap module provides components for the Bootstrap UI framework.

```python
from viol.bootstrap import Button, Card, Alert, Modal
from viol.html import div, p

# Create a button
button = Button("Click Me", color="primary", size="lg")

# Create a card
card = Card(
    header="Card Title",
    body=p("This is the card content."),
    footer="Card Footer"
)

# Create an alert
alert = Alert("This is an alert message", color="warning")

# Create a modal
modal = Modal(
    title="Modal Title",
    body=p("This is the modal content."),
    footer=Button("Close", color="secondary")
)
```

### Layout Module

The layout module provides components and utilities for structuring web applications.

```python
from flask import Flask
from viol import BasicLayout, init_app
from viol.html import div, h1, p

# Initialize Flask app
app = Flask(__name__)
init_app(app)

# Create a basic layout
content = div([
    h1("Welcome to Viol"),
    p("This is a simple page created with Viol.")
])
layout = BasicLayout(
    body=content,
    title="My Viol App"
)

# Render the layout
html = layout.render()
```

## 4. Common Usage Patterns

### Creating Basic HTML Elements

```python
from viol.html import div, p, h1, a, img
from viol.core import render

# Simple text content
paragraph = p("This is a paragraph.")

# Elements with attributes
link = a("Click here", attrs={"href": "https://example.com", "target": "_blank"})

# Void elements
image = img(attrs={"src": "image.jpg", "alt": "An image"})

# Nested elements
content = div([
    h1("Title"),
    p("Paragraph with a ", [
        a("link", attrs={"href": "#"})
    ])
], attrs={"class": "container"})

# Render to HTML
html = render(content)
```

### Building Component Hierarchies

```python
from viol.html import div, header, main, footer, nav, ul, li, a
from viol.core import render

# Create a page structure
page = div([
    header([
        nav([
            ul([
                li(a("Home", attrs={"href": "/"})),
                li(a("About", attrs={"href": "/about"})),
                li(a("Contact", attrs={"href": "/contact"}))
            ], attrs={"class": "nav"})
        ])
    ], attrs={"class": "header"}),
    main([
        # Main content here
    ], attrs={"class": "main"}),
    footer([
        # Footer content here
    ], attrs={"class": "footer"})
], attrs={"class": "page"})

# Render to HTML
html = render(page)
```

### Working with Attributes and Classes

```python
from viol.html import div
from viol.core import render

# Adding classes
content = div("Content", attrs={"class": ["container", "mt-3", "p-2"]})

# Data attributes
modal_trigger = div("Click me", attrs={
    "data-toggle": "modal",
    "data-target": "#myModal"
})

# Inline styles
styled_div = div("Styled content", attrs={
    "style": "color: red; font-size: 16px;"
})

# Combining attributes
combined = div("Content", attrs={
    "class": ["container", "text-center"],
    "id": "content",
    "data-role": "container"
})
```

### Handling Events and Interactivity

```python
from viol.html import div, button
from viol.core import EventHandler, render

# Create a button that loads content on click
load_button = button("Load Data")
load_event = EventHandler(
    method="get",
    rule="/api/data",
    target="#result",
    trigger="click"
)
load_button.events.append(load_event)

# Create a div that updates periodically
auto_update = div("Loading...", attrs={"id": "updates"})
update_event = EventHandler(
    method="get",
    rule="/api/updates",
    trigger="every 5s"
)
auto_update.events.append(update_event)

# Create a form input that validates on change
input_field = div([
    input(attrs={"type": "text", "name": "username", "id": "username"})
])
validate_event = EventHandler(
    method="post",
    rule="/api/validate",
    trigger="change",
    target="#validation-message"
)
input_field.events.append(validate_event)
```

### Using Bootstrap Components

```python
from viol.bootstrap import Button, Card, Alert, Navbar, Modal
from viol.html import div, p
from viol.core import render

# Create a navbar
navbar = Navbar(
    brand="My App",
    items=[
        ("Home", "/"),
        ("About", "/about"),
        ("Contact", "/contact")
    ]
)

# Create a card with a button
card = Card(
    header="Feature",
    body=[
        p("This is a feature description."),
        Button("Learn More", color="primary")
    ],
    footer="Last updated: Today"
)

# Create a modal with a form
modal = Modal(
    title="Login",
    body=[
        # Form elements here
    ],
    footer=[
        Button("Close", color="secondary"),
        Button("Login", color="primary")
    ]
)

# Create an alert
alert = Alert("Operation completed successfully!", color="success")

# Render to HTML
html = render(div([navbar, card, alert]))
```

### Creating Layouts

```python
from flask import Flask
from viol import BasicLayout, init_app
from viol.html import div, h1, p
from viol.bootstrap import Navbar, Card

# Initialize Flask app
app = Flask(__name__)
init_app(app)

# Create a navbar
navbar = Navbar(
    brand="My App",
    items=[
        ("Home", "/"),
        ("About", "/about"),
        ("Contact", "/contact")
    ]
)

# Create main content
content = div([
    h1("Welcome to My App"),
    p("This is a simple application built with Viol."),
    Card(
        header="Feature",
        body=p("Feature description goes here.")
    )
], attrs={"class": "container mt-3"})

# Create a layout
layout = BasicLayout(
    body=[navbar, content],
    title="My Viol App"
)

# Render the layout
html = layout.render()
```

### Flask Integration

```python
from flask import Flask
from viol import init_app, BasicLayout
from viol.html import div, h1, p
from viol.bootstrap import Navbar, Card, Button

# Initialize Flask app
app = Flask(__name__)
init_app(app)

# Create components
navbar = Navbar(
    brand="My App",
    items=[
        ("Home", "/"),
        ("About", "/about"),
        ("Contact", "/contact")
    ]
)

# Define routes
@app.route("/")
def home():
    content = div([
        h1("Welcome to My App"),
        p("This is the home page."),
        Card(
            header="Feature",
            body=p("Feature description goes here."),
            footer=Button("Learn More", color="primary")
        )
    ], attrs={"class": "container mt-3"})
    
    layout = BasicLayout(
        body=[navbar, content],
        title="Home - My Viol App"
    )
    
    return layout.render()

@app.route("/about")
def about():
    content = div([
        h1("About"),
        p("This is the about page.")
    ], attrs={"class": "container mt-3"})
    
    layout = BasicLayout(
        body=[navbar, content],
        title="About - My Viol App"
    )
    
    return layout.render()

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
```

## 5. Integration Guide

### Flask Application Setup

```python
from flask import Flask
from viol import init_app

# Create Flask app
app = Flask(__name__)

# Initialize Viol with the app
init_app(app)

# Optional: Customize static folder and URL path
init_app(app, static_folder="custom_static", static_url_path="/assets")
```

### Serving Static Assets

Viol automatically registers a Flask Blueprint that provides access to its static assets (CSS, JavaScript) and templates. The default static URL path is `/viol/static`.

```python
# In your HTML or components
css_url = url_for('viol.static', filename='css/bootstrap.min.css')
js_url = url_for('viol.static', filename='js/bootstrap.min.js')
htmx_url = url_for('viol.static', filename='js/htmx.min.js')
```

### Template Rendering

Viol uses Jinja2 for template rendering. The `BasicLayout` component provides a standard HTML page structure with customizable title, body content, and optional extra content for the head and body sections.

```python
from viol import BasicLayout
from viol.html import div, h1, p

# Create content
content = div([
    h1("Welcome"),
    p("This is a page created with Viol.")
])

# Create layout
layout = BasicLayout(
    body=content,
    title="My Page",
    extra_head_content='<meta name="description" content="A Viol example">',
    extra_body_content='<script>console.log("Page loaded");</script>'
)

# Render to HTML
html = layout.render()
```

### Route Handling

```python
from flask import Flask, request, jsonify
from viol import init_app, BasicLayout
from viol.html import div, form, input, button
from viol.core import EventHandler

app = Flask(__name__)
init_app(app)

@app.route("/")
def home():
    # Create a form with HTMX
    form_element = form([
        input(attrs={"type": "text", "name": "query", "placeholder": "Search..."}),
        button("Search", attrs={"type": "submit"})
    ])
    
    # Add HTMX event handler
    event = EventHandler(
        method="post",
        rule="/search",
        target="#results",
        trigger="submit"
    )
    form_element.events.append(event)
    
    # Create layout
    content = div([
        form_element,
        div(attrs={"id": "results"})
    ], attrs={"class": "container mt-3"})
    
    layout = BasicLayout(
        body=content,
        title="Search"
    )
    
    return layout.render()

@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query", "")
    # Process search query
    results = f"Results for: {query}"
    return results
```

## 6. Best Practices

### Component Organization

1. **Create reusable components**: Define custom components for UI elements that are used multiple times.

```python
from viol.core import Component, render
from viol.html import div, h2, p

class FeatureCard(Component):
    def __init__(self, title, description):
        self.title = title
        self.description = description
    
    def render(self):
        return render(div([
            h2(self.title),
            p(self.description)
        ], attrs={"class": "feature-card"}))

# Usage
feature1 = FeatureCard("Feature 1", "Description of feature 1")
feature2 = FeatureCard("Feature 2", "Description of feature 2")
```

2. **Organize components by feature**: Group related components together.

3. **Use composition over inheritance**: Compose components from smaller components rather than creating deep inheritance hierarchies.

### Code Structure

1. **Separate concerns**: Keep presentation logic separate from business logic.

2. **Use type hints**: Leverage Python's type system for better code quality and IDE support.

```python
from typing import List, Optional
from viol.core import Component, render
from viol.html import div, ul, li

class MenuComponent(Component):
    def __init__(self, items: List[str], active_index: Optional[int] = None):
        self.items = items
        self.active_index = active_index
    
    def render(self) -> str:
        menu_items = []
        for i, item in enumerate(self.items):
            is_active = i == self.active_index
            menu_items.append(li(
                item,
                attrs={"class": "active" if is_active else ""}
            ))
        
        return render(div(
            ul(menu_items, attrs={"class": "menu"}),
            attrs={"class": "menu-container"}
        ))
```

3. **Follow consistent naming conventions**: Use descriptive names for components and variables.

### Performance Considerations

1. **Minimize component nesting**: Excessive nesting can lead to performance issues.

2. **Use lazy loading**: Load components only when needed.

```python
from flask import Flask
from viol import init_app, BasicLayout
from viol.html import div
from viol.core import EventHandler

app = Flask(__name__)
init_app(app)

@app.route("/")
def home():
    content_container = div(attrs={"id": "content"})
    
    # Add lazy loading event
    event = EventHandler(
        method="get",
        rule="/content",
        trigger="load"
    )
    content_container.events.append(event)
    
    layout = BasicLayout(
        body=content_container,
        title="Lazy Loading Example"
    )
    
    return layout.render()

@app.route("/content")
def content():
    # This content is loaded only when needed
    return "Lazy loaded content"
```

3. **Cache rendered components**: Cache the HTML output of expensive components.

### Error Handling

1. **Validate input data**: Ensure that component inputs are valid.

```python
from viol.core import Component, render
from viol.html import div, p

class UserProfile(Component):
    def __init__(self, user_data):
        if not isinstance(user_data, dict):
            raise TypeError("user_data must be a dictionary")
        
        required_fields = ["name", "email"]
        for field in required_fields:
            if field not in user_data:
                raise ValueError(f"user_data missing required field: {field}")
        
        self.user_data = user_data
    
    def render(self):
        return render(div([
            p(f"Name: {self.user_data['name']}"),
            p(f"Email: {self.user_data['email']}")
        ], attrs={"class": "user-profile"}))
```

2. **Handle missing data gracefully**: Provide fallbacks for missing or invalid data.

3. **Use try-except blocks**: Catch and handle exceptions appropriately.

```python
from viol.core import render
from viol.html import div, p

def render_user_profile(user_data):
    try:
        name = user_data.get("name", "Unknown")
        email = user_data.get("email", "No email provided")
        
        return render(div([
            p(f"Name: {name}"),
            p(f"Email: {email}")
        ], attrs={"class": "user-profile"}))
    except Exception as e:
        return render(div(
            p(f"Error rendering user profile: {str(e)}"),
            attrs={"class": "error"}
        ))
```

### Testing Strategies

1. **Unit test components**: Test individual components in isolation.

```python
import unittest
from viol.html import div, p
from viol.core import render

class TestComponents(unittest.TestCase):
    def test_div_rendering(self):
        # Test simple div
        simple_div = div("Hello")
        self.assertEqual(render(simple_div), "<div>Hello</div>")
        
        # Test div with attributes
        div_with_attrs = div("Hello", attrs={"class": "greeting"})
        self.assertEqual(render(div_with_attrs), '<div class="greeting">Hello</div>')
        
        # Test nested div
        nested_div = div([p("Hello")])
        self.assertEqual(render(nested_div), "<div><p>Hello</p></div>")
```

2. **Integration test pages**: Test complete pages or views.

3. **Use snapshot testing**: Compare rendered HTML with expected output.

## 7. Troubleshooting

### Common Issues and Solutions

#### Issue: Components not rendering correctly

**Solution**: Check that you're using the `render` function correctly.

```python
from viol.core import render
from viol.html import div

# Incorrect
html = div("Content").render()  # This only works for Component subclasses

# Correct
html = render(div("Content"))
```

#### Issue: Attributes not appearing in rendered HTML

**Solution**: Ensure attributes are passed correctly.

```python
from viol.html import div

# Incorrect
div("Content", class_="container")  # class_ is not a parameter

# Correct
div("Content", attrs={"class": "container"})
```

#### Issue: Events not triggering

**Solution**: Check that events are properly attached to elements.

```python
from viol.html import button
from viol.core import EventHandler

# Create button
btn = button("Click me")

# Create event handler
event = EventHandler(
    method="get",
    rule="/api/data",
    target="#result",
    trigger="click"
)

# Attach event to button
btn.events.append(event)
```

#### Issue: Flask integration not working

**Solution**: Ensure Viol is properly initialized with the Flask app.

```python
from flask import Flask
from viol import init_app

app = Flask(__name__)
init_app(app)  # This must be called before using Viol with Flask
```

### Debugging Techniques

1. **Inspect rendered HTML**: Print the rendered HTML to see what's being generated.

```python
from viol.core import render
from viol.html import div

component = div("Content", attrs={"class": "container"})
html = render(component)
print(html)  # <div class="container">Content</div>
```

2. **Check component structure**: Print the component structure to debug issues.

```python
from viol.html import div, p

component = div([
    p("Paragraph 1"),
    p("Paragraph 2")
], attrs={"class": "container"})

print(component.tag)  # div
print(component.attrs)  # AttrMultiDict({'class': ['container']})
print(len(component.children))  # 2
```

3. **Use Flask's debug mode**: Enable Flask's debug mode to see detailed error messages.

```python
app.run(debug=True)
```

### Error Messages Explained

#### AttributeError: 'NoneType' object has no attribute 'append'

This often occurs when trying to append to a non-existent list, such as when accessing `events` on an element that doesn't have an events list.

**Solution**: Ensure the element has an events list before appending.

```python
from viol.html import div
from viol.core import EventHandler

div_element = div("Content")
event = EventHandler(method="get", rule="/api/data")

# Check if events exists
if hasattr(div_element, "events"):
    div_element.events.append(event)
else:
    print("Element does not have events attribute")
```

#### TypeError: Object of type X is not JSON serializable

This can occur when trying to use complex objects in attributes that need to be serialized.

**Solution**: Convert complex objects to strings or basic types before using them in attributes.

```python
import json
from viol.html import div

data = {"name": "John", "age": 30}

# Incorrect
div("Content", attrs={"data-user": data})  # data is not serializable

# Correct
div("Content", attrs={"data-user": json.dumps(data)})
```

#### ValueError: Invalid attribute name

This occurs when using invalid characters in attribute names.

**Solution**: Use valid attribute names according to HTML standards.

```python
from viol.html import div

# Incorrect
div("Content", attrs={"data:user": "John"})  # : is not valid in attribute names

# Correct
div("Content", attrs={"data-user": "John"})