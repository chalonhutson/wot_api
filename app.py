from os import environ
from src import app

if __name__ == "__main__":
    app.env = environ["DEV_ENVIRONMENT"]
    app.run(debug=False)