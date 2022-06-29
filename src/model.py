from os import environ
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

if __name__ == "__main__":
    from controller import generate_api_key
else:
    from .controller import generate_api_key

db = SQLAlchemy()


class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(99), nullable=False)
    last_name = db.Column(db.String(99), nullable=False)
    discord = db.Column(db.String(99), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, first_name, last_name, discord):
        self.first_name = first_name
        self.last_name = last_name
        self.discord = discord

    def __repr__(self):
        return f"<User: id={self.id}, name={self.first_name} {self.last_name}, discord={self.discord_tag}>"

class APIKey(db.Model):

    __tablename__ = "api_keys"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    api_key = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    active = db.Column(db.Boolean, default=True)

    def __init__(self, user_id):
        self.api_key = generate_api_key({u.api_key for u in APIKey.query.all()})
        self.user_id = user_id
        self.active = True

class APIRequest(db.Model):

    __tablename__ = "api_requests"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    endpoint = db.Column(db.String(99))
    success = db.Column(db.Boolean)

    def __init__(self, user_id, endpoint, success):
        self.user_id = user_id
        self.endpoint = endpoint
        self.success = success

class Character(db.Model):

    __tablename__ = "characters"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(99), nullable=False)
    title = db.Column(db.String(99), nullable=True)
    race = db.Column(db.String(99), nullable=True)
    homeland = db.Column(db.String(99), nullable=True)

    def __init__(self, name, title, race, homeland):
        self.name = name
        self.title = title
        self.race = race
        self.homeland = homeland

    def __repr__(self):
        return f"<Character: id={self.id}, name={self.name}>"


def generate_characters():
    from character_generator import wot_characters
    db.session.add_all([
        Character(ch.name, ch.title, ch.race, ch.homeland)
        for ch in wot_characters
    ])
    db.session.commit()

def connect_to_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = environ["POSTGRES_URI"]
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    from flask import Flask
    connect_to_db(Flask(__name__))
    print("Connected to DB.")