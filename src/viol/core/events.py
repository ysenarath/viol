import copy
import re
import weakref
from typing import TYPE_CHECKING, Any

from viol.core.attributes import AttrMultiDict, AttrsProperty
from viol.core.base import Component
from viol.utils.collections import ValidatedList

__all__ = [
    "EventHandler",
    "EventHandlerList",
]

if TYPE_CHECKING:
    from viol.core.element import Element


class EventHandler(AttrMultiDict, Component):
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


class EventHandlerList(ValidatedList[EventHandler]):
    def __init__(
        self, bound: Element, data: list[EventHandler] | EventHandler | None = None
    ):
        super().__init__()
        self.bound = weakref.ref(bound)
        if isinstance(data, EventHandler):
            data = [data]
        self.extend(data or [])

    class Match:
        def __init__(self, repl: str):
            self.found = False
            self.repl = repl

        def __call__(self, event: re.Match[str]) -> str:
            self.found = True
            return self.repl

    def validate(self, value: Any) -> EventHandler:
        event = (
            copy.deepcopy(value)
            if isinstance(value, EventHandler)
            else EventHandler(**value)
        )
        match = self.Match(f"#{self.bound().attrs.id}")
        # replace or add the trigger (directing to the bound element)
        event.trigger = re.sub(r"(?<=from:)([#\w]+)", match, event.trigger)
        if not match.found:
            event.trigger = f"{event.trigger} from:{match.repl}"
        return event
