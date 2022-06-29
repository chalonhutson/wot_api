from os import environ
from flask import Flask, render_template, url_for, jsonify, request
from .model import db, User, Character
from .forms import RegisterForm

app = Flask(__name__)
app.config["SECRET_KEY"] = environ["SECRET_KEY"]


@app.route("/")
def home():
    return render_template("home.html", title="WOT API")

@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if request.method == "POST" and form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        discord = form.discord.data

        if User.query.filter_by(discord_tag=discord).first():
            return "You've already gotten an API key. Message Chalon for a new one."
        else:
            new_user = User(first_name, last_name, discord)
            db.session.add(new_user)
            db.session.commit()
            return f"<h2>Here is your API key, please keep it safe.</h2><h1>{new_user.api_key}</h1>"
    else:
        return render_template("register.html", form=form)

@app.route("/characters")
def characters():
    characters = Character.query.all()
    return render_template("characters.html",titie="WOT Characters", characters=characters)

@app.route("/character/<id>")
def character(id):
    character = Character.query.get(id)
    return render_template("character.html", title=character.name, character=character)

@app.route("/api/characters")
def api_characters():
    token = request.args.get("token")
    if not token:
        return "No API key given."
    if not User.query.filter_by(api_key=token).first():
        return "Failed. Incorrect API Key given."
    else:
        return jsonify([
            {
                "id": c.id,
                "name": c.name,
                "title": c.title,
                "race": c.race,
                "homeland": c.homeland
            }
            for c in Character.query.all()
        ])

@app.route("/api/character/<id>")
def api_character(id):
    token = request.args.get("token")
    if not token:
        return "No API key given."

    user = User.query.filter_by(api_key=token).first()
    if not user:
        return "Failed. Incorrect API Key given."
    
    character = Character.query.get(id)

    if character:
        return jsonify({
            "id": character.id,
            "name": character.name,
            "title": character.title,
            "race": character.race,
            "homeland": character.homeland
        })
    return "cool"