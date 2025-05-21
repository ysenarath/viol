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
        static_url_path=static_url_path or "/viol/static",
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
        extra_head_content = []
        if self.extra_head_content:
            extra_head_content.append(self.extra_head_content)
        if "extra_head_content" in self.ctx:
            extra_head_content.append(self.ctx["extra_head_content"])
        self.ctx["extra_head_content"] = render(extra_head_content)
        self.ctx["body"] = render(self.body)
        extra_body_content = []
        if self.extra_body_content:
            extra_body_content.append(self.extra_body_content)
        if "extra_body_content" in self.ctx:
            extra_body_content.append(self.ctx["extra_body_content"])
        self.ctx["extra_body_content"] = render(extra_body_content)
        return self.template.render(url_for=url_for, **self.ctx)
