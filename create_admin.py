from main import *
print("Initialising db")
db.create_all()
username=input("username for admin account")
password=input("password for admin account")
db.session.add(User(username=username , password=password , rank=2))
db.session.commit()
