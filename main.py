from flask import render_template , Flask , request , session , redirect , url_for
import os
from sqlalchemy import desc
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
	img_num = db.Column(db.Integer , default = 0)
	timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	bumptime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	body = db.Column(db.String(500))
	img_ext = db.Column(db.String(10))
	password = db.Column(db.String(500))
	#pinned = db.Column(db.Integer)  #is it pinned or not? 

class Post(db.Model):
	id = db.Column(db.Integer , unique=True , primary_key=True) #number, not the cookie id
	name = db.Column(db.String(50))
	img_name = db.Column(db.String(200) , default="")
	img_num = db.Column(db.Integer , default = 0)
	time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	body = db.Column(db.String(500))
	thread_id = db.Column(db.Integer)
	img_ext = db.Column(db.String(10))
	password = db.Column(db.String(500))
	options = db.Column(db.String(50)) #noko sage
	board = db.Column(db.String(50))
	timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Boards(db.Model):
	name = db.Column(db.String(50), primary_key=True)
	desc = db.Column(db.String(500))
	last_id = db.Column(db.Integer , default = 0) #to generate new id

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





@app.route("/")
def index():
	return "RikChan"

@app.route("/login", methods=["GET" , "POST"])
@app.route("/login/", methods=["GET" , "POST"])
def login():
	if request.method == "POST":
		u = User.query.filter_by(username = request.form["username"]).all()[0]
		if dec(u.password , request.form["password"]):
			session["username"] = u.username
			session["rank"] = u.rank
			print(session["username"] , session["rank"])
	if "username" in session:
		return redirect(url_for("index"))
	return render_template("login.html")

@app.route("/logout")
@app.route("/logout/")
def logout():
	if "username" in session:
		session.pop("username")
		session.pop("rank")


@app.route("/_ct_", methods=["GET" , "POST"])
@app.route("/_ct_/", methods=["GET" , "POST"])
def ct():
	if "rank" in session:
		if session["rank"] == 2:
			if request.method == "POST":
				print(request.form)
				db.session.add(Boards(name = request.form["board"] , desc = request.form["desc"]))
				db.session.commit()
			return render_template("ct.html")
		else:
			return "stfu"
	else:
		return "lol go away"


@app.route("/<board>" , methods=["GET" , "POST"])
@app.route("/<board>/", methods=["GET" , "POST"])
def board_home(board):
	#Thread.query.filter_by(board="meta").all()
	#from sqlalchemy import desc
	#Thread.query.order_by(desc(Thread.timestamp)).all() order by time from timestamp
	bo = None
	boards = Boards.query.all()
	for b in boards:
		if b.name == board:
			exists = True
			bo = b

	if request.method == "POST":
		#print(request.form)
		if bo:
			t = Thread(id = bo.last_id+1 , name = request.form["name"] , body = request.form["body"] , password = enc(request.form["password"]), board = board)
			print(bo.last_id)
			bo.last_id = bo.last_id + 1
			db.session.commit()
			print(bo.last_id)
			db.session.add(t)
			db.session.commit()
			return render_template("board.html" ,Post = Post, board = board , desc = bo.desc , threads = Thread.query.filter_by(board=board).order_by(desc(Thread.bumptime)).all())

	if bo:
		return render_template("board.html" ,Post = Post, board = board , desc = bo.desc , threads = Thread.query.filter_by(board=board).order_by(desc(Thread.bumptime)).all())
	else:
		return "e404"

@app.route("/<board>/<int:thread_id>/" , methods=["GET" , "POST"])
@app.route("/<board>/<int:thread_id>", methods=["GET" , "POST"])
def board_thread(board , thread_id):
	#Thread.query.filter_by(board="meta").all()
	#from sqlalchemy import desc
	#Thread.query.order_by(desc(Thread.timestamp)).all() order by time from timestamp
	#try:
	thread = Thread.query.filter_by(board=board).filter_by(id=thread_id).all()[0]
	bo = Boards.query.filter_by(name=board).all()[0]
	#except:
	#	thread = None

	if request.method == "POST":
		#print(request.form)
		if thread:
			p = Post(id = bo.last_id+1 , name = request.form["name"] , body = request.form["body"] , password = enc(request.form["password"]), board = board , thread_id = thread_id)
			print(bo.last_id)
			bo.last_id = bo.last_id + 1
			db.session.commit()
			thread.bumptime = datetime.datetime.utcnow()
			db.session.commit()
			thread.bump = thread.bump+1
			db.session.commit()
			print(bo.last_id)
			db.session.add(p)
			db.session.commit()
			return render_template("thread.html" , board = board , thread_id = thread_id , thread=thread, posts = Post.query.filter_by(board=board).filter_by(thread_id = thread_id).order_by(desc(Post.timestamp)).all())

	if thread:
		return render_template("thread.html" , board = board , thread_id = thread_id , thread=thread, posts = Post.query.filter_by(board=board).filter_by(thread_id = thread_id).order_by(desc(Post.timestamp)).all())
	else:
		return "e404"



if __name__ == "__main__":
	app.debug = True
	app.run()