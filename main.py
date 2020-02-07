from flask import render_template
from config import *

boards = Boards.query.all()


@app.route("/")
def index():
    return "welcome"

@app.route("/<board>" , methods=["GET" , "POST"])
@app.route("/<board>/", methods=["GET" , "POST"])
def board_home(board):
    #for b in boards:
    #    if b.name == board:
     #       #return b.name + "\n" + b.desc

    return render_template("board.html") # , threads = ["wfe" , "wef" , "few"])


if __name__ == "__main__":
    app.debug = True
    app.run()