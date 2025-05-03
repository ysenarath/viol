"""Demonstration of the new html_v2 module with type-safe elements."""

from flask import Flask, request, url_for

import viol
from viol import BasicLayout, html, render

app = Flask(__name__)

viol.init_app(app)


@app.route("/")
def home():
    # Create a container with proper typing
    body = [
        html.div(
            [
                html.h1(["HTML Dynamic Add/Remove Demo"], attrs={"class": "title"}),
                html.div(
                    [
                        html.h2("Contacts"),
                        html.table(
                            [
                                html.thead(
                                    [
                                        html.tr(
                                            [
                                                html.th("Name"),
                                                html.th("Email"),
                                                html.th("Actions"),
                                            ]
                                        )
                                    ]
                                ),
                                html.tbody(
                                    id="contacts-table",
                                    children=[],
                                ),
                            ],
                            attrs={"class": "table"},
                        ),
                        html.h2("Add A Contact"),
                        html.form(
                            [
                                html.label(
                                    [
                                        "Name",
                                        html.input(
                                            attrs={
                                                "name": "name",
                                                "type": "text",
                                            }
                                        ),
                                    ]
                                ),
                                html.label(
                                    [
                                        "Email",
                                        html.input(
                                            attrs={
                                                "name": "email",
                                                "type": "email",
                                            }
                                        ),
                                    ]
                                ),
                                html.button(
                                    "Submit",
                                    attrs={
                                        "type": "submit",
                                        "class": "btn btn-primary",
                                    },
                                ),
                            ],
                            events=[
                                {
                                    "method": "post",
                                    "rule": url_for("add_user"),
                                    "trigger": "submit",
                                    "target": "#contacts-table",
                                    "swap": "innerHTML",
                                }
                            ],
                            id="contact-form",
                            hyperscript="on htmx:afterRequest reset() me",
                        ),
                    ],
                    id="table-and-form",
                ),
            ]
        ),
    ]

    return render(BasicLayout(body=body))


@app.route("/user/add", methods=["POST"])
def add_user():
    data = dict(request.form)
    name = data.get("name")
    email = data.get("email")
    items = [
        html.tr(
            [
                html.td(name),
                html.td(email),
                html.td(
                    html.button(
                        "Delete",
                        attrs={
                            "class": "btn btn-danger",
                            "hx-delete": url_for("delete_user", email=email),
                            "hx-target": "#contacts-table",
                            "hx-swap": "innerHTML",
                        },
                    )
                ),
            ]
        ),
    ]
    return render(items)


@app.route("/user/delete/<email>", methods=["DELETE"])
def delete_user(email: str):
    return render([])


if __name__ == "__main__":
    app.run(port=8000, debug=True)
