from __future__ import annotations

import uuid

from flask import render_template

from viol import Server
from viol.core import RenderableList
from viol.html.button import Button

app = Server(__name__)


@app.route("/click", methods=["POST", "GET"])
def clicked():
    uid = uuid.uuid4().hex
    return f"<h1>{uid}</h1>"


@app.route("/")
def home():
    button = Button(
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
            {
                "rule": "/click",
                "method": "get",
                "trigger": "mouseover",
                "target": "#output",
                "swap": "innerHTML",
            },
        ],
        id="my-button",
    )
    body = RenderableList(
        [
            "<h1>Home</h1>",
            "<p>Welcome to the home page</p>",
            button,
            "<div id='output'></div>",
        ]
    )
    return render_template(
        "index.html", title="Hello World!", body=body.render(world="John")
    )


if __name__ == "__main__":
    app.run(port=8000, debug=True)
