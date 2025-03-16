Layout Example
==============

This example demonstrates how to create basic HTML layouts using viol's HTML components.

Basic HTML Structure
-----------------

The example shows how to create a minimal HTML document structure:

.. code-block:: python

    from viol.html.doctype import DOCTYPE
    from viol.html.head import Head
    from viol.html.html import Html

    layout = [
        DOCTYPE,
        Html(
            [
                Head(),
                "Hello, world!",
            ]
        ),
    ]

    print(layout.render())

Components Used
-------------

1. **DOCTYPE**
    * Represents the HTML5 DOCTYPE declaration
    * Added at the beginning of the document

2. **Html**
    * The root element of an HTML document
    * Contains all other elements

3. **Head**
    * Contains metadata about the document
    * Can be extended with title, meta tags, and stylesheets

Output
------

The above code generates the following HTML:

.. code-block:: html

    <!DOCTYPE html>
    <html>
        <head></head>
        Hello, world!
    </html>

Key Concepts
----------

1. **Component Composition**
    * Components can be nested within each other
    * Lists can be used to group multiple components

2. **Rendering**
    * The `render()` method converts the components to HTML
    * Components automatically handle proper HTML formatting and indentation

3. **Flexibility**
    * Components can contain both other components and plain text
    * Easy to extend with additional HTML elements and attributes