from __future__ import annotations

from pathlib import Path

from flask import Flask

__all__ = [
    "Server",
]


class Server(Flask):
    def __init__(self, *args, **kwargs):
        kwargs["static_folder"] = Path(__file__).parent / "static"
        kwargs["template_folder"] = Path(__file__).parent / "templates"
        super().__init__(*args, **kwargs)
