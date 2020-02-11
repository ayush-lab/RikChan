from flask import render_template , Flask , request , session , redirect , url_for , send_from_directory
import os
from sqlalchemy import desc , asc
basedir = os.path.abspath(os.path.dirname(__file__))
from werkzeug.security import generate_password_hash as enc
from werkzeug.security import check_password_hash as dec
from werkzeug.utils import secure_filename
from hashlib import sha1
from flask_sqlalchemy import SQLAlchemy
import datetime
import secrets
import string

app = Flask("__main__" , template_folder=basedir+"/templates")

app.config["UPLOAD_FOLDER"] = basedir + "/static/media"
app.config["MAX_CONTENT_PATH"] = 4*1024*1024
def allowed(filename):
	print(filename)
	return filename.split(".")[len(filename.split("."))-1] in ['jpg','jpeg','png','webm' , 'gif'] , filename.split(".")[len(filename.split("."))-1]

app.config['SECRET_KEY'] = 'thytyhjeyt'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

def gen(N):
	return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(N)) 

class Thread(db.Model):
	uni = db.Column(db.String(100) , primary_key = True)
	board = db.Column(db.String(50))
	bump = db.Column(db.Integer , default = 0)
	id = db.Column(db.Integer) #number, not the cookie id
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
	uni = db.Column(db.String(100), primary_key=True)
	id = db.Column(db.Integer) #number, not the cookie id
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

class Media(db.Model):
	board = db.Column(db.String(50), primary_key=True)
	jpg = db.Column(db.Integer, default=0)
	jpeg = db.Column(db.Integer, default=0)
	png = db.Column(db.Integer, default=0)
	gif = db.Column(db.Integer, default=0)
	webm = db.Column(db.Integer, default=0)

def tripcodegen(thing):
	return sha1(thing.encode("utf-8")).hexdigest()[:8]
#Create the schema
db.create_all()





@app.route("/")
def index():
	board_list = []
	for b in Boards.query.all():
		board_list.append("<a href="+url_for("board_home",board=b.name)+">" + b.name + "</a>")
	string = "<h1>RikChan</h1></br>Boards List</br>[ "
	for b in board_list:
		string+=b+" / "
	if string!="<h1>RikChan</h1></br>Boards List</br>[ ":
		string = string[0:len(string)-2]
	string+="]"
	return "<title>RikChan</title>\n<center>"+string+"\n</center>"



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

@app.route("/media/<path:p>")
@app.route("/media/<path:p>/")
def serve(p):
	return send_from_directory(app.config["UPLOAD_FOLDER"] , p)

@app.route("/_ct_", methods=["GET" , "POST"])
@app.route("/_ct_/", methods=["GET" , "POST"])
def ct():
	if "rank" in session:
		if session["rank"] == 2:
			if request.method == "POST":
				print(request.form)
				db.session.add(Boards(name = request.form["board"] , desc = request.form["desc"]))
				db.session.commit()
				print("Created MEDIA")
				db.session.add(Media(board = request.form["board"]))
				db.session.commit()
				#redirect(url_for("board_home" , board=request.form["board"]))
			return render_template("ct.html")
		else:
			return "stfu"
	else:
		return "lol go away"


@app.route("/<board>/_del_" , methods=["POST"])
@app.route("/<board>/_del_/" ,  methods=["POST"])
def d(board):
	print(request.form)
	password = request.form["password"]
	li = list(request.form.items())
	print(li)
	for i in li:
		if i[1] =="THREAD":
			a = Thread.query.filter_by(board=board).filter_by(id=i[0]).all()[0]
			if dec(a.password , password) or session["rank"] == 2:
				if a.img_ext:
					fi = a.board + str(a.img_num) + "." + a.img_ext
					os.remove(basedir+"/static/media/"+fi)
				db.session.delete(a)
				db.session.commit()

		elif i[1] == "POST":
			a = Post.query.filter_by(board=board).filter_by(id=i[0]).all()[0]
			if dec(a.password , password) or session["rank"] == 2:
				if a.img_ext:
					fi = a.board + str(a.img_num) + "." + a.img_ext
					os.remove(basedir+"/static/media/"+fi)
				db.session.delete(a)
				db.session.commit()

	return redirect(url_for("board_home" , board=board))


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
		#print(request.files)
		f = None
		if bo:
			t = None
			if "file" in request.files:
				file = request.files["file"]
				file_name = secure_filename(file.filename)
				print("FILE FOUND")
				print(file_name)
				if allowed(file_name)[0]:
					if allowed(file_name)[1] == "gif":
						med = Media.query.filter_by(board=board).all()[0]
						file.save(os.path.join(app.config['UPLOAD_FOLDER'],board + str(med.gif+1)+".gif"))
						med.gif = med.gif + 1
						db.session.commit()
						f = "gif"
					elif allowed(file_name)[1] == "jpeg":
						med = Media.query.filter_by(board=board).all()[0]
						file.save(os.path.join(app.config['UPLOAD_FOLDER'],board + str(med.jpeg+1) + ".jpeg"))
						med.jpeg = med.jpeg + 1
						db.session.commit()
						f = "jpeg"
					elif allowed(file_name)[1] == "png":
						med = Media.query.filter_by(board=board).all()[0]
						file.save(os.path.join(app.config['UPLOAD_FOLDER'],board + str(med.png+1) + ".png"))
						med.png = med.png + 1
						db.session.commit()
						f = "png"
					elif allowed(file_name)[1] == "jpg":
						med = Media.query.filter_by(board=board).all()[0]
						file.save(os.path.join(app.config['UPLOAD_FOLDER'],board + str(med.jpg+1) + ".jpg"))
						med.jpg = med.jpg + 1
						db.session.commit()
						f = "jpg"
					elif allowed(file_name)[1] == "webm":
						med = Media.query.filter_by(board=board).all()[0]
						file.save(os.path.join(app.config['UPLOAD_FOLDER'],board + str(med.webm+1) + ".webm"))
						med.webm = med.webm + 1
						db.session.commit()
						f = "webm"
			#else:
			if not f:
				t = Thread(uni = bo.name + str(bo.last_id+1),id = bo.last_id+1 , name = request.form["name"] , body = request.form["body"] , password = enc(request.form["password"]), board = board)
			else:
				print(f , "f")
				med = Media.query.filter_by(board=board).all()[0]
				file_name = secure_filename(file.filename)
				if f == "gif":
					t = Thread(img_ext = f , img_num = med.gif, img_name=file_name, uni = bo.name + str(bo.last_id+1),id=bo.last_id + 1, name=request.form["name"], body=request.form["body"],
							   password=enc(request.form["password"]), board=board)
				elif f == "jpg":
					t = Thread(img_ext=f, img_num=med.jpg,uni = bo.name + str(bo.last_id+1), img_name=file_name, id=bo.last_id + 1,
							   name=request.form["name"], body=request.form["body"],
							   password=enc(request.form["password"]), board=board)
				elif f == "jpeg":
					t = Thread(img_ext=f, img_num=med.jpeg, uni = bo.name + str(bo.last_id+1), img_name=file_name, id=bo.last_id + 1,
							   name=request.form["name"], body=request.form["body"],
							   password=enc(request.form["password"]), board=board)
				elif f == "png":
					t = Thread(img_ext=f, img_num=med.png, uni = bo.name + str(bo.last_id+1), img_name=file_name, id=bo.last_id + 1,
							   name=request.form["name"], body=request.form["body"],
							   password=enc(request.form["password"]), board=board)
				elif f == "webm":
					t = Thread(img_ext=f, img_num=med.webm ,uni = bo.name + str(bo.last_id+1), img_name=file_name, id=bo.last_id + 1,
							   name=request.form["name"], body=request.form["body"],
							   password=enc(request.form["password"]), board=board)



			print(bo.last_id)
			bo.last_id = bo.last_id + 1
			db.session.commit()
			print(bo.last_id)
			db.session.add(t)
			db.session.commit()

			return render_template("board.html" , gen=gen , Post = Post, board = board , desc = bo.desc , threads = Thread.query.filter_by(board=board).order_by(desc(Thread.bumptime)).all())

	if bo:
		return render_template("board.html" ,gen=gen ,Post = Post, board = board , desc = bo.desc , threads = Thread.query.filter_by(board=board).order_by(desc(Thread.bumptime)).all())
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
		print(request.files)
		f = None
		if thread:
			if "file" in request.files:
				file = request.files["file"]
				file_name = secure_filename(file.filename)
				print("FILE FOUND")
				print(file_name)
				if allowed(file_name)[0]:
					if allowed(file_name)[1] == "gif":
						med = Media.query.filter_by(board=board).all()[0]
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], board + str(med.gif + 1) + ".gif"))
						med.gif = med.gif + 1
						db.session.commit()
						f = "gif"
					elif allowed(file_name)[1] == "jpeg":
						med = Media.query.filter_by(board=board).all()[0]
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], board + str(med.jpeg + 1) + ".jpeg"))
						med.jpeg = med.jpeg + 1
						db.session.commit()
						f = "jpeg"
					elif allowed(file_name)[1] == "png":
						med = Media.query.filter_by(board=board).all()[0]
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], board + str(med.png + 1) + ".png"))
						med.png = med.png + 1
						db.session.commit()
						f = "png"
					elif allowed(file_name)[1] == "jpg":
						med = Media.query.filter_by(board=board).all()[0]
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], board + str(med.jpg + 1) + ".jpg"))
						med.jpg = med.jpg + 1
						db.session.commit()
						f = "jpg"
					elif allowed(file_name)[1] == "webm":
						med = Media.query.filter_by(board=board).all()[0]
						file.save(os.path.join(app.config['UPLOAD_FOLDER'], board + str(med.webm + 1) + ".webm"))
						med.webm = med.webm + 1
						db.session.commit()
						f = "webm"
			# else:
			if not f:
				p = Post(uni=bo.name + str(bo.last_id + 1), thread_id = thread_id, id=bo.last_id + 1, name=request.form["name"],
						   body=request.form["body"], password=enc(request.form["password"]), board=board)
			else:
				print(f, "f")
				med = Media.query.filter_by(board=board).all()[0]
				file_name = secure_filename(file.filename)
				if f == "gif":
					p = Post(img_ext=f, thread_id = thread_id, img_num=med.gif, img_name=file_name, uni=bo.name + str(bo.last_id + 1),
							   id=bo.last_id + 1, name=request.form["name"], body=request.form["body"],
							   password=enc(request.form["password"]), board=board)
				elif f == "jpg":
					p = Post(img_ext=f, thread_id = thread_id, img_num=med.jpg, uni=bo.name + str(bo.last_id + 1), img_name=file_name,
							   id=bo.last_id + 1,
							   name=request.form["name"], body=request.form["body"],
							   password=enc(request.form["password"]), board=board)
				elif f == "jpeg":
					p = Post(img_ext=f, thread_id = thread_id, img_num=med.jpeg, uni=bo.name + str(bo.last_id + 1), img_name=file_name,
							   id=bo.last_id + 1,
							   name=request.form["name"], body=request.form["body"],
							   password=enc(request.form["password"]), board=board)
				elif f == "png":
					p = Post(img_ext=f, thread_id = thread_id, img_num=med.png, uni=bo.name + str(bo.last_id + 1), img_name=file_name,
							   id=bo.last_id + 1,
							   name=request.form["name"], body=request.form["body"],
							   password=enc(request.form["password"]), board=board)
				elif f == "webm":
					p = Post(img_ext=f, thread_id = thread_id, img_num=med.webm, uni=bo.name + str(bo.last_id + 1), img_name=file_name,
							   id=bo.last_id + 1,
							   name=request.form["name"], body=request.form["body"],
							   password=enc(request.form["password"]), board=board)

			#print(bo.last_id)
			#bo.last_id = bo.last_id + 1
			#db.session.commit()
			#print(bo.last_id)
			#db.session.add(t)
			#db.session.commit()


			#p = Post(uni = bo.name + str(bo.last_id+1),id = bo.last_id+1 , name = request.form["name"] , body = request.form["body"] , password = enc(request.form["password"]), board = board , thread_id = thread_id)
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
			return render_template("thread.html" ,gen=gen , board = board , thread_id = thread_id , thread=thread, posts = Post.query.filter_by(board=board).filter_by(thread_id = thread_id).order_by(asc(Post.timestamp)).all())

	if thread:
		return render_template("thread.html" ,gen=gen , board = board , thread_id = thread_id , thread=thread, posts = Post.query.filter_by(board=board).filter_by(thread_id = thread_id).order_by(asc(Post.timestamp)).all())
	else:
		return "e404"



if __name__ == "__main__":
	app.debug = True
	app.run()