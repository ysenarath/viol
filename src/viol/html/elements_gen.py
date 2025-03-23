from pathlib import Path

import jinja2
import pandas as pd

cwd = Path(__file__).parent

df = pd.read_csv(cwd / "HTMLElements.csv", encoding="utf-8")

df = df.assign(Attributes=df["Attributes"].str.split(";"))

df = df.explode("Attributes", ignore_index=True)

df = df.assign(
    # 'h1, h2, h3, h4, h5, h6'
    Element=df["Element"].str.split(",").apply(lambda x: list(map(str.strip, x)))
)

df = df.explode("Element", ignore_index=True)

global_attrs = [
    "accesskey",
    "autocapitalize",
    "autocorrect",
    "autofocus",
    "contenteditable",
    "dir",
    "draggable",
    "enterkeyhint",
    "hidden",
    "inert",
    "inputmode",
    "is",
    "itemid",
    "itemprop",
    "itemref",
    "itemscope",
    "itemtype",
    "lang",
    "nonce",
    "popover",
    "spellcheck",
    "style",
    "tabindex",
    "title",
    "translate",
    "writingsuggestions",
    "class",
    "id",
    "slot",
]

text = """from __future__ import annotations

from typing import Any, Generic, TypedDict, TypeVar

from viol.core import Element, EventHandler, RenderableType

A = TypeVar("A")

__all__ = [
{% for element in elements %}
    "{{ element }}",
{% endfor %}
]


class ElementBuilder(Generic[A]):
    def __init__(self, tag: str, attrs_type: type[A]) -> None:
        self.tag = tag
        self.attrs_type = attrs_type

    def __call__(
        self,
        children: RenderableType | list[RenderableType] = None,
        attrs: A | None = None,
        events: list[EventHandler] | EventHandler | None = None,
        id: str | None = None,
        _: str | None = None,
    ) -> Element:
        return Element(
            tag=self.tag,
            children=children,
            attrs=attrs,
            events=events,
            id=id,
            _=_,
        )


"""

elements = set()

for element in df["Element"].unique():
    if element == "MathML math":
        elements.add("math")
        text += """
math = ElementBuilder(
    "math", dict
)
"""
    elif element == "SVG svg":
        elements.add("svg")
        text += """
svg = ElementBuilder(
    "svg", dict
)
"""
    else:
        attrs: list = df[df["Element"] == element]["Attributes"].unique().tolist()
        var = element if element != "del" else "del_"
        elements.add(var)
        if "globals" in attrs:
            attrs.remove("globals")
            attrs.extend(global_attrs)
        attrs = list({s.strip() for s in attrs})
        text += f"""
{var} = ElementBuilder(
    "{element}",
    TypedDict(
        "Attrs",
        {{
            {", ".join([f'"{attr}": Any' for attr in attrs])}{"," if attrs else ""}
        }},
    ),
)
"""

env = jinja2.Environment()
text = env.from_string(text).render(elements=elements)

# write to file
with open(cwd / "elements.py", "w") as f:
    f.write(text)
