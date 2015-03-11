from flask import render_template, flash, redirect, url_for, session, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from datetime import datetime
from .forms import LoginForm, AddTodoForm
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
	todos = reversed(Todo.query.paginate(1, 3).items)

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

@app.route('/todolist', methods=['GET', 'POST'])
@login_required
def todolist():
	todos = reversed(Todo.query.all())

	form = AddTodoForm()
	if form.validate_on_submit():
		assigned = ""
		if form.forBrad.data:
			assigned += "Brad "
		if form.forKara.data:
			if "Brad" in assigned:
				assigned += "and "
			assigned += "Kara "

		t = Todo(title=form.title.data, description=form.description.data,
				assigned=assigned, timestamp=datetime.utcnow(),
				creator=g.user.username, done=False)
		db.session.add(t)
		db.session.commit()
		flash('Your todo item has been added!')
		return redirect(url_for('todolist'))

	return render_template('todolist-client.html', title='Todo',
							user=g.user, todos=todos, form=form)

@app.route('/markdone/<int:id>')
@login_required
def markdone(id):
	todo = Todo.query.get(id)
	if todo is None:
		flash('This item does not exist')
		return redirect(url_for('todolist'))
	todo.done = 1
	db.session.add(todo)
	db.session.commit()
	return redirect(url_for('todolist'))

@app.route('/delete/<int:id>')
@login_required
def delete(id):
	todo = Todo.query.get(id)
	if todo is None:
		flash('This item does not exist')
		return redirect(url_for('todolist'))
	db.session.delete(todo)
	db.session.commit()
	return redirect(url_for('todolist'))