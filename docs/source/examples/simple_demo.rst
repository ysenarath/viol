Simple Demo
===========

This example demonstrates the basic features of viol, including:

* Creating interactive buttons with HTMX
* Handling events (click, mouseover)
* Using Bootstrap components
* Dynamic content updates
* Hyperscript integration

Application Setup
---------------

First, we create a Flask-based Server instance:

.. code-block:: python

    from viol import Server, render
    app = Server(__name__)

Interactive Components
-------------------

Click Button
^^^^^^^^^^^

A button that updates content when clicked:

.. code-block:: python

    click_btn = Button(
        "Hello, {{ world }}!",
        attrs={"class": "btn btn-primary"},
        events=[
            {
                "rule": "/click",
                "method": "post",
                "trigger": "click",
                "target": "#output",
                "swap": "innerHTML",
            },
        ],
        id="my-button-{{ctx.component.uuid}}",
        _="on click toggle .btn-primary .btn-secondary on me",
    )

The button:
* Uses Bootstrap classes for styling
* Sends a POST request to /click when clicked
* Updates the element with id="output"
* Uses Hyperscript to toggle button classes

Mouseover Button
^^^^^^^^^^^^^

A button that responds to hover events:

.. code-block:: python

    mouseover_btn = Button(
        "Hello, {{ world }}!",
        attrs={"class": "btn btn-primary"},
        events=[
            {
                "rule": "/mouseover",
                "method": "post",
                "trigger": "mouseover",
                "target": "#output",
                "swap": "innerHTML",
            },
        ],
        id="my-button-{{ctx.component.uuid}}",
    )

Route Handlers
------------

The application defines several routes to handle different interactions:

.. code-block:: python

    @app.route("/click", methods=["POST", "GET"])
    def clicked():
        text = "You clicked the button!"
        return f"<h1>{text}</h1>"

    @app.route("/mouseover", methods=["POST", "GET"])
    def mouseover():
        text = "You hovered over the button!"
        return f"<h1>{text}</h1>"

Main Page Layout
-------------

The main page combines various components:

.. code-block:: python

    @app.route("/")
    def home():
        # ... button definitions ...
        body = [
            simple_navbar(),
            click_btn,
            mouseover_btn,
            "<div id='output'></div>",
            h1,
            accordion_btn,
            "<div id='accordion'>",
            Alert("Hello World!", variant="danger"),
        ]
        return render_template(
            "index.html",
            title="Hello World!",
            body=render(body),
        )

Running the Application
--------------------

To run the demo:

.. code-block:: python

    if __name__ == "__main__":
        app.run(port=8000, debug=True)

This will start the server on port 8000 in debug mode.

Key Features Demonstrated
----------------------

1. **Component-Based Development**: Using viol's components like Button, Alert
2. **Event Handling**: Both click and mouseover events
3. **HTMX Integration**: Dynamic content updates without full page reloads
4. **Bootstrap Integration**: Using Bootstrap classes and components
5. **Hyperscript**: Adding client-side interactivity
6. **Template Integration**: Using Flask's template engine with viol components