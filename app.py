from os import environ
from src import app
from src.model import connect_to_db

if __name__ == "__main__":
    connect_to_db(app)
    app.env = "development"
    app.run(port=8000, host="localhost", debug=True)