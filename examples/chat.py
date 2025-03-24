"""Demonstration of the new html_v2 module with type-safe elements."""

from flask import Flask, url_for

import viol
from viol import Layout, html, render

app = Flask(__name__)

viol.init_app(app)


@app.route("/")
def chat():
    # Create a container with proper typing
    body = [
        html.div(
            [
                html.h1(attrs={"class": "title"}, children=["Chat"]),
                html.div([], attrs={"class": "chat-container"}, id="chatHistory"),
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
                        "type": "button",
                        "class": "btn btn-primary",
                    },
                    events=[
                        {
                            "method": "get",
                            "rule": url_for("submit"),
                            "trigger": "click",
                            "target": "#chatHistory",
                            "swap": "beforeend transition:true",
                            "vals": "js:{...getChatHistory()}",
                        }
                    ],
                    id="form-demo-button",
                ),
            ],
            attrs={"class": "container"},
        ),
        html.script("""
function extractHistoryItem(item) {
    return {
        role: item.querySelector('.role').textContent,
        content: item.querySelector('.content').textContent
    };
}

function getChatHistory() {
    // add the last line to get the chat history
    let chatHistory = document.querySelector('#chatHistory');
    // add the last line to get the chat history
    let values = document.querySelectorAll('#chatHistory .chatHistoryItem');
    let history = [];
    if (values) {
        history = Array.from(values).map(extractHistoryItem);
    }
    return history;
}
"""),
    ]
    return render(Layout(body=body))


@app.route("/submit", methods=["GET"])
def submit():
    return render(
        html.div(
            [
                html.span(
                    "Assistant",
                    attrs={"class": "role"},
                ),
                html.span(
                    "Hello!",
                    attrs={"class": "content"},
                ),
            ],
            attrs={"class": "chatHistoryItem"},
        ),
    )


if __name__ == "__main__":
    app.run(port=8000, debug=True)
