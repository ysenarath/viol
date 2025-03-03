from __future__ import annotations

from flask import render_template

from viol import Server
from viol.core import Element, FlatList
from viol.elements.button import Button

app = Server(__name__)


@app.route("/click", methods=["POST", "GET"])
def clicked():
    text = "You clicked the button!"
    return f"<h1>{text}</h1>"


@app.route("/mouseover", methods=["POST", "GET"])
def mouseover():
    text = "You hovered over the button!"
    return f"<h1>{text}</h1>"


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
        id="my-button-{uuid}",
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
        id="my-button-{uuid}",
    )
    h1 = Element(
        "h1",
        "Hello!",
        _="on click go to url https://htmx.org",
    )
    body = FlatList(
        [
            "<h1>Home</h1>",
            "<p>Welcome to the home page</p>",
            click_btn,
            mouseover_btn,
            "<div id='output'></div>",
            h1,
        ]
    )
    return render_template(
        "index.html",
        title="Hello World!",
        body=body.render(world="John"),
    )


if __name__ == "__main__":
    app.run(port=8000, debug=True)
