from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)

class AddTodoForm(Form):
	title = StringField('title', validators=[DataRequired()])
	description = StringField('description', validators=[])
	forBrad = BooleanField('forBrad', default=False)
	forKara = BooleanField('forKara', default=False)