from os import environ
from flask import Flask, render_template, url_for, jsonify, request
from flask_login import LoginManager
from flask_migrate import Migrate

from .model import db, connect_to_db, User, APIKey, APIRequest, Character
from .forms import RegisterForm

app = Flask(__name__)
app.config["SECRET_KEY"] = environ["SECRET_KEY"]
app.config['SQLALCHEMY_DATABASE_URI'] = environ["POSTGRES_URI"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_to_db(app)

migrate = Migrate(app, db)



login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/")
def home():
    return render_template("home.html", title="WOT API")




@app.route("/api-key", methods=["POST", "GET"])
def api_key():
    form = RegisterForm()
    
    first_name = form.first_name.data
    last_name = form.last_name.data
    discord = form.discord.data


    if request.method == "POST" and form.validate_on_submit():
        if User.query.filter_by(discord=discord).first():
            return "You've already gotten an API key. Message Chalon for a new one."
        else:
            new_user = User(first_name, last_name, discord)
            db.session.add(new_user)
            db.session.commit()
            new_api_key = APIKey(new_user.id)
            db.session.add(new_api_key)
            db.session.commit()

            return f"<h2>Here is your API key, please keep it safe.</h2><h1>{new_api_key.api_key}</h1>"
    else:
        return render_template("get-token.html", form=form)

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
    api_key_ref = APIKey.query.filter_by(api_key=token).first()
    if not api_key_ref:
        return "Failed. Incorrect API Key given."
    if not api_key_ref.active:
        new_api_request = APIRequest(api_key_ref.user_id, "/api/characters", False)
        db.session.add(new_api_request)
        db.session.commit()
        return "Your API key is revoked. Message Chalon for a new one."
    else:
        new_api_request = APIRequest(api_key_ref.user_id, "/api/characters", True)
        db.session.add(new_api_request)
        db.session.commit()
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
    api_key_ref = APIKey.query.filter_by(api_key=token).first()
    if not api_key_ref:
        return "Failed. Incorrect API Key given."
    if not api_key_ref.active:
        new_api_request = APIRequest(api_key_ref.user_id, f"/api/character/{id}", False)
        db.session.add(new_api_request)
        db.session.commit()
        return "Your API key is revoked. Message Chalon for a new one."
    else:
        new_api_request = APIRequest(api_key_ref.user_id, f"/api/character/{id}", True)
        db.session.add(new_api_request)
        db.session.commit()
    
    character = Character.query.get(id)

    if not character:
        new_api_request = APIRequest(api_key_ref.user_id, f"/api/character/{id}", False)
        db.session.add(new_api_request)
        db.session.commit()
        return f"There is no character with the id of {id}."
        

    if character:
        return jsonify({
            "id": character.id,
            "name": character.name,
            "title": character.title,
            "race": character.race,
            "homeland": character.homeland
        })
    return "cool"