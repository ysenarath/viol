from __future__ import annotations

from pathlib import Path

from flask import Blueprint, Flask, url_for
from jinja2 import Environment, FileSystemLoader

from viol.core import Component
from viol.core.base import render

fdir = Path(__file__).parent


def init_app(
    app: Flask,
    static_folder: str | Path | None = None,
    static_url_path: str | None = None,
) -> None:
    layout = Blueprint(
        "viol",
        __name__,
        static_folder=static_folder or fdir / "static",
        static_url_path=static_url_path or "/__viol/static",
    )
    app.register_blueprint(layout)


class BasicLayout(Component):
    def __init__(
        self,
        body: str = "",
        title: str = "Viol",
        extra_head_content: str | None = None,
        extra_body_content: str | None = None,
    ) -> None:
        self.env = Environment(loader=FileSystemLoader(fdir / "templates"))
        self.template = self.env.get_template("index.html")
        self.title = title
        self.extra_head_content = extra_head_content
        self.body = body
        self.extra_body_content = extra_body_content

    def render(self) -> str:
        self.ctx["title"] = self.title
        self.ctx["extra_head_content"] = render(self.extra_head_content)
        self.ctx["body"] = render(self.body)
        self.ctx["extra_body_content"] = render(self.extra_body_content)
        return self.template.render(url_for=url_for, **self.ctx)
