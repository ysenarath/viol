from __future__ import annotations

from viol.core import AttrList, Element, Event, Renderable


class Button(Element, prefix="btn-"):
    def __init__(
        self,
        children: str | Renderable | list[Renderable | str] | None = None,
        attrs: AttrList = None,
        id: str | None = None,
        events: list[Event] | Event | None = None,
    ):
        super().__init__(
            tag="button",
            children=children,
            attrs=attrs,
            id=id,
            events=events,
        )


if __name__ == "__main__":
    button = Button(
        "Hello, {{ world }}!",
        attrs={"class": "btn btn-primary"},
        events=[
            {
                "rule": "/click",
                "method": "post",
                "trigger": "click",
                "target": "#output",
                "swap": "outerHTML",
            },
            {
                "rule": "/click",
                "method": "get",
                "trigger": "mouseover",
                "target": "#output",
                "swap": "outerHTML",
            },
        ],
        id="my-button",
    )

    from flask import Flask

    app = Flask(__name__)
    with app.app_context():
        print(button.render(world="John"))
