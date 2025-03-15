from viol.html.doctype import DOCTYPE
from viol.html.head import Head
from viol.html.html import Html

layout = [
    DOCTYPE,
    Html(
        [
            Head(),
            "Hello, world!",
        ]
    ),
]


print(layout.render())
