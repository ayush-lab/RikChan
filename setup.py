from main import *
import os

if not os.path.isfile("data.db"):
	print("Initialising Database")
	db.create_all()
else:
	print("Database already exists")

if not os.path.exists("static/media"):
	os.makedirs("static/media")
else:
	print("static/media folder already exists")