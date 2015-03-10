from app import db

class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(140))
	description = db.Column(db.String(280))
	assigned = db.Column(db.String(64))
	timestamp = db.Column(db.DateTime)
	creator = db.Column(db.String(64))
	done = db.Column(db.Integer)

	def __repr__(self):
		return '<Todo %r>' % (self.title)

class User():
	username = ""

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(id):
		return 1