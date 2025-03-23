from __future__ import annotations

from pathlib import Path

from flask import Blueprint, Flask, url_for
from jinja2 import Environment, FileSystemLoader

from viol.core import Component
from viol.core.base import render

__all__ = []

cwd = Path(__file__).parent


def init_app(
    app: Flask,
    static_folder: str | Path | None = None,
    static_url_path: str | None = None,
) -> None:
    layout = Blueprint(
        "viol",
        __name__,
        static_folder=static_folder or cwd / "static",
        static_url_path=static_url_path or "/viol/static",
    )
    app.register_blueprint(layout)


class Layout(Component):
    def __init__(
        self,
        body: str = "",
        title: str = "Viol",
        styles: str | None = None,
        scripts: str | None = None,
    ) -> None:
        self.env = Environment(loader=FileSystemLoader(cwd / "templates"))
        self.template = self.env.get_template("index.html")
        self.title = title
        self.styles = styles
        self.body = body
        self.scripts = scripts

    def render(self) -> str:
        self.ctx["title"] = self.title
        self.ctx["styles"] = render(self.styles)
        self.ctx["body"] = render(self.body)
        self.ctx["scripts"] = render(self.scripts)
        return self.template.render(url_for=url_for, **self.ctx)
