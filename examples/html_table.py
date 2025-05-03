"""Demonstration of the new html_v2 module with type-safe elements."""

from flask import Flask, request, session, url_for

import viol
from viol import BasicLayout, html, render

app = Flask(__name__)
app.secret_key = "some_secret"  # Required for sessions


viol.init_app(app)


@app.route("/")
def home():
    # Initialize contacts in session if not already present
    if "contacts" not in session:
        session["contacts"] = [
            {"name": "John Doe", "email": "john.doe@example.com"},
            {"name": "Jane Smith", "email": "jane.smith@example.com"},
        ]

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
                                    children=[
                                        html.tr(
                                            [
                                                html.td([contact["name"]]),
                                                html.td([contact["email"]]),
                                                html.td(
                                                    [
                                                        html.button(
                                                            "Delete",
                                                            attrs={
                                                                "class": "btn btn-danger",
                                                                "hx-delete": url_for(
                                                                    "delete_user",
                                                                    email=contact[
                                                                        "email"
                                                                    ],
                                                                ),
                                                                "hx-target": "#contacts-table",
                                                                "hx-swap": "innerHTML",
                                                            },
                                                        )
                                                    ]
                                                ),
                                            ]
                                        )
                                        for contact in session["contacts"]
                                    ],
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
    contacts = session["contacts"]
    contacts.append({"name": name, "email": email})
    session["contacts"] = contacts
    contacts = session["contacts"]
    items = [
        html.tr(
            [
                html.td([contact["name"]]),
                html.td([contact["email"]]),
                html.td(
                    [
                        html.button(
                            "Delete",
                            attrs={
                                "class": "btn btn-danger",
                                "hx-delete": url_for(
                                    "delete_user", email=contact["email"]
                                ),
                                "hx-target": "#contacts-table",
                                "hx-swap": "innerHTML",
                            },
                        )
                    ]
                ),
            ]
        )
        for contact in contacts
    ]
    return render(items)


@app.route("/user/delete/<email>", methods=["DELETE"])
def delete_user(email: str):
    contacts = session["contacts"]
    contact_to_delete = next(
        (contact for contact in contacts if contact["email"] == email), None
    )
    if contact_to_delete:
        contacts.remove(contact_to_delete)
        session["contacts"] = contacts
    contacts = session["contacts"]
    items = [
        html.tr(
            [
                html.td([contact["name"]]),
                html.td([contact["email"]]),
                html.td(
                    [
                        html.button(
                            "Delete",
                            attrs={
                                "class": "btn btn-danger",
                                "hx-delete": url_for(
                                    "delete_user", email=contact["email"]
                                ),
                                "hx-target": "#contacts-table",
                                "hx-swap": "innerHTML",
                            },
                        )
                    ]
                ),
            ]
        )
        for contact in contacts
    ]
    return render(items)


if __name__ == "__main__":
    app.run("localhost", 5000, debug=True)
