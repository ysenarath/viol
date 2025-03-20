from __future__ import annotations

from collections.abc import Iterable, Mapping, MutableMapping
from html import escape
from typing import Any, ClassVar, TypeVar

from multidict import CIMultiDict

from viol.core.base import render

__all__ = [
    "AttrList",
]

T = TypeVar("T")


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
