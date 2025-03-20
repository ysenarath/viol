from __future__ import annotations

import abc
import functools
import uuid
from collections.abc import Iterable, MutableMapping
from contextvars import Context, ContextVar, copy_context
from typing import Any, TypeGuard, TypeVar

from jinja2 import Template

__all__ = [
    "RenderableType",
    "render",
]

T = TypeVar("T")

render_ctx: ContextVar[ContextDict] = ContextVar("render_ctx", default=None)


class ContextDict(MutableMapping[str, Any]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent: ContextDict | None = None
        self.component: Component | None = None

    def __getitem__(self, key: str) -> Any:
        try:
            return super().__getitem__(key)
        except KeyError:
            if self.parent is not None:
                return self.parent[key]
            raise

    def __setitem__(self, key: str, value: Any) -> None:
        super().__setitem__(key, value)

    def __delitem__(self, key: str) -> None:
        try:
            super().__delitem__(key)
        except KeyError:
            if self.parent:
                del self.parent[key]
            raise

    def __iter__(self) -> Iterable[str]:
        keys = set(self.keys())
        if self.parent:
            keys.update(self.parent.keys())
        return iter(keys)

    def __len__(self) -> int:
        keys = set(self.keys())
        if self.parent:
            keys.update(self.parent.keys())
        return len(keys)


class Component(abc.ABC):
    uuid: str

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        obj.uuid = uuid.uuid4().hex
        return obj

    @property
    def ctx(self) -> ContextDict:
        return render_ctx.get()

    @abc.abstractmethod
    def render(self) -> str: ...

    def render_with_context(self) -> str:
        ctx = ContextDict()
        parent = render_ctx.get()
        ctx.parent = parent
        ctx.component = self
        token = render_ctx.set(ctx)
        try:
            return super().__getattribute__("render")()
        finally:
            if token:
                render_ctx.reset(token)

    def __getattribute__(self, name: str) -> Any:
        attr = super().__getattribute__(name)
        if name == "render":
            # copy the current context
            ctx: Context = copy_context()
            return functools.partial(ctx.run, self.render_with_context)
        return attr


RenderableType = Component | Iterable[Component] | str | None


def is_renderable(obj: Any) -> TypeGuard[RenderableType]:
    if obj is None:
        # None is renderable as an empty string
        return True
    if isinstance(obj, (Component, str)):
        # Components and strings are renderable
        return True
    if isinstance(obj, Iterable) and not isinstance(obj, str):
        # All elements of an iterable must be renderable
        # Caution: iterators will be consumed
        return all(is_renderable(c) for c in obj)
    # Not renderable
    return False


def render(r: RenderableType) -> str:
    # None
    if r is None:
        return ""
    if isinstance(r, Component):
        # components
        return r.render()
    if isinstance(r, Iterable) and not isinstance(r, str):
        # lists, tuples, sets, etc.
        return " ".join(render(c) for c in r)
    # template to render
    r: Template = Template(r)
    ctx = render_ctx.get()
    if ctx is None:
        return r.render()
    return r.render(ctx=ctx)
