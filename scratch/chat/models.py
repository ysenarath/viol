from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str | None] = mapped_column(unique=True, nullable=True)

    def __init__(self, username: str, password: str, email: str | None = None):
        password_hash = generate_password_hash(password)
        super().__init__(username=username, password_hash=password_hash, email=email)

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Message(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    session_id: Mapped[str] = mapped_column(nullable=False)
    sender_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    receiver_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    parent_id: Mapped[int] = mapped_column(ForeignKey("message.id"))

    sender = db.relationship("User", foreign_keys=[sender_id])
    receiver = db.relationship("User", foreign_keys=[receiver_id])
    parent = db.relationship("Message", foreign_keys=[parent_id])

    def __repr__(self):
        return f"<Message {self.id}"


def init_app(app: Flask, path: str | Path) -> SQLAlchemy:
    # configure the SQLite database, relative to the app instance folder
    if isinstance(path, Path):
        path = Path(path)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{path}"
    # initialize the app with the extension
    db.init_app(app)
    if not path.exists():
        # create the database if it does
        with app.app_context():
            db.create_all()
