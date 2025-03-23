"""Demonstration of the new html_v2 module with type-safe elements."""

from flask import Flask, url_for

import viol
from viol import Layout, html, render

app = Flask(__name__)

viol.init_app(app)


@app.route("/")
def chat():
    # Create a container with proper typing
    body = html.div(
        [
            html.h1(attrs={"class": "title"}, children=["Chat"]),
            html.div(
                [],
                attrs={"class": "chat-container"},
                id="chatHistory",
            ),
            html.form(
                [
                    # Input with type checking
                    html.input(
                        attrs={
                            "type": "text",
                            "name": "message",
                            "placeholder": "Enter your message",
                            "required": "true",
                            "class": "form-control",
                        }
                    ),
                    # Button with type checking
                    html.button(
                        "Send",
                        attrs={
                            "type": "submit",
                            "class": "btn btn-primary",
                        },
                        # add input to chat history
                        _="on click append \"<p class='user'>You</p><p class='message'>\" + document.querySelector('#form-demo input').value + \"</p>\" to #chatHistory",
                    ),
                ],
                attrs={
                    "class": "form-container",
                },
                id="form-demo",
                events=[
                    {
                        "method": "get",
                        "rule": url_for("submit"),
                        "trigger": "submit",
                        "target": "#chatHistory",
                        "swap": "beforeend",
                    }
                ],
            ),
        ],
        attrs={"class": "container"},
    )

    return render(Layout(body=body))


@app.route("/submit", methods=["GET"])
def submit():
    return render(html.p("Message sent!", attrs={"class": "message"}))


if __name__ == "__main__":
    app.run(port=8000, debug=True)
