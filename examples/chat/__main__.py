"""Demonstration of the new html_v2 module with type-safe elements."""

import uuid
from pathlib import Path

from flask import Flask, request, session, url_for

import viol
from viol import BasicLayout, html, render

from . import models
from .models import Message, User, db
from .users import app as users_bp

app = Flask(__name__)
app.register_blueprint(users_bp)

app.secret_key = "super secret key"

viol.init_app(app)

DATABASE = Path(__file__).parent / "sessions.db"

models.init_app(app, DATABASE)


@app.route("/")
def chat():
    session_id = session.get("session_id", None)
    if session_id is None:
        session["session_id"] = uuid.uuid4().hex
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
    return render(BasicLayout(body=body))


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
