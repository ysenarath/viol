"""Demonstration of the new html_v2 module with type-safe elements."""

from flask import Flask

import viol
from viol import BasicLayout, html, render
from viol.bootstrap.alerts import Alert
from viol.bootstrap.badge import Badge
from viol.bootstrap.buttons import Button

from .components.accordion import sample_accordion
from .components.breadcrumb import simple_breadcrumb
from .components.navbar import simple_navbar

app = Flask(__name__)

viol.init_app(app)


@app.route("/")
def home():
    # Create a container with proper typing
    body = [
        simple_navbar(
            items=[
                {"name": "Accordion", "href": "/accordion"},
                # alerts
                {"name": "Alerts", "href": "/alerts"},
                # badge
                {"name": "Badges", "href": "/badges"},
            ]
        ),
        html.div(
            [
                simple_breadcrumb(),
                html.h1("Welcome to the Bootstrap App"),
                html.p("This is a simple example of using Bootstrap with Flask."),
            ],
            attrs={"class": ["container"]},
            id="main-content",
        ),
    ]
    return render(BasicLayout(body=body))


@app.route("/accordion")
def about_page():
    example = sample_accordion()
    bed = simple_breadcrumb()
    return render([bed, example])


@app.route("/alerts")
def alerts_page():
    example = html.div(
        [
            Alert("This is a primary alert!", variant="primary"),
            Alert("This is a secondary alert!", variant="secondary"),
            Alert("This is a success alert!", variant="success"),
            Alert("This is a danger alert!", variant="danger"),
            Alert("This is a warning alert!", variant="warning"),
            Alert("This is an info alert!", variant="info"),
            Alert("This is a light alert!", variant="light"),
            Alert("This is a dark alert!", variant="dark"),
        ],
        attrs={"class": ["container"]},
    )
    bed = simple_breadcrumb()
    return render([bed, example])


@app.route("/badges")
def badges_page():
    example = html.div(
        [
            html.h1(["Example heading ", Badge("New", bg_color="secondary")]),
            html.h2(["Example heading ", Badge("New", bg_color="secondary")]),
            html.h3(["Example heading ", Badge("New", bg_color="secondary")]),
            html.h4(["Example heading ", Badge("New", bg_color="secondary")]),
            html.h5(["Example heading ", Badge("New", bg_color="secondary")]),
            html.h6(["Example heading ", Badge("New", bg_color="secondary")]),
            Button(
                [
                    "Notifications ",
                    Badge(
                        "4",
                        bg_color="secondary",
                        attrs={
                            "class": [
                                "position-absolute",
                                "top-0",
                                "start-100",
                                "translate-middle",
                            ]
                        },
                    ),
                ],
                color="primary",
            ),
            Button(
                ["Inbox ", Badge("99+", bg_color="danger")],
                color="primary",
                attrs={"class": ["position-relative"]},
            ),
        ],
        attrs={"class": ["container"]},
    )
    bed = simple_breadcrumb()
    return render([bed, example])
