"""
HTML Elements Generator
======================

Purpose
-------
This script generates the elements.py file by processing the HTMLElements.csv data file.
It creates ElementBuilder instances for all standard HTML elements with their respective
attributes.

Core Functionality
-----------------
- Reads HTML element definitions from HTMLElements.csv
- Processes element attributes and global attributes
- Generates TypedDict definitions for element attributes
- Creates ElementBuilder instances for each HTML element
- Writes the generated code to elements.py

Dependencies
-----------
- pandas: For reading and processing CSV data
- jinja2: For template rendering
- pathlib: For file path handling

Usage Examples
-------------
# Run this script to regenerate elements.py after updating HTMLElements.csv
$ python -m src.viol.html.elements_gen

Edge Cases
---------
- Special handling for 'del' element (renamed to 'del_' to avoid Python keyword conflict)
- Special handling for MathML and SVG elements
- Global attributes are added to all elements that include 'globals' in their attributes

Version History
--------------
1.0.0 - Initial stable release
"""

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
        hyperscript: str | None = None,
    ) -> Element:
        return Element(
            tag=self.tag,
            children=children,
            attrs=attrs,
            events=events,
            id=id,
            hyperscript=hyperscript,
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
