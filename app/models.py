from app import db, app

import sys
if sys.version_info >= (3, 0):
	enable_search = False
else:
	enable_search = True
	import flask.ext.whooshalchemy as whooshalchemy

class Todo(db.Model):
	__searchable__ = ['title']

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(140))
	description = db.Column(db.String(280))
	assigned = db.Column(db.String(64))
	timestamp = db.Column(db.DateTime)
	creator = db.Column(db.String(64))
	done = db.Column(db.Integer)

	def __repr__(self):
		return '<Todo %r>' % (self.title)

if enable_search:
	whooshalchemy.whoosh_index(app, Todo)

class Event(db.Model):
	__searchable__ = ['title']

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(140))
	date = db.Column(db.DateTime)
	assigned = db.Column(db.String(64))
	creator = db.Column(db.String(64))

	def __repr__(self):
		return '<Event %r>' % (self.title)

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