import json

from flask import Blueprint, make_response, request, session, url_for

from viol import BasicLayout, html, render

from .models import User, db

app = Blueprint("users", __name__)

ALERT_LEVELS = {
    "primary",
    "secondary",
    "success",
    "danger",
    "warning",
    "info",
    "light",
    "dark",
}


def validate_alert_level(level: str) -> bool:
    if level.lower() == "error":
        level = "danger"
    if level.lower() in ALERT_LEVELS:
        return level.lower()
    return "info"


def alert(trigger: dict | str) -> str:
    if isinstance(trigger, str):
        trigger = {"level": "info", "message": trigger}
    if not trigger:
        return ""
    message = trigger.get("message", "")
    resp = make_response(message)
    resp.headers["HX-Trigger"] = json.dumps(
        {
            "violAlert": {
                "level": validate_alert_level(trigger["level"]),
                "message": trigger["message"],
            }
        }
    )
    return resp


@app.route("/users/register", methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        trigger = None
        username = request.form["username"]
        password = request.form["password"]
        try:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            # return "User registered"
            trigger = {"level": "success", "message": "User registered"}
        except Exception as e:
            db.session.rollback()
            if "UNIQUE constraint failed: user.username" in str(e):
                trigger = {"level": "error", "message": "User already exists"}
            else:
                trigger = {"level": "error", "message": "Error registering user"}
        return alert(trigger)
    return render(
        BasicLayout(
            body=[
                html.form(
                    [
                        html.label("Username:"),
                        html.input(
                            attrs={
                                "type": "text",
                                "name": "username",
                                "required": "true",
                            }
                        ),
                        html.label("Password:"),
                        html.input(
                            attrs={
                                "type": "password",
                                "name": "password",
                                "required": "true",
                            }
                        ),
                        html.button("Register", attrs={"type": "submit"}),
                    ],
                    attrs={"method": "post"},
                    events=[
                        {
                            "method": "post",
                            "rule": url_for("users.register_user"),
                            "trigger": "submit",
                            "target": "body",
                            "swap": "none",
                        }
                    ],
                    id="user-register-form",
                )
            ]
        )
    )


@app.route("/users/profile", methods=["GET", "POST"])
def show_profile():
    user_id = session.get("user_id", None)
    trigger = None
    if user_id is None:
        trigger = {"level": "error", "message": "User not logged in"}
    else:
        user: User | None = User.query.get(user_id)
        if user is None:
            trigger = {"level": "error", "message": "User not found"}
        elif request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            current_password = request.form["current_password"]
            if user.check_password(current_password):
                user.username = username
                user.set_password(password)
                try:
                    db.session.commit()
                    trigger = {"level": "success", "message": "User updated"}
                except Exception as e:
                    db.session.rollback()
                    if "UNIQUE constraint failed: user.username" in str(e):
                        trigger = {
                            "level": "error",
                            "message": "Username already exists",
                        }
                    else:
                        trigger = {"level": "error", "message": "Error updating user"}
            else:
                trigger = {"level": "error", "message": "Invalid credentials"}
    if trigger:
        return alert(trigger)
    return render(
        BasicLayout(
            body=[
                html.form(
                    [
                        html.label("Username:"),
                        html.input(
                            attrs={
                                "type": "text",
                                "name": "username",
                                "required": "true",
                                "value": user.username,
                            }
                        ),
                        html.label("Current Password:"),
                        html.input(
                            attrs={
                                "type": "password",
                                "name": "current_password",
                                "required": "true",
                            }
                        ),
                        html.label("Password:"),
                        html.input(
                            attrs={
                                "type": "password",
                                "name": "password",
                                "required": "true",
                            }
                        ),
                        html.button("Update", attrs={"type": "submit"}),
                    ],
                    attrs={"method": "post"},
                    events=[
                        {
                            "method": "post",
                            "rule": url_for("users.show_profile"),
                            "trigger": "submit",
                            "target": "body",
                            "swap": "none",
                        }
                    ],
                    id="user-profile-form",
                )
            ]
        )
    )


@app.route("/users/logout", methods=["GET", "POST"])
def logout_user():
    session.pop("user_id", None)
    return alert({"level": "success", "message": "User logged out"})


@app.route("/users/login", methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        trigger = None
        username = request.form["username"]
        password = request.form["password"]
        user: User | None = User.query.filter_by(username=username).first()
        if isinstance(user, User):
            if user.check_password(password):
                session["user_id"] = user.id
                # return "User logged in: " + user.username
                trigger = {
                    "level": "success",
                    "message": "User logged in: " + user.username,
                }
            else:
                # return "Invalid credentials"
                trigger = {"level": "error", "message": "Invalid credentials"}
        else:
            trigger = {"level": "error", "message": "User not found"}
        if trigger:
            return alert(trigger)
    return render(
        BasicLayout(
            body=[
                html.form(
                    [
                        html.label("Username:"),
                        html.input(
                            attrs={
                                "type": "text",
                                "name": "username",
                                "required": "true",
                            }
                        ),
                        html.label("Password:"),
                        html.input(
                            attrs={
                                "type": "password",
                                "name": "password",
                                "required": "true",
                            }
                        ),
                        html.button("Login", attrs={"type": "submit"}),
                    ],
                    attrs={"method": "post"},
                    events=[
                        {
                            "method": "post",
                            "rule": url_for("users.login_user"),
                            "trigger": "submit",
                            "target": "body",
                            "swap": "none",
                        }
                    ],
                    id="user-login-form",
                )
            ]
        )
    )


@app.route("/users", methods=["GET"])
def show_users():
    return render(
        BasicLayout(
            body=[
                html.a("Register", attrs={"href": url_for("users.register_user")}),
                html.a("Login", attrs={"href": url_for("users.login_user")}),
                html.a("Profile", attrs={"href": url_for("users.show_profile")}),
                html.a("Logout", attrs={"href": url_for("users.logout_user")}),
                html.h1("Users"),
                html.ul([html.li(user.username) for user in User.query.all()]),
            ]
        )
    )
