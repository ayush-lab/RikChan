from main import *
import sys
if sys.argv[1] == "cp":
	u = User.query.filter_by(username=sys.argv[2]).all()[0]
	u.password = enc(sys.argv[3])
	db.session.commit()
elif sys.argv[1] == "cr":
	u = User.query.filter_by(username=sys.argv[2]).all()[0]
	u.rank = sys.argv[3]
	db.session.commit()
elif sys.argv[1] == "cpr":
	u = User.query.filter_by(username=sys.argv[2]).all()[0]
	u.password = enc(sys.argv[3])
	u.rank = sys.argv[4]
	db.session.commit()
else:
	db.session.add(User(username=sys.argv[1] , password=enc(sys.argv[2]) , rank=int(sys.argv[3])))
	db.session.commit()
