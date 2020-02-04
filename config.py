import os
basedir = os.path.abspath(os.path.dirname(__file__))

from flask_sqlalchemy import SQLAlchemy
import datetime
from flask import Flask
app = Flask("__main__")


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

class Post(db.Model):
    id = db.Column(db.Integer , unique=True , primary_key=True) #number, not the cookie id
    name = db.Column(db.String(50))
    img_name = db.Column(db.String(200) , default="")
    img_num = db.Column(db.Integer , default = 0 , unique = True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    body = db.Column(db.String(500))
    thread_id = db.Column(db.Integer)
    img_ext = db.Column(db.String(10))

class Boards(db.model):
    name = db.Column(db.String(50))
    desc = db.Column(db.String(500))


#Create the schema
db.create_all()