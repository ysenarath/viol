"""Demonstration of the new html_v2 module with type-safe elements."""

from flask import Flask, url_for

import viol
from viol import BasicLayout, html, render

app = Flask(__name__)

viol.init_app(app)


@app.route("/")
def home():
    # Create a container with proper typing
    body = html.div(
        [
            html.h1(attrs={"class": "title"}, children=["Type-Safe HTML Demo"]),
            html.p(
                attrs={"class": "description"},
                children=["This demonstrates the new type-safe HTML elements."],
            ),
            html.form(
                [
                    # Input with type checking
                    html.input(
                        attrs={
                            "type": "email",  # IDE will show valid input types
                            "name": "email",
                            "placeholder": "Enter your email",
                            "required": "true",
                            "class": "form-control",
                        }
                    ),
                    # Button with type checking
                    html.button(
                        "Submit",
                        attrs={
                            "type": "submit",
                            "class": "btn btn-primary",
                        },
                    ),
                ],
                attrs={
                    "class": "form-container",
                },
                id="form-demo",
                events=[
                    {
                        "method": "post",
                        "rule": url_for("submit"),
                        "trigger": "submit",
                        "target": "#result",
                        "swap": "innerHTML",
                        "confirm": "Are you sure?",
                    }
                ],
            ),
            html.button(
                "Click me",
                attrs={
                    "class": "btn btn-primary",
                },
                events=[
                    {
                        "method": "get",
                        "rule": "/submit2",
                        "confirm": "Are you sure 2?",
                        "target": "#result",
                        "swap": "innerHTML",
                    }
                ],
            ),
            html.div(["Results will appear here"], id="result"),
        ],
        attrs={"class": "container"},
        id="main-container",
    )

    return render(BasicLayout(body=body))


@app.route("/submit", methods=["POST"])
def submit():
    return "<p>Form submitted successfully!</p>"


@app.route("/submit2", methods=["GET"])
def submit2():
    return "<p>Form submitted successfully 2!</p>"


if __name__ == "__main__":
    app.run(port=8000, debug=True)
