from __future__ import annotations

import abc
import functools
import uuid
import weakref
from collections import UserDict
from collections.abc import Iterable, Sequence
from contextvars import Context, ContextVar, copy_context
from typing import Any, TypeGuard, TypeVar, Union

from jinja2 import Template

__all__ = [
    "Component",
    "RenderableType",
    "render",
]

T = TypeVar("T")

render_ctx: ContextVar[ContextDict] = ContextVar("render_ctx", default=None)


class ListView(Sequence[T]):
    def __init__(self, object: T, attr: str):
        self.get_object = weakref.ref(object)
        self.attr = attr

    def __iter__(self) -> Iterable[T]:
        obj = self.get_object()
        while obj is not None:
            obj = getattr(obj, self.attr)
            yield obj

    def __len__(self) -> int:
        obj = self.get_object()
        count = 0
        while obj is not None:
            count += 1
            obj = getattr(obj, self.attr)
        return count

    def __getitem__(self, index: int) -> T:
        obj = self.get_object()
        for _ in range(index):
            if obj is None:
                msg = f"index {index} out of range for '{self.attr}'"
                raise IndexError(msg)
            obj = getattr(obj, self.attr)
        return obj


class ContextDict(UserDict[str, Any]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent: ContextDict | None = None
        self.component: Component | None = None

    @property
    def parents(self) -> ListView[ContextDict]:
        return ListView(self, "parent")

    def __getitem__(self, key: str) -> Any:
        try:
            return super().__getitem__(key)
        except KeyError:
            if self.parent is not None:
                return self.parent[key]
            raise

    def __delitem__(self, key: str) -> None:
        try:
            super().__delitem__(key)
        except KeyError:
            if self.parent:
                del self.parent[key]
            raise

    def __iter__(self) -> Iterable[str]:
        keys = set(super().__iter__())
        if self.parent:
            keys.update(self.parent.__iter__())
        return iter(keys)

    def __len__(self) -> int:
        return len(set(self.keys()))


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


RenderableType = Union[
    Component,
    Iterable[Component],
    str,
    None,
]


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
    if isinstance(r, str):
        r: Template = Template(r)
    ctx = render_ctx.get()
    if ctx is None:
        return r.render()
    return r.render(ctx=ctx)
