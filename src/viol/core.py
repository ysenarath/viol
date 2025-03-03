from __future__ import annotations

import abc
import copy
import re
import uuid
import weakref
from collections import UserList
from collections.abc import Iterable, MutableSequence
from dataclasses import dataclass
from html import escape
from typing import Any, Protocol, TypeVar, runtime_checkable

from flask import render_template_string

__all__ = [
    "AttrList",
    "ComponentBase",
    "ComponentBaseConfig",
    "Element",
    "Event",
    "Renderable",
    "RenderableList",
    "VoidElement",
]

T = TypeVar("T")


@runtime_checkable
class Renderable(Protocol):
    def render(self, **ctx: Any) -> str: ...


class AttrList(UserList[tuple[str, Any]]):
    def __init__(self, data: Any) -> AttrList:
        if isinstance(data, dict):
            data = data.items()
        super().__init__(data or [])

    def to_string(self) -> str:
        return " ".join([f'{escape(k)}="{escape(str(v))}"' for k, v in self])

    def __repr__(self) -> str:
        return self.to_string()


@dataclass
class ComponentBaseConfig:
    prefix: str = ""


class ComponentBase(abc.ABC):
    config: ComponentBaseConfig

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__()
        cls.config = ComponentBaseConfig()
        for k, v in kwargs.items():
            if hasattr(cls.config, k):
                setattr(cls.config, k, v)

    def __init__(
        self, id: str | None = None, events: list[Event] | Event | None = None
    ):
        super().__init__()
        self.id = id
        self.events = EventList(self, events)

    @property
    def id(self) -> str | None:
        if not getattr(self, "_id", None):
            prefix = self.config.prefix.format(self=self)
            self._id = f"{prefix}{uuid.uuid4().hex}"
        return self._id

    @id.setter
    def id(self, value: str | None) -> None:
        self._id = escape(value) if value else None

    @abc.abstractmethod
    def render(self, **ctx: Any) -> str:
        pass

    def render_events(self) -> tuple[str, str]:
        if self.events:
            events = iter(self.events)
            event_attr = next(events).to_string()
            event_divs = "".join(e.render() for e in events)
            return event_attr, event_divs
        return "", ""


@dataclass
class Event(ComponentBase, prefix="hx-event-"):
    rule: str | None = None
    method: str | None = None
    trigger: str | None = None
    target: str | None = None
    swap: str | None = None
    include: str | None = None

    def to_string(self) -> str:
        attr = " ".join(
            [
                f'{k}="{v}"'
                for k, v in {
                    f"hx-{self.method}": self.rule,
                    "hx-trigger": self.trigger,  # click, mouseover, etc
                    "hx-target": self.target,
                    "hx-swap": self.swap,
                    "hx-include": self.include,
                }.items()
                if v
            ]
        )
        return attr.strip()

    def __repr__(self) -> str:
        return self.to_string()

    def render(self, **ctx: Any) -> str:
        return f"<div id={self.id} {self.to_string()}></div>"


class ValidatedList(MutableSequence[T]):
    def __init__(self, data: Iterable[T] | None = None):
        self._data = data or []

    def validate(self, value: Any) -> T:
        return value

    def __getitem__(self, i: int) -> T:
        return self._data[i]

    def __setitem__(self, i: int, value: Any) -> None:
        self._data[i] = self.validate(value)

    def __delitem__(self, i: int) -> None:
        del self._data[i]

    def insert(self, i: int, value: Any) -> None:
        self._data.insert(i, self.validate(value))

    def __len__(self) -> int:
        return len(self._data)


class EventList(ValidatedList[Event]):
    def __init__(self, bound: ComponentBase, data: list[Event] | Event | None = None):
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

    def validate(self, value: Any) -> Any:
        event = copy.deepcopy(value) if isinstance(value, Event) else Event(**value)
        match = self.Match(f"#{self.bound().id}")
        event.trigger = re.sub(r"(?<=from:)([#\w]+)", match, event.trigger)
        if not match.found:
            event.trigger = f"{event.trigger} from:{match.repl}"
        return event


class RenderableList(ValidatedList[str | Renderable]):
    def __init__(self, data: str | list[Any] | None = None):
        super().__init__()
        if isinstance(data, str):
            data = [data]
        self.extend(data or [])

    @classmethod
    def _unwrap(cls, items: Iterable[Any]):
        for item in items:
            if isinstance(item, (str, Renderable)):
                yield item
            else:
                yield from cls._unwrap(item)

    def render(self, **ctx: Any) -> str:
        html = ""
        for item in self._unwrap(self):
            html += (
                render_template_string(item, **ctx)
                if isinstance(item, str)
                else item.render(**ctx)
            )
        return html


class Element(ComponentBase, prefix="hx-{self.tag}-"):
    def __init__(
        self,
        tag: str,
        children: str | Renderable | list[Renderable | str] | None = None,
        attrs: AttrList = None,
        id: str | None = None,
        events: list[Event] | Event | None = None,
    ):
        self.tag = tag
        self.children = children
        self.attrs = AttrList(attrs)
        super().__init__(id=id, events=events)

    @classmethod
    def _render(cls, children: Any, **ctx: Any) -> str:
        if isinstance(children, Renderable):
            return children.render(**ctx)
        if isinstance(children, Iterable) and not isinstance(children, str):
            return "".join(cls._render(c, **ctx) for c in children)
        return render_template_string(children, **ctx)

    def render(self, **ctx: Any) -> str:
        children = self._render(self.children, **ctx)
        tag = escape(self.tag)
        attr_id = f'id="{self.id}"' if self.id else ""
        attrs = self.attrs.to_string()
        event, other_events = self.render_events()
        return f"<{tag} {attr_id} {attrs} {event}>{children}</{tag}>{other_events}"


class VoidElement(Element):
    def __init__(
        self,
        tag: str,
        attrs: AttrList = None,
        id: str | None = None,
        events: list[Event] | Event | None = None,
    ):
        super().__init__(tag=tag, children=None, attrs=attrs, id=id, events=events)

    def render(self, **ctx: Any) -> str:
        tag = escape(self.tag)
        attrs = self.attrs.to_string()
        attr_id = f'id="{self.id}"' if self.id else ""
        event, other_events = self.render_events()
        return f"<{tag} {attr_id} {attrs} {event} />{other_events}"
