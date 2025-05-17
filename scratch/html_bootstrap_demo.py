"""Demonstration of the new html_v2 module with type-safe elements."""

from accordion import sample_accordion
from flask import Flask
from navbar import simple_navbar

import viol
from viol import BasicLayout, html, render
from viol.bootstrap.badge import Badge
from viol.bootstrap.breadcrumb import Breadcrumb

app = Flask(__name__)

viol.init_app(app)


@app.route("/")
def home():
    # Create a container with proper typing
    body = [
        simple_navbar(),
        html.div(
            Breadcrumb(
                [("Home", "/"), ("Library", "/library"), "Data"],
            ),
            attrs={"class": "container py-3"},
        ),
        html.div(
            sample_accordion(),
            attrs={"class": "container"},
        ),
        html.h1(
            [
                "Hello, World!",
                Badge("New"),
            ],
            attrs={"class": "text-center"},
        ),
    ]

    return render(BasicLayout(body=body))


if __name__ == "__main__":
    app.run(port=8000, debug=True)
