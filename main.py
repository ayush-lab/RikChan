from flask import render_template , Flask
import os
basedir = os.path.abspath(os.path.dirname(__file__))
from werkzeug.security import generate_password_hash as enc
from werkzeug.security import check_password_hash as dec
from hashlib import sha1
from flask_sqlalchemy import SQLAlchemy
import datetime
app = Flask("__main__" , template_folder=basedir+"/templates")


app.config['SECRET_KEY'] = 'thytyhjeyt'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)


class Thread(db.Model):
	board = db.Column(db.String(50))
	bump = db.Column(db.Integer , default = 0)
	id = db.Column(db.Integer , unique=True , primary_key = True) #number, not the cookie id
	name = db.Column(db.String(50))
	img_name = db.Column(db.String(200) , default="")
	img_num = db.Column(db.Integer , default = 0 , unique = True)
	timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	body = db.Column(db.String(500))
	img_ext = db.Column(db.String(10))
	password = db.Column(db.String(500))
	#pinned = db.Column(db.Integer)  #is it pinned or not? 

class Post(db.Model):
	id = db.Column(db.Integer , unique=True , primary_key=True) #number, not the cookie id
	name = db.Column(db.String(50))
	img_name = db.Column(db.String(200) , default="")
	img_num = db.Column(db.Integer , default = 0 , unique = True)
	time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	body = db.Column(db.String(500))
	thread_id = db.Column(db.Integer)
	img_ext = db.Column(db.String(10))
	password = db.Column(db.String(500))
	options = db.Column(db.String(50)) #noko sage

class Boards(db.Model):
	name = db.Column(db.String(50), primary_key=True)
	desc = db.Column(db.String(500))
	last_id = db.Column(db.Integer) #to generate new id

class User(db.Model):
	username = db.Column(db.String(50), primary_key=True)
	password = db.Column(db.String(500))
	email = db.Column(db.String(500))
	#rank 0 = janny
	#rank 1 = mod
	#rank 2 = admin
	rank = db.Column(db.Integer, default=0)
	board_name = db.Column(db.String(50))

def tripcodegen(thing):
	return sha1(thing.encode("utf-8")).hexdigest()[:8]
#Create the schema
db.create_all()



boards = Boards.query.all()

@app.route("/")
def index():
	return "welcome"

@app.route("/<board>" , methods=["GET" , "POST"])
@app.route("/<board>/", methods=["GET" , "POST"])
def board_home(board):
	exists = False
	for b in boards:
		if b.name == board:
			exists = True
	if exists:
		return render_template("board.html" , board = board) # , threads = ["wfe" , "wef" , "few"])
	else:
		return "e404"


if __name__ == "__main__":
	app.debug = True
	app.run()