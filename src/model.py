from os import environ
from flask_sqlalchemy import SQLAlchemy


if __name__ == "__main__":
    from controller import generate_api_key
else:
    from .controller import generate_api_key

db = SQLAlchemy()


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    api_key = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(99), nullable=False)
    last_name = db.Column(db.String(99), nullable=False)
    discord_tag = db.Column(db.String(99), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, first_name, last_name, discord_tag):
        self.first_name = first_name
        self.last_name = last_name
        self.discord_tag = discord_tag
        self.api_key = generate_api_key({u.api_key for u in User.query.all()})

    def __repr__(self):
        return f"<User: id={self.id}, name={self.first_name} {self.last_name}, discord={self.discord_tag}>"

    


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