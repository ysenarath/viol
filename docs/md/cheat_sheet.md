# Viol AI Cheat Sheet

A concise reference guide for AI systems working with the viol package.

## Table of Contents

- [Common HTML Elements](#common-html-elements)
- [Attribute Handling](#attribute-handling)
- [Event Handling](#event-handling)
- [Bootstrap Components](#bootstrap-components)
- [Layout Patterns](#layout-patterns)
- [Integration Snippets](#integration-snippets)
- [Common Workflows](#common-workflows)

## Common HTML Elements

### Basic Element Creation

| Method | Example | Output |
|--------|---------|--------|
| Element class | `Element("div", "Hello")` | `<div>Hello</div>` |
| html module | `html.div("Hello")` | `<div>Hello</div>` |
| VoidElement | `VoidElement("img", attrs={"src": "img.jpg"})` | `<img src="img.jpg" />` |
| html module (void) | `html.img(attrs={"src": "img.jpg"})` | `<img src="img.jpg" />` |

### Nesting Elements

```python
# Using Element class
container = Element("div", [
    Element("h1", "Title"),
    Element("p", "Paragraph")
], attrs={"class": "container"})

# Using html module
container = html.div([
    html.h1("Title"),
    html.p("Paragraph")
], attrs={"class": "container"})
```

### Common HTML Elements

```python
from viol.html import div, p, h1, a, img, ul, li, form, input, button, span, table, tr, td

# Text elements
heading = h1("Page Title")
paragraph = p("This is a paragraph")
link = a("Click here", attrs={"href": "https://example.com"})

# Lists
list_items = ul([
    li("Item 1"),
    li("Item 2"),
    li("Item 3")
])

# Forms
login_form = form([
    div(input(attrs={"type": "text", "name": "username", "placeholder": "Username"})),
    div(input(attrs={"type": "password", "name": "password", "placeholder": "Password"})),
    div(button("Login", attrs={"type": "submit"}))
], attrs={"method": "post", "action": "/login"})

# Images
image = img(attrs={"src": "image.jpg", "alt": "Description"})

# Tables
simple_table = table([
    tr([td("Cell 1"), td("Cell 2")]),
    tr([td("Cell 3"), td("Cell 4")])
], attrs={"class": "table"})
```

## Attribute Handling

### Setting Attributes

```python
# During element creation
element = html.div("Content", attrs={
    "id": "main",
    "class": ["container", "mt-3"],
    "data-toggle": "modal",
    "style": "color: blue;"
})

# After element creation
element.attrs["id"] = "new-id"
element.attrs["class"].append("text-center")
element.attrs["data-target"] = "#myModal"
```

### Attribute Access Methods

| Method | Example | Description |
|--------|---------|-------------|
| Dictionary access | `element.attrs["id"]` | Access attribute by key |
| Property access | `element.attrs.id` | Access common attributes as properties |
| Class list | `element.attrs.class_` | Access class list as a property |
| To string | `element.attrs.to_string()` | Convert attributes to HTML string |

### Special Attribute Handling

```python
# Class attribute (always a list)
element.attrs["class"] = ["btn", "btn-primary"]  # Set as list
element.attrs["class"] = "btn btn-primary"       # Set as space-separated string
element.attrs.class_.append("active")            # Append to class list
element.attrs.class_.remove("btn-primary")       # Remove from class list

# Boolean attributes
element.attrs["disabled"] = True                 # Renders as disabled="disabled"
element.attrs["required"] = "required"           # Explicit value

# Data attributes
element.attrs["data-id"] = "123"
element.attrs["data-toggle"] = "tooltip"
```

## Event Handling

### Creating Event Handlers

```python
from viol.core import EventHandler
from viol.html import button, div

# Create an event handler
click_event = EventHandler(
    method="get",                # HTTP method (get, post, put, patch, delete)
    rule="/api/data",            # URL or endpoint
    target="#result",            # Target element to update
    trigger="click",             # Event that triggers the request
    swap="innerHTML"             # How to swap the response
)

# Create a button with the event handler
btn = button("Load Data")
btn.events.append(click_event)

# Multiple events on one element
div_element = div("Content", id="content")
div_element.events.append(EventHandler(
    method="get",
    rule="/api/data",
    target="#result",
    trigger="click"
))
div_element.events.append(EventHandler(
    method="post",
    rule="/api/update",
    trigger="dblclick"
))
```

### Common Event Attributes

| Attribute | Description | Example |
|-----------|-------------|---------|
| method | HTTP method | `"get"`, `"post"`, `"put"`, `"patch"`, `"delete"` |
| rule | URL or endpoint | `"/api/data"`, `"/users/123"` |
| trigger | Event that triggers the request | `"click"`, `"submit"`, `"change"`, `"load"` |
| target | Target element to update | `"#result"`, `".container"`, `"closest div"` |
| swap | How to swap the response | `"innerHTML"`, `"outerHTML"`, `"beforeend"` |
| include | Additional elements to include | `"#form"`, `"closest form"` |
| confirm | Confirmation message | `"Are you sure?"` |
| vals | Additional values to include | `'{"id": 123}'` |

### Event Trigger Types

```python
# Common trigger types
click_event = EventHandler(method="get", rule="/api/data", trigger="click")
submit_event = EventHandler(method="post", rule="/api/submit", trigger="submit")
change_event = EventHandler(method="post", rule="/api/validate", trigger="change")
load_event = EventHandler(method="get", rule="/api/init", trigger="load")
timer_event = EventHandler(method="get", rule="/api/refresh", trigger="every 5s")

# Trigger modifiers
delayed_event = EventHandler(method="get", rule="/api/search", trigger="keyup changed delay:500ms")
throttled_event = EventHandler(method="get", rule="/api/update", trigger="scroll throttle:500ms")
once_event = EventHandler(method="get", rule="/api/load", trigger="revealed once")
```

## Bootstrap Components

### Buttons

```python
from viol.bootstrap.buttons import Button

# Basic button
primary_btn = Button("Click Me", color="primary")

# Button variants
secondary_btn = Button("Secondary", color="secondary")
success_btn = Button("Success", color="success")
danger_btn = Button("Danger", color="danger")

# Button sizes
small_btn = Button("Small", color="primary", size="sm")
large_btn = Button("Large", color="primary", size="lg")

# Outline buttons
outline_btn = Button("Outline", color="primary", outline=True)

# Disabled buttons
disabled_btn = Button("Disabled", color="primary", disabled=True)

# Button as link
link_btn = Button("Link", color="primary", href="/page")

# Button with type
submit_btn = Button("Submit", color="primary", type="submit")
```

### Cards

```python
from viol.bootstrap.card import Card

# Basic card
basic_card = Card(
    header="Card Title",
    body="This is the card content.",
    footer="Card Footer"
)

# Card with complex content
from viol.html import p, h5, ul, li

complex_card = Card(
    header=h5("Featured"),
    body=[
        p("Some quick example text to build on the card title."),
        ul([
            li("Item 1"),
            li("Item 2"),
            li("Item 3")
        ])
    ],
    footer=Button("Learn More", color="primary")
)
```

### Alerts

```python
from viol.bootstrap.alerts import Alert

# Basic alert
info_alert = Alert("This is an info alert.", color="info")

# Alert variants
success_alert = Alert("Success!", color="success")
warning_alert = Alert("Warning!", color="warning")
danger_alert = Alert("Danger!", color="danger")

# Alert with dismiss button
dismissible_alert = Alert("Dismissible alert.", color="primary", dismissible=True)
```

### Navbar

```python
from viol.bootstrap.navbar import Navbar

# Basic navbar
navbar = Navbar(
    brand="My App",
    items=[
        ("Home", "/"),
        ("About", "/about"),
        ("Contact", "/contact")
    ]
)

# Navbar with active item
navbar_with_active = Navbar(
    brand="My App",
    items=[
        ("Home", "/", True),  # Active item
        ("About", "/about"),
        ("Contact", "/contact")
    ],
    color="dark",
    expand="lg"
)
```

### Modal

```python
from viol.bootstrap.modal import Modal
from viol.html import p, form, input, label

# Basic modal
basic_modal = Modal(
    title="Modal Title",
    body="Modal content goes here.",
    footer=Button("Close", color="secondary")
)

# Modal with form
form_modal = Modal(
    title="Login",
    body=form([
        div([
            label("Username:", attrs={"for": "username"}),
            input(attrs={"type": "text", "id": "username", "class": "form-control"})
        ]),
        div([
            label("Password:", attrs={"for": "password"}),
            input(attrs={"type": "password", "id": "password", "class": "form-control"})
        ])
    ]),
    footer=[
        Button("Close", color="secondary"),
        Button("Login", color="primary", type="submit")
    ],
    id="loginModal",
    size="lg"
)
```

## Layout Patterns

### Container Layouts

```python
from viol.html import div, h1, p

# Basic container
container = div([
    h1("Page Title"),
    p("Content goes here.")
], attrs={"class": "container"})

# Container with padding
padded_container = div([
    h1("Page Title"),
    p("Content goes here.")
], attrs={"class": "container py-4"})

# Fluid container
fluid_container = div([
    h1("Page Title"),
    p("Content goes here.")
], attrs={"class": "container-fluid"})
```

### Grid Layouts

```python
from viol.html import div, h2, p

# Basic row with columns
grid = div([
    div([  # Row
        div(h2("Column 1"), attrs={"class": "col-md-6"}),
        div(h2("Column 2"), attrs={"class": "col-md-6"})
    ], attrs={"class": "row"})
], attrs={"class": "container"})

# Multiple rows
multi_row_grid = div([
    div([  # Row 1
        div(h2("Header"), attrs={"class": "col-12"})
    ], attrs={"class": "row"}),
    div([  # Row 2
        div(p("Sidebar"), attrs={"class": "col-md-3"}),
        div(p("Main content"), attrs={"class": "col-md-9"})
    ], attrs={"class": "row"}),
    div([  # Row 3
        div(p("Footer"), attrs={"class": "col-12"})
    ], attrs={"class": "row"})
], attrs={"class": "container"})

# Responsive columns
responsive_grid = div([
    div([
        div(p("Small: 12, Medium: 6, Large: 4"), 
            attrs={"class": "col-12 col-md-6 col-lg-4"}),
        div(p("Small: 12, Medium: 6, Large: 4"), 
            attrs={"class": "col-12 col-md-6 col-lg-4"}),
        div(p("Small: 12, Medium: 12, Large: 4"), 
            attrs={"class": "col-12 col-md-12 col-lg-4"})
    ], attrs={"class": "row"})
], attrs={"class": "container"})
```

### Card Layouts

```python
from viol.bootstrap.card import Card
from viol.html import div

# Card deck (equal height)
card_deck = div([
    div([
        Card(header="Card 1", body="Content 1"),
        Card(header="Card 2", body="Content 2"),
        Card(header="Card 3", body="Content 3")
    ], attrs={"class": "card-deck"})
], attrs={"class": "container"})

# Card grid
card_grid = div([
    div([  # Row
        div(Card(header="Card 1", body="Content 1"), 
            attrs={"class": "col-md-4 mb-4"}),
        div(Card(header="Card 2", body="Content 2"), 
            attrs={"class": "col-md-4 mb-4"}),
        div(Card(header="Card 3", body="Content 3"), 
            attrs={"class": "col-md-4 mb-4"})
    ], attrs={"class": "row"})
], attrs={"class": "container"})
```

## Integration Snippets

### Flask Application Setup

```python
from flask import Flask, request, redirect, url_for
import viol
from viol import BasicLayout, html, render

# Initialize Flask app
app = Flask(__name__)
viol.init_app(app)

# Custom static folder and URL path (optional)
viol.init_app(app, static_folder="custom_static", static_url_path="/assets")
```

### Route Handling

```python
@app.route("/")
def home():
    # Create content
    content = html.div([
        html.h1("Welcome"),
        html.p("This is a page created with Viol.")
    ], attrs={"class": "container"})
    
    # Create layout
    layout = BasicLayout(
        body=content,
        title="My Page",
        extra_head_content=f'<link rel="stylesheet" href="{url_for("static", filename="css/custom.css")}">'
    )
    
    # Render to HTML
    return layout.render()
```

### Form Processing

```python
@app.route("/submit", methods=["POST"])
def submit():
    # Get form data
    name = request.form.get("name", "")
    email = request.form.get("email", "")
    
    # Process data
    # ...
    
    # Redirect to another page
    return redirect(url_for("success"))

# Form with HTMX
@app.route("/search")
def search_form():
    form = html.form([
        html.input(attrs={"type": "text", "name": "query", "placeholder": "Search..."}),
        html.button("Search", attrs={"type": "submit"})
    ])
    
    # Add HTMX event handler
    event = EventHandler(
        method="post",
        rule="/search-results",
        target="#results",
        trigger="submit"
    )
    form.events.append(event)
    
    content = html.div([
        form,
        html.div(attrs={"id": "results"})
    ])
    
    return render(BasicLayout(body=content))

@app.route("/search-results", methods=["POST"])
def search_results():
    query = request.form.get("query", "")
    # Process search
    results = f"Results for: {query}"
    return results  # Return HTML fragment for HTMX
```

### Serving Static Assets

```python
# In your HTML or components
css_url = url_for('viol.static', filename='css/bootstrap.min.css')
js_url = url_for('viol.static', filename='js/bootstrap.min.js')
htmx_url = url_for('viol.static', filename='js/htmx.min.js')

# Custom CSS in layout
layout = BasicLayout(
    body=content,
    title="My Page",
    extra_head_content=f'<link rel="stylesheet" href="{url_for("static", filename="css/custom.css")}">'
)
```

## Common Workflows

### Form Handling

```python
from viol.html import div, form, input, label, button
from viol.core import EventHandler
from flask import url_for

def create_contact_form():
    """Create a contact form with validation."""
    contact_form = form([
        div([
            label("Name:", attrs={"for": "name", "class": "form-label"}),
            input(attrs={
                "type": "text",
                "id": "name",
                "name": "name",
                "class": "form-control",
                "required": "true"
            })
        ], attrs={"class": "mb-3"}),
        div([
            label("Email:", attrs={"for": "email", "class": "form-label"}),
            input(attrs={
                "type": "email",
                "id": "email",
                "name": "email",
                "class": "form-control",
                "required": "true"
            })
        ], attrs={"class": "mb-3"}),
        div([
            label("Message:", attrs={"for": "message", "class": "form-label"}),
            textarea(attrs={
                "id": "message",
                "name": "message",
                "class": "form-control",
                "rows": "5",
                "required": "true"
            })
        ], attrs={"class": "mb-3"}),
        div([
            button("Submit", attrs={
                "type": "submit",
                "class": "btn btn-primary"
            })
        ])
    ], attrs={"id": "contact-form"})
    
    # Add HTMX validation
    email_input = contact_form.children[1].children[1]
    validate_event = EventHandler(
        method="post",
        rule="/validate-email",
        trigger="change",
        target="next .invalid-feedback"
    )
    email_input.events.append(validate_event)
    
    # Add form submission handler
    submit_event = EventHandler(
        method="post",
        rule="/submit-contact",
        trigger="submit",
        target="#form-result"
    )
    contact_form.events.append(submit_event)
    
    return contact_form
```

### Data Display

```python
from viol.html import div, table, thead, tbody, tr, th, td
from viol.bootstrap.badge import Badge

def create_user_table(users):
    """Create a table to display user data."""
    return div([
        table([
            thead([
                tr([
                    th("ID"),
                    th("Name"),
                    th("Email"),
                    th("Status"),
                    th("Actions")
                ])
            ]),
            tbody([
                tr([
                    td(user["id"]),
                    td(user["name"]),
                    td(user["email"]),
                    td(Badge(user["status"], 
                        color="success" if user["status"] == "Active" else "secondary")),
                    td(div([
                        Button("Edit", color="primary", size="sm", 
                              attrs={"data-id": user["id"]}),
                        Button("Delete", color="danger", size="sm", 
                              attrs={"data-id": user["id"]})
                    ], attrs={"class": "btn-group"}))
                ]) for user in users
            ])
        ], attrs={"class": "table table-striped"})
    ], attrs={"class": "table-responsive"})
```

### Navigation

```python
from viol.bootstrap.navbar import Navbar
from viol.bootstrap.breadcrumb import Breadcrumb

def create_navigation(active_page):
    """Create a navigation system with navbar and breadcrumbs."""
    # Create navbar
    navbar = Navbar(
        brand="My App",
        items=[
            ("Home", "/", active_page == "home"),
            ("Products", "/products", active_page == "products"),
            ("About", "/about", active_page == "about"),
            ("Contact", "/contact", active_page == "contact")
        ],
        color="dark",
        expand="lg"
    )
    
    # Create breadcrumbs based on active page
    breadcrumb_items = [("Home", "/")]
    
    if active_page == "products":
        breadcrumb_items.append(("Products", None))
    elif active_page == "about":
        breadcrumb_items.append(("About", None))
    elif active_page == "contact":
        breadcrumb_items.append(("Contact", None))
    
    breadcrumbs = Breadcrumb(breadcrumb_items)
    
    return div([
        navbar,
        div(breadcrumbs, attrs={"class": "container mt-3"})
    ])
```

### HTMX Interactions

```python
from viol.html import div, button, input, ul, li
from viol.core import EventHandler

def create_live_search():
    """Create a live search component with HTMX."""
    search_input = input(attrs={
        "type": "text",
        "name": "query",
        "placeholder": "Search...",
        "class": "form-control"
    })
    
    # Add search event
    search_event = EventHandler(
        method="get",
        rule="/api/search",
        trigger="keyup changed delay:500ms",
        target="#search-results"
    )
    search_input.events.append(search_event)
    
    return div([
        div(search_input, attrs={"class": "mb-3"}),
        div(attrs={"id": "search-results", "class": "list-group"})
    ])

def create_infinite_scroll():
    """Create an infinite scroll component with HTMX."""
    content_div = div([
        div([
            # Initial content
            div("Item 1", attrs={"class": "card mb-2 p-3"}),
            div("Item 2", attrs={"class": "card mb-2 p-3"}),
            div("Item 3", attrs={"class": "card mb-2 p-3"})
        ], attrs={"id": "content"}),
        div("Loading more...", attrs={"id": "loading", "class": "text-center p-3"})
    ])
    
    # Add infinite scroll event
    loading_div = content_div.children[1]
    load_event = EventHandler(
        method="get",
        rule="/api/more-items?page=2",
        trigger="intersect once",
        target="#content",
        swap="beforeend"
    )
    loading_div.events.append(load_event)
    
    return content_div