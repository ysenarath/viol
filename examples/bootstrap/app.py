"""Demonstration of the new html_v2 module with type-safe elements."""

from flask import Flask

import viol
from viol import BasicLayout, html, render

from .components.navbar import simple_navbar

app = Flask(__name__)

viol.init_app(app)


@app.route("/")
def home():
    # Create a container with proper typing
    body = [
        simple_navbar(
            items=[
                {"name": "About", "href": "/about"},
                {"name": "Contact", "href": "/contact"},
            ]
        ),
        html.div(
            children=[
                html.h1("Welcome to the Bootstrap App"),
                html.p("This is a simple example of using Bootstrap with Flask."),
            ],
            attrs={"class": ["container"]},
            id="main-content",
        ),
    ]
    return render(BasicLayout(body=body))


@app.route("/about")
def about_page():
    return "About Page"


@app.route("/contact")
def contact_page():
    return "Contact Page"


@app.route("/home")
def home_page():
    return "Home Page"
