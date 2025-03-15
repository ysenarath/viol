from __future__ import annotations

from accordion import sample_accordion
from flask import render_template
from navbar import simple_navbar

from viol import Server, render
from viol.bootstrap.alert import Alert
from viol.html import H1, Button

app = Server(__name__)


@app.route("/click", methods=["POST", "GET"])
def clicked():
    text = "You clicked the button!"
    return f"<h1>{text}</h1>"


@app.route("/mouseover", methods=["POST", "GET"])
def mouseover():
    text = "You hovered over the button!"
    return f"<h1>{text}</h1>"


@app.route("/accordion", methods=["POST", "GET"])
def accordion():
    return render(sample_accordion())


@app.route("/")
def home():
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
    h1 = H1(
        "H1 Header (Do not click me)",
        _="on click go to url https://htmx.org",
    )
    accordion_btn = Button(
        "Accordion",
        attrs={"class": "btn btn-primary"},
        events=[
            {
                "rule": "/accordion",
                "method": "get",
                "trigger": "click",
                "target": "#accordion",
                "swap": "innerHTML",
            },
        ],
        id="my-button-{{ctx.component.uuid}}",
    )
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


if __name__ == "__main__":
    app.run(port=8000, debug=True)
