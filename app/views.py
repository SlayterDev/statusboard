from flask import render_template, flash, redirect, url_for, session, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm
from .models import Todo, User

@lm.user_loader
def load_user(id):
	return User()

def after_login(username, password):
	if username != 'Brad' and username != 'Kara':
		flash('Invalid login. Please Try again')
		return redirect(url_for('login'))
	if username == 'Brad' and password != 'potato':
		flash('Invalid login. Please Try again')
		return redirect(url_for('login'))
	user = User()
	user.username = username
	remember_me = False
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None)
	login_user(user, remember=remember_me)
	return redirect(url_for('todolist'))

@app.before_request
def before_request():
	g.user = current_user

@app.route('/')
@app.route('/index')
@login_required
def index():
	todos = [
		{
			'title': 'Take out the trash',
			'assigned': 'Brad',
			'done': False
		},
		{
			'title': 'Clean the litter box',
			'assigned': 'Kara',
			'done': True
		}
	]

	return render_template('index.html', title='Home', user=g.user,
							todos=todos)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data
		return after_login(form.username.data, form.password.data)
	return render_template('login.html', title='Login', form=form)

@app.route('/todolist')
@login_required
def todolist():
	todos = [
		{
			'title': 'Take out the trash',
			'assigned': 'Brad',
			'done': False
		},
		{
			'title': 'Clean the litter box',
			'assigned': 'Kara',
			'done': True
		}
	]
	return render_template('todolist-client.html', title='Todo',
							user=g.user, todos=todos)