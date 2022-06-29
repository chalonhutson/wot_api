from os import environ
from src import app
from src.model import connect_to_db

if __name__ == "__main__":
    app.config['SQLALCHEMY_DATABASE_URI'] = environ["POSTGRES_URI"]
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    connect_to_db(app)
    app.env = environ["DEV_ENVIRONMENT"]
    app.run(debug=False)