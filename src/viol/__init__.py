"""
Viol Main Package
================

Purpose
-------
The main Viol package serves as the entry point to the Viol library, providing
convenient access to the most commonly used components and functions from various
submodules. It simplifies imports by exposing key functionality directly from the
top-level package.

Core Functionality
-----------------
- Access to the core rendering function
- Basic layout components for structuring web applications
- Application initialization utilities for Flask integration

Dependencies
-----------
- viol.core: For the core rendering functionality
- viol.layout: For layout components and application initialization

Usage Examples
-------------
>>> from viol import render, BasicLayout, init_app
>>>
>>> # Initialize a Flask application
>>> from flask import Flask
>>> app = Flask(__name__)
>>> init_app(app)
>>>
>>> # Create a basic layout
>>> layout = BasicLayout(
...     body="Hello, World!",
...     title="My Viol App"
... )
>>>
>>> # Render the layout
>>> html = render(layout)

Edge Cases
---------
- The package only exposes the most commonly used components
- For more specialized functionality, import directly from the appropriate submodule
- Version tracking is maintained at the package level

Version History
--------------
1.0.0 - Initial stable release
"""

from viol.core import render
from viol.layout import BasicLayout, init_app

__version__ = "0.0.1"

__all__ = [
    "BasicLayout",
    "init_app",
    "render",
]
