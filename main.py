from flask import Flask

from config import app

@app.route("/")
def index():
    return "welcome"

if __name__ == "__main__":
    app.debug = True
    app.run()