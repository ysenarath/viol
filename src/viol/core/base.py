from __future__ import annotations

import abc
import copy
import functools
import re
import uuid
import weakref
from collections.abc import Iterable, Mapping, MutableMapping
from contextvars import Context, ContextVar, copy_context
from html import escape
from typing import Any, ClassVar, TypeGuard, TypeVar

from jinja2 import Template
from multidict import CIMultiDict

from viol.utils.collections import ValidatedList

__all__ = [
    "AttrList",
    "Element",
    "Event",
    "RenderableType",
    "VoidElement",
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


class AttrsProperty:
    methods: ClassVar[set[str]] = {"get", "post", "put", "patch", "delete"}

    def __init__(self, prefix: str = "", name: str | None = None):
        self.prefix = prefix
        self.name = name

    def __set_name__(self, owner: Any, name: str, /) -> None:
        if self.name:
            return
        self.name = f"{self.prefix}{name}"

    def __get__(self, instance: AttrList | None, owner: Any = None) -> str | None:
        if instance is None:
            return self
        if self.name == f"{self.prefix}method":
            for method in self.methods:
                if instance.get(f"{self.prefix}{method}"):
                    return method
        if self.name == f"{self.prefix}rule":
            for method in self.methods:
                rule = instance.get(f"{self.prefix}{method}")
                if rule:
                    return rule
        # if self.name == "id":
        #   # set the id to the uuid value
        #   instance["id"] = uuid.uuid4().hex
        # return instance.get(self.name)
        return instance[self.name]

    def __set__(self, instance: AttrList | None, value: Any) -> None:
        if instance is None:
            msg = f"{self.name} must be set on an Event instance"
            raise AttributeError(msg)
        if self.name == f"{self.prefix}method":
            # find current method
            current_method = None
            for method in self.methods:
                current_method = f"{self.prefix}{method}"
                if current_method in instance:
                    break
            # get and delete the current rule
            current_rule = instance[current_method]
            del instance[current_method]
            # set the new method
            instance[f"{self.prefix}{value}"] = current_rule
        elif self.name == f"{self.prefix}rule":
            # find current method
            current_method = None
            for method in self.methods:
                current_method = f"{self.prefix}{method}"
                if current_method in instance:
                    break
            # set the new rule for the current method
            instance[current_method] = value
        else:
            instance[self.name] = value


class AttrList(MutableMapping[str, T]):
    id = AttrsProperty()
    _ = AttrsProperty()
    class_ = AttrsProperty(name="class")
    style = AttrsProperty()

    def __init__(self, *args: Mapping[str, T] | None, **kwargs: T):
        if args:
            if len(args) > 1:
                msg = "at most one mapping is allowed"
                raise TypeError(msg)
            if args[0] is None:
                args = {}
        self._data = CIMultiDict(*args, **kwargs)

    def __getitem__(self, key: str) -> T:
        return self._data[key]

    def __setitem__(self, key: str, value: T) -> None:
        self._data[key] = value

    def __delitem__(self, key: str) -> None:
        del self._data[key]

    def __iter__(self) -> Iterable[str]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def to_string(self) -> str:
        items = []
        for k, v in self.items():
            try:
                v = render(v)  # noqa: PLW2901
            except Exception as e:
                msg = f"unable to render value '{v}' for attribute '{k}' due to {type(e).__name__}({e})"
                raise ValueError(msg) from None
            items.append(f'{escape(k)}="{escape(v)}"')
        return " ".join(items)

    def __repr__(self) -> str:
        return self.to_string()


class Event(AttrList, Component):
    method = AttrsProperty("hx-")
    rule = AttrsProperty("hx-")
    trigger = AttrsProperty("hx-")
    target = AttrsProperty("hx-")
    swap = AttrsProperty("hx-")
    include = AttrsProperty("hx-")
    sync = AttrsProperty("hx-")

    def __init__(
        self,
        rule: str | None = None,
        method: str | None = None,
        trigger: str | None = None,
        target: str | None = None,
        swap: str | None = None,
        include: str | None = None,
        sync: str | None = None,
    ):
        attrs = [
            (k, v)
            for k, v in {
                f"hx-{method}": rule,
                "hx-trigger": trigger,
                "hx-target": target,
                "hx-swap": swap,
                "hx-include": include,
                "hx-sync": sync,
            }.items()
            if v
        ]
        super().__init__(attrs)

    def render(self) -> str:
        return f"<div {self.to_string()}></div>"


class EventList(ValidatedList[Event]):
    def __init__(self, bound: Element, data: list[Event] | Event | None = None):
        super().__init__()
        self.bound = weakref.ref(bound)
        if isinstance(data, Event):
            data = [data]
        self.extend(data or [])

    class Match:
        def __init__(self, repl: str):
            self.found = False
            self.repl = repl

        def __call__(self, event: re.Match[str]) -> str:
            self.found = True
            return self.repl

    def validate(self, value: Any) -> Event:
        event = copy.deepcopy(value) if isinstance(value, Event) else Event(**value)
        match = self.Match(f"#{self.bound().attrs.id}")
        # replace or add the trigger (directing to the bound element)
        event.trigger = re.sub(r"(?<=from:)([#\w]+)", match, event.trigger)
        if not match.found:
            event.trigger = f"{event.trigger} from:{match.repl}"
        return event


class Element(Component):
    def __init__(
        self,
        tag: str,
        children: RenderableType | list[RenderableType] | None = None,
        attrs: AttrList = None,
        id: str | None = None,
        events: list[Event] | Event | None = None,
        _: str | None = None,
    ):
        super().__init__()
        self.tag = tag
        self.children = children
        self.attrs = AttrList(attrs)
        if id:
            self.attrs.id = id
        if _:
            self.attrs._ = _
        self.events = EventList(self, events)

    def render(self) -> str:
        children = render(self.children)
        tag = escape(self.tag)
        attrs = self.attrs.to_string()
        if self.events:
            event = self.events[0].to_string()
            other_events = render(self.events[1:])
            return f"<{tag} {attrs} {event}>{children}</{tag}>{other_events}"
        return f"<{tag} {attrs}>{children}</{tag}>"


class VoidElement(Element):
    def __init__(
        self,
        tag: str,
        attrs: AttrList = None,
        id: str | None = None,
        events: list[Event] | Event | None = None,
        _: str | None = None,
    ):
        super().__init__(tag=tag, children=None, attrs=attrs, id=id, events=events, _=_)

    def render(self) -> str:
        tag = escape(self.tag)
        attrs = self.attrs.to_string()
        if self.events:
            event = self.events[0].to_string()
            other_events = render(self.events[1:])
            return f"<{tag} {attrs} {event} />{other_events}"
        return f"<{tag} {attrs} />"
